---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EDK2构建系统缺失
translated: true
type: note
---

`buildffs.py`脚本执行失败，因为它依赖**EDK2构建系统**，而当前机器未安装。正如[README](https://github.com/xCuri0/ReBarUEFI#build)所述：

> *"将其克隆到[edk2](https://github.com/tianocore/edk2)目录树内后，使用提供的buildffs.py脚本构建DXE驱动。"*

脚本的运行条件如下：

1. **ReBarUEFI必须克隆在EDK2目录树*内部*** —— 例如 `edk2/ReBarUEFI/ReBarDxe/`
2. **需配置EDK2环境** —— 执行 `source edksetup.sh`（设置 `$WORKSPACE`、`$EDK_TOOLS_PATH` 等变量），并编译好 `BaseTools`
3. **安装依赖项** —— `nasm`、`iasl`、`uuid-dev`、`python3-pefile`
4. 然后在 `edk2/ReBarUEFI/ReBarDxe/` 目录下执行：

   ```bash
   source ../edksetup.sh   # 从edk2根目录
   python buildffs.py
   ```

5. 脚本会切换到 `../../`（EDK2根目录）并运行 `build` 命令

**遇到的问题：**

- ❌ `ModuleNotFoundError: No module named 'pefile'` → 已修复（在虚拟环境中安装）
- ❌ `FileNotFoundError: [Errno 2] No such file or directory: 'build'` → `build` 是EDK2的构建工具，需要完整的EDK2环境

**本地构建步骤：**

```bash
# 克隆EDK2
git clone --recursive https://github.com/tianocore/edk2.git
cd edk2

# 在EDK2内部克隆ReBarUEFI
git clone https://github.com/xCuri0/ReBarUEFI.git

# 安装依赖（macOS）
brew install nasm acpica
pip install pefile

# 构建BaseTools
make -C BaseTools

# 加载环境并构建
source edksetup.sh
cd ReBarUEFI/ReBarDxe
python3 buildffs.py
```

**若仅需预编译的 `.ffs` 文件**，可直接从 [Releases页面](https://github.com/xCuri0/ReBarUEFI/releases) 下载 —— 无需本地构建。
