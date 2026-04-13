# 请求文件上传

## 基本用法

用 `UploadFile` 和 `File` 声明文件上传端点：

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    return {"filename": file.filename, "content_type": file.content_type}
```

必须安装 `python-multipart`：`pip install python-multipart`

## UploadFile 的属性

| 属性 | 说明 |
|------|------|
| filename | 文件名 |
| content_type | MIME 类型（如 image/png）|
| file | Python 文件对象 |
| size | 文件大小（字节）|

## 单文件上传

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(description="上传文件")):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.file.seek(0, 2),  # 文件大小
    }
```

## 多文件上传

用 `list[UploadFile]` 接收多个文件：

```python
from fastapi import File, UploadFile

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile] = File()):
    return [
        {"filename": f.filename, "content_type": f.content_type}
        for f in files
    ]
```

## 可选文件上传

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No file uploaded"}
    return {"filename": file.filename}
```

传入空文件时 `file` 为 `None`。

## 小结

- `UploadFile` 是 FastAPI 提供的文件包装对象
- `File()` 表示文件为必填
- `File(default=None)` 表示可选
- `list[UploadFile]` 接收多个文件
- 需安装 `python-multipart`
