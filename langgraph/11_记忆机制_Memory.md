# LangGraph 记忆机制（Memory）

## 两种记忆类型

LangGraph 支持两种记忆：

| 类型 | 作用范围 | 实现方式 |
|------|---------|---------|
| **短期记忆** | 同一会话（同一 thread_id）内 | Checkpointer |
| **长期记忆** | 跨会话（不同 thread_id）间 | Store |

---

## 短期记忆：Checkpointer

### 基本用法

编译图时传入 Checkpointer，多轮对话自动共享状态：

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState

checkpointer = InMemorySaver()

builder = StateGraph(MessagesState)
# ... 添加节点
graph = builder.compile(checkpointer=checkpointer)

# 第一轮：传入 thread_id
config = {"configurable": {"thread_id": "1"}}
graph.invoke(
    {"messages": [{"role": "user", "content": "hi! I am Bob"}]},
    config
)

# 第二轮：同一 thread_id，自动记得上下文
graph.invoke(
    {"messages": [{"role": "user", "content": "what is my name?"}]},
    config
)
# 模型知道 Bob
```

### 生产环境：Postgres Checkpointer

```python
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # checkpointer.setup()  # 首次使用需调用
    graph = builder.compile(checkpointer=checkpointer)
```

### 生产环境：Redis Checkpointer

```python
from langgraph.checkpoint.redis import RedisSaver

DB_URI = "redis://localhost:6379"
with RedisSaver.from_conn_string(DB_URI) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
```

### 生产环境：MongoDB Checkpointer

```python
from langgraph.checkpoint.mongodb import MongoDBSaver

DB_URI = "localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
```

---

## 长期记忆：Store（跨会话）

Store 是跨线程（不同 thread_id）的持久化存储，适合保存用户偏好等长期信息。

### 基本用法

```python
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph

store = InMemoryStore()
builder = StateGraph(...)
graph = builder.compile(store=store)

# 存入记忆
namespace = ("user_123", "memories")
memory_id = str(uuid.uuid4())
store.put(namespace, memory_id, {"data": "用户喜欢深色模式"})

# 读取记忆
memories = store.search(namespace)
```

### 在节点中访问 Store

通过 `Runtime` 对象注入 Store，节点函数中通过 `runtime.store` 访问：

```python
from dataclasses import dataclass
from langgraph.runtime import Runtime

@dataclass
class Context:
    user_id: str

async def call_model(state: MessagesState, runtime: Runtime[Context]):
    user_id = runtime.context.user_id
    namespace = (user_id, "memories")

    # 语义搜索记忆
    memories = await runtime.store.asearch(
        namespace,
        query=state["messages"][-1].content,
        limit=3
    )

    # 存入新记忆
    await runtime.store.aput(
        namespace, str(uuid.uuid4()),
        {"data": "User prefers dark mode"}
    )

builder = StateGraph(MessagesState, context_schema=Context)
graph = builder.compile(store=store)

# 调用时传入上下文
graph.invoke(
    {"messages": [{"role": "user", "content": "hi"}]},
    {"configurable": {"thread_id": "1"}},
    context=Context(user_id="user_123")
)
```

### 语义搜索

配置 embedding 模型后，支持自然语言查询：

```python
from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore

embeddings = init_embeddings("openai:text-embedding-3-small")
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1536,
    }
)

# 存入记忆
store.put(("user_123", "memories"), "1", {"text": "I love pizza"})
store.put(("user_123", "memories"), "2", {"text": "I am a plumber"})

# 自然语言搜索
items = store.search(
    ("user_123", "memories"),
    query="I'm hungry",
    limit=1
)
```

### 生产环境：Postgres Store

```python
from langgraph.store.postgres import PostgresStore

DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresStore.from_conn_string(DB_URI) as store:
    # store.setup()  # 首次使用需调用
    graph = builder.compile(store=store)
```

### 生产环境：Redis Store

```python
from langgraph.store.redis import RedisStore

DB_URI = "redis://localhost:6379"
with RedisStore.from_conn_string(DB_URI) as store:
    graph = builder.compile(store=store)
```

---

## 短期记忆管理（防止上下文溢出）

对话太长会超过 LLM 的 context window，有几种处理方式：

### 1. 修剪消息（Trim）

用 `trim_messages` 限制 token 数量：

```python
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately
)

def call_model(state: MessagesState):
    messages = trim_messages(
        state["messages"],
        strategy="last",                         # 保留最近的消息
        token_counter=count_tokens_approximately,
        max_tokens=128,
        start_on="human",
        end_on=("human", "tool"),
    )
    response = model.invoke(messages)
    return {"messages": [response]}
```

### 2. 删除消息（Delete）

用 `RemoveMessage` 从状态中永久删除消息：

```python
from langchain.messages import RemoveMessage

def delete_messages(state):
    messages = state["messages"]
    if len(messages) > 2:
        # 删除最早的 2 条消息
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}

# 删除所有消息
from langgraph.graph.message import REMOVE_ALL_MESSAGES
def delete_all(state):
    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}
```

### 3. 总结消息（Summarize）

将早期消息总结，替换为摘要，保留上下文同时节省 token。

---

## 小结

| 组件 | 作用 | 关键 API |
|------|------|---------|
| **Checkpointer** | 同一 thread_id 内的状态历史 | `InMemorySaver`, `PostgresSaver` |
| **Store** | 跨 thread_id 的长期记忆 | `InMemoryStore`, `PostgresStore` |
| **trim_messages** | 修剪消息，防止上下文溢出 | `strategy="last"`, `max_tokens=128` |
| **RemoveMessage** | 删除指定消息 | `RemoveMessage(id=m.id)` |
| **Runtime** | 在节点中注入 Store 访问 | `runtime.store.search/put` |
