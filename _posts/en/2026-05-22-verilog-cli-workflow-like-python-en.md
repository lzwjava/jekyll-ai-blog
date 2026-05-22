---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verilog CLI Workflow Like Python
translated: false
type: note
---

Given your background — terminal-first, Python-native, CLI tools builder — the answer is obvious:

---

## **Icarus Verilog (`iverilog`)**

```bash
brew install icarus-verilog
```

That's it. One tool. Feels exactly like GCC.

```bash
iverilog -o sim counter.v counter_tb.v
./sim
```

- No GUI
- No license
- No project files
- Output in terminal
- Errors look like compiler errors you already know
- Pairs perfectly with VSCode + Claude for AI-assisted Verilog

---

**The loop you'll be in:**

```
write .v  →  iverilog  →  read errors  →  ask Claude  →  fix  →  repeat
```

Same as your Python REPL workflow. Start with `picorv32` as reference code when stuck.