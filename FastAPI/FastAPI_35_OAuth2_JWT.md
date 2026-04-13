# OAuth2 JWT

## JWT 令牌结构

JWT 包含三部分：
- Header：令牌类型和签名算法
- Payload：用户信息和过期时间
- Signature：防篡改签名

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjAwMDAwMDAwMH0.signature
```

## 完整实现

```python
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return TokenData()
        return TokenData(username=username)
    except JWTError:
        return TokenData()

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401)
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    return {"username": username}
```

## 安全最佳实践

1. **使用 HTTPS**：生产环境必须 HTTPS
2. **密钥管理**：SECRET_KEY 放环境变量，不要硬编码
3. **短期 Token**：ACCESS_TOKEN_EXPIRE_MINUTES = 30 分钟
4. **密码哈希**：永远用 bcrypt，不存明文密码
5. **Token 不存敏感信息**：Payload 是明文的，任何人都能解码

## 小结

JWT = Header.Payload.Signature，防篡改。Token 的 Payload（用户信息）是明文的，任何人都能解码，不要存密码等敏感信息。
