# JSON 流响应

## StreamingResponse

`StreamingResponse` 返回流式数据，适合大数据集或实时输出：

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def iter_csv():
    for i in range(10000):
        yield f"id,{i},{i*2}\n"

@app.get("/download")
async def download():
    return StreamingResponse(
        iter_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    )
```

`media_type` 指定内容类型，`headers` 添加响应头。

## JSON 流（JSON Lines）

每次返回一行 JSON：

```python
import json

async def generate_jsonl():
    for i in range(100):
        yield json.dumps({"id": i, "data": f"item {i}"}) + "\n"

@app.get("/stream-jsonl")
async def stream_jsonl():
    return StreamingResponse(
        generate_jsonl(),
        media_type="application/x-ndjson"
    )
```

## 小结

- `StreamingResponse` 返回流数据，不等待全部生成
- `media_type="application/x-ndjson"` 每次返回一行 JSON
- 适合：大文件下载、实时数据流、数据库游标查询
