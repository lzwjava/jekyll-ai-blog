---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Session Files and Inspection
translated: false
type: note
---

2. Session files: ~/.hermes/sessions/
Hermes stores request dumps in ~/.hermes/sessions/. You can inspect them directly: GitHub
bash# List sessions
ls ~/.hermes/sessions/

# Grep for token usage across all sessions

grep -r "input_tokens\|output_tokens" ~/.hermes/sessions/ | tail -50

# Pretty-print a specific session

cat ~/.hermes/sessions/<session_id>.json | python3 -m json.tool | grep -A5 "usage"
