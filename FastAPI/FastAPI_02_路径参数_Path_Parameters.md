# 路径参数

## 基本用法

URL 中的 `{item_id}` 就是路径参数，在函数参数中声明同名参数来接收：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}
```

访问 `GET /items/5`，`item_id` 的值就是字符串 `"5"`。

## 类型注解

给路径参数加上类型注解，FastAPI 会自动：

1. 把字符串 `"5"` 转成整数 `5`
2. 如果不是合法整数（如 `"foo"`），返回 422 错误

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

访问 `GET /items/5` 返回 `{"item_id": 5}`（整数）。  
访问 `GET /items/foo` 返回 422 Unprocessable Entity。

## 路径参数顺序

**重要**：固定路径要写在动态路径前面，否则动态路径会先匹配到：

```python
# 正确顺序
@app.get("/users/me")          # 固定路径，要写在前面
@app.get("/users/{user_id}")  # 动态路径

# 错误顺序（永远匹配到第二个）
@app.get("/users/{user_id}")   # 动态路径
@app.get("/users/me")          # 固定路径，这个永远不会被匹配到
```

## 多个路径参数

一个 URL 可以有多个路径参数：

```python
@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}
```

访问 `GET /users/42/items/1`，`user_id=42`、`item_id=1`。

## 带验证的路径参数

用 `Path` 可以给路径参数加更细的验证规则：

```python
from fastapi import FastAPI, Path

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(title="商品ID", ge=1)):
    return {"item_id": item_id}
```

常用验证参数：
- `ge=1`：必须 >= 1
- `le=100`：必须 <= 100
- `gt=0`：必须 > 0
- `title`：文档里显示的中文标题

## 小结

| 要点 | 说明 |
|------|------|
| `{param}` 声明 | URL 里的 {param} |
| 类型注解 | 自动转换和验证类型 |
| 参数名一致 | 函数参数名要和 {param} 名一致 |
| 顺序 | 固定路径写在动态路径前面 |
