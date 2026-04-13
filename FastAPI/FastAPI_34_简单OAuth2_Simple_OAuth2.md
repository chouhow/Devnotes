# 简单 OAuth2

## OAuth2 密码模式

OAuth2 的密码模式（Password Flow）是最简单的认证方式：

```
1. POST /token  →  发送 username + password，返回 access_token
2. GET /items/    →  携带 access_token，获取受保护资源
```

## Token 端点

```python
from fastapi import Depends, FastAPI, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashed",  # 实际应用中用 bcrypt 哈希
        "disabled": False,
    }
}

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=401)
    # 验证密码（实际应用中用 pwd_context.verify）
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
```

## 密码哈希

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash("secret")       # 创建哈希
pwd_context.verify("secret", hashed)   # 验证，返回 True
```

生产中永远不要明文存储密码。

## 受保护的路由

```python
@app.get("/items/")
async def read_items(
    current_user = Depends(oauth2_scheme)
):
    return [{"item": "Foo"}, {"item": "Bar"}]
```

未携带有效 Token 访问 → 401 错误。

## 小结

- Token 端点接收用户名密码，返回 access_token
- 后续请求携带 `Authorization: Bearer <token>`
- FastAPI 的依赖注入自动处理认证
