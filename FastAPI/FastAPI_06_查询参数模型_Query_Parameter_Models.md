# 查询参数模型

## 背景

当查询参数很多时，一个个声明很繁琐。用 Pydantic 模型可以集中管理所有查询参数的验证规则。

## 基本用法

定义一个 Pydantic 模型，用 `Field` 声明验证规则，然后用 `Query` 接收：

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, ge=0, le=100)
    offset: int = Field(0, ge=0)
    filter: str | None = Field(None, min_length=3)

@app.get("/items")
async def read_items(
    filter_query: FilterParams = Query()
):
    return filter_query
```

访问 GET /items?limit=10&offset=0。

## Field 验证参数

| 参数 | 作用 | 示例 |
|------|------|------|
| default | 默认值 | default=100 |
| ge / gt / le / lt | 数值范围 | ge=0 |
| min_length / max_length | 字符串长度 | min_length=3 |
| pattern | 正则表达式 | pattern=r"^\\d+$" |
| title | Swagger 标题 | title="分页大小" |
| description | 参数说明 | description="返回数量上限" |

## 禁止额外查询参数

加入 `model_config = {"extra": "forbid"}`，未声明的查询参数会被拒绝：

```python
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # FastAPI 0.114.0+
    limit: int = Field(100, ge=0, le=100)
    offset: int = Field(0, ge=0)
```

传入 /items?limit=10&offset=0&unknown=1 → 422 错误。

## 适用场景

- 查询参数很多，超过 3-4 个
- 多端点共用同一套查询规则
- 需要对额外参数做严格控制

## 小结

- 用 Pydantic 模型集中管理查询参数验证规则
- `Field` 定义具体规则
- `model_config = {"extra": "forbid"}` 拒绝额外参数
- 适用于参数多、共用规则、需要严格校验的场景
