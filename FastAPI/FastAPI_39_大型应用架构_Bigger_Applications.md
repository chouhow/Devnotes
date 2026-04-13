# 大型应用架构

## 为什么要模块化

代码全放一个文件会难以维护。模块化让每个功能独立，团队协作更容易，测试更简单。

## 目录结构

```
.
├── main.py              # 主入口，聚合所有路由
├── dependencies.py     # 共享依赖
├── routers/
│   ├── __init__.py
│   ├── items.py         # /items 路由
│   └── users.py         # /users 路由
├── models/
│   ├── __init__.py
│   └── schemas.py      # Pydantic 模型
└── database.py          # 数据库配置
```

## 主入口（main.py）

```python
from fastapi import FastAPI
from routers import items, users

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
```

## 路由模块（routers/items.py）

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[Item])
async def read_items(
    current_user: User = Depends(get_current_user)
):
    return fake_items

@router.get("/{item_id}")
async def read_item(
    item_id: int,
    current_user: User = Depends(get_current_user)
):
    return {"item_id": item_id}
```

`APIRouter` 管理一组路由，`prefix` 添加统一前缀。

## 共享依赖（dependencies.py）

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    # 验证 Token...
    return {"username": "johndoe"}
```

依赖单独放一个文件，所有模块共用。

## 小结

- 每个路由模块用 `APIRouter` 管理
- `app.include_router()` 把路由模块注册到主应用
- `prefix` 给路由组加前缀，`tags` 在 Swagger UI 分组
- 共享逻辑放 `dependencies.py`
