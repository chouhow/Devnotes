# 装饰器中的依赖

## 在装饰器中声明依赖

有些依赖不需要在函数签名中使用，可以直接写在装饰器中：

```python
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="x-api-key")

async def verify_api_key(
    api_key: str = Security(api_key_header)
):
    if api_key != "secret-key":
        raise HTTPException(status_code=403)

@app.get("/items/", dependencies=[Depends(verify_api_key)])
async def read_items():
    return [{"item": "Foo"}]
```

通过 `dependencies=[...]` 在装饰器中声明，不需要在函数签名中注入。

## SecurityScopes

`SecurityScopes` 支持 OAuth2 权限范围：

```python
from fastapi import Security
from fastapi.security import SecurityScopes

scopes = SecurityScopes(scopes=["items", "admin"])

def verify_scopes(
    scopes: SecurityScopes = Security(SecurityScopes)
):
    if "items" not in scopes.scopes:
        raise HTTPException(status_code=403)
```

## 多个依赖

```python
@app.get("/admin/", dependencies=[Depends(verify_key), Depends(verify_admin)])
async def admin_only():
    return {"admin": True}
```

## 小结

- `dependencies=[...]` 在装饰器中声明依赖，不需要在函数签名中
- 适合 API Key 验证、全局权限检查等不需要在业务逻辑中使用的依赖
- 路径操作签名保持干净，依赖逻辑与业务逻辑分离
