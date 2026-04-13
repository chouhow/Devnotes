# 测试

## TestClient

FastAPI 提供 `TestClient`，无需启动服务器即可测试：

```bash
pip install httpx
```

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

## 同步测试

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test"})
    assert response.status_code == 200
    assert "item_id" in response.json()
```

## 异步测试

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_async_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
```

## 依赖覆盖

测试时 Mock 掉数据库等依赖：

```python
def override_get_user():
    return {"username": "testuser"}

app.dependency_overrides[get_current_user] = override_get_user

def test_protected_endpoint():
    response = client.get("/users/me")
    assert response.json() == {"username": "testuser"}
```

## 调试

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 小结

- `TestClient` 无需启动服务器，直接测试 FastAPI 应用
- `dependency_overrides` Mock 掉认证、数据库等依赖
- Pytest 集成更方便：`pytest.ini` 配置 `asyncio_mode = auto`
