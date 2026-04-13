# 元数据与文档配置

## 应用级元数据

```python
from fastapi import FastAPI

app = FastAPI(
    title="我的 FastAPI 应用",
    description="这是一个功能强大的 API。",
    summary="FastAPI 官方教程中文版",
    version="1.0.0",
    contact={
        "name": "技术支持团队",
        "url": "https://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)
```

这些信息出现在 Swagger UI 顶部。

## 标签元数据

`openapi_tags` 给端点分组：

```python
app = FastAPI(openapi_tags=[
    {"name": "users", "description": "用户相关操作。"},
    {"name": "items", "description": "项目管理操作。"},
])

@app.get("/users/", tags=["users"])
async def get_users(): ...

@app.get("/items/", tags=["items"])
async def get_items(): ...
```

## OpenAPI URL

```python
app = FastAPI(
    docs_url="/docs",        # Swagger UI
    redoc_url="/docs-redoc", # ReDoc
    openapi_url="/api/openapi.json",  # JSON Schema
)

# 禁用所有文档
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
```

## 小结

元数据让 API 文档更完整、专业。标签元数据在 Swagger UI 中分组，OpenAPI URL 配置文档访问路径。
