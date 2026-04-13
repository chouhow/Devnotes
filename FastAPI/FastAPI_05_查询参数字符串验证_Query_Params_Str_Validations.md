# 查询参数字符串验证

## 基本用法

`Query` 用来给查询参数添加验证规则：

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(q: str = Query(default=None)):
    return {"q": q}
```

## 字符串长度限制

| 参数 | 作用 | 示例 |
|------|------|------|
| min_length | 最小字符数 | min_length=3 |
| max_length | 最大字符数 | max_length=50 |

```python
@app.get("/items")
async def read_items(
    q: str = Query(min_length=3, max_length=50)
):
    return {"q": q}
```

## 正则表达式

`pattern` 用正则表达式限制字符串格式：

```python
@app.get("/items")
async def read_items(
    q: str = Query(pattern=r"^startswith"))
    return {"q": q}
```

参数必须以 "startswith" 开头，否则返回 422。

## 参数描述

`description` 在 Swagger UI 中显示参数说明：

```python
@app.get("/items")
async def read_items(
    q: str = Query(description="搜索关键词，至少3个字符")
):
    return {"q": q}
```

## 多重验证

可以同时用多个验证条件：

```python
@app.get("/items")
async def read_items(
    q: str = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9]+$"
    )
):
    return {"q": q}
```

## 必需参数

不设默认值即为必需参数：

```python
@app.get("/items")
async def read_items(
    q: str = Query(min_length=3)  # 无默认值 = 必需
):
    return {"q": q}
```

## 小结

- `Query` 给查询参数添加验证规则
- `min_length`/`max_length` 限制字符长度
- `pattern` 用正则限制格式
- `description` 添加 Swagger UI 文档
- 默认值设为 `None` 表示可选，不设默认值表示必需
