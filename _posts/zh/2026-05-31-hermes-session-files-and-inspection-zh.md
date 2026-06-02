---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes会话文件与检查
translated: true
type: note
---

2. Session files: ~/.hermes/sessions/
Hermes 将 request dumps 存储在 ~/.hermes/sessions/ 中。您可以直接检查它们：GitHub
bash# List sessions
ls ~/.hermes/sessions/

# Grep for token usage across all sessions

grep -r "input_tokens\|output_tokens" ~/.hermes/sessions/ | tail -50

# Pretty-print a specific session

cat ~/.hermes/sessions/<session_id>.json | python3 -m json.tool | grep -A5 "usage"
