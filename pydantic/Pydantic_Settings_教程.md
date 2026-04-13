# Pydantic Settings 教程 — BaseSettings 完全指南

> Pydantic Settings 是 Pydantic V2 的官方配置管理扩展，让你用声明式方式管理应用配置。

---

## 目录

1. [安装](#1-安装)
2. [基础用法：BaseSettings](#2-基础用法-basesettings)
3. [敏感信息管理](#3-敏感信息管理)
4. [多环境配置](#4-多环境配置)
5. [进阶用法](#5-进阶用法)
6. [Config 配置详解](#6-config-配置详解)
   - [6.1 为什么需要 Config](#61-为什么需要-config)
   - [6.2 V2 推荐写法（SettingsConfigDict）](#62-v2-推荐写法settingsconfigdict)
   - [6.3 SettingsConfigDict 常见设置项](#63-settingsconfigdict-常见设置项)
     - [读取来源](#读取来源)
     - [字段名映射规则](#字段名映射规则)
     - [空值与未知字段处理](#空值与未知字段处理)
     - [自定义解析](#自定义解析)
     - [综合示例](#综合示例)

---

## 1. 安装

```bash
pip install pydantic-settings
```

---

## 2. 基础用法：BaseSettings

### 2.1 最简单的配置类

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    debug: bool = False
    port: int = 8000

# 自动从环境变量读取
settings = Settings()
print(settings.app_name)  # "My App" 或环境变量 APP_NAME 的值
```

### 2.2 为什么用 BaseSettings？

| 传统方式 | BaseSettings |
|---------|--------------|
| `os.environ.get("PORT", 8000)` | `port: int = 8000` |
| 手动类型转换 | 自动类型验证 |
| 硬编码默认值 | 环境变量覆盖默认值 |
| 配置散落各处 | 集中管理 |

---

### 2.3 环境变量自动映射

Python 字段名 → 环境变量名，遵循以下规则：

> **规则 1：snake_case 自动转为全大写下划线（SCREAMING_SNAKE_CASE）**
> **规则 2：默认严格匹配大小写**

| Python 字段名 | 环境变量名（自动转换后） |
|--------------|------------------------|
| `app_name` | `APP_NAME` |
| `database_url` | `DATABASE_URL` |
| `max_connections` | `MAX_CONNECTIONS` |
| `api_key` | `API_KEY` |

`case_sensitive` 控制是否区分大小写：

```python
# case_sensitive=True（默认）：严格匹配
field_name: str  # 只认 FIELD_NAME

# case_sensitive=False：忽略大小写
model_config = SettingsConfigDict(case_sensitive=False)
field_name: str  # FIELD_NAME / field_name / Field_Name 都能读到
```

### 2.4 字段验证与类型

支持所有 Pydantic 标准类型：

```python
from pydantic_settings import BaseSettings
from typing import List, Dict, Set

class Settings(BaseSettings):
    port: int = 8000              # int
    rate: float = 1.0            # float
    enabled: bool = True         # bool
    name: str = "app"            # str
    allowed_hosts: List[str] = ["localhost"]   # 列表
    extra: Dict[str, str] = {}   # 字典
    admin_emails: Set[str] = set()  # 集合
```

### 2.5 .env 文件支持

Pydantic Settings 原生支持 `.env` 配置文件。将所有环境变量写入 `.env` 文件，由 Pydantic 自动读取并注入 Settings 字段，无需手动 `load_dotenv()`。

对应的 `.env` 文件：

```env
APP_NAME=我的应用
DEBUG=true
PORT=3000
```

多文件覆盖（后声明的文件优先级更高）：

```python
model_config = SettingsConfigDict(
    env_file=[".env", ".env.local"],   # .env.local 优先级更高
    extra="ignore",
)
```

空值不覆盖（防止空字符环境变量覆盖字段默认值）：

```python
model_config = SettingsConfigDict(
    env_file=".env",
    env_ignore_empty=True,   # PORT="" 不会覆盖 port=8000
)
```

> 更多配置项（`case_sensitive`、`env_prefix`、`env_nested_delimiter`、`extra` 等）见 **[5.3 SettingsConfigDict 常见设置项](#53-settingsconfigdict-常见设置项)**。

### 2.6 嵌套字段

配置项较多时，用 Pydantic 模型嵌套组织，通过 `__` 分隔符映射环境变量：


配置项较多时，用 Pydantic 模型嵌套组织，通过 `__` 分隔符映射环境变量：

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",   # DATABASE__HOST 对应 database.host
        case_sensitive=False,
    )

    app_name: str = "My App"
    database: DatabaseConfig = DatabaseConfig()

settings = Settings()
print(settings.database.host)    # 从 DATABASE__HOST 读取
print(settings.database.port)    # 从 DATABASE__PORT 读取
```

对应 `.env` 写法：

```env
APP_NAME=我的应用
DATABASE__HOST=localhost
DATABASE__PORT=5432
DATABASE__NAME=mydb
```

---


### 2.7 不将敏感信息写入日志


```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SecretStr 在打印时显示 "********"
    secret_key: SecretStr
    database_url: SecretStr

settings = Settings()
print(settings.secret_key)  # Secret('**********')
```

### 3.1 敏感字段配置

在 `BaseSettings` 中，**所有字段本质上都是从环境变量读取的配置项**，`model_config` 只是辅助设置。以下是几种典型配置方式：

#### 3.1.2 用 validation_alias 改映射名

当 Python 字段名和环境变量名不一致时，用 `validation_alias` 指定实际读取的环境变量名：

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Python 字段名 db_url，读取 DB_URL 环境变量
    db_url: str = Field(validation_alias="DB_URL")

    # Python 字段名 api_key，读取 API_KEY；无默认值，必须提供
    api_key: str = Field(..., validation_alias="API_KEY")

    # 字段名带下划线，默认读大写下划线（SECRET_KEY）
    # 用 validation_alias 显式指定任意名称
    db_pass: str = Field(default="root", validation_alias="DB_PASSWORD")
```

**为什么用 `validation_alias`**：代码里用小写下划线命名（`api_key`、`db_pass`），`.env` 文件用大写下划线（`API_KEY`、`DB_PASSWORD`），互不干扰。


#### 3.1.3 必填字段 vs 可选字段


```python
class Settings(BaseSettings):
    # 必填：无默认值，环境变量不存在则启动时报错
    database_url: str

    # 必填但可读性更强：Field(...) 表示必须提供
    api_key: str = Field(
        ...,
        validation_alias="API_KEY",
        description="调用外部 API 的密钥"
    )

    # 可选：有默认值，环境变量不存在时使用默认值
    debug: bool = False
    port: int = 8000
```

> **`...`（Ellipsis，省略号）**：Pydantic 语法，表示该字段**必须提供值**，与"无默认值"含义相同。`Field(...)` 即声明此字段不可省略。

## 3 多环境配置

### 3.1 环境变量切换

```python
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "development")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}",
        env_file_encoding="utf-8",
    )

    app_name: str = "My App"
    debug: bool = False
    database_url: str
```

## 4 进阶用法

### 4.1 运行时动态更新配置

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8000

settings = Settings()

# 运行时修改（不推荐用于生产）
settings.port = 9000
print(settings.port)  # 9000
```

### 4.2 配置验证（model_validator）

```python
from pydantic_settings import BaseSettings
from pydantic import model_validator

class Settings(BaseSettings):
    database_url: str
    pool_size: int = 5

    @model_validator(mode="after")
    def validate_pool_size(self):
        if self.pool_size < 1:
            raise ValueError("pool_size 必须 >= 1")
        return self

settings = Settings(database_url="postgresql://localhost/db", pool_size=0)
# → raise ValueError: pool_size 必须 >= 1
```

### 4.3 读取 YAML 配置文件

```python
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

def load_yaml_config():
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

yaml_config = load_yaml_config()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "My App"
    debug: bool = False

settings = Settings(**yaml_config)
```

---



### 5.1 为什么需要 Config？

回顾一下 Pydantic Settings 的工作方式：

```
环境变量 / .env 文件  ──▶  BaseSettings 类  ──▶  Python 对象
（外部数据源）         （规则由 Config 定义）    （应用程序用）
```

`BaseSettings` 类只定义"有哪些字段"，真正控制"怎么读取这些数据"的，是 **`class Config`**。
这是一个 Pydantic 内部设计的*约定大于配置*的机制：
- 只要你在 Settings 子类里写一个类属性名为 `Config` 的类
- Pydantic 运行时就会自动找到它，读取里面的配置项
- 用于控制 BaseSettings 的读取行为

```python
class Settings(BaseSettings):
    # 字段定义 —— 定义有哪些配置项
    app_name: str
    debug: bool = False

    # Config 内部类 —— 定义怎么读取这些配置项
    class Config:
        env_file = ".env"              # 从 .env 文件读
        case_sensitive = False         # 不区分大小写
        env_prefix = "APP_"            # 加全局前缀
```

> **换个角度理解**：`class Config` 就相当于是 `BaseSettings` 的使用说明书，告诉它：
> - 去哪里找配置文件？
> - 字段名怎么和环境变量对应？
> - 大小写是否敏感？
> - 遇到未知字段是跳过还是报错？

Pydantic Settings 支持两种写法，**效果等价**，V2 推荐用 `model_config`：

```python
# V1 旧写法（仍能用）
class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = False

# V2 新写法（推荐）
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
```

### 5.2 V2 推荐写法（SettingsConfigDict）

`SettingsConfigDict` 是 V2 推荐的写法，将配置项从 `class Config` 中抽离出来，直接作为 `model_config` 类属性赋值。效果完全等价，但代码更简洁。

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str
    debug: bool = False
```

`SettingsConfigDict` 本质上就是一个字典，继承自 `dict`，Pydantic 会自动识别并读取其中的键值对。

### 5.3 SettingsConfigDict 常见设置项

下面列出 `SettingsConfigDict` 中最常用的配置项，按功能分组说明。

#### 读取来源

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `env_file` | `str \| Path \| list[str \| Path] \| None` | `None` | 从哪个 .env 文件读取。设为 `.env` 读取单文件；设为 `[" .env", ".env.local"]` 时，后者会覆盖前者重复的字段。|
| `env_file_encoding` | `str` | 自动检测 | .env 文件编码，含中文建议设为 `"utf-8"` |



**`.env` 文件格式**（对应 `env_file` 设置）：

```env
# 键值对，等号左右不加引号（字符串值可加可不加引号）
APP_NAME=我的应用
DEBUG=true
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=your-secret-key-here
```

**常见疑问**：

- `.env.local` 会**覆盖** `.env` 中的同名字段，用于本地开发覆盖默认值：
  ```python
  model_config = SettingsConfigDict(
      env_file=[".env", ".env.local"],  # .env.local 优先级更高
      extra="ignore",
  )
  ```
- `env_ignore_empty=True` 可防止空字符串环境变量覆盖字段默认值：
  ```python
  model_config = SettingsConfigDict(
      env_file=".env",
      env_ignore_empty=True,  # PORT="" 不会覆盖 port=8000
  )
  ```

#### 字段名映射规则

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `case_sensitive` | `bool` | `True` | `False` = 字段名 `app_name` 可以从 `APP_NAME`、`App_Name`、`app_name` 等任意大小写形式的环境变量读取 |
| `env_prefix` | `str` | `""` | 所有字段统一加前缀（只影响**系统环境变量**，不影响 .env 中的字段名）。设为 `"APP_"` 后，`port` 字段实际读取 `APP_PORT` 环境变量 |
| `env_nested_delimiter` | `str \| None` | `None` | 嵌套字段分隔符。设为 `"__"` 后，`database.host` 字段从 `DATABASE__HOST` 环境变量读取 |

> **重要**：`env_prefix` 只对**系统环境变量**生效，`.env` 文件中的字段名不受前缀影响。

#### 空值与未知字段处理

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `env_ignore_empty` | `bool` | `False` | `True` = 空字符串形式的环境变量不覆盖字段默认值 |
| `env_parse_none` | `set[str]` | `{}` | 将指定字符串解析为 `None`，例如设为 `{"", "none", "null"}` 后，环境变量值为 `"none"` 时字段收到 `None` 而非字符串 `"none"` |
| `extra` | `"allow" \| "ignore" \| "forbid"` | `"ignore"` | 遇到未在 Settings 类中定义的字段时的行为：`"ignore"`=忽略（默认）；`"allow"`=存入 `__pydantic_extra__`；`"forbid"`=抛出异常 |

#### 自定义解析

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `env_decode` | `dict[str, Callable]` | `{}` | 自定义字段解码方式，例如 `{"extra": json.loads}` 可让 `extra` 字段从 JSON 字符串环境变量读取 |

#### 综合示例

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env", ".env.local"],  # .env.local 覆盖 .env 的重复字段
        env_file_encoding="utf-8",         # 含中文必设
        case_sensitive=False,              # 忽略大小写
        env_prefix="APP_",                 # APP_PORT 读 port
        env_nested_delimiter="__",         # DATABASE__HOST 读 database.host
        env_ignore_empty=True,            # 空字符串不覆盖默认值
        extra="ignore",                   # 忽略 .env 中未定义的字段
    )

    app_name: str
    port: int = 8000
    database_host: str
    database_port: int = 5432
    debug: bool = False
    secret_key: str
    allowed_hosts: list[str] = ["localhost"]
```

对应 `.env` 文件：

```env
APP_NAME=我的应用
APP_PORT=3000
DATABASE__HOST=localhost
DATABASE__PORT=5432
DEBUG=true
APP_SECRET_KEY=my-super-secret-key
ALLOWED_HOSTS=["api.example.com","cdn.example.com"]
```

对应系统环境变量（`env_prefix="APP_"` 影响系统变量，不影响 .env）：

```bash
export APP_PORT=3000
export APP_SECRET_KEY=secret
```

