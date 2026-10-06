---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restart Build with More Parallel Jobs
translated: false
type: note
---

Yes, absolutely — you're already using 2 parallel jobs (`-j 2`), and the machine can do more:

**Host specs:**
- **4 CPU cores**
- **7.7 GB RAM** (~6.0 GB available)

**Recommendation: `-j 4`** (one job per core), though `-j 3` is the safe choice if you hit memory pressure. Each `nvcc` instance on heavy mmq templates can eat 1–2 GB, and with 6 GB available, 4 jobs is workable but 3 leaves more headroom.

**Good news:** the build is incremental — the ~128 `.o` files already compiled will be kept. If you kill the current build and restart with higher parallelism, only the 1–2 in-flight nvcc compilations get thrown away.

Would you like me to:
1. **Kill the current build** (PID 9650/9651) and restart with `cmake --build build -j 4`?
2. Or leave the current one alone (it's ~68% through the CUDA stage anyway, so restarting mainly helps for the remaining ~61 template instances + the CPU-side binaries)?

If you want to restart, the command would be:

```bash
ssh lzw@192.168.1.137 '
cd ~/projects/llama.cpp
kill 9651 9650 2>/dev/null  # stop current build
sleep 2
cmake --build build -j 4 2>&1 | tail -50
echo "=== BUILD EXIT DONE ==="
ls -la build/bin/ 2>/dev/null
'
```

Shall I run it? (Say the word and I'll kill + relaunch with `-j 4`.)
