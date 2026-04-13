# 调试

## 启动开发服务器

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- `--reload`：代码改动后自动重启，开发时用
- `--host 0.0.0.0`：局域网可访问

## __name__ == "__main__"

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

直接 `python main.py` 启动服务器。

## 断点调试

VS Code 或 PyCharm 中设置断点：

VS Code `launch.json`：
```json
{
    "name": "Python: FastAPI",
    "type": "python",
    "request": "launch",
    "module": "uvicorn",
    "args": ["main:app", "--reload"],
    "jinja": true
}
```

PyCharm：Run → Edit Configurations → Python → 设置 `main:app` 和 `--reload`。

## 日志

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("启动完成")
```

## 小结

- `uvicorn main:app --reload` 开发服务器
- `if __name__ == "__main__"` 直接 `python main.py` 启动
- IDE 断点调试
