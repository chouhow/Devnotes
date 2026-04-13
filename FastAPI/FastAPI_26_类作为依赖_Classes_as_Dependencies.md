# 类作为依赖

## 基本用法

依赖可以是函数，也可以是类。类依赖更清晰：

```python
class CommonParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonParams = Depends(CommonParams)):
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}
```

FastAPI 自动调用 `CommonParams(...)` 并将实例注入到参数中。

## 数据库会话示例

类依赖非常适合管理数据库连接：

```python
class DBSession:
    def __init__(self):
        self.session = None
    def __enter__(self):
        self.session = connect_to_db()
        return self.session
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

def get_db():
    return DBSession()

@app.get("/users/")
async def read_users(
    db: DBSession = Depends(get_db)
):
    return db.session.query(User).all()
```

FastAPI 自动处理 `__enter__` / `__exit__`。

## vs 函数依赖

| 特性 | 函数依赖 | 类依赖 |
|------|---------|--------|
| 简洁性 | 适合简单逻辑 | 适合需要初始化的逻辑 |
| 可读性 | 扁平结构 | 更接近 OO 风格 |
| 状态管理 | 无状态 | 可以有实例状态 |
| 测试 | 容易 mock | 可以创建实例测试 |

## 小结

类依赖通过 `__init__` 接收参数，`__enter__` / `__exit__` 处理初始化和清理。FastAPI 自动调用。
