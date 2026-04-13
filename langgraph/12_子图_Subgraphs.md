# LangGraph 子图（Subgraphs）

## 什么是子图

子图是把一个图作为另一个图的节点来使用。适用于：

- 构建**多智能体系统**（Multi-Agent）
- 在多个图中**复用同一组节点**
- **团队分工**：各组独立开发自己的子图，只要接口（输入/输出 schema）不变

---

## 两种调用方式

| 方式 | 使用场景 | 状态 schema |
|------|---------|-----------|
| [在节点内调用子图](#在节点内调用子图) | 父子图**状态 schema 不同**，需要状态转换 | 各自独立 |
| [把子图作为节点添加](#把子图作为节点添加) | 父子图**共享状态 key**（如 messages）| 自动同步 |

---

## 在节点内调用子图

当父子图状态 schema 不同时（如多智能体系统，每个 Agent 有独立的消息历史），在节点函数中手动调用子图并做状态转换：

```python
class SubgraphState(TypedDict):
    bar: str  # 与父图不共享

class ParentState(TypedDict):
    foo: str  # 与子图不共享

# 子图
subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# 父图中：状态转换后调用子图，结果转换回来
def call_subgraph(state: ParentState):
    subgraph_output = subgraph.invoke({"bar": state["foo"]})  # 父 -> 子
    return {"foo": subgraph_output["bar"]}  # 子 -> 父

builder = StateGraph(ParentState)
builder.add_node("node_1", call_subgraph)
```

### 多级子图（父 → 子 → 孙）

```python
# 祖父图
class GrandChildState(TypedDict):
    my_grandchild_key: str

grandchild = StateGraph(GrandChildState)
grandchild.add_node("grandchild_1", grandchild_1)
grandchild.add_edge(START, "grandchild_1")
grandchild_graph = grandchild.compile()

# 子图（调用祖父图）
class ChildState(TypedDict):
    my_child_key: str

def call_grandchild(state: ChildState):
    output = grandchild_graph.invoke({"my_grandchild_key": state["my_child_key"]})
    return {"my_child_key": output["my_grandchild_key"] + " today?"}

# 父图（调用子图）
class ParentState(TypedDict):
    my_key: str

def call_child(state: ParentState):
    output = child_graph.invoke({"my_child_key": state["my_key"]})
    return {"my_key": output["my_child_key"]}
```

---

## 把子图作为节点添加

当父子图**共享状态 key** 时（典型场景：多 Agent 通过共享 `messages` key 通信），直接把编译好的子图传给 `add_node`：

```python
from langgraph.graph.state import StateGraph, START

# 子图（与父图共享 foo key）
class SubgraphState(TypedDict):
    foo: str    # 与父图共享
    bar: str    # 子图私有

def subgraph_node_1(state: SubgraphState):
    return {"bar": "bar"}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# 父图
builder = StateGraph(SubgraphState)  # 同样 schema
builder.add_node("node_1", subgraph)  # 直接传子图，无需 wrapper
builder.add_edge(START, "node_1")
```

子图直接读写父图的状态通道，无需手动转换。

---

## 子图持久化模式

子图的 `checkpointer` 参数控制子图内部数据在调用之间如何保存：

| 模式 | `checkpointer=` | 说明 |
|------|----------------|------|
| **每次调用独立（默认）** | `None` | 每次调用独立，子图无记忆 |
| **按线程持久化** | `True` | 同一线程内多次调用累积状态 |
| **无状态** | `False` | 无检查点，不支持中断和容错 |

> **注意**：父图必须编译时带 checkpointer，子图的持久化功能才生效。

### 每次调用独立（Per-invocation，默认）

适用于多 Agent 系统，每次调用独立处理一个请求。子图无记忆，支持 `interrupt()` 和容错：

```python
from langchain.agents import create_agent

# 子 Agent（不设 checkpointer，每次调用独立）
fruit_agent = create_agent(
    model="gpt-4.1-mini",
    tools=[fruit_info],
    prompt="You are a fruit expert..."
)

# 父 Agent（带 checkpointer，支持中断和恢复）
agent = create_agent(
    model="gpt-4.1-mini",
    tools=[ask_fruit_expert, ask_veggie_expert],
    checkpointer=MemorySaver()
)
```

特点：
- 每次调用独立，`interrupt()` 可暂停恢复
- 多 Agent 并行调用无冲突
- 子 Agent 不记住前一次调用

### 按线程持久化（Per-thread）

子图需要在同一线程内累积记忆（如研究助手多轮对话）：

```python
# 子 Agent 启用 checkpointer=True
fruit_agent = create_agent(
    model="gpt-4.1-mini",
    tools=[fruit_info],
    prompt="You are a fruit expert...",
    checkpointer=True  # 同线程累积状态
)
```

特点：
- 同一线程内多次调用累积记忆
- **不支持并行调用**（会写冲突）

> ⚠️ 使用 `ToolCallLimitMiddleware` 防止 LLM 并行调用同一子 Agent：

```python
from langchain.agents.middleware import ToolCallLimitMiddleware

agent = create_agent(
    model="gpt-4.1-mini",
    tools=[ask_fruit_expert],
    middleware=[ToolCallLimitMiddleware(tool_name="ask_fruit_expert", limit=1)]
)
```

---

## 小结

- **状态 schema 不同** → 在节点函数中手动调用子图，做状态转换
- **状态 schema 共享** → 直接把编译好的子图传给 `add_node`
- 子图持久化三种模式：`None`（每次独立）、`True`（按线程累积）、`False`（无状态）
- `interrupt()` 在子图中可用（需父图有 checkpointer）
- 多 Agent 并行调用 → 用 `None`（每次独立）；子 Agent 需要多轮记忆 → 用 `True`
