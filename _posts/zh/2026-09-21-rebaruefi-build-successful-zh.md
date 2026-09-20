---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ReBarUEFI 构建成功
translated: true
type: note
---

完成。`python3 buildffs.py` 现在可以正常工作，并生成了 `.ffs` 文件。

## 结果

```
Build/ReBarUEFI/RELEASE_GCC/X64/ReBarDxe.ffs   (12,338 字节)
Build/ReBarUEFI/RELEASE_GCC/X64/ReBarDxe.efi   (12,288 字节)
```

FFS 头部包含预期的 GUID（`a8ee1777-...`），并且 PE 上设置了 NX_COMPAT 标志（`DllCharacteristics=0x0100`）。

## 我的修复/操作

1. **安装依赖**（nasm、通过 acpica-tools 安装的 iasl、系统 Python 的 pefile）：
   ```bash
   sudo apt-get install -y nasm acpica-tools python3-pefile
   ```
   （`uuid-dev` 已经存在。）

2. **使用系统 Python 3.12 构建 BaseTools**（不使用 Homebrew 的 3.14，因为它在 `PATH` 中排在首位且缺少 `pefile`）：
   ```bash
   cd /home/lzw/projects/edk2
   export PYTHON_COMMAND=/usr/bin/python3
   make -C BaseTools
   ```

3. **生成 Conf 文件并进行配置**：
   ```bash
   source edksetup.sh --reconfig
   ```
   然后编辑 `Conf/target.txt`：
   - `ACTIVE_PLATFORM = ReBarUEFI/ReBarDxe/ReBar.dsc`
   - `TARGET = RELEASE`
   - `TARGET_ARCH = X64`
   - `TOOL_CHAIN_TAG = GCC`  ← **重要**：此 EDK2 树移除了 `GCC5`（`tools_def.txt` v3.06 移除了 GCC48/GCC49/GCC5），因此原来的 `GCC5` 会导致“Tool chain [GCC5] is not defined”错误。

4. **运行构建**：
   ```bash
   cd /home/lzw/projects/edk2
   export PYTHON_COMMAND=/usr/bin/python3
   source edksetup.sh >/dev/null
   cd ReBarUEFI/ReBarDxe
   /usr/bin/python3 buildffs.py
   ```

日志中看似吓人的一行——`cp: cannot stat '.../*.pdb': No such file or directory`——是无害的，并且被构建明确忽略（`Error 1 (ignored)`）；PDB 文件在 GCC 构建中根本就不存在。

## 后续重现构建的一行命令

```bash
cd /home/lzw/projects/edk2 && export PYTHON_COMMAND=/usr/bin/python3 && source edksetup.sh >/dev/null && cd ReBarUEFI/ReBarDxe && /usr/bin/python3 buildffs.py
```