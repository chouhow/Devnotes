# 子依赖

## 依赖的依赖

一个依赖可以依赖另一个依赖，形成依赖链：

```python
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: str | None = None
):
    if q:
        return q
    return last_query or ""

@app.get("/items/")
async def read_query(
    q: str = Depends(query_or_cookie_extractor)
):
    return {"q": q}
```

`query_or_cookie_extractor` 先调用 `query_extractor` 获取 `q`，然后决定返回 `q` 还是 `last_query`。

## 多层依赖链

```
路径操作函数
  └── 依赖 A
        └── 依赖 B
              └── 依赖 C
```

FastAPI 按正确顺序解析，同一请求内缓存结果。

## 缓存

FastAPI 会在同一请求内缓存依赖的返回值，不会重复执行：

```python
def get_heavy_resource():
    print("执行一次（会被缓存）")
    return {"resource": "heavy data"}

@app.get("/a")
async def endpoint_a(data: dict = Depends(get_heavy_resource)):
    return data

@app.get("/b")
async def endpoint_b(data: dict = Depends(get_heavy_resource)):
    return data
```

两次调用 `endpoint_a` 和 `endpoint_b`，`get_heavy_resource` 只执行一次。

## 小结

- 子依赖通过 `Depends(other_dependency)` 引用其他依赖
- FastAPI 自动处理整个依赖链的执行顺序
- 同一请求内依赖结果被缓存，不会重复执行
