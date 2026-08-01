---
audio: false
generated: true
image: false
lang: en
layout: post
title: UV_CACHE_DIR Cache Mechanics Explained
translated: false
type: note
---

Question: How does `UV_CACHE_DIR` work in `uv pip install`?

Answer:

`UV_CACHE_DIR` tells **uv** where to store its cache files instead of using the default cache location.

`uv` is Astral's fast Python package manager. It aggressively caches:

* downloaded wheels (`*.whl`)
* source distributions (`*.tar.gz`)
* built wheels
* metadata
* git dependencies
* Python installations (depending on usage)

Normally:

Linux:

```bash
~/.cache/uv
```

macOS:

```bash
~/Library/Caches/uv
```

Windows:

```text
%LOCALAPPDATA%\uv\cache
```

When you run:

```bash
export UV_CACHE_DIR=/mnt/data/uv-cache

uv pip install --python /usr/bin/python3.12 --break-system-packages -e .
```

you are saying:

```
uv
 |
 +-- use /mnt/data/uv-cache
       |
       +-- downloaded packages
       +-- wheels
       +-- build artifacts
       +-- metadata
```

instead of:

```
~/.cache/uv
```

---

## Why use it?

Common cases:

### 1. Docker / ephemeral machines

Example:

```bash
export UV_CACHE_DIR=/tmp/uv-cache
uv pip install torch
```

The cache can be reused during the container lifetime.

---

### 2. GPU cloud machines

Your command looks like a GPU cloud / `/mnt/data` environment.

Many GPU providers have:

```
/
├── home
│   └── user
│       └── .cache
└── mnt
    └── data
        └── persistent disk
```

`/mnt/data` often survives reboot or snapshot.

So:

```bash
export UV_CACHE_DIR=/mnt/data/uv-cache
```

means:

"keep my Python package cache on persistent storage."

Next time:

```bash
uv pip install torch
```

does not need to download hundreds of MB/GB again.

---

## How cache hit works

First install:

```bash
uv pip install transformers
```

Flow:

```
PyPI
 |
 | download
 v
/mnt/data/uv-cache
 |
 | install
 v
python environment
```

Second install:

```
uv
 |
 | check cache
 |
 +---- package exists
        |
        v
    install immediately
```

Example:

First:

```
Downloading torch-2.7.1-cp312.whl
  800 MB
```

Second:

```
Resolved 50 packages
Installed in 5s
```

because the wheel is already cached.

---

## Difference between cache and installed packages

Important:

`UV_CACHE_DIR` is **not** where packages are installed.

Your command:

```bash
uv pip install --python /usr/bin/python3.12 -e .
```

installs into:

```
/usr/lib/python3.12/site-packages
```

or your active environment.

Cache:

```
/mnt/data/uv-cache
```

is only a download/build store.

Think:

```
cache                  environment
-----                  -----------
/mnt/data/uv-cache --> /usr/lib/python3.12/site-packages
```

Deleting cache:

```bash
rm -rf /mnt/data/uv-cache
```

does NOT uninstall packages.

---

## Useful commands

See cache size:

```bash
du -sh /mnt/data/uv-cache
```

Clean cache:

```bash
uv cache clean
```

Show cache location:

```bash
uv cache dir
```

Example:

```bash
$ UV_CACHE_DIR=/mnt/data/uv-cache uv cache dir

/mnt/data/uv-cache
```

---

For LLM development (`sglang`, `vllm`, `torch`, CUDA wheels), using a persistent `UV_CACHE_DIR` is especially useful because a single environment can easily download **10–30GB** of wheels.