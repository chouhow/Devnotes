# LangGraph 本地服务器

在本地运行 LangGraph 应用，用于开发和测试。

---

## 前置要求

- LangSmith API Key（免费注册）
- Python 3.11+

---

## 1. 安装 LangGraph CLI

```bash
pip install -U "langgraph-cli[inmem]"
```

---

## 2. 创建 LangGraph 应用

使用模板创建新项目：

```bash
langgraph new path/to/your/app --template new-langgraph-project-python
```

不指定模板会显示交互式菜单，可选择其他模板。

---

## 3. 安装依赖

```bash
cd path/to/your/app
pip install -e .
```

`-e` 表示编辑模式，本地修改会立即生效。

---

## 4. 配置环境变量

复制 `.env.example` 为 `.env`，填入 API Key：

```bash
LANGSMITH_API_KEY=lsv2...
OPENAI_API_KEY=sk-...
```

---

## 5. 启动本地服务器

```bash
langgraph dev
```

输出示例：

```
INFO:langgraph_api.cli:
Welcome to
╦ ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║ ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴ ┴ ┴
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

---

## 6. 在 Studio 中测试

访问 Studio URL：

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

在 Studio 中可以：
- 可视化图结构
- 与 Agent 交互
- 调试执行流程

**Safari 用户**：使用 `--tunnel` 创建安全隧道：

```bash
langgraph dev --tunnel
```

---

## 7. 测试 API

### Python SDK

```bash
pip install langgraph-sdk
```

```python
from langgraph_sdk import get_client

client = get_client(url="http://127.0.0.1:2024")

# 创建线程
thread = await client.threads.create()

# 发送消息
response = await client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id="default",
    input={"messages": [{"role": "user", "content": "Hello"}]}
)
```

### REST API

```bash
curl -X POST "http://127.0.0.1:2024/threads" \
  -H "Content-Type: application/json"

curl -X POST "http://127.0.0.1:2024/threads/{thread_id}/runs" \
  -H "Content-Type: application/json" \
  -d '{"assistant_id": "default", "input": {"messages": []}}'
```

---

## 说明

`langgraph dev` 启动的是**内存模式**，仅用于开发和测试。生产环境请使用 LangSmith Deployment 或自托管。

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `langgraph dev` | 启动开发服务器 |
| `langgraph dev --tunnel` | 创建安全隧道（Safari 需要）|
| `langgraph new` | 创建新项目 |
