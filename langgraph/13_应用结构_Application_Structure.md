# LangGraph 应用结构

LangGraph 应用由以下部分组成：
- 一个或多个图（Graphs）
- 配置文件 `langgraph.json`
- 依赖文件（`requirements.txt` 或 `pyproject.toml`）
- 可选的 `.env` 环境变量文件

---

## 目录结构示例

### Python (requirements.txt)

```
my-app/
├── my_agent/              # 项目代码
│   ├── utils/             # 工具函数
│   │   ├── __init__.py
│   │   ├── tools.py       # 图的工具
│   │   ├── nodes.py       # 节点函数
│   │   └── state.py       # 状态定义
│   ├── __init__.py
│   └── agent.py           # 图构建代码
├── .env                   # 环境变量
├── requirements.txt       # 依赖
└── langgraph.json         # LangGraph 配置
```

### Python (pyproject.toml)

```
my-app/
├── my_agent/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   ├── nodes.py
│   │   └── state.py
│   ├── __init__.py
│   └── agent.py
├── .env
├── langgraph.json
└── pyproject.toml         # 依赖配置
```

---

## 配置文件 langgraph.json

```json
{
  "dependencies": [
    "langchain_openai",
    "./your_package"
  ],
  "graphs": {
    "my_agent": "./your_package/your_file.py:agent"
  },
  "env": ".env"
}
```

| 字段 | 说明 |
|------|------|
| `dependencies` | 依赖包列表，支持 PyPI 包和本地包 |
| `graphs` | 图定义，`名称: 文件路径:变量名` |
| `env` | 环境变量文件路径 |

---

## 核心文件说明

### agent.py（图构建）

```python
from langgraph.graph import StateGraph, START, END
from .utils.state import State
from .utils.nodes import node1, node2

builder = StateGraph(State)
builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", END)

agent = builder.compile()
```

### state.py（状态定义）

```python
from typing_extensions import TypedDict
from langchain.messages import BaseMessage

class State(TypedDict):
    messages: list[BaseMessage]
    context: dict
```

### nodes.py（节点函数）

```python
def node1(state: State):
    # 处理逻辑
    return {"messages": [...]}

def node2(state: State):
    # 处理逻辑
    return {"context": {...}}
```

### tools.py（工具定义）

```python
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"
```

---

## 依赖配置

### requirements.txt

```
langgraph
langchain
langchain-openai
```

### pyproject.toml

```toml
[project]
name = "my-agent"
version = "0.1.0"
dependencies = [
    "langgraph",
    "langchain",
    "langchain-openai",
]

[project.optional-dependencies]
dev = ["pytest"]
```

---

## 环境变量 .env

```bash
LANGSMITH_API_KEY=lsv2...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

---

## 部署到 LangSmith

按此结构组织代码后，推送到 GitHub，即可在 LangSmith 中一键部署。

---

## 小结

| 文件 | 作用 |
|------|------|
| `langgraph.json` | 配置依赖、图、环境变量 |
| `agent.py` | 构建和编译图 |
| `state.py` | 定义状态 schema |
| `nodes.py` | 节点处理函数 |
| `tools.py` | 工具定义 |
| `requirements.txt` / `pyproject.toml` | 依赖管理 |
| `.env` | 环境变量 |
