# 安全初步

## 场景

需要保护某些端点，只有登录用户才能访问。传统做法是在每个端点里写认证逻辑，FastAPI 的依赖注入让这件事变得干净。

## 依赖注入方式保护端点

```python
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic

security = HTTPBasic()

def get_current_user(
    credentials = Depends(security)
):
    return credentials

@app.get("/users/me")
async def read_current_user(
    current_user = Depends(get_current_user)
):
    return current_user
```

`get_current_user` 是认证逻辑，`Depends(get_current_user)` 自动注入到路径操作。

## 用户数据模型

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
```

## HTTPBasic 认证

```python
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = get_user(credentials.username)
    if not user:
        raise HTTPException(status_code=401)
    return user
```

## HTTPBearer（Bearer Token）

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(
    token: str = Depends(security)
):
    return verify_token(token)
```

## 小结

- `Depends(security)` 在参数中注入认证逻辑
- 返回用户信息供路径操作使用
- 支持 HTTPBasic 和 HTTPBearer
