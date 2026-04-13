# 第一步

## 安装 FastAPI

```bash
pip install fastapi
pip install "uvicorn[standard]"   # ASGI 服务器
```

`fastapi` 是框架本身，`uvicorn` 是用来运行它的服务器（类似 Node.js 的 `node`）。

## 第一个应用

创建文件 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

## 启动服务器

```bash
uvicorn main:app --reload
```

- `main:app` 表示从 `main.py` 导入 `app` 实例
- `--reload` 表示代码改动后自动重启，开发时常用

服务器运行在 `http://127.0.0.1:8000`。

## 打开交互式文档

FastAPI 会自动生成两份交互式 API 文档：

| 地址 | 工具 |
|------|------|
| http://127.0.0.1:8000/docs | Swagger UI（推荐）|
| http://127.0.0.1:8000/redoc | ReDoc |

直接访问 `/docs`，可以填写参数、点击 "Execute"，看到真实响应。

## API 声明方式

装饰器声明路由，HTTP 方法决定操作类型：

```python
@app.get("/")
@app.post("/items")
@app.put("/items/{item_id}")
@app.delete("/items/{item_id}")
@app.patch("/items/{item_id}")
```

## 路径参数

URL 中的 `{item_id}` 是路径参数：

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

访问 `GET /items/5` 返回 `{"item_id": 5}`。

## 返回值

直接 return 一个 dict/list，FastAPI 会自动：

- 序列化成 JSON
- 设置正确的 `Content-Type: application/json`
- 如果类型不合法（如传了字符串而非整数），返回明确的错误信息

## 小结

用 FastAPI 写一个带类型验证的 JSON API，只需要：

1. 安装 `fastapi` + `uvicorn`
2. 写一个 `FastAPI()` 实例，加几个装饰器
3. `uvicorn main:app --reload` 启动
4. 打开 `/docs` 调试

这就是 FastAPI 的起点。
