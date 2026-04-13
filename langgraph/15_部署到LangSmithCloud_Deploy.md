# LangGraph 部署到 LangSmith Cloud

LangSmith Cloud 是专为 Agent 工作负载设计的托管平台，支持从 GitHub 仓库直接部署，自动处理基础设施、扩缩容和运维。

---

## 前置要求

- GitHub 账号
- LangSmith 账号（免费注册）
- 代码已按 LangGraph 标准组织（见 Application Structure）

---

## 部署步骤

### 1. 创建 GitHub 仓库

代码必须放在 GitHub 仓库中（公开或私有均可）。确保：
- 已按 [Local Server 指南](local-server.md) 配置好 LangGraph 应用
- `langgraph.json` 配置正确
- 依赖在 `requirements.txt` 或 `pyproject.toml` 中

### 2. 在 LangSmith 中创建部署

1. 登录 [LangSmith](https://smith.langchain.com)
2. 左侧导航栏选择 **Deployments**
3. 点击 **+ New Deployment**
4. 连接 GitHub 账号（首次使用或添加私有仓库）
5. 选择要部署的仓库
6. 点击 **Submit** 开始部署（约 15 分钟）

### 3. 在 Studio 中测试

部署完成后：
1. 点击部署详情页的 **Studio** 按钮
2. 在 Studio 界面中与 Agent 交互，验证功能正常

### 4. 获取 API URL

在部署详情页找到 **API URL**，格式如：

```
https://api.smith.langchain.com/v1/your-deployment-id
```

### 5. 测试 API

```bash
curl -X POST "https://api.smith.langchain.com/v1/your-deployment-id/invoke" \
  -H "Authorization: Bearer $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"messages": [{"role": "user", "content": "Hello"}]}}'
```

---

## 其他部署选项

| 选项 | 说明 | 适用场景 |
|------|------|---------|
| **LangSmith Cloud** | 全托管，自动扩缩容 | 快速上线，无运维负担 |
| **Control Plane（混合/自托管）** | 控制平面托管，执行环境自托管 | 数据敏感，需要本地执行 |
| **Standalone Servers** | 完全自托管 | 完全控制，已有基础设施 |

---

## 环境变量配置

在 LangSmith 部署设置中配置环境变量：

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql://...
```

---

## 监控和日志

部署后在 LangSmith 中查看：
- **Traces**：每次调用的详细追踪
- **Metrics**：调用次数、延迟、错误率
- **Logs**：应用日志和错误信息

---

## 更新部署

推送代码到 GitHub 后，LangSmith 自动检测并重新部署（可配置自动/手动）。

---

## 小结

LangSmith Cloud 让部署 LangGraph 应用变得简单：
1. 代码推送到 GitHub
2. 在 LangSmith 中链接仓库
3. 自动构建和部署
4. 通过 API URL 调用

适合快速上线和不想管理基础设施的场景。
