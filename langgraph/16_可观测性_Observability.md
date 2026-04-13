# LangGraph 可观测性（Observability）

LangSmith 提供完整的可观测性支持，帮助调试、评估和监控 LangGraph 应用。

---

## 前置要求

- LangSmith 账号（免费注册）：smith.langchain.com
- LangSmith API Key

---

## 启用追踪

设置环境变量：

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

默认追踪会记录到 `default` 项目。

---

## 选择性追踪

用 `tracing_context` 控制特定调用是否追踪：

```python
import langsmith as ls

# 这次调用会被追踪
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})

# 这次不会被追踪
agent.invoke({"messages": [{"role": "user", "content": "Another"}]})
```

---

## 指定项目

### 静态配置（全局）

```bash
export LANGSMITH_PROJECT=my-agent-project
```

### 动态配置（单次调用）

```python
import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Send email"}]
    })
```

---

## 添加元数据

为追踪添加自定义元数据，方便筛选和分析：

```python
from langsmith import trace

@trace(metadata={"agent_type": "email", "version": "1.0"})
def send_email_agent(input_data):
    return agent.invoke(input_data)

# 或运行时添加
with ls.tracing_context(metadata={"user_id": "123"}):
    agent.invoke({...})
```

---

## 敏感数据脱敏

防止敏感信息（密码、API Key 等）被记录：

```python
from langsmith.anonymizer import Anonymizer

anonymizer = Anonymizer(
    patterns=[
        r"password[=:]\s*\S+",
        r"api[_-]?key[=:]\s*\S+",
    ]
)

with ls.tracing_context(anonymizer=anonymizer):
    agent.invoke({"password": "secret123"})  # 会被脱敏为 ***
```

---

## 查看追踪

登录 LangSmith → 选择项目 → 查看 Traces：

- **执行步骤**：每个节点的输入输出
- **延迟**：每个步骤耗时
- **Token 消耗**：LLM 调用成本
- **错误**：异常和堆栈

---

## 调试本地应用

```python
# 本地开发时启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 追踪特定调用
with ls.tracing_context(enabled=True, project_name="debug"):
    result = agent.invoke({"input": "test"})
```

---

## 监控生产环境

- **Dashboard**：实时查看调用量、延迟、错误率
- **Alerts**：设置阈值告警
- **Compare**：对比不同版本的性能

---

## 小结

| 功能 | 方法 |
|------|------|
| 启用追踪 | `LANGSMITH_TRACING=true` |
| 选择性追踪 | `tracing_context(enabled=True)` |
| 指定项目 | `LANGSMITH_PROJECT` 或 `tracing_context(project_name=...)` |
| 添加元数据 | `trace(metadata={...})` 或 `tracing_context(metadata={...})` |
| 敏感数据脱敏 | `Anonymizer` |
