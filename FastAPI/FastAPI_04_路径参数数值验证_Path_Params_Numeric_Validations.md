# 路径参数数值验证

## 基本用法

上一节讲了路径参数的基本用法，这一节讲如何对路径参数做数值验证。

用 `Path` 可以给路径参数加上验证规则：

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(title="商品ID")):
    return {"item_id": item_id}
```

## 数值范围验证

| 参数 | 含义 | 示例 |
|------|------|------|
| ge | 大于或等于（>=）| ge=1 |
| gt | 大于（>）| gt=0 |
| le | 小于或等于（<=）| le=1000 |
| lt | 小于（<）| lt=10 |

常用组合：

```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(title="商品ID", ge=1, le=1000)
):
    return {"item_id": item_id}
```

`item_id` 必须 >= 1 且 <= 1000，否则返回 422。

## 浮点数验证

同样适用于 float 类型：

```python
from fastapi import Path

@app.get("/items/{price}")
async def read_price(price: float = Path(gt=0.0, description="价格必须大于零")):
    return {"price": price}
```

## 元数据

`Path` 还可以设置文档元数据：

```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        title="商品ID",
        description="商品的唯一标识符",
        ge=1
    )
):
    return {"item_id": item_id}
```

| 参数 | 作用 |
|------|------|
| title | Swagger UI 中显示的标题 |
| description | 参数说明 |
| ge / gt / le / lt | 数值范围 |
| min_length / max_length | 字符串长度限制 |
| pattern | 正则表达式限制 |

## 小结

- `Path` 用来验证路径参数
- `ge`/`gt`/`le`/`lt` 控制数值范围
- `title`/`description` 添加 Swagger UI 文档元数据
- 类型注解（如 `int`）和 `Path` 验证可以同时使用
