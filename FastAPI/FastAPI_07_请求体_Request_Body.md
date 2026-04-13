# 请求体

## 什么是请求体

GET 请求通常带查询参数，POST/PUT 请求通常带请求体（Request Body），即随请求发送的 JSON 数据。

FastAPI 用 Pydantic 模型来声明请求体，并自动完成验证和类型转换。

## 基本用法

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

发送 POST /items/ 请求，Body 传入 JSON：

```json
{
    "name": "Foo",
    "description": "A very nice Item",
    "price": 42.0,
    "tax": 3.2
}
```

FastAPI 自动验证 JSON 结构，类型不匹配返回 422。

## 请求体 + 路径参数

三者可以同时使用：

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,      # 路径参数
    item: Item,        # 请求体
    q: str | None = None  # 查询参数
):
    return {"item_id": item_id, "item": item, "q": q}
```

URL：PUT /items/5?q=searchterm
Body：Item 的 JSON

## 嵌套模型

Pydantic 模型可以嵌套：

```python
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    price: float
    image: Image | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

Body：
```json
{
    "name": "Foo",
    "price": 35.4,
    "image": {
        "url": "http://example.com/img.jpg",
        "name": "The Foo image"
    }
}
```

## 小结

- 请求体用 Pydantic 模型声明，FastAPI 自动验证
- `Item | None = None` 表示可选字段
- 路径参数、查询参数、请求体可以同时使用
- 嵌套模型自动处理深层 JSON
