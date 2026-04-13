# 中间件

## 什么是中间件

中间件是在请求到达路径操作之前、或响应返回给客户端之前执行的代码。

```
请求 → 中间件A → 中间件B → 路径操作 → 中间件B（响应）→ 中间件A（响应）→ 客户端
```

## 自定义中间件

用 `@app.middleware("http")` 注册：

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

`call_next` 将请求传递给下一个中间件或路径操作，`response` 是处理后的响应。

## 多个中间件

注册多个中间件，按注册顺序执行：

```python
app = FastAPI()

@app.middleware("http")
async def middleware_a(request: Request, call_next):
    print("A before")
    response = await call_next(request)
    print("A after")
    return response

@app.middleware("http")
async def middleware_b(request: Request, call_next):
    print("B before")
    response = await call_next(request)
    print("B after")
    return response
```

执行顺序：middleware_a(before) → middleware_b(before) → 路径操作 → middleware_b(after) → middleware_a(after)

## 小结

- 中间件在请求和响应流中都可以修改数据
- `@app.middleware("http")` 注册
- `call_next(request)` 传递给下一个
- 返回 `response` 可以修改响应头或内容
