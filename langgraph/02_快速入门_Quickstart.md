# LangGraph 快速入门

本文演示如何用 LangGraph 构建一个计算器 Agent，分别用 **Graph API** 和 **Functional API** 两种方式实现。

---

## 前置要求

- 安装 LangGraph：`pip install langgraph`
- 设置 LLM（以 Anthropic Claude 为例）：`export ANTHROPIC_API_KEY=your-key`

---

## 方式一：Graph API

Graph API 把 Agent 定义为**节点和边的图**，适合复杂的工作流。

### 1. 定义工具和模型

```python
from langchain.tools import tool
from langchain.chat_models import init_chat_model

model = init_chat_model("claude-sonnet-4-6", temperature=0)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide a by b."""
    return a / b

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)
```

### 2. 定义状态

```python
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]  # 新消息追加到列表
    llm_calls: int
```

`Annotated[..., operator.add]` 的作用：保证新消息追加到列表而不是替换。

### 3. 定义 LLM 节点

```python
from langchain.messages import SystemMessage

def llm_call(state: dict):
    response = model_with_tools.invoke(
        [SystemMessage(content="You are a helpful arithmetic assistant.")] + state["messages"]
    )
    return {"messages": [response], "llm_calls": state.get("llm_calls", 0) + 1}
```

### 4. 定义工具节点

```python
from langchain.messages import ToolMessage

def tool_node(state: dict):
    results = []
    for tool_call in state["messages"][-1].tool_calls:
        result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        results.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
    return {"messages": results}
```

### 5. 定义路由逻辑（条件边）

LLM 返回 `tool_calls` 时调用工具节点，否则结束：

```python
from langgraph.types import Command, Send

def should_continue(state: dict):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool_node"
    return "__end__"
```

### 6. 构建图

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue)
builder.add_edge("tool_node", "llm_call")
graph = builder.compile()

# 可视化
display(Image(graph.get_graph().draw_mermaid_png()))
```

### 7. 调用

```python
result = graph.invoke({"messages": [], "llm_calls": 0})
print(result["messages"][-1].content)
```

---

## 方式二：Functional API

Functional API 把 Agent 定义为**单个函数**，适合简单场景。

### 1. 定义入口函数

```python
from langgraph.func import entrypoint, task

@task
def multiply(a: int, b: int) -> int:
    return a * b

@task
def add(a: int, b: int) -> int:
    return a + b

@task
def divide(a: int, b: int) -> float:
    return a / b

@entrypoint()
def calculator(state: dict) -> dict:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        results = []
        for call in last.tool_calls:
            result = {"add": add, "multiply": multiply, "divide": divide}[call["name"]].invoke(call["args"])
            results.append({"role": "tool", "content": str(result), "tool_call_id": call["id"]})
        return {"messages": results}
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph = calculator.compile()
```

### 2. 调用

```python
result = graph.invoke({"messages": [{"role": "user", "content": "What is 5 * 3?"}]})
print(result["messages"][-1].content)
```

---

## 两种方式对比

| 特性 | Graph API | Functional API |
|------|-----------|--------------|
| 代码风格 | 节点 + 边 | 单个入口函数 |
| 适用场景 | 复杂工作流，多路由 | 简单线性逻辑 |
| 灵活性 | 高（可自定义条件边）| 中（路由逻辑在函数内）|
| 可视化 | 天然支持 | 支持 |
| 学习曲线 | 较陡 | 较平缓 |
