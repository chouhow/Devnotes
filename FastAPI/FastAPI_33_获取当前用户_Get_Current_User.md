# 获取当前用户

## 从 Token 中提取用户

用户登录后获得 Token，后续请求携带 Token，从 Token 中解析出用户信息：

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token: str):
    return {"username": "johndoe"}

async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/users/me")
async def read_users_me(
    current_user = Depends(get_current_user)
):
    return current_user
```

## 完整流程

```
客户端发送 Bearer Token
  ↓
OAuth2PasswordBearer 提取 Token
  ↓
get_current_user 验证并解析 Token
  ↓
返回用户信息，注入到路径操作函数
```

## 小结

- `OAuth2PasswordBearer(tokenUrl="token")` 声明 Token 来源
- `get_current_user` 从 Token 解析用户信息
- 抛出 HTTP 401 表示认证失败
