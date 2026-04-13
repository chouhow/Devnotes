# 静态文件

## 配置静态文件服务

FastAPI 自带静态文件支持：

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World with Static Files"}
```

`app.mount` 把 `/static` 路径绑定到本地 `static/` 目录。

## 目录结构

```
.
├── main.py
└── static/
    ├── css/styles.css
    ├── js/app.js
    └── images/logo.png
```

访问 `http://127.0.0.1:8000/static/css/styles.css`

## 注意事项

- `app.mount` 挂载后，`/static/` 路径由 `StaticFiles` 处理，不会到达路径操作
- 生产环境推荐用 Nginx 等反向代理提供静态文件，性能更好

## 小结

`app.mount("/static", StaticFiles(directory="static"))` 提供静态文件服务。生产环境建议用 Nginx。
