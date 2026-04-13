# 请求体更新（PUT vs PATCH）

## PUT vs PATCH

| 方法 | 语义 | 效果 |
|------|------|------|
| PUT | 完整替换 | 必须提供所有字段 |
| PATCH | 部分更新 | 只需提供要更新的字段 |

## PATCH 实现（部分更新）

用 Pydantic 模型的 `model_dump(exclude_unset=True)` 实现真正的部分更新：

```python
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None

items = {}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        items[item_id] = item
    else:
        # 只更新用户实际传入的字段
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(items[item_id], key, value)
    return items[item_id]
```

`exclude_unset=True` 会返回一个只包含显式传入字段的字典，不含默认值。

## PUT 实现（完整替换）

所有字段必填，缺失则报错：

```python
class Item(BaseModel):
    name: str     # 必填
    price: float  # 必填
    description: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    items[item_id] = item
    return item
```

## 两者对比

```python
# PATCH - 只需传要改的字段
PATCH /items/5
Body: {"price": 15.99}  # name 和 description 保持不变

# PUT - 必须传所有字段
PUT /items/5
Body: {"name": "New Name", "price": 15.99, "description": "New"}
# 缺失 name 会报错
```

## 小结

- PUT = 全量替换，PATCH = 部分更新
- `model_dump(exclude_unset=True)` 获取用户实际传入的字段
- `model_dump()` 获取所有字段（含默认值）
- `model_dump(exclude_unset=True)` 用于 PATCH 的增量更新
