# 依赖注入

## 什么是依赖注入

依赖注入（Dependency Injection）是 FastAPI 的核心特性。指的是在路径操作函数中声明"依赖"，FastAPI 自动处理解析、注入和清理。

## 第一个依赖

声明一个函数作为依赖，在路径操作参数中用 `Depends` 引用：

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def query_params(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(query_params)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(query_params)):
    return commons
```

FastAPI 自动在调用路径操作之前先调用 `query_params`，把返回值注入 `commons` 参数。

## 函数依赖 vs 类依赖

依赖可以是函数，也可以是类：

```python
# 函数依赖
def get_db():
    db = DBSession()
    yield db
    db.close()

# 类依赖
class CommonParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonParams = Depends(CommonParams)):
    return commons
```

类依赖更清晰，适合需要初始化的复杂逻辑。

## 子依赖（依赖的依赖）

一个依赖可以依赖另一个依赖，形成链条：

```python
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: str | None = None
):
    return q or last_query or ""

@app.get("/items/")
async def read_query(
    q: str = Depends(query_or_cookie_extractor)
):
    return {"q": q}
```

FastAPI 按正确顺序解析整个依赖链，并在同一请求内缓存结果。

## 装饰器中的依赖

不需要在函数签名中注入，用 `dependencies=[...]`：

```python
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="x-api-key")

@app.get("/items/", dependencies=[Depends(verify_api_key)])
async def read_items():
    return [{"item": "Foo"}]
```

## 全局依赖

给整个 FastAPI 实例加全局依赖，所有路径操作都会执行：

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

所有端点都先执行 `verify_api_key` 检查。

## 带 Yield 的依赖（清理资源）

用 `yield` 在请求结束后执行清理代码：

```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()  # 请求结束后执行
```

`yield` 之后的代码总是执行，即使发生异常也会执行（相当于 `finally`）。

## 小结

- `Depends(fn)` 声明依赖，FastAPI 自动解析并注入
- 依赖可以是函数或类
- 子依赖形成链，`yield` 用于清理资源
- `dependencies=[...]` 用于装饰器，`app=` 用于全局
