# 表单

## 基本用法

表单数据和请求体不同：表单使用 `application/x-www-form-urlencoded` 或 `multipart/form-data` 编码，而请求体使用 `application/json`。

用 `Form` 声明表单字段：

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

必须安装 `python-multipart`：`pip install python-multipart`

## 必填字段

表单字段和查询参数一样，默认必填：

```python
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

缺少任一字段返回 422 错误。

## 可选字段

```python
@app.post("/login/")
async def login(
    username: str = Form(),
    password: str = Form(),
    remember_me: bool = Form(default=False)
):
    return {"username": username, "remember_me": remember_me}
```

## 多个 Form 参数

```python
from fastapi import FastAPI, Form

class FormData(BaseModel):
    username: str
    password: str

# 或者直接用多个 Form 参数
@app.post("/submit/")
async def submit(
    username: str = Form(),
    password: str = Form(),
    data: str = Form()
):
    return {"username": username, "password": password, "data": data}
```

## 小结

- 表单参数用 `Form` 声明
- 安装：`pip install python-multipart`
- `Form(default=None)` 表示可选
- `Form(...)` 表示必填
