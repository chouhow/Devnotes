# 请求体多个参数

## 多个 Pydantic 模型

同一个路径操作中可以有多个请求体参数。FastAPI 根据参数名确定哪个 Pydantic 模型对应哪个 JSON 对象。

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: str | None = None

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User
):
    return {"item_id": item_id, "item": item, "user": user}
```

Body 格式：

```json
{
    "item": {
        "name": "Foo",
        "price": 42.0
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

## 单一标量值放入请求体

有时一个参数不是模型，而是一个单独的值（如整数），用 `Body` 把标量值也放入请求体：

```python
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    importance: int = Body(gt=0)  # 标量，放进请求体
):
    return {"item_id": item_id, "item": item, "importance": importance}
```

Body：
```json
{
    "item": {"name": "Foo", "price": 42.0},
    "importance": 3
}
```

## Embed 单个 Body 参数

如果只有一个模型参数，希望 JSON 格式为 `{"item": {...}}` 而不是平铺的 `{...}`，用 `embed=True`：

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(embed=True)  # 嵌入到 {"item": {...}}
):
    return {"item_id": item_id, "item": item}
```

Body：
```json
{
    "item": {
        "name": "Foo",
        "price": 42.0
    }
}
```

## 小结

- 多个 Pydantic 模型参数按参数名映射到 JSON 对象
- `Body` 把标量值也放入请求体并添加验证
- `embed=True` 把单个模型参数嵌入一个 key 下
