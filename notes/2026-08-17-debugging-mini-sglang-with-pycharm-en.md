---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debugging Mini-SGLang with PyCharm
translated: false
type: note
---

Here's the full explanation, grounded in what I verified in your repo.

## Why the interpreter matters (the `run_python.sh` story)

Your `run_python.sh` exists for a reason:

```bash
exec /usr/bin/python3.12 -s "$@"
```

The `-s` flag **disables the user site-packages** (`~/.local/lib/python3.12/site-packages`), which has torch 2.11.0. That version breaks `sgl_kernel` with an `undefined symbol: c10_cuda_check_implementation`. The *system* site-packages (`/usr/lib/python3/dist-packages`) has the working torch 2.9.1 + sgl_kernel 0.3.21 + flashinfer 0.6.16.

Good news: **your `.idea/minisgl.iml` already points at `/usr/bin/python3.12`** (`<orderEntry type="jdk" jdkName="/usr/bin/python3.12" .../>`), so PyCharm's interpreter is already correct. If you ever switch it, that's what breaks. To verify in PyCharm: *Settings → Project: mini-sglang → Python Interpreter* → it should show `/usr/bin/python3.12`, and the package list should show **torch 2.9.x, not 2.11.0**.

**One subtlety:** PyCharm doesn't pass `-s` by default, but you can replicate it in the run config's *Interpreter options* field (see below). Without it, PyCharm may import the user-site torch 2.11.0 and crash with the same `undefined symbol` error. Check *Run → Edit Configurations → Interpreter options* — it needs `-s`.

## How PyCharm's multiprocessing debugging works (the magic you asked about)

PyCharm's debugger (`pydevd`) doesn't need any `debugpy.listen()` code in your project. The mechanism:

1. When you press **Debug**, PyCharm launches the main process with a modified `PYTHONPATH`/environment and `sitecustomize` hooks that auto-start `pydevd` attached to the IDE. It also sets env vars like `PYCHARM_HOSTED=1` and `PYDEVD_*`.
2. **The key trick:** those environment variables live in `os.environ` of the debugged process.
3. When `launch.py` calls `mp.Process(target=..., ...)` — which it does for the schedulers, tokenizer, and detokenizer — the `multiprocessing` module **inherits the parent's environment** into each child. With `spawn`, the child re-imports `__main__` / the target module, and that import triggers `sitecustomize` → which sees `PYCHARM_HOSTED` → auto-attaches a second `pydevd` connection to the IDE, registered as a new "Python process" in the Debug tool window.
4. Your breakpoints are **propagated automatically**: set a breakpoint in `scheduler/scheduler.py`, and every process that imports that file (main + each TP scheduler child) gets it. When the child hits it, the whole process tree **pauses together** (PyCharm's default "Suspend all threads" / "Suspend all processes").

So it works here because `launch.py` creates children with the standard `multiprocessing` API from the debugged process. If a child ever did `os.execv` with a different interpreter or daemonized away, auto-attach would break — but that's not the case here.

## Step-by-step run config (with real values for your machine)

I checked your GPU (`RTX 4070, 12GB`) and local models. **DeepSeek-V2-Lite is 30GB — it won't fit.** The 626MB GPT-2 at `/mnt/data/sec-edgar-gpt-124m-model/` is the right debug target.

*Run → Edit Configurations → ➕ → Python*:

| Field | Value |
|---|---|
| Name | `minisgl-debug` |
| **Module name** | `minisgl` (not "script path" — use the dropdown) |
| Interpreter options | `-s` |
| Working directory | `/mnt/data/mini-sglang` |
| Parameters | `--model-path /mnt/data/sec-edgar-gpt-124m-model --tp-size 1 --port 1919 --dtype float32` |
| Environment variables | `PYTHONUNBUFFERED=1` (add via the env-var editor) |
| Run with Python Console | unchecked (keep standard debugger) |

Notes on the parameters:
- `--model-path ...` is the only **required** arg (`parser.add_argument(..., required=True)` in `args.py`).
- `--tp-size 1` → only **one** scheduler child process to juggle instead of N. Multi-GPU debugging multiplies the process tree.
- `--dtype float32` → the 124M GPT-2 is fine in fp32, avoids dtype-conversion code paths during your first debugging session. (You can switch to `--dtype bfloat16` later.)
- `--num-tokenizer 0` is the default (shared tokenizer/detokenizer) — keep it; fewer processes.
- `--shell-mode` runs an interactive prompt instead of uvicorn — not what you want for API debugging, but handy if you want to debug request handling in a REPL.

Then press **Debug**. The Debug tool window will show the process tree:

```
minisgl-debug (main)                          ← api_server.py (FastAPI/uvicorn, port 1919)
├── minisgl-TP0-scheduler                     ← scheduler/scheduler.py, engine, kvcache
├── minisgl-tokenizer-0                       ← tokenizer/
└── minisgl-detokenizer-0                     ← tokenizer/ (detokenize path)
```

You can pause/kill individual processes from the tree, and there's a "Resume all processes" toggle so you can debug one child while others run.

## Concrete debugging workflow

1. Set a breakpoint in `python/minisgl/scheduler/prefill.py` (first request) and one in `decode.py`.
2. Start the server via the run config; curl a request:
   ```bash
   curl http://127.0.0.1:1919/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt2","messages":[{"role":"user","content":"Hello!"}],"max_tokens":16}'
   ```
3. Execution stops in the **TP0-scheduler** process. You can:
   - **Evaluate** `len(seq_ids)`, `batch.seq_lens` — tensors render as shape/dtype in the Variables pane (PyCharm renders torch tensors natively).
   - Step over CUDA kernel calls (FlashInfer/sgl_kernel) — you can't step *into* them (compiled C++), so use *Step Over* at those lines.
   - Use the **Evaluate Expression** (`⌥F8`) for `tensor.shape`, `isinstance(x, torch.Tensor)`.
4. To debug the HTTP layer instead, set the breakpoint in `server/api_server.py` — that hits in the **main** process.

## Caveats specific to this project

- **`mp.set_start_method("spawn", force=True)`** is fine — PyCharm auto-attach works with spawn via env-var inheritance. The one thing to avoid: *never* add your own `debugpy`/`pdb` calls while also using PyCharm's debugger — two debuggers attached to one process conflict (port/file-lock issues).
- **CUDA kernels are opaque**: FlashAttention/FlashInfer/sgl_kernel JIT C++ can't be stepped into; Python breakpoints around them work.
- **`torch.inference_mode()`** is active inside `_run_scheduler` — tensor autograd history is off, so you can't inspect `grad_fn`. That's expected.
- **GPU memory**: the 12GB card also holds the KV cache; the GPT-2 124M leaves ~11GB free, plenty. If you later use DeepSeek-V2-Lite you'd need `--tp-size 2` across two GPUs or accept OOM.
- **pdb's `breakpoint()`** inside a spawned child attaches to the child's stdin — with PyCharm running the show, don't mix them.

Want me to write the PyCharm run-configuration XML (`.idea/runConfigurations/minisgl_debug.xml`) so it appears in your Run Configurations dropdown automatically?