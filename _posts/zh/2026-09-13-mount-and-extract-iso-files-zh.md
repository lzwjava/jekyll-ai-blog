---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 挂载与提取ISO文件
translated: true
type: note
---

是的，当然可以！有几种方法可以提取或查看ISO文件的内容。

**在Linux/macOS上（使用终端）：**

最常见的方法是**挂载**它：

```bash
# 创建挂载点
mkdir /mnt/iso

# 挂载ISO文件（Linux）
sudo mount -o loop yourfile.iso /mnt/iso

# 然后浏览它
ls /mnt/iso
```

或者使用`7zip`**不挂载直接解压**：

```bash
# 安装7zip
sudo apt install p7zip-full   # Ubuntu/Debian

# 解压
7z x yourfile.iso -o./output_folder
```

**在macOS上：**

```bash
# 直接在Finder中双击.iso文件，或者：
hdiutil mount yourfile.iso
```

**在Windows上：**

- 在文件资源管理器中**双击**ISO文件（Windows 10/11会自动挂载）
- 或者右键单击 → **“挂载”**
- 使用**7-Zip** → 右键单击 → 解压到当前文件夹

**使用Python（用于脚本/自动化）：**

```python
import subprocess

# 挂载（Linux）
subprocess.run(["sudo", "mount", "-o", "loop", "file.iso", "/mnt/iso"])
```

---

**ISO文件内部通常包含的内容：**

| ISO类型 | 内容 |
|---|---|
| 操作系统安装盘（如Ubuntu） | `boot/`, `casper/`, `.vmlinuz`, `initrd` |
| 游戏光盘 | 游戏文件, `autorun.inf` |
| 软件安装程序 | `setup.exe`, 配置文件 |
| 蓝光/DVD | `BDMV/`, `VIDEO_TS/` |

是否需要针对某个特定的ISO文件或使用场景提供帮助？