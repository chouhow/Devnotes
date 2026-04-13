# 服务端推送事件

## Server-Sent Events（SSE）

SSE 允许服务器向浏览器推送实时更新，无需 WebSocket 或轮询：

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_stream():
    for i in range(10):
        yield f"data: Message {i}\n\n"
        await asyncio.sleep(1)

@app.get("/events")
async def events():
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

浏览器端用 EventSource 接收：
```javascript
const source = new EventSource("/events");
source.onmessage = (event) => {
    console.log("收到：", event.data);
};
```

## 小结

SSE 是单向（服务端→浏览器），适合：实时通知、日志推送、进度更新。与 WebSocket 的双向通信不同，SSE 只需服务器单向推送数据。
