# LangGraph 持久化执行（Durable Execution）

## 什么是持久化执行

持久化执行是一种在关键节点保存进度的技术，让工作流可以**暂停后从断点恢复**，而不是从头重跑。

典型场景：
- **人工审核（Human-in-the-loop）**：流程暂停等待人工确认，确认后继续
- **长时间任务**：LLM 调用超时、网络故障等，恢复后不重复已完成的步骤

LangGraph 通过内置的**持久化层（Persistence Layer）**实现这一能力——每一步的状态都会保存到持久化存储中。

---

## 启用持久化执行的三个要求

### 1. 配置 Checkpointer

Checkpointer 负责保存每一步的状态：

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

### 2. 指定 Thread ID

每次执行时传入 `thread_id`，用于追踪同一工作流实例的历史：

```python
from langchain_core.utils.uuid import uuid7

thread_id = str(uuid7())
config = {"configurable": {"thread_id": thread_id}}

graph.invoke({"input": "..."}, config)
```

### 3. 用 @task 包裹副作用操作

**关键点**：恢复工作流时，代码不是从中断的那一行继续，而是从最近的节点（Node）或入口点（Entrypoint）重新执行。因此，有副作用的操作（API 调用、文件写入等）必须用 `@task` 包裹，避免重复执行。

```python
from langgraph.func import task

@task
def call_external_api(url: str):
    return requests.get(url).text[:100]
```

---

## 确定性与一致性重放

恢复工作流时，LangGraph 会从最近的检查点**重放**所有步骤，直到到达中断点。因此代码必须满足：

| 要求 | 说明 |
|------|------|
| **避免重复副作用** | 一个节点内有多个副作用操作，每个都要单独包成 `@task` |
| **封装非确定性操作** | 随机数生成等不确定操作必须放在 `@task` 或节点内 |
| **幂等性** | 尽量让 API 调用等操作幂等，避免重试时产生重复数据 |

---

## 持久化模式（Durability Modes）

三种模式，性能与可靠性的权衡：

| 模式 | 何时保存 | 性能 | 可靠性 |
|------|---------|------|--------|
| `"exit"` | 仅在整个图执行结束时 | 最高 | 最低（崩溃不可恢复）|
| `"async"` | 异步保存（下一步执行时并行写入）| 较高 | 较高 |
| `"sync"` | 每步执行前同步保存 | 较低 | 最高 |

```python
graph.stream(
    {"input": "test"},
    durability="sync"   # 或 "async" / "exit"
)
```

---

## 节点内使用 @task

如果一个节点内有多个副作用操作，不必拆成多个节点，直接用 `@task` 包裹每个操作：

```python
from langgraph.func import task

@task
def _make_request(url: str):
    return requests.get(url).text[:100]

def call_api(state: State):
    futures = [_make_request(url) for url in state["urls"]]
    results = [f.result() for f in futures]
    return {"results": results}
```

恢复时，已完成的 `@task` 结果直接从持久化层读取，不会重新发起请求。

---

## 恢复工作流

启用持久化执行后，两种恢复场景：

**1. 主动暂停/恢复（Human-in-the-loop）**

用 `interrupt()` 暂停，用 `Command` 恢复。

**2. 故障自动恢复**

发生异常后，用相同的 `thread_id` 重新调用，传入 `None` 作为输入：

```python
# 第一次执行（中途失败）
graph.invoke({"url": "https://example.com"}, config)

# 恢复执行（从上次检查点继续）
graph.invoke(None, config)
```

---

## 恢复的起始点

| 使用方式 | 恢复起始点 |
|---------|-----------|
| StateGraph（Graph API）| 中断所在节点的**开头** |
| 子图调用 | 调用子图的**父节点**开头 |
| Functional API | 中断所在 `entrypoint` 的**开头** |
