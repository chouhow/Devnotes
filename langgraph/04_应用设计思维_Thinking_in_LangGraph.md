# LangGraph 应用设计思维

## 什么是 LangGraph 的思维方式

LangGraph 的核心是把复杂的工作流拆成**离散的步骤**，每个步骤变成一个节点，节点之间用边连接。

LangGraph 适合的场景：

- 需要**多轮交互**（如对话 Agent）
- 需要**人工审核**（Human-in-the-loop）
- 需要**多次工具调用**（如研究助手）
- 需要**容错和恢复**（如长时间运行的工作流）

---

## 五步设计法

### Step 1：把工作流拆成离散步骤

识别流程中每个独立的步骤，每个步骤对应一个节点（Node）。然后画出这些步骤之间的连接关系。

以**邮件处理 Agent** 为例：

```
读取邮件 → 分类意图 → [搜索文档 / 创建工单 / 草稿回复]
                                   ↓
                               人工审核 → 发送回复
```

各节点的职责：

| 节点 | 职责 | 说明 |
|------|------|------|
| 读取邮件 | 提取并解析邮件内容 | Data 步骤 |
| 分类意图 | LLM 判断紧急程度和话题 | LLM 步骤 |
| 搜索文档 | 查询知识库获取答案 | Data 步骤 |
| 创建工单 | 创建 Bug 跟踪工单 | Action 步骤 |
| 草稿回复 | LLM 生成回复草稿 | LLM 步骤 |
| 人工审核 | 人工审批或直接处理 | User Input 步骤 |
| 发送回复 | 发送邮件 | Action 步骤 |

---

### Step 2：确定每步的类型

每个节点属于以下四种类型之一：

| 类型 | 适用场景 | 特点 |
|------|---------|------|
| **LLM 步骤** | 需要理解、分析、生成文字、做推理决策 | 调用 LLM，返回文本或结构化数据 |
| **Data 步骤** | 从外部数据源获取信息 | 如知识库搜索、API 查询 |
| **Action 步骤** | 执行外部操作（发邮件、创建工单）| 有副作用，需要幂等性 |
| **User Input 步骤** | 需要人工介入、审批、输入 | 与 Human-in-the-loop 结合 |

### LLM 步骤

用于理解、分析、生成文字：

```python
# 分类意图
def classify_intent(state: EmailState):
    prompt = f"判断以下邮件的紧急程度和话题：\n{state['email_content']}"
    result = llm.invoke(prompt)
    return {"intent": result}
```

### Data 步骤

从外部获取数据，需要重试策略：

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2))
def search_docs(query: str):
    return vector_store.similarity_search(query, k=3)
```

### Action 步骤

执行外部操作，需要幂等性：

```python
@task
def send_email(to: str, body: str):
    # 幂等实现：先查重再发送
    existing = db.emails.find_one({"to": to, "body_hash": hash(body)})
    if existing:
        return {"email_id": existing["id"]}
    return {"email_id": db.emails.insert_one({"to": to, "body": body}).inserted_id}
```

### User Input 步骤

```python
from langgraph.types import interrupt, Command

def human_review(state: EmailState):
    # 暂停，等待人工审批
    approved = interrupt({
        "question": "是否批准发送此回复？",
        "reply": state["draft_reply"]
    })
    if approved:
        return {"status": "approved"}
    return {"status": "rejected"}
```

---

### Step 3：确定状态的 schema

每个节点需要什么数据，就把什么放进状态（State）。常见模式：

#### 只读（Pass State Through）

不需要累积数据，只是透传：

```python
class State(TypedDict):
    email_content: str  # 透传，不累积

def read_email(state: State):
    return {"email_content": "email text..."}  # 替换值
```

#### 累积（Append to State）

需要在多步间累积数据：

```python
from typing_extensions import Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]  # 累积新消息
    email_content: str                        # 透传
```

#### 广播（Broadcast）

多个节点需要访问同一数据：

```python
# 设置通道，让多个节点都能订阅
builder.add_edge("classify_intent", "search_docs")  # search_docs 读取 classify_intent 的输出
```

---

### Step 4：定义路由逻辑

哪些节点在什么情况下执行？

#### 固定路由

总是执行同一后继节点：

```python
builder.add_edge("read_email", "classify_intent")
# read_email 完成后总是执行 classify_intent
```

#### 条件路由

根据状态决定下一个节点：

```python
def route_intent(state: EmailState):
    intent = state["intent"]
    if intent == "bug":
        return "create_ticket"
    elif intent == "refund":
        return "process_refund"
    else:
        return "draft_reply"
```

---

### Step 5：处理边界情况

| 边界情况 | 处理方式 |
|---------|---------|
| LLM 返回错误 | 重试，或降级处理 |
| 工具调用超时 | 幂等设计 + 重试 |
| 人工审核超时 | 自动升级或取消 |
| 循环次数过多 | 设置 `max_steps` |

---

## LangGraph 常用设计模式

### 反思模式（Reflection）

让 LLM 审视自己的输出：

```
LLM 生成 → LLM 审查 → [通过？] → 是：输出  否：回到 LLM 生成
```

### 并行工具调用

多个工具同时调用：

```python
def parallel_search(state: State):
    futures = [
        search_docs.query(state["query"])
        for _ in range(3)  # 并行 3 次
    ]
    results = [f.result() for f in futures]
    return {"search_results": results}
```

### 多 Agent 协作

```
用户 → 主 Agent → 专家 Agent A / 专家 Agent B → 汇总 → 输出
```

每个专家 Agent 是独立的子图，主 Agent 负责协调。

---

## 小结

LangGraph 设计五步：
1. **拆步骤**：把工作流拆成离散节点
2. **定类型**：LLM / Data / Action / User Input
3. **定 State**：透传 or 累积 or 广播
4. **定路由**：固定 or 条件
5. **处理边界**：重试、幂等、超时、循环上限
