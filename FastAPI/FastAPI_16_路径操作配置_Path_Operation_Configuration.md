# 路径操作配置

## HTTP 状态码

`status_code` 控制返回的 HTTP 状态码：

```python
@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    return None
```

常用状态码：
- `200` 默认值（成功）
- `201` 创建成功
- `204` 成功无响应体（适合 DELETE）
- `422` 验证失败

## 标签（tags）

`tags` 在 Swagger UI 中对端点分组：

```python
@app.post("/items/", tags=["items"])
async def create_item(item: Item):
    return item

@app.get("/items", tags=["items"])
async def read_items():
    return [{"name": "Foo"}]
```

## 摘要和描述

```python
from fastapi import FastAPI, Body

@app.post(
    "/items/",
    summary="创建商品",
    description="创建一个新的商品记录，支持批量创建。",
    response_description="创建的商品对象"
)
async def create_item(
    item: Item = Body(openapi_example={
        "name": "Bar",
        "price": 35.4,
        "description": "A very nice Item",
    })
):
    return item
```

- `summary`：端点摘要
- `description`：支持 Markdown 格式的详细说明
- `response_description`：响应描述

## 标记为废弃

`deprecated=True` 在 Swagger UI 中显示警告：

```python
@app.get("/items/", deprecated=True)
async def read_items():
    return [{"item": "Foo"}]
```

## 响应字段过滤

`response_model_exclude` 和 `response_model_include` 过滤响应字段：

```python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude={"tax"}  # 不返回 tax 字段
)
async def read_item(item_id: int):
    return items[item_id]
```

## 小结

| 参数 | 作用 |
|------|------|
| status_code | HTTP 状态码 |
| tags | Swagger UI 中的分组 |
| summary | 端点摘要 |
| description | 详细说明（支持 Markdown）|
| response_description | 响应说明 |
| deprecated | 标记为废弃 |
| response_model_include/exclude | 过滤响应字段 |
