# 请求体嵌套模型

## 列表字段

请求体中的字段可以是列表：

```python
class Item(BaseModel):
    name: str
    tags: list[str] = []
```

Body：`{"name": "Foo", "tags": ["rock", "pop"]}`

## 集合类型（自动去重）

用 `set` 自动去除重复值：

```python
class Item(BaseModel):
    name: str
    tags: set[str] = set()
```

传入 `["rock", "rock", "metal"]` → 自动变成 `{"rock", "metal"}`。

## 嵌套 Pydantic 模型

模型可以包含其他 Pydantic 模型：

```python
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
```

Body：
```json
{
    "name": "Foo",
    "price": 42.0,
    "image": {
        "url": "http://example.com/img.jpg",
        "name": "The Foo image"
    }
}
```

## HttpUrl 类型（URL 验证）

用 `pydantic` 的 `HttpUrl` 可以验证 URL 格式：

```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str
```

传入无效 URL（如 "foo"）→ 返回 422 错误。

## 列表的子模型

子模型列表也能声明：

```python
class Item(BaseModel):
    name: str
    images: list[Image] | None = None
```

Body：
```json
{
    "name": "Foo",
    "images": [
        {"url": "http://example.com/1.jpg", "name": "img1"},
        {"url": "http://example.com/2.jpg", "name": "img2"}
    ]
}
```

## 任意字典

用 `Dict[str, float]` 定义键值对结构：

```python
class Offer(BaseModel):
    offer_name: str
    offer_code: str
    base_price: float
    ratings: Dict[str, float] = {}
```

## 小结

- 列表字段：`list[str]` 或 `set[str]`
- 集合自动去重
- 嵌套模型直接声明其他 Pydantic 模型
- `HttpUrl` 验证 URL 格式
- 任意字典用 `Dict[str, float]`
