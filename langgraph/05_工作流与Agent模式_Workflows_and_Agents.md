# LangGraph 工作流与 Agent 模式

LangGraph 实现了多种经典 LLM 应用模式。以下是常见模式的实现方法。

---

## 1. Prompt Chaining（提示链）

多个 LLM 调用串联，前一个的输出作为后一个的输入。适用于：
- 翻译文档（先翻译，再润色）
- 内容验证（先生成，再检查一致性）

```python
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str

def generate_joke(state: State):
    msg = llm.invoke(f"Write a short joke about {state['topic']}")
    return {"joke": msg.content}

def check_punchline(state: State):
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "Fail"

def improve_joke(state: State):
    msg = llm.invoke(f"Make this joke funnier: {state['joke']}")
    return {"improved_joke": msg.content}

def polish_joke(state: State):
    msg = llm.invoke(f"Add a twist: {state['improved_joke']}")
    return {"final_joke": msg.content}

workflow = StateGraph(State)
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)
workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke",
    check_punchline,
    {"Fail": "improve_joke", "Pass": END}
)
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

chain = workflow.compile()
result = chain.invoke({"topic": "cats"})
```

---

## 2. Parallelization（并行化）

多个 LLM 同时处理，提高速度或增加多样性。

### 2.1 分治（Divide and Conquer）

```python
def parallel_section(state: State):
    # 同时处理多个段落
    sections = state["sections"]
    futures = [summarize_section(s) for s in sections]
    results = [f.result() for f in futures]
    return {"summaries": results}

def aggregate(state: State):
    # 汇总所有结果
    return {"final": "\n".join(state["summaries"])}

workflow = StateGraph(State)
workflow.add_node("parallel", parallel_section)
workflow.add_node("aggregate", aggregate)
workflow.add_edge(START, "parallel")
workflow.add_edge("parallel", "aggregate")
```

### 2.2 投票（Voting）

```python
def generate_candidate(state: State):
    # 生成多个候选答案
    return {"candidates": [llm.invoke(prompt).content for _ in range(3)]}

def vote(state: State):
    # 投票选出最佳
    best = max(state["candidates"], key=lambda x: score(x))
    return {"answer": best}
```

---

## 3. Routing（路由）

根据输入内容路由到不同的处理路径。

```python
def classify_query(state: State):
    result = llm.invoke(f"Classify: {state['query']}")
    return {"category": result.content}

def route(state: State):
    category = state["category"]
    if category == "technical":
        return "technical_support"
    elif category == "billing":
        return "billing_support"
    return "general_support"

workflow = StateGraph(State)
workflow.add_conditional_edges(
    START,
    route,
    {
        "technical_support": "tech_node",
        "billing_support": "billing_node",
        "general_support": "general_node"
    }
)
```

---

## 4. Orchestrator-Workers（协调器-工作者）

中央协调器动态分解任务，分配给多个工作者并行执行，最后汇总。

```python
def orchestrator(state: State):
    # 分析任务，分解为子任务
    plan = llm.invoke(f"Plan steps for: {state['task']}")
    return {"plan": parse_plan(plan.content)}

def worker(state: State):
    # 执行子任务
    task = state["current_task"]
    result = llm.invoke(f"Do: {task}")
    return {"results": [result.content]}

def aggregate(state: State):
    # 汇总所有工作者结果
    return {"final": combine(state["results"])}

workflow = StateGraph(State)
workflow.add_node("orchestrator", orchestrator)
workflow.add_node("worker", worker)
workflow.add_node("aggregate", aggregate)
workflow.add_edge(START, "orchestrator")
workflow.add_edge("orchestrator", "worker")
workflow.add_edge("worker", "aggregate")
```

---

## 5. Evaluator-Optimizer（评估-优化）

一个 LLM 生成，另一个评估，循环直到满足条件。

```python
def generate(state: State):
    result = llm.invoke(f"Generate: {state['prompt']}")
    return {"output": result.content}

def evaluate(state: State):
    score = llm.invoke(f"Score 1-10: {state['output']}")
    return {"score": int(score.content)}

def should_continue(state: State):
    if state["score"] >= 8 or state["iteration"] > 3:
        return "done"
    return "improve"

def improve(state: State):
    better = llm.invoke(f"Improve: {state['output']}")
    return {"output": better.content, "iteration": state["iteration"] + 1}

workflow = StateGraph(State)
workflow.add_node("generate", generate)
workflow.add_node("evaluate", evaluate)
workflow.add_node("improve", improve)
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "evaluate")
workflow.add_conditional_edges(
    "evaluate",
    should_continue,
    {"done": END, "improve": "improve"}
)
workflow.add_edge("improve", "evaluate")
```

---

## 6. Agent（自主智能体）

Agent 自主决定下一步行动，循环直到完成。

```python
from langgraph.prebuilt import create_react_agent

tools = [search_docs, create_ticket, send_email]

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=MemorySaver()  # 支持中断和恢复
)

# Agent 自主决定：
# 1. 是否需要工具
# 2. 调用哪个工具
# 3. 何时结束
result = agent.invoke({"messages": [{"role": "user", "content": "Help me"}]})
```

---

## 模式对比

| 模式 | 结构 | 适用场景 |
|------|------|---------|
| Prompt Chaining | 线性链 | 可分解的确定性任务 |
| Parallelization | 并行分支 | 分治、投票、多样性 |
| Routing | 条件分支 | 不同类型输入需要不同处理 |
| Orchestrator-Workers | 中心-辐射 | 复杂任务需要动态分解 |
| Evaluator-Optimizer | 循环 | 需要高质量输出，可迭代改进 |
| Agent | 自主循环 | 开放性问题，需要工具调用 |

---

## 如何选择

- **确定性流程** → Prompt Chaining / Routing
- **需要速度** → Parallelization
- **复杂任务** → Orchestrator-Workers
- **质量要求高** → Evaluator-Optimizer
- **开放性问题** → Agent
