# 安全认证

## 概述

FastAPI 提供了完整的安全认证体系，包括：
- HTTPBasic 认证
- API Key 认证
- OAuth2 密码模式
- JWT Bearer Token

## 快速入门：OAuth2 密码模式

OAuth2 的密码模式（Password Flow）是最简单的认证方式：

```
1. POST /token  →  发送用户名+密码，返回 access_token
2. GET /items/  →  携带 access_token，获取受保护资源
```

## 完整流程

```python
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401)
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=401)
    return user
```

## 安装依赖

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
```

## 小结

- OAuth2 密码模式：用户名+密码 → access_token
- JWT Token：防篡改的用户凭证
- `pwd_context.hash()` 创建密码哈希
- `jwt.encode` / `jwt.decode` 处理 Token
