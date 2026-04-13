# LangGraph 测试

## 概述

为 LangGraph Agent 添加测试，确保功能正确。本文介绍针对自定义图结构的测试模式。

---

## 前置要求

```bash
pip install -U pytest
```

---

## 基本测试模式

因为 LangGraph Agent 依赖状态，推荐在每个测试中创建新的图实例，并使用新的 checkpointer。

```python
import pytest
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def create_graph() -> StateGraph:
    class MyState(TypedDict):
        my_key: str

    graph = StateGraph(MyState)
    graph.add_node("node1", lambda state: {"my_key": "hello from node1"})
    graph.add_node("node2", lambda state: {"my_key": "hello from node2"})
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", END)
    return graph

def test_basic_agent_execution():
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)

    result = compiled_graph.invoke(
        {"my_key": "initial_value"},
        config={"configurable": {"thread_id": "1"}}
    )

    assert result["my_key"] == "hello from node2"
```

---

## 测试单个节点

编译后的图通过 `graph.nodes` 暴露每个节点的引用，可以单独测试：

```python
def test_individual_node_execution():
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)

    # 只调用 node1（绕过 checkpointer）
    result = compiled_graph.nodes["node1"].invoke(
        {"my_key": "initial_value"}
    )

    assert result["my_key"] == "hello from node1"
```

---

## 部分执行（Partial Execution）

对于大型图，可以测试部分执行：

```python
def test_partial_execution():
    graph = create_graph()
    compiled = graph.compile()

    # 只执行到 node1
    result = compiled.invoke(
        {"my_key": "initial"},
        config={
            "configurable": {"thread_id": "1"},
            "until": "node1"  # 只执行到 node1
        }
    )

    assert result["my_key"] == "hello from node1"
```

---

## Mock 外部依赖

使用 `unittest.mock` 或 `pytest-mock` 替换外部调用：

```python
from unittest.mock import patch

def test_with_mocked_llm():
    with patch("my_app.llm") as mock_llm:
        mock_llm.invoke.return_value = {"content": "mocked response"}

        graph = create_graph()
        result = graph.compile().invoke({"input": "test"})

        assert result["output"] == "mocked response"
```

---

## 测试 Human-in-the-loop

测试中断和恢复：

```python
from langgraph.types import Command

def test_interrupt_and_resume():
    graph = create_graph_with_interrupt()
    compiled = graph.compile(checkpointer=MemorySaver())

    config = {"configurable": {"thread_id": "1"}}

    # 第一次调用，遇到 interrupt 暂停
    result = compiled.invoke({"input": "test"}, config)
    assert result["__interrupt__"] is not None

    # 恢复执行
    result = compiled.invoke(Command(resume="approved"), config)
    assert result["status"] == "completed"
```

---

## 测试流式输出

```python
async def test_streaming():
    graph = create_graph()
    compiled = graph.compile()

    chunks = []
    async for chunk in compiled.astream(
        {"input": "test"},
        stream_mode="messages"
    ):
        chunks.append(chunk)

    assert len(chunks) > 0
```

---

## 测试最佳实践

| 实践 | 说明 |
|------|------|
| 每个测试新建图实例 | 避免状态污染 |
| 使用 MemorySaver | 测试环境用内存 checkpointer |
| Mock 外部 API | LLM、数据库等外部调用 mock 掉 |
| 测试单个节点 | 快速定位问题节点 |
| 测试中断恢复 | 确保 Human-in-the-loop 逻辑正确 |
