---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compile Failure in PyTorch Triton
translated: false
type: note
---

That's `torch.compile` failing — Triton tried to invoke `gcc` to build a CUDA helper module and gcc returned non-zero. The smoke run never hit this because we forced `--compile=False`.

**Fastest fix: just disable compile.** You lose 20–30% throughput (so ~59h instead of ~42h for 19073 iters), but training is otherwise identical and the model quality is the same.

```bash
cd /mnt/data/nanoGPT
tmux new -s nano    # or: tmux attach -t nano
source venv/bin/activate

PYTORCH_ALLOC_CONF=expandable_segments:True \
python -u train.py config/train_fineweb_gpt3.py --compile=False 2>&1 \
  | tee -a out-fineweb-gpt3/train.log
```

### One thing that looks off

The traceback paths are `/home/lzw/.local/lib/python3.11/...` — that's **system Python 3.11**, not the nanoGPT venv (which I used earlier was Python 3.14 at `/mnt/data/nanoGPT/venv/bin/python`). Did you forget `source venv/bin/activate` in your tmux session? That's not what's causing this error (the gcc failure would happen in either env), but you'll want consistency for the long run.

Check:
```bash
which python && python -c "import sys; print(sys.executable, sys.version)"
```

### Optional: actually fix compile (if you want the speedup)

The gcc compile fails — to see *why*, run gcc with the same args manually from the traceback. Common causes on Ubuntu:

```bash
# Quick checks
gcc --version
ls /usr/local/cuda/lib64/libcuda.so* /usr/lib/x86_64-linux-gnu/libcuda.so*
ls /usr/local/cuda/include/cuda.h
echo $CUDA_HOME
```

Typical fixes:
- `sudo apt install nvidia-cuda-toolkit` (gets the headers Triton needs)
- `export CUDA_HOME=/usr/local/cuda` and `export PATH=$CUDA_HOME/bin:$PATH` before running
- Or: re-run the smoke command — sometimes Triton's stale `~/.triton/cache` causes phantom failures; `rm -rf ~/.triton/cache` clears it

**My recommendation:** start the long run with `--compile=False` now (you already lost time on the failed start). Diagnose compile in parallel during the first day — if you get it working, kill, resume with `--init_from=resume` and `compile=True`. No data wasted.