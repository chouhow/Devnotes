# LangGraph 运行时（Pregel）

## 概述

`Pregel` 是 LangGraph 的核心运行时，负责管理 LangGraph 应用的执行。

编译一个 `StateGraph` 或创建一个 `@entrypoint` 会生成一个 `Pregel` 实例，可以调用。

**名称来源**：Pregel 来自 Google 的 Pregel 算法，描述了一种基于图的大规模并行计算方法。

---

## 三阶段执行模型

每一步（Step）包含三个阶段：

```
Plan（计划） → Execute（执行） → Update（更新）→ 重复，直到无节点可执行
```

### 1. Plan（计划）

确定本步要执行哪些节点（Actor）：
- 第一步：选择订阅特殊输入通道的节点
- 后续步骤：选择上一步更新过通道的节点

### 2. Execute（执行）

并行执行所有选中的节点，直到：
- 全部完成
- 有一个失败
- 到达超时

**关键**：执行阶段中，通道的更新对其他节点不可见，直到下一步。

### 3. Update（更新）

把各节点写入的值更新到通道。

---

## Actor（执行单元）

Actor = `PregelNode`，订阅通道、从通道读取、向通道写入。可以理解为 Pregel 算法中的"角色"。`PregelNode` 实现了 LangChain 的 Runnable 接口。

---

## Channel（通道）

通道用于 Actor 之间的通信。每个通道有：
- **值类型**（Value Type）：存储的值类型
- **更新类型**（Update Type）
- **更新函数**（Update Function）：对一系列更新应用合并规则

LangGraph 内置通道：

| 通道 | 作用 | 适用场景 |
|------|------|---------|
| `LastValue` | 存储最新值 | 输入/输出、在步骤间传递数据 |
| `Topic` | Pub/Sub 主题，可累积多个值 | 多值传递、结果收集 |
| `BinaryOperatorAggregate` | 用二元操作符合并 | 聚合计算（如累加）|
| `EphemeralValue` | 临时值，只在当前步可见 | 临时中间结果 |

---

## 直接使用 Pregel API

大多数用户通过 `StateGraph` API 或 `@entrypoint` 使用，但也可以直接操作 Pregel。

### 单节点示例

```python
from langgraph.channels import EphemeralValue
from langgraph.pregel import Pregel, NodeBuilder

node1 = (
    NodeBuilder()
    .subscribe_only("a")
    .do(lambda x: x + x)
    .write_to("b")
)

app = Pregel(
    nodes={"node1": node1},
    channels={
        "a": EphemeralValue(str),
        "b": EphemeralValue(str),
    },
    input_channels=["a"],
    output_channels=["b"],
)

result = app.invoke({"a": "foo"})
# {'b': 'foofoo'}
```

### 多节点示例

```python
from langgraph.channels import LastValue, EphemeralValue
from langgraph.pregel import Pregel, NodeBuilder

node1 = (
    NodeBuilder()
    .subscribe_only("a")
    .do(lambda x: x + x)
    .write_to("b")
)
node2 = (
    NodeBuilder()
    .subscribe_only("b")
    .do(lambda x: x + x)
    .write_to("c")
)

app = Pregel(
    nodes={"node1": node1, "node2": node2},
    channels={
        "a": EphemeralValue(str),
        "b": LastValue(str),
        "c": EphemeralValue(str),
    },
    input_channels=["a"],
    output_channels=["b", "c"],
)

result = app.invoke({"a": "foo"})
# {'b': 'foofoo', 'c': 'foofoofoofoo'}
```

### Topic（主题）通道

Topic 用于在节点间传递多个值：

```python
from langgraph.channels import Topic, EphemeralValue

node1 = NodeBuilder().subscribe_only("a").write_to("b")
node2 = NodeBuilder().subscribe_only("b").do(lambda x: x).write_to("c")

app = Pregel(
    nodes={"node1": node1, "node2": node2},
    channels={
        "a": EphemeralValue(str),
        "b": Topic(str),      # 累积多个值
        "c": EphemeralValue(str),
    },
    input_channels=["a"],
    output_channels=["c"],
)
```

### BinaryOperatorAggregate（聚合）通道

用二元操作符合并值，常用于累加：

```python
from langgraph.channels import BinaryOperatorAggregate
import operator

app = Pregel(
    nodes={"counter": counter_node},
    channels={"count": BinaryOperatorAggregate(int, operator.add)},
    input_channels=["input"],
    output_channels=["count"],
)
```

### 循环（Cycle）

图中可以有环（循环），通过设置 `channels` 手动管理：

```python
# 定义节点
node1 = NodeBuilder().subscribe_only("a").do(lambda x: x + 1).write_to("b")
node2 = NodeBuilder().subscribe_only("b").do(lambda x: x + 1).write_to("a")  # 循环回 a

app = Pregel(
    nodes={"node1": node1, "node2": node2},
    channels={
        "a": LastValue(int),
        "b": LastValue(int),
    },
    input_channels=["a"],
    output_channels=["a"],
    # max_steps 控制循环上限，防止无限循环
)
```

---

## 小结

- **Pregel** = LangGraph 核心运行时，管理 Actor 和 Channel
- **Actor** = `PregelNode`，读取/写入通道
- **Channel** = Actor 间通信，有 LastValue / Topic / BinaryOperatorAggregate / EphemeralValue
- **三阶段**：Plan → Execute（并行）→ Update，循环直到无可执行节点
- 大多数场景通过 `StateGraph` API 使用，不直接操作 Pregel
