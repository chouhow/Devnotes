# 请求体字段

## 基本用法

`Field` 在 Pydantic 模型中给字段添加验证规则，和 `Path` / `Query` 的用法一致。

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        title="商品描述",
        max_length=300
    )
    price: float = Field(
        gt=0,
        description="价格必须大于零"
    )
    tax: float | None = None
```

## Field 验证参数

| 参数 | 作用 | 示例 |
|------|------|------|
| default | 默认值 | default=None |
| title | Swagger 标题 | title="商品ID" |
| description | 字段说明 | description="..." |
| ge / gt / le / lt | 数值范围 | ge=0 |
| min_length / max_length | 字符串长度 | min_length=1 |
| pattern | 正则表达式 | pattern=r"^\\d+$" |

## 示例

```python
class Item(BaseModel):
    name: str = Field(title="商品名")
    description: str | None = Field(
        default=None,
        title="商品描述",
        max_length=300
    )
    price: float = Field(gt=0, description="价格必须大于零")
    tax: float | None = Field(None, ge=0)
```

传入 price=-1 或 description 超过 300 字符，都会返回 422 错误。

## 小结

- `Field` 在 Pydantic 模型中给字段加验证规则
- `title` / `description` 自动出现在 Swagger UI 中
- 验证规则与 `Path` / `Query` 一致
