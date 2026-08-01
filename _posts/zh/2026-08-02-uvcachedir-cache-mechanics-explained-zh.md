---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UV_CACHE_DIR 缓存机制详解
translated: true
type: note
---

问题: `UV_CACHE_DIR` 在 `uv pip install` 中如何工作?

答案:

`UV_CACHE_DIR` 告诉 **uv** 将缓存文件存储到何处, 而不是使用默认的缓存位置.

`uv` 是 Astral 的快速 Python 包管理器. 它会积极缓存:

* downloaded wheels (`*.whl`)
* source distributions (`*.tar.gz`)
* built wheels
* metadata
* git dependencies
* Python installations (depending on usage)

通常:

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

当你运行:

```bash
export UV_CACHE_DIR=/mnt/data/uv-cache

uv pip install --python /usr/bin/python3.12 --break-system-packages -e .
```

你的意思是:

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

而不是:

```
~/.cache/uv
```

---

## 为什么使用它?

常见情况:

### 1. Docker / 临时机器

示例:

```bash
export UV_CACHE_DIR=/tmp/uv-cache
uv pip install torch
```

缓存可以在容器生命周期内重复使用.

---

### 2. GPU 云机器

你的命令看起来像是在 GPU 云 / `/mnt/data` 环境中.

许多 GPU 提供商拥有:

```
/
├── home
│   └── user
│       └── .cache
└── mnt
    └── data
        └── persistent disk
```

`/mnt/data` 通常会在重启或快照后保留.

所以:

```bash
export UV_CACHE_DIR=/mnt/data/uv-cache
```

意思是:

"将我的 Python 包缓存保留在持久化存储上."

下次:

```bash
uv pip install torch
```

无需再次下载数百 MB/GB.

---

## 缓存命中如何工作

首次安装:

```bash
uv pip install transformers
```

流程:

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

第二次安装:

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

示例:

首次:

```
Downloading torch-2.7.1-cp312.whl
  800 MB
```

第二次:

```
Resolved 50 packages
Installed in 5s
```

因为 wheel 已被缓存.

---

## 缓存与已安装包的区别

重要:

`UV_CACHE_DIR` **不是**包安装的位置.

你的命令:

```bash
uv pip install --python /usr/bin/python3.12 -e .
```

安装到:

```
/usr/lib/python3.12/site-packages
```

或者你的激活环境.

缓存:

```
/mnt/data/uv-cache
```

仅仅是一个下载/构建存储.

可以这样理解:

```
cache                  environment
-----                  -----------
/mnt/data/uv-cache --> /usr/lib/python3.12/site-packages
```

删除缓存:

```bash
rm -rf /mnt/data/uv-cache
```

**不会**卸载包.

---

## 有用命令

查看缓存大小:

```bash
du -sh /mnt/data/uv-cache
```

清理缓存:

```bash
uv cache clean
```

显示缓存位置:

```bash
uv cache dir
```

示例:

```bash
$ UV_CACHE_DIR=/mnt/data/uv-cache uv cache dir

/mnt/data/uv-cache
```

---

对于 LLM 开发 (`sglang`, `vllm`, `torch`, CUDA wheels), 使用持久化的 `UV_CACHE_DIR` 特别有用, 因为单个环境很容易下载 **10-30GB** 的 wheels.