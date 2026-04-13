# 查询参数

## 基本用法

路径参数是 URL 路径里的动态值（如 /items/{item_id}），查询参数是 URL 中 ? 后面的参数。

直接在函数参数中声明，FastAPI 自动识别为查询参数：

```python
from fastapi import FastAPI

app = FastAPI()

fake_items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items[skip : skip + limit]
```

访问 GET /items?skip=0&limit=10，返回前10条数据。

## 类型自动转换

查询参数声明了 int，FastAPI 自动把 URL 中的字符串转成整数。如果无效（如传了 abc），返回 422 错误。

```python
def read_items(skip: int = 0, limit: int = 10):
    ...
```

GET /items?skip=abc 返回 422 Unprocessable Entity。

## 布尔值处理

true、false、1、0 都能自动识别为布尔值：

GET /items?short=true    -> short = True
GET /items?short=False -> short = False
GET /items?short=1      -> short = True

## 可选参数

| 声明方式 | 效果 |
|----------|------|
| q: str | 必需 |
| q: str = None | 可选，默认 None |
| q: str = "foo" | 可选，有默认值 |
| q: int = 10 | 可选，默认 10 |

## 路径参数和查询参数同时使用

两者互不影响，各自声明即可：

```python
@app.get("/users/{user_id}/items")
def get_user_items(user_id: int, skip: int = 0, limit: int = 10):
    return {"user_id": user_id, "skip": skip, "limit": limit}
```

访问 GET /users/5/items?skip=2&limit=20。

## 小结

查询参数是 URL 中 ? 后面的参数，直接声明为函数参数即可。默认值使参数变为可选，类型注解自动完成类型验证和转换。