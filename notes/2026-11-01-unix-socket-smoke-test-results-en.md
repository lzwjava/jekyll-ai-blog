---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unix Socket Smoke Test Results
translated: false
type: note
---

Smoke run done. Working tree is clean (HEAD = `482279b server : add support for .sock communication`), so I smoke-tested the new `.sock` (AF_UNIX) support in `whisper-server`.

## Results — works

| Test | Command | Result |
|---|---|---|
| Build | `cmake --build build --target whisper-server whisper-cli` | OK |
| Start on socket | `whisper-server -m models/ggml-tiny.en.bin --host /tmp/whisper-smoke.sock` | socket created, `whisper server listening at unix://...` |
| Static file `GET /` | `curl --unix-socket .../` | 200, 2130 bytes |
| `GET /health` | | `{"status":"ok"}` |
| `POST /inference` (multipart) | `-F file=@samples/jfk.wav` | correct transcript of JFK sample |
| `POST /inference` streaming | `-F stream=true` | correct transcript |
| `POST /load` | `-F model=...` | `Load was successful!` |
| 3 concurrent inferences | parallel curl | all 3 correct |
| Relative path | `--host rel.sock` | works |
| Abstract namespace | `--host @whisper-smoke.sock` + `curl --abstract-unix-socket` | works (no filesystem entry) |
| TCP regression | `--host 127.0.0.1 --port 18089` | `/health` + `/inference` unchanged |

## Issues found

1. **Stale socket file blocks restart** (main issue). After shutdown (both SIGINT and SIGTERM) the `.sock` file is left on disk, so the next start on the same path fails:
   ```
   couldn't bind to unix socket: /tmp/whisper-smoke.sock   (exit code 1)
   ```
   `httplib.h` never `unlink()`s on bind/close, and the `clean_up` lambda in `examples/server/server.cpp:1305` only prints timings and frees the ctx. A stale file from a crashed/killed server has the same effect. Workaround today: `rm` the file first, or use the abstract namespace (`--host @name.sock`).

2. **Unhelpful error for over-long paths.** With a path > 107 bytes, `create_socket()` in `httplib.h:3544` returns `INVALID_SOCKET` silently, so the user only sees the generic `couldn't bind to unix socket: <long path>` with no hint about `sun_path` limits. Same for a non-existent parent directory.

Both are cosmetic-to-moderate; the transport itself and the TCP path are fine. Want me to look at a fix for #1 (unlink in `clean_up`, plus unlink-before-bind for stale files)?