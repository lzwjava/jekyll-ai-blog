---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Test Across Five Input Lengths
translated: false
type: note
---

Done. Added a `ww sglang test` command that exercises the running SGLang server (`Qwen/Qwen2.5-0.5B-Instruct` on port 30010) across five input lengths.

**Changes:**

- **`ww/sglang/test.py`** (new) — streams chat completions with input lengths from ~11 to ~4,700 tokens; reports TTFT, total latency, output tokens, throughput (tok/s), finish reason, and a response snippet per case. Uses SGLang's `/v1/tokenize` extension for exact token counts (streaming chunks here omit `usage`), plus a non-streaming probe and a health/model listing at start. Options: `--url`, `--port`, `--model`, `--max-tokens`, `--no-stream`, `--timeout`.
- **`ww/main.py`** — added `sglang` group routing + help text in `_print_help()`.
- **`completions/_ww`** — registered `sglang` top-level command and `sglang_cmds` for tab completion.

**Sample run against your live server:**

```
case           input     TTFT    total    out    tok/s  finish  response
--------------------------------------------------------------------------------------------
tiny            11t      10ms      37ms     9    240.4  stop      'Hello! How can I assist you today?'
short           73t      10ms      82ms    25    303.2  stop      'The text discusses the beauty and complexity of '
medium         306t       9ms      88ms    27    306.7  stop      'The text describes the beauty of mathematics in '
long         1,189t      10ms     203ms    67    329.5  stop      'Based on the content of the text, here are three'
huge         4,711t      14ms      84ms    24    286.4  stop      'The quick brown fox jumps over the lazy dog whil'

Checks:
  [ OK ] tiny     11 in -> 9 out, finish=stop
  ... (all 5 OK)

Worst TTFT:   huge (4,711 input tokens) = 14ms
```

Also verified `--help`, bad-port error handling, and syntax. Usage: `ww sglang test` (default), `ww sglang test --port 30011`, `ww sglang test --url http://host:30010 --max-tokens 256`.