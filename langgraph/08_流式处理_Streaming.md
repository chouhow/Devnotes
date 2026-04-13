# LangGraph 流式处理（Streaming）

## 概述

LangGraph 的流式系统在生成完整响应之前就把中间结果实时推送给客户端，显著提升用户体验（特别是 LLM 调用有延迟时）。

主要方法：
- `stream()`：同步流式
- `astream()`：异步流式

---

## 基本用法

传入一个或多个 stream mode，控制返回哪种数据：

```python
for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode=["updates", "custom"],
    version="v2",
):
    if chunk["type"] == "updates":
        for node_name, state in chunk["data"].items():
            print(f"Node {node_name} updated: {state}")
    elif chunk["type"] == "custom":
        print(f"Status: {chunk['data']['status']}")
```

---

## 流式模式（Stream Modes）

| 模式 | 内容 | 典型用途 |
|------|------|---------|
| `"values"` | 每个 step 后的完整状态快照 | 调试 |
| `"updates"` | 每个 step 中节点的输出 | 生产环境 |
| `"messages"` | LLM 输出的 token（最常用）| 逐字显示 AI 回复 |
| `"messages-discounted"` | LLM token，去重（不含追加的内容）| 同上 |
| `"custom"` | `get_stream_writer()` 写入的自定义数据 | 进度提示 |
| `"debug"` | 详细的调试信息 | 开发调试 |
| `"checkpoints"` | 每个 step 后的检查点快照 | 时间旅行 |
| `"tasks"` | 每个任务的状态（pending/running/completed）| 并行任务监控 |

### messages 模式（LLM Token）

最常用的流式输出，实时显示 LLM 生成的文字：

```python
from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def on_chat_model_start(self, *args, **kwargs):
        pass
    def on_llm_new_token(self, token: str, *args, **kwargs):
        print(token, end="", flush=True)

async for event in graph.astream(
    {"messages": [{"role": "user", "content": "Tell me a joke"}]},
    stream_mode="messages",
    config={"callbacks": [StreamHandler()]},
):
    pass  # StreamHandler 自动处理输出
```

### 自定义数据流（custom）

用 `get_stream_writer()` 在节点中自定义流式输出（如进度提示）：

```python
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

class State(TypedDict):
    topic: str
    joke: str

def generate_joke(state: State):
    writer = get_stream_writer()
    writer({"status": "thinking of a joke..."})
    return {"joke": f"Why did the {state['topic']} go to school?"}

graph = (
    StateGraph(State)
    .add_node(generate_joke)
    .add_edge(START, "generate_joke")
    .add_edge("generate_joke", END)
    .compile()
)

for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode=["updates", "custom"],
    version="v2",
):
    # custom 数据由 writer() 写入
    pass
```

### 多个模式同时使用

```python
for chunk in graph.stream(
    initial_input,
    stream_mode=["updates", "messages", "custom", "tasks"],
    version="v2",
):
    if chunk["type"] == "updates":
        ...  # 节点输出
    elif chunk["type"] == "messages":
        ...  # LLM token
    elif chunk["type"] == "custom":
        ...  # 自定义进度
    elif chunk["type"] == "tasks":
        ...  # 任务状态
```

---

## 按 LLM 调用过滤（messages）

在有多次 LLM 调用的图中，只流式某一次调用的 token：

```python
# 多个 LLM 调用时，按 invocation_id 过滤
for chunk in graph.stream(
    input_data,
    stream_mode="messages",
    version="v2",
):
    if chunk.get("invocation_id") == "my_target_invocation":
        token = chunk["data"][0].content
        print(token, end="", flush=True)
```

---

## 按节点过滤（updates）

```python
# 只看特定节点的状态更新
for chunk in graph.stream(input_data, stream_mode="updates", version="v2"):
    if "generate_joke" in chunk["data"]:
        print(chunk["data"]["generate_joke"])
```

---

## 子图输出（subgraph）

流式子图时带上 `subgraphs=True`：

```python
for chunk in graph.stream(
    input_data,
    stream_mode="updates",
    subgraphs=True,  # 包含子图输出
    version="v2",
):
    if chunk.get("subgraph"):
        print(f"Subgraph: {chunk['data']}")
```

---

## 检查点流式（checkpoints）

每个 step 的完整状态快照，可用于时间旅行调试：

```python
for chunk in graph.stream(
    input_data,
    stream_mode="checkpoints",
    version="v2",
):
    print(f"Checkpoint at step: {chunk['config']['configurable']['checkpoint_id']}")
    print(f"State: {chunk['data']}")
```

---

## v2 格式变化

v2 的 `stream` 和 `invoke` 有新格式：

```python
# v2 invoke 格式
result = graph.invoke(input_data, version="v2")

# v2 stream 格式
for chunk in graph.stream(input_data, version="v2"):
    # v2 chunk 是字典，有 "type" 和 "data" 字段
    print(chunk["type"], chunk["data"])
```

### Pydantic 和 dataclass 状态转换

v2 自动把 Pydantic/dataclass 状态转换为 `dict`：

```python
# v1: graph.invoke 返回 Pydantic 对象
# v2: graph.invoke 返回 dict（更易处理）
```

---

## 生产环境建议

- **messages 模式**：实时显示 AI 回复，给用户即时反馈
- **updates 模式**：在多 Agent 系统中跟踪各节点状态
- **tasks 模式**：并行 Agent 执行时监控任务完成情况
- **custom 模式**：显示 "AI 正在思考..." 等进度提示

---

## 小结

- `stream()` / `astream()` 是核心 API
- `"messages"` 模式最常用，实时显示 LLM token
- `"updates"` 模式显示节点输出，适合多 Agent
- `"custom"` + `get_stream_writer()` 可自定义进度提示
- `"checkpoints"` 用于时间旅行调试
- v2 统一了输出格式（带 `type` 和 `data` 字段）
