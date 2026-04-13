# 额外数据类型

## 支持的数据类型

FastAPI 支持比 JSON 更多的 Python 内置类型：

| 类型 | 说明 |
|------|------|
| datetime | 日期时间 |
| date | 日期 |
| time | 时间 |
| UUID | 通用唯一标识符 |
| frozenset | 不可变集合（自动去重）|
| Decimal | 高精度十进制数 |
| bytes | 字节串 |

## datetime / date / time

```python
from datetime import datetime, date, time
from fastapi import FastAPI

app = FastAPI()

@app.post("/items/")
async def create_item(
    created_at: datetime,
    event_date: date,
    event_time: time | None = None
):
    return {
        "created_at": created_at,
        "event_date": event_date,
        "event_time": event_time
    }
```

请求体：
```json
{
    "created_at": "2024-07-19T14:30:00",
    "event_date": "2024-07-19",
    "event_time": "14:30:00"
}
```

## UUID

UUID 是通用唯一标识符：

```python
from uuid import UUID

@app.get("/items/{item_id}")
async def read_item(item_id: UUID):
    return {"item_id": item_id}
```

访问 `GET /items/123e4567-e89b-12d3-a456-426614174000`

## frozenset（自动去重）

```python
class Item(BaseModel):
    name: str
    tags: frozenset[str]
```

传入 `["rock", "rock", "metal"]` → 自动变成 `{"rock", "metal"}`。

## Decimal（高精度）

```python
from decimal import Decimal

class Item(BaseModel):
    name: str
    price: Decimal  # 比 float 精度更高
```

## bytes

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes):
    return {"file_size": len(file)}
```

## 小结

FastAPI 自动处理这些类型的序列化/反序列化。
- `datetime` 系列 → ISO 格式字符串
- `UUID` → 字符串
- `frozenset` → 列表（自动去重）
- `Decimal` → 字符串（保持精度）
- `bytes` → Base64 或普通字节
