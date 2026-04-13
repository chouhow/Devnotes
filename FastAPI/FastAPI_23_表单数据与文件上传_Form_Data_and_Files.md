# 表单数据与文件上传

## 基本用法

同一个端点可以同时接收表单字段和文件：

```python
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/upload/")
async def create_upload(
    file: UploadFile = File(description="上传头像"),
    username: str = Form(description="用户名"),
    bio: str = Form(default="") = Form(description="个人简介")
):
    return {
        "username": username,
        "bio": bio,
        "avatar": file.filename,
        "content_type": file.content_type
    }
```

请求格式：`multipart/form-data`（必须），同时包含文件和表单字段。

## 请求格式

Content-Type 必须为 `multipart/form-data`，FastAPI 自动处理文件流。

文件放在 `file` 字段，表单数据放在 `username` 和 `bio` 字段。

## 小结

- 表单和文件可以同时声明
- `File` 用于文件参数，`Form` 用于表单字段
- 请求格式：`multipart/form-data`
- 同时适合头像上传 + 用户信息等场景
