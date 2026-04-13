# 错误处理

## HTTPException

路径操作中抛出 `HTTPException`：

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestler"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

返回 404，Body：`{"detail": "Item not found"}`

## HTTPException 参数

```python
raise HTTPException(
    status_code=404,
    detail="Item not found",
    headers={"X-Error": "There goes my error"}
)
```

`headers` 可以返回自定义响应头。

## 自定义异常处理器

用 `@app.exception_handler` 注册全局异常处理器：

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Name {exc.name} is forbidden"}
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"name": name}
```

## 常用 HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 400 | 请求格式错误（Bad Request）|
| 401 | 未认证（Unauthorized）|
| 403 | 无权限（Forbidden）|
| 404 | 资源不存在（Not Found）|
| 422 | 验证失败（Unprocessable Entity）|
| 500 | 服务器内部错误（Internal Error）|

## 小结

- `HTTPException` 在路径操作中抛出，返回标准错误响应
- `@app.exception_handler` 注册自定义异常处理器
- 全局异常处理器返回 `JSONResponse`
