---
audio: false
generated: true
image: false
lang: en
layout: post
title: JSON Power Tool for Terminal
translated: false
type: note
---

**jq** is a super popular and extremely useful **command-line JSON processor**.

Think of it as **"sed/awk/grep for JSON"** — a lightweight tool that lets you easily:

- pretty-print JSON (make it readable)
- extract specific fields/values
- filter data
- transform/restructure JSON
- map, reduce, sort, join, calculate things
- handle very nested/complex structures

…all directly from the terminal, usually piped together with `curl`, `kubectl`, `aws cli`, `git`, logs, config files, APIs, etc.

### Quick examples

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

Your command

```bash
apt install jq -y
```

installs this tool on Debian/Ubuntu systems (very common in Docker containers, servers, WSL, cloud VMs, dev environments).

Current latest version (as of early 2026) is around **1.8.x** — tiny binary (~1–2 MB), written in C, no runtime dependencies, extremely fast.

Basically: if you work with APIs, Kubernetes, Terraform output, Docker metadata, logs in JSON format, config files, or any kind of automation/scripting → **jq is almost mandatory**.

Highly recommended to learn at least the basics — it saves insane amounts of time. 😄

Official site (very good tutorial there): https://jqlang.org/
