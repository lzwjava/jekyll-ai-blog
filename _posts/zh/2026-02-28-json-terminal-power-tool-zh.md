---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终端 JSON 强大工具
translated: true
type: note
---

**jq** 是一个超级流行且极其有用的 **command-line JSON processor**。

将其视为 **“sed/awk/grep for JSON”** —— 一个轻量级工具，让您轻松：

- pretty-print JSON（使其可读）
- 提取特定字段/值
- 过滤数据
- 转换/重构 JSON
- map、reduce、sort、join、计算等
- 处理非常嵌套/复杂的结构

…全部直接从终端执行，通常与 `curl`、`kubectl`、`aws cli`、`git`、日志、配置文件、API 等管道结合使用。

### 快速示例

```bash
# Pretty-print messy JSON
curl https://api.github.com/users/jqlang | jq

# Get just one field
curl https://api.github.com/users/jqlang | jq '.name'

# Get several fields in a new object
curl https://api.github.com/users/jqlang | jq '{name, login, followers}'

# Filter array items
curl https://jsonplaceholder.typicode.com/posts | jq '.[] | select(.id <= 3)'

# Change structure + rename keys
... | jq '.[] | {title: .title | ascii_upcase, userId}'
```

您的命令

```bash
apt install jq -y
```

会在 Debian/Ubuntu 系统上安装此工具（在 Docker 容器、服务器、WSL、云 VM、开发环境中非常常见）。

当前最新版本（截至 2026 年初）约为 **1.8.x** —— 微小二进制文件（~1–2 MB），用 C 语言编写，无运行时依赖，极快。

基本上：如果您处理 APIs、Kubernetes、Terraform 输出、Docker 元数据、JSON 格式日志、配置文件，或任何自动化/脚本 → **jq 几乎是必备的**。

强烈推荐至少学习基础知识——它能节省海量时间。😄

官方网站（那里有非常好的教程）：https://jqlang.org/