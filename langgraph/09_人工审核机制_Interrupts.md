# LangGraph 人工审核机制（Interrupts）

## 什么是 Interrupts

`interrupt()` 可以在图的任意位置暂停执行，等待外部输入后再继续。这实现了**人工介入（Human-in-the-loop）**模式——人在关键节点审批、修改状态或编辑工具调用结果。

与传统静态断点不同，`interrupt()` 是**动态**的，可以放在代码任意位置，基于业务逻辑决定是否暂停。

关键行为：
- **Checkpointer 保存位置**：暂停时自动保存当前图状态，用 `thread_id` 追踪
- **`interrupt()` 传递值**：`interrupt("消息内容")` 里的值会出现在流输出的 `chunk["interrupts"]` 中
- **任意 JSON 可序列化值**：可以传字符串、对象、数组等

---

## 暂停：interrupt()

在节点中调用 `interrupt()`，LangGraph 会保存状态并等待恢复：

```python
from langgraph.types import interrupt

def approval_node(state: State):
    # 暂停，等待审批
    approved = interrupt("Do you approve this action?")
    return {"approved": approved}
```

调用 `interrupt()` 后的流程：

1. 图执行在 `interrupt()` 处**挂起**
2. Checkpointer **保存状态**（生产环境用持久化 checkpointer）
3. 值返回给调用方（`result["__interrupt__"]` 或 `result.interrupts`）
4. 图**无限期等待**，直到用 `Command` 恢复

---

## 恢复：Command

用 `Command(resume=值)` 重新调用图，把外部输入传回去：

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "thread-1"}}

# 第一次调用，遇到 interrupt 暂停
result = graph.invoke({"input": "data"}, config=config, version="v2")

# 查看中断信息
print(result.interrupts)
# > (Interrupt(value='Do you approve this action?'),)

# 恢复，传入 True（审批通过）
graph.invoke(Command(resume=True), config=config, version="v2")
```

**恢复要点：**
- 必须用**同一个 thread_id**
- `Command(resume=...)` 的值成为 `interrupt()` 的返回值
- 节点从头开始重新执行（`interrupt()` 之前的代码会再次运行）
- `resume` 可以传任意 JSON 可序列化的值

---

## 常见模式

### 审批工作流

在执行关键操作前暂停，等人工审批：

```python
from langgraph.types import interrupt, Command

def approval_node(state: State) -> Command[Literal["proceed", "cancel"]]:
    is_approved = interrupt({
        "question": "是否继续此操作？",
        "details": state["action_details"]
    })
    if is_approved:
        return Command(goto="proceed")
    else:
        return Command(goto="cancel")
```

恢复时传 `True` 或 `False`：

```python
graph.invoke(Command(resume=True), config=config)   # 审批通过
graph.invoke(Command(resume=False), config=config)  # 拒绝
```

### 审核并修改状态

让审核人查看并修改 LLM 生成的内容后再继续：

```python
def review_node(state: State):
    edited_content = interrupt({
        "instruction": "请审核并修改以下内容",
        "content": state["generated_text"]
    })
    return {"generated_text": edited_content}
```

恢复时传入修改后的内容：

```python
graph.invoke(Command(resume="修改后的内容"), config=config)
```

### 在 Tool 中使用 Interrupt

把审核逻辑直接写在 Tool 里，让 Tool 被调用时自动暂停：

```python
from langchain.tools import tool
from langgraph.types import interrupt

@tool
def send_email(to: str, subject: str, body: str):
    response = interrupt({
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "确认发送此邮件？"
    })
    if response.get("action") == "approve":
        final_body = response.get("body", body)
        return f"Email sent with body: {final_body}"
    return "Email cancelled"
```

### 并行多中断处理

多个并行分支同时遇到 `interrupt()`，用 `resume_map` 一次性恢复：

```python
# 所有并行节点暂停
interrupted_result = graph.invoke({"vals": []}, config)

# 从结果中提取所有中断的 ID，映射到各自的恢复值
resume_map = {
    i.id: f"answer for {i.value}"
    for i in interrupted_result["__interrupt__"]
}

# 一次性恢复所有中断
result = graph.invoke(Command(resume=resume_map), config)
```

---

## 流式 Human-in-the-loop

同时流式输出 AI 消息和节点更新，检测到中断时暂停并等待用户输入：

```python
from langgraph.types import Command

async for chunk in graph.astream(
    initial_input,
    stream_mode=["messages", "updates"],
    subgraphs=True,
    config=config,
    version="v2",
):
    if chunk["type"] == "messages":
        # 处理流式消息
        msg, _ = chunk["data"]
        if hasattr(msg, "content"):
            display_streaming_content(msg.content)

    elif chunk["type"] == "updates":
        if "__interrupt__" in chunk["data"]:
            # 检测到中断，获取用户输入后恢复
            interrupt_info = chunk["data"]["__interrupt__"][0].value
            user_response = get_user_input(interrupt_info)
            initial_input = Command(resume=user_response)
            break
```

---

## 小结

| 组件 | 作用 |
|------|------|
| `interrupt("消息")` | 在任意位置暂停，返回值给调用方 |
| `Command(resume=值)` | 恢复执行，值成为 `interrupt()` 的返回值 |
| Checkpointer | 保存图状态，确保断点可恢复 |
| `thread_id` | 追踪同一会话，重复使用恢复同一会话 |
