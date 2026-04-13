# Cookie 参数

## 基本用法

用 `Cookie` 声明接收请求中的 Cookie：

```python
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/items")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}
```

Cookie 参数名要完全匹配（如 `ads_id`）。

## 需要 Cookie 的路径操作

```python
from fastapi import FastAPI, Cookie
from typing import Annotated

app = FastAPI()

@app.get("/items")
async def read_items(
    cookies: Annotated[str | None, Cookie()] = None
):
    return {"cookies": cookies}
```

## 小结

- Cookie 参数用 `Cookie` 声明
- 参数名与 Cookie 名完全一致
- 支持 `Cookie(default=None)` 表示可选
