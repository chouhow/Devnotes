# Header 参数

## 基本用法

用 `Header` 声明接收 HTTP 请求头：

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"user_agent": user_agent}
```

## 自动转换命名格式

HTTP 请求头通常用 kebab-case（如 `X-Custom-Header`），Python 变量名用 snake_case（如 `x_custom_header`）。

FastAPI 自动转换，无需额外配置：

```python
from fastapi import FastAPI, Header

@app.get("/items")
async def read_items(
    x_request_id: str | None = Header(default=None)
):
    return {"x_request_id": x_request_id}
```

请求头 `X-Request-Id: abc` → `x_request_id = "abc"`

## 常用 Header 参数

```python
from fastapi import FastAPI, Header

@app.get("/items")
async def read_items(
    content_type: str | None = Header(default=None),
    user_agent: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None)
):
    return {
        "content_type": content_type,
        "user_agent": user_agent,
        "x_request_id": x_request_id
    }
```

## 禁止额外 Header

用 `Header` 模型限制允许的 Header：

```python
from pydantic import BaseModel

class Headers(BaseModel):
    model_config = {"extra": "forbid"}  # FastAPI 0.114.0+
    x_custom_header: str | None = None
```

未声明的 Header 传入会返回 422 错误。

## 小结

- Header 参数用 `Header` 声明
- `X-Custom-Header` 自动映射到 `x_custom_header`（kebab-case → snake_case）
- `Header` 支持默认值和类型注解
- 可用 `BaseModel` + `model_config={"extra": "forbid"}` 拒绝额外 Header
