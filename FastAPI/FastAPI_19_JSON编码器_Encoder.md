# JSON 兼容编码器

## 背景

有时你需要把 Pydantic 模型存入数据库，但数据库往往只接受 JSON 兼容的数据。问题在于：

- `datetime` 对象不是 JSON 类型，直接存会报错
- Pydantic 模型是一个 Python 对象，数据库也不认识
- 你需要把它们转成"JSON 能接受"的形式

## jsonable_encoder 是什么

`jsonable_encoder()` 是 FastAPI 提供的一个函数，专门把任意 Python 对象转成 JSON 兼容的数据类型。

它做了两件事：

- Pydantic 模型（如 `Item`）→ 转成普通 `dict`
- `datetime` 对象 → 转成 ISO 格式的字符串（`"2024-01-15T10:30:00"`）

转换结果是**一个普通的 Python 数据结构**（字典 / 列表），里面的值全都是 JSON 原生支持的类型，可以直接序列化或存入数据库。

## 完整示例

```python
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# 模拟只接受 JSON 数据的数据库
fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    # 把 Pydantic 模型转成 JSON 兼容的字典
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

## 注意

`jsonable_encoder` 返回的是 Python 数据结构，不是 JSON 字符串。如果要得到 `"{\"title\": \"...\"}"` 这种格式的字符串，还需要再调用一次 `json.dumps()`。

另外，这个函数不只你用得上——FastAPI 内部处理请求和响应时也在用这个函数做数据转换。
