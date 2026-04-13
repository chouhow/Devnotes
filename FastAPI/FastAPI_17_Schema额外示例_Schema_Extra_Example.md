# Schema 额外示例

## Field 添加示例

在 Pydantic 模型字段上用 `Field` 添加示例值：

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., example="Foo")
    price: float = Field(..., example=42.0)
    description: str | None = Field(None, example="A very nice Item")
    tax: float | None = Field(None, example=3.2)
```

`...` 表示必填，`example` 在 Swagger UI 中显示示例值。

## 示例参数（openapi_example）

用 `Body(openapi_example={...})` 一次性为整个请求体提供示例：

```python
from fastapi import FastAPI, Body

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        openapi_example={
            "name": "Bar",
            "price": 35.4,
            "description": "A very nice Item",
        }
    )
):
    return {"item_id": item_id, "item": item}
```

Swagger UI 中直接显示示例值，可以一键执行。

## JSON Schema Extra

在 Pydantic 模型中用 `json_schema_extra` 自定义 JSON Schema：

```python
class Item(BaseModel):
    name: str
    json_schema_extra = {
        "examples": [
            {"name": "Foo", "price": 42.0}
        ]
    }
```

## 小结

- `Field(example=...)` 给单个字段添加示例
- `Body(openapi_example={...})` 给整个请求体提供示例
- `json_schema_extra` 自定义 JSON Schema
- 示例值在 Swagger UI 中可直接"Execute"
