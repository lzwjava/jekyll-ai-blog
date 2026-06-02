---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Python 开发中的 INI 文件
translated: true
type: note
---

问题：INI 文件在 Python 开发中是什么，它如何用于配置？

答案：

**INI 文件**（“initialization”文件的缩写）是一种简单、人类可读的文本格式，最初由 Windows 推广用于存储配置设置。它包括：

- 方括号中的节 `[section]`
- 键值对，如 `key = value`
- 以 `;` 或 `#` 开头的可选注释

典型的 `config.ini` 文件示例：

```ini
[database]
host = localhost
port = 5432
username = admin
password = secret123

[app]
debug = true
log_level = INFO
theme = dark
```

### INI 文件在 Python 开发中的使用方式

Python 通过 `configparser` 模块（在 Python 2 中称为 `ConfigParser`）内置支持读写 INI 文件。

#### 读取 INI 文件

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# 访问值
db_host = config['database']['host']          # 'localhost'
debug = config.getboolean('app', 'debug')     # True
port = config.getint('database', 'port')       # 5432
```

#### 写入或修改 INI 文件

```python
config['app']['theme'] = 'light'
config['database']['port'] = '3306'

with open('config.ini', 'w') as configfile:
    config.write(configfile)
```

### 为什么开发者仍然在 Python 项目中使用 INI 文件

- 极其简单且可读（非常适合中小型应用程序、devops 脚本、工具）
- 无需外部依赖（内置模块）
- 非常适用于分层配置
- 易于手动或通过脚本编辑
- 常见于遗留项目、桌面应用程序、科学工具和一些 Web 框架（例如，旧的 Django 或 Flask 设置）

### 现代替代方案（目前通常首选）

| 格式   | 模块/库              | 优点                              | 典型用例                      |
|----------|------------------------|-----------------------------------|-----------------------------------|
| JSON     | `json` (内置)       | 通用、严格的语法                  | API、Web 应用程序                 |
| YAML     | PyYAML 或 ruamel.yaml  | 可读性强、支持注释                | DevOps、Docker、现代 Python 应用程序|
| TOML     | tomllib (Python 3.11+) | 简洁，正成为 Python 的首选        | pyproject.toml、新项目            |
| .env     | python-dotenv          | 简单的 key=value，无节结构      | 环境变量                      |

### 总结

INI 文件是一种经典的、轻量级的配置格式，Python 利用 `configparser` 提供原生支持。尽管像 TOML 和 YAML 这样的新格式在现代 Python 项目中更受欢迎（尤其是自 `pyproject.toml` 成为标准以来），但当注重简单性和零依赖时，INI 文件仍然完全有效且被广泛使用。
