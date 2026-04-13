# LangGraph 持久化存储（Persistence）

## 为什么需要持久化

LangGraph 的持久化层将图状态保存为**检查点（Checkpoint）**。编译图时指定 Checkpointer 后，每一步执行的状态都会按**线程（Thread）**组织保存。

持久化是以下能力的基础：

| 能力 | 说明 |
|------|------|
| **人工审核（Human-in-the-loop）** | 暂停图执行，人工审批后继续 |
| **对话记忆（Memory）** | 多轮对话之间保持上下文 |
| **时间旅行调试（Time Travel）** | 回放任意历史检查点，调试或分叉 |
| **容错** | 节点失败后从最后一个成功检查点恢复 |

---

## 核心概念

### Thread（线程）

Thread 是每次运行绑定的唯一 ID，用 `thread_id` 标识：

```python
config = {"configurable": {"thread_id": "1"}}
graph.invoke({"input": "..."}, config)
```

同一个 `thread_id` 共享状态历史，不同 `thread_id` 互不影响。**调用 Checkpointer 时必须指定 `thread_id`**，否则无法保存状态或从中断点恢复。

### Checkpoint（检查点）

检查点是某一时刻图的完整快照，保存为 `StateSnapshot` 对象。每个 Super-step（超级步）边界保存一次检查点。

#### Super-step（超级步）

Super-step 是图中所有节点并行执行一次的"_tick"。对于顺序图 `START -> A -> B -> END`：

```
输入 → node_A → node_B → 结束
  ↓        ↓        ↓
检查点0  检查点1   检查点2
```

#### 检查点的字段

`StateSnapshot` 的主要字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `values` | dict | 该检查点的所有通道值 |
| `next` | tuple | 接下来要执行的节点列表，空 = 图结束 |
| `config` | dict | 包含 `thread_id`、`checkpoint_ns`、`checkpoint_id` |
| `metadata` | dict | 执行元数据：`source`（input/loop/update）、`writes`、`step` |
| `created_at` | str | ISO 8601 时间戳 |
| `parent_config` | dict | 上一个检查点的配置 |
| `tasks` | tuple | 本步待执行的任务（含中断信息）|

---

## 获取和更新状态

### 获取当前状态

```python
# 获取最新检查点
config = {"configurable": {"thread_id": "1"}}
state = graph.get_state(config)

# 指定具体 checkpoint_id 获取历史检查点
config = {"configurable": {
    "thread_id": "1",
    "checkpoint_id": "1ef663ba-28fe-6528-8002-5a559208592c"
}}
state = graph.get_state(config)
```

### 获取状态历史

```python
# 获取完整执行历史（最新在前）
history = list(graph.get_state_history(config))
for checkpoint in history:
    print(checkpoint.metadata["step"], checkpoint.values)
```

### 查找特定检查点

```python
# 查找某节点执行前的检查点
before_node_b = next(s for s in history if s.next == ("node_b",))

# 按 step 编号查找
step_2 = next(s for s in history if s.metadata["step"] == 2)

# 查找有中断的检查点
interrupted = next(
    s for s in history
    if s.tasks and any(t.interrupts for t in s.tasks)
)
```

---

## 重放（Replay）

用 `checkpoint_id` 重放历史检查点之后的所有步骤：

```python
config = {
    "configurable": {
        "thread_id": "1",
        "checkpoint_id": "某个历史checkpoint_id"
    }
}
graph.invoke(None, config)  # 输入传 None，从检查点恢复
```

已保存的节点结果不会重新执行，之后的节点（包括 LLM 调用、API 请求、中断）会重新触发。

---

## 更新状态

用 `update_state` 直接编辑检查点状态，生成新检查点（旧检查点不受影响）：

```python
# 更新状态（通过 reducer 合并）
graph.update_state(config, {"foo": "new_value"})

# 指定作为某个节点更新（影响下一个执行节点）
graph.update_state(config, {"foo": "x"}, as_node="node_b")
```

---

## Memory Store（跨线程存储）

### Checkpointer vs Store

| | Checkpointer | Store |
|--|-------------|-------|
| 作用域 | 同一 `thread_id` 内共享 | **跨线程**共享 |
| 用途 | 同一会话的状态历史 | 跨会话的长期信息（如用户偏好）|

### 基本用法

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

# 定义命名空间
user_id = "user-123"
namespace = (user_id, "memories")

# 存储记忆
memory_id = str(uuid.uuid4())
store.put(namespace, memory_id, {"food_preference": "I like pizza"})

# 读取记忆
memories = store.search(namespace)
print(memories[-1].dict())
```

### 语义搜索

配置 embedding 模型后，支持自然语言查询：

```python
from langchain.embeddings import init_embeddings

store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "dims": 1536,
        "fields": ["food_preference"]  # 指定嵌入哪些字段
    }
)

# 自然语言搜索
memories = store.search(
    namespace,
    query="What does the user like to eat?",
    limit=3
)
```

### 在 LangGraph 中使用

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()  # 同一会话状态
store = InMemoryStore(...)      # 跨会话长期记忆

# 编译时同时传入
graph = builder.compile(
    checkpointer=checkpointer,
    store=store
)

# 调用时指定 thread_id 和 user_id
config = {"configurable": {"thread_id": "1", "user_id": "user-123"}}
graph.invoke({"messages": [...]}, config)
```

---

## 小结

- **Checkpointer** 保存每一步的图状态快照，同一 `thread_id` 共享
- **`thread_id` 必须指定**，否则无法持久化和恢复
- **Super-step** 是检查点边界，一个超级步内所有节点并行执行
- **Store** 跨线程存储长期信息（用户偏好等），支持语义搜索
- 生产环境用 `PostgresSaver` / `RedisSaver` 等持久化 Checkpointer，`PostgresStore` / `RedisStore` 存储
