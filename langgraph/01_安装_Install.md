# LangGraph 安装

## 基础安装

```bash
pip install -U langgraph
```

或

```bash
uv pip install -U langgraph
```

---

## 配合 LangChain 使用

LangGraph 通常需要配合 LLM 和工具定义使用。文档示例使用 LangChain：

```bash
pip install -U langchain
```

---

## Python 版本要求

- Python 3.10+

---

## LLM Provider 安装

根据使用的 LLM 提供商，单独安装对应包：

```bash
# OpenAI
pip install langchain-openai

# Anthropic
pip install langchain-anthropic

# Azure OpenAI
pip install langchain-azure-openai

# Google
pip install langchain-google-genai

# 其他提供商见官方集成页面
```

---

## 完整开发环境

```bash
# 基础
pip install langgraph langchain

# OpenAI + Anthropic
pip install langchain-openai langchain-anthropic

# 测试
pip install pytest

# 持久化（可选）
pip install langgraph-checkpoint-postgres  # PostgreSQL
pip install langgraph-checkpoint-redis     # Redis
```

---

## 验证安装

```python
import langgraph
print(langgraph.__version__)
```
