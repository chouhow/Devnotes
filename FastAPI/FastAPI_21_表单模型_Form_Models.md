# 请求体模型

## 基本用法

和查询参数模型一样，请求体也可以用 Pydantic 模型统一管理验证规则：

```python
from pydantic import BaseModel, Field

class LoginForm(BaseModel):
    username: str
    password: str
```

用 `Form` 接收请求体中的表单数据：

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(data: LoginForm = Form()):
    return {"username": data.username}
```

## 添加验证规则

用 `Field` 给表单字段添加验证：

```python
class LoginForm(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)
    remember_me: bool = Field(default=False)
```

传入用户名不足 3 个字符 → 422 错误。

## 禁止额外字段

用 `model_config = {"extra": "forbid"}` 拒绝未声明的字段：

```python
class FormData(BaseModel):
    model_config = {"extra": "forbid"}  # FastAPI 0.114.0+
    username: str
    password: str
```

传入额外字段 → 422 错误。

## 普通 Form 参数 vs Pydantic 模型表单

| 特性 | 普通 Form 参数 | Pydantic 模型表单 |
|------|-------------|----------------|
| 字段复用 | 不能 | 可以 |
| 集中验证 | 各自为政 | 统一 Field |
| 禁用额外字段 | 不能 | `extra="forbid"` 可以 |
| 继承 | 不支持 | 支持模型继承 |

## 小结

- 用 Pydantic 模型管理表单字段验证
- `Field` 定义具体规则
- `extra="forbid"` 拒绝额外字段
- 适合多端点共用同一套表单字段的场景
