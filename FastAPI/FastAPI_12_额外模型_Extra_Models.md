# 额外模型

## Create/Read 分离

同一资源的创建和读取需要不同的数据模型：
- 创建时需要密码
- 读取时不应该返回密码

用多个 Pydantic 模型分开管理：

```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str  # 创建时需要密码

class UserRead(UserBase):
    user_id: int   # 读取时不返回密码
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
```

`response_model=UserRead` 确保密码不会被泄露。

## 使用 response_model

```python
@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate):
    return {"user_id": 1, **user.model_dump()}
```

返回的数据严格遵循 `UserRead`，密码不会被包含在响应中。

## 模型继承

模型可以继承其他模型的字段：

```python
class BaseItem(BaseModel):
    name: str
    price: float

class ItemWithDescription(BaseItem):
    description: str

class ItemWithTax(BaseItem):
    tax: float
```

`ItemWithDescription` 自动拥有 name、price 和 description 三个字段。

## EmailStr 类型

`EmailStr` 是 Pydantic 内置类型，自动验证 Email 格式：

```python
class UserCreate(UserBase):
    password: str
    email: EmailStr  # 格式验证：包含 @ 和域名
```

传入 `notanemail` → 422 错误。

## 小结

- 多个模型分别对应不同的操作（创建/读取/更新）
- `response_model` 自动过滤响应字段，防止密码泄露
- Pydantic 模型可以继承其他模型的字段
- `EmailStr` 自动验证 Email 格式
