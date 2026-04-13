# 后台任务

## BackgroundTasks

`BackgroundTasks` 在响应返回后执行后台操作（发邮件、日志、数据库更新等），无需等待：

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str, message: str):
    # 实际发邮件的逻辑
    print(f"Sending email to {email}: {message}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, message="Notification!")
    return {"message": "后台任务已调度"}
```

响应立即返回，后台执行 `send_email`。

## 多个后台任务

```python
@app.post("/")
async def root(
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(task1)
    background_tasks.add_task(task2)
    return {"message": "多个后台任务已调度"}
```

## 与 Depends + yield 的区别

| 特性 | BackgroundTasks | Depends + yield |
|------|--------------|----------------|
| 执行时机 | 响应发送后 | 请求处理完成后（可保证顺序 |
| 执行顺序 | 不保证 | 保证 |
| 适用场景 | 发送通知等 | 数据库提交、清理 |

## 小结

- `BackgroundTasks.add_task(fn, args...)` 调度后台任务
- 响应立即返回，不阻塞
- 适合发邮件、日志记录等轻量级后台操作
- 重量级任务（队列、批处理）用 Celery + Redis
