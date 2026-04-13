# LangGraph 时间旅行（Time Travel）

## 概述

LangGraph 通过**检查点（Checkpoint）**实现时间旅行：

- **Replay（重放）**：从某个历史检查点重新执行
- **Fork（分叉）**：从某个历史检查点分叉，修改状态，探索另一条路

两者都基于检查点：检查点之前的节点不重复执行，检查点之后的节点重新执行（LLM 调用、API 请求、中断都会重新触发，可能产生不同结果）。

---

## Replay（重放）

从某个历史检查点重新执行，用于调试或修复问题。

```python
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7

class State(TypedDict):
    topic: str
    joke: str

def generate_topic(state: State):
    return {"topic": "socks in the dryer"}

def write_joke(state: State):
    return {"joke": f"Why do {state['topic']} disappear? They elopes!"}

checkpointer = InMemorySaver()
graph = (
    StateGraph(State)
    .add_node("generate_topic", generate_topic)
    .add_node("write_joke", write_joke)
    .add_edge(START, "generate_topic")
    .add_edge("generate_topic", "write_joke")
    .compile(checkpointer=checkpointer)
)

# Step 1：正常执行
config = {"configurable": {"thread_id": str(uuid7())}}
result = graph.invoke({}, config)

# Step 2：找到历史检查点
history = list(graph.get_state_history(config))
for state in history:
    print(f"next={state.next}, checkpoint_id={state.config['configurable']['checkpoint_id']}")

# Step 3：从 write_joke 之前重放
before_joke = next(s for s in history if s.next == ("write_joke",))
replay_result = graph.invoke(None, before_joke.config)
# write_joke 重新执行，generate_topic 不再执行
```

> ⚠️ **注意**：重放会重新执行节点，LLM 调用和 API 请求会重新触发，结果可能不同。

---

## Fork（分叉）

从某个历史检查点分叉，**修改状态**，探索另一条路径。不会影响原有历史。

```python
# 从 write_joke 之前分叉，修改 topic
before_joke = next(s for s in history if s.next == ("write_joke",))

# Fork：修改状态，创建新分支
fork_config = graph.update_state(
    before_joke.config,
    values={"topic": "chickens"}
)

# 从分叉点继续执行
fork_result = graph.invoke(None, fork_config)
print(fork_result["joke"])  # 关于 chicken 的笑话，不是 socks
```

> ⚠️ **注意**：`update_state` **不会回滚**线程，它创建的是一个新检查点，原有执行历史保持不变。

---

## 指定分叉的节点（as_node）

默认 LangGraph 会从检查点的历史记录推断节点。如果分叉时出现冲突或需要精确控制，可以用 `as_node` 显式指定：

```python
# 告诉 LangGraph：这个更新是 generate_topic 产生的
# 执行从 write_joke（generate_topic 的后继）继续
fork_config = graph.update_state(
    before_joke.config,
    values={"topic": "chickens"},
    as_node="generate_topic"
)
```

需要显式指定 `as_node` 的场景：
- **并行分支**：同一步有多个节点更新状态
- **全新线程**：设置初始状态（测试时常用）
- **跳过节点**：想让某个节点"已经执行过"

---

## 与中断（Interrupt）结合

如果在图中有 `interrupt()`，时间旅行会重新触发中断：

```python
from langgraph.types import interrupt, Command

class State(TypedDict):
    value: list[str]

def ask_human(state: State):
    answer = interrupt("What is your name?")
    return {"value": [f"Hello, {answer}!"]}

def final_step(state: State):
    return {"value": ["Done"]}

# 完整执行：ask_name -> ask_age -> final
config = {"configurable": {"thread_id": "1"}}
graph.invoke({"value": []}, config)               # 中断于 ask_name
graph.invoke(Command(resume="Alice"), config)     # 中断于 ask_age
graph.invoke(Command(resume="30"), config)       # 完成

# 从 ask_name 之前重放
history = list(graph.get_state_history(config))
before_ask = [s for s in history if s.next == ("ask_name",)][-1]
graph.invoke(None, before_ask.config)  # 再次触发 ask_name 的中断，等待新输入

# 从 ask_name 之前分叉，修改状态
fork_config = graph.update_state(before_ask.config, {"value": ["forked"]})
graph.invoke(None, fork_config)  # 触发中断
graph.invoke(Command(resume="Bob"), fork_config)
# 结果：{"value": ["forked", "Hello, Bob!", "Done"]}
```

### 在两个中断之间分叉

```python
# ask_name -> ask_age -> final，完成两个中断后：

# 从两个中断之间分叉（在 ask_name 之后，ask_age 之前）
history = list(graph.get_state_history(config))
between = [s for s in history if s.next == ("ask_age",)][-1]

fork_config = graph.update_state(between.config, {"value": ["modified"]})
result = graph.invoke(None, fork_config)
# ask_name 的结果保留（"name:Alice"）
# ask_age 触发中断，等待新答案
```

---

## 子图中的时间旅行

子图的时间旅行粒度取决于子图是否有自己的 checkpointer：

| 模式 | 说明 |
|------|------|
| **继承 checkpointer（默认）** | 子图作为单一超级步，只有一个父级检查点。只能从子图整体之前分叉/重放，不能定位到子图内部 |
| **子图独立 checkpointer** | 子图有自己的检查点历史，可以从子图内部任意节点分叉/重放 |

### 默认（继承 checkpointer）

```python
# 子图无独立 checkpointer（默认）
subgraph = StateGraph(State).compile()  # 继承父图的 checkpointer
graph = builder.compile(checkpointer=InMemorySaver())

# 只能从子图整体之前分叉
history = list(graph.get_state_history(config))
before_sub = [s for s in history if s.next == ("subgraph_node",)][-1]
fork_config = graph.update_state(before_sub.config, {"value": ["forked"]})
graph.invoke(None, fork_config)  # 整个子图重新执行，无法定位到子图内部
```

### 独立 checkpointer

```python
# 子图有独立 checkpointer=True
subgraph = StateGraph(State).compile(checkpointer=True)
graph = builder.compile(checkpointer=InMemorySaver())

# 获取子图内部的检查点
parent_state = graph.get_state(config, subgraphs=True)
sub_config = parent_state.tasks[0].state.config

# 从子图内部节点分叉
fork_config = graph.update_state(sub_config, {"value": ["forked"]})
graph.invoke(None, fork_config)  # 只重放该节点之后的部分
```

---

## 小结

- **Replay**：`get_state_history` → `invoke(None, checkpoint_config)`
- **Fork**：`update_state(checkpoint_config, values={})` → `invoke(None, new_config)`
- `update_state` **不回滚**，创建的是新分支
- Replay 重新执行节点，LLM 调用会再次触发
- 子图默认作为单一超级步，有独立 checkpointer 才能细粒度时间旅行
