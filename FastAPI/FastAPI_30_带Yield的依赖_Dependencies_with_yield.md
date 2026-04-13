# 带 Yield 的依赖

## 清理资源（yield）

用 `yield` 在请求完成后执行清理代码：

```python
async def get_db():
    db = DBSession()
    yield db
    db.close()  # 请求完成后执行
```

`yield` 之后（这里是 `db.close()`）的代码无论请求是否成功都会执行，类似 `try/finally`。

## 数据库会话

```python
from typing import Generator

async def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserSchema)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

请求结束后 `db.close()` 总会被调用。

## 与异常处理结合

`yield` 之后的代码即使请求出错也会执行：

```python
async def get_db():
    db = connect()
    try:
        yield db
    except Exception:
        db.rollback()  # 出错时回滚
    finally:
        db.close()  # 总是执行
```

## 多个带 Yield 的依赖

```python
async def dependency_a():
    resource_a = acquire_a()
    try:
        yield resource_a
    finally:
        release_a(resource_a)

async def dependency_b():
    resource_b = acquire_b()
    try:
        yield resource_b
    finally:
        release_b(resource_b)

@app.post("/")
async def root(
    a: ResourceA = Depends(dependency_a),
    b: ResourceB = Depends(dependency_b)
):
    return {"a": a, "b": b}
```

FastAPI 按声明顺序执行 setup 和 teardown。

## 小结

- `yield` 用于请求结束后的清理代码（数据库连接、文件句柄等）
- 无论请求是否成功，`yield` 之后的代码总执行（类似 `finally`）
- 多个带 yield 的依赖按声明顺序执行
