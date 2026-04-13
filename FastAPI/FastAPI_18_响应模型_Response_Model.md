# 响应模型

## response_model 参数

`response_model` 控制返回给客户端的数据格式，常用场景是过滤敏感字段：

```python
from pydantic import BaseModel
from fastapi import FastAPI

class UserBase(BaseModel):
    username: str
    email: str

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    pass

app = FastAPI()

@app.get("/user/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user_db = get_user_from_db(user_id)  # 返回 UserInDB（含密码字段）
    return user_db  # FastAPI 自动过滤，只返回 UserOut 的字段
```

`hashed_password` 不会被泄露。

## 过滤响应字段

```python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude={"tax"}  # 不返回 tax 字段
)
async def read_item(item_id: int):
    return items[item_id]
```

| 参数 | 作用 |
|------|------|
| response_model_include={"name", "price"} | 只返回指定字段 |
| response_model_exclude={"password"} | 排除指定字段 |

## 嵌套模型

嵌套的 Pydantic 模型也会被过滤：

```python
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

class ResponseItem(BaseModel):
    item: Item
    count: int

@app.get("/items-with-count", response_model=ResponseItem)
async def read_items():
    return ResponseItem(item=Item(name="Foo", price=42.0), count=1)
```

返回：`{"item": {"name": "Foo", "price": 42.0, "description": null}, "count": 1}`

FastAPI 自动处理嵌套模型的序列化。

## 小结

- `response_model` 自动过滤响应字段，防止密码等敏感数据泄露
- `response_model_include` / `response_model_exclude` 精细控制
- 嵌套模型也会被正确过滤
- `response_model` 只影响响应，不影响请求验证
