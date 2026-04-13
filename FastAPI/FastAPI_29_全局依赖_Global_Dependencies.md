# 全局依赖

## 为整个应用添加依赖

用 `app.dependencies = [...]` 给所有路径操作添加依赖：

```python
from fastapi import FastAPI, Depends, Header

app = FastAPI()

async def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403)

app.dependencies = [Depends(verify_api_key)]

@app.get("/items/")
async def read_items():
    return [{"item": "Foo"}]

@app.get("/users/")
async def read_users():
    return [{"username": "john"}]
```

现在所有端点都会先执行 `verify_api_key` 检查。

## 与中间件的区别

| 特性 | 依赖注入 | 中间件 |
|------|---------|--------|
| 注入路径操作参数 | 可以 | 不可以 |
| 抛出 HTTPException | 可以 | 不可以 |
| 响应修改 | 不可以 | 可以 |
| 执行顺序 | 精确控制 | 固定顺序 |
| 注册方式 | `app=..., dependencies=[...]` | `app.add_middleware(...)` |

## 常用场景

- 全局 API Key 验证
- 全局请求日志
- 全局租户隔离
- 全局速率限制

## 小结

`app.dependencies = [...]` 给所有端点添加全局依赖，适合横切关注点（Cross-Cutting Concerns）。
