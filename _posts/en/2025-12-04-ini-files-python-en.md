---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: INI Files in Python Development
translated: false
type: note
---

Question: What is an INI file in Python development, and how is it used for configuration?

Answer:

An **INI file** (short for "initialization" file) is a simple, human-readable text format originally popularized by Windows for storing configuration settings. It consists of:

- Sections in square brackets `[section]`
- Key-value pairs like `key = value`
- Optional comments starting with `;` or `#`

Example of a typical `config.ini` file:

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

### How INI files are used in Python development

Python has built-in support for reading and writing INI files via the `configparser` module (called `ConfigParser` in Python 2).

#### Reading an INI file

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access values
db_host = config['database']['host']          # 'localhost'
debug = config.getboolean('app', 'debug')     # True
port = config.getint('database', 'port')       # 5432
```

#### Writing or modifying an INI file

```python
config['app']['theme'] = 'light'
config['database']['port'] = '3306'

with open('config.ini', 'w') as configfile:
    config.write(configfile)
```

### Why developers still use INI files in Python projects

- Extremely simple and readable (great for small to medium apps, devops scripts, tools)
- No need for external dependencies (built-in module)
- Works well for hierarchical configuration
- Easy to edit manually or with scripts
- Common in legacy projects, desktop apps, scientific tools, and some web frameworks (e.g., older Django or Flask setups)

### Modern alternatives (often preferred today)

| Format   | Module/Library         | Pros                              | Typical Use Case                  |
|----------|------------------------|-----------------------------------|-----------------------------------|
| JSON     | `json (built-in)       | Universal, strict syntax          | APIs, web apps                    |
| YAML     | PyYAML or ruamel.yaml  | Very readable, supports comments  | DevOps, Docker, modern Python apps|
| TOML     | tomllib (Python 3.11+)| Clean, becoming Python's favorite | pyproject.toml, new projects      |
| .env     | python-dotenv          | Simple key=value, no sections     | Environment variables             |

### Summary

INI files are a classic, lightweight configuration format that Python supports natively with `configparser`. While newer formats like TOML and YAML are more popular in modern Python projects (especially since `pyproject.toml` became standard), INI files are still perfectly valid and widely used when simplicity and zero dependencies matter.
