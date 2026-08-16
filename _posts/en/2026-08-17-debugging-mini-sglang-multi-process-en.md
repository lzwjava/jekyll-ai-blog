---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debugging Mini-SGLang Multi-Process
translated: false
type: note
---

Now I understand the project. Here's how to debug Mini-SGLang:

## Key fact: this project is multi-process

`launch_server()` (`python/minisgl/server/launch.py`) spawns **separate OS processes** via `multiprocessing` with `spawn`:

| Process | What it runs |
|---|---|
| Main process | FastAPI/uvicorn API server (`api_server.py`) |
| 1 per TP rank | Scheduler (`_run_scheduler` → `scheduler/scheduler.py`) |
| N+1 | Tokenizer / detokenizer workers (`tokenize_worker`) |

They talk via ZMQ. This matters because **a breakpoint in the main process won't hit code running in a child process**, and `spawn` means child processes re-import everything from scratch.

Also note: the debugger must use the **same interpreter as `run_python.sh`** (`/usr/bin/python3.12 -s`), because the user site-packages have torch 2.11.0 which breaks `sgl_kernel`. `debugpy` is **not installed** yet — you'll need it for anything but plain `pdb`.

---

## Option 1 — Easiest: debug the offline `LLM` API (single process)

`python/minisgl/llm/llm.py` exposes a `Scheduler` subclass that runs everything in **one process** — no multiprocessing, no ZMQ, no server. This is the best way to step through scheduling/prefill/decode logic:

```python
# /tmp/debug_llm.py
import sys; sys.path.insert(0, "/mnt/data/mini-sglang/python")
from minisgl.llm import LLM

llm = LLM("/path/to/model", dtype=torch.bfloat16)  # set breakpoint in Scheduler.__init__
out = llm.generate("Hello, my name is")             # breakpoint in scheduler.py / prefill.py
print(out)
```

Run it with pdb or the VS Code debugger:

```bash
/usr/bin/python3.12 -s /tmp/debug_llm.py          # plain run
/usr/bin/python3.12 -s -m pdb /tmp/debug_llm.py   # pdb CLI
```

Or insert `breakpoint()` directly in `scheduler.py` etc. (equivalent to `pdb.set_trace()`). Note: the scheduler runs inside `torch.inference_mode()`, which is fine for pdb.

## Option 2 — Debug the server (main process + spawned children)

The only reliable way to debug spawned child processes is **remote attach with `debugpy`** (installed with the system python so it survives the `-s` flag):

```bash
/usr/bin/python3.12 -s -m pip install debugpy
```

Then add this at the top of the child target in `launch.py` (e.g. in `_run_scheduler`):

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))   # each spawned process listens on same port; VS Code shows a picker
debugpy.wait_for_client()
```

Start the server normally, then in VS Code use a "Python Debugger: Attach" configuration — VS Code will ask which process to attach to (main uvicorn process, `minisgl-TP0-scheduler`, tokenizers). Attach to the one you set the breakpoint in.

**Breakpoint placement tips:**
- HTTP layer → `server/api_server.py` (main process)
- Scheduling loop → `scheduler/scheduler.py` (`run_forever`), `prefill.py`, `decode.py` (child process)
- Tokenization → `tokenizer/` (child process)

## Option 3 — VS Code launch.json

```jsonc
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to minisgl process",
      "type": "debugpy",
      "request": "attach",
      "connect": { "host": "127.0.0.1", "port": 5678 },
      "processId": "${command:pickProcess}" // lets you pick the scheduler/tokenizer process
    },
    {
      "name": "Run offline LLM (single process)",
      "type": "debugpy",
      "request": "launch",
      "program": "/tmp/debug_llm.py",
      "python": "/usr/bin/python3.12",
      "args": ["-s"] // replicate run_python.sh's -s (disables user site-packages)
    }
  ]
}
```

## Option 4 — PyCharm (this project has `.idea/`)

- Open the project, set the interpreter to `/usr/bin/python3.12` (the system interpreter — avoid the broken user-site torch 2.11.0).
- PyCharm automatically supports `multiprocessing` with `spawn`: when you launch `python -m minisgl` from a run config, child processes automatically connect to the same debugger (no debugpy code needed). Run config: module `minisgl`, add the CLI args from `--help` (e.g. `--model-path ... --tp-size 1`), and set `PYTHONUNBUFFERED=1`.

---

## Caveats

1. **CUDA kernels** (`sgl_kernel`, `flashinfer`, JIT-compiled attention kernels) can't be stepped through — breakpoints only work in Python code.
2. Use `--tp-size 1` while debugging; multi-GPU adds N scheduler processes to juggle.
3. `mp.set_start_method("spawn", force=True)` — child processes re-import modules, so put debugpy listen code in the child *target function*, not module top-level.
4. `run_api_server` runs `uvicorn.run(...)` directly, so if you attach to the main process, breakpoints in `api_server.py` will hit.

Want me to set up `.vscode/launch.json` or add a debugpy hook to `launch.py` for you?