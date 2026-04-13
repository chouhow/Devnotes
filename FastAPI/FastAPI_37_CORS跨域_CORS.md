# CORS 跨域资源共享

## 什么是 CORS

CORS（Cross-Origin Resource Sharing）控制浏览器允许哪个域名的网页请求 API。

## 基本用法

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| allow_origins | 允许的源列表 | `["http://localhost:3000"]` |
| allow_credentials | 允许携带 Cookie | `True` |
| allow_methods | 允许的 HTTP 方法 | `["GET", "POST"]` |
| allow_headers | 允许的请求头 | `["Authorization"]` |
| expose_headers | 暴露给浏览器读取的头 | `["X-Custom-Header"]` |
| max_age | 预检请求缓存时间（秒）| `600` |

## 常用配置

```python
# 开发环境：允许所有源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 生产环境：精确控制
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## 小结

CORS 控制在浏览器中运行的网页能否访问你的 API。前端和后端在不同域名时必须配置 CORS。
