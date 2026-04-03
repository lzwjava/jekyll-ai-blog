---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在macOS上安装和使用mtr
translated: true
type: note
---

**提问：** macOS是否有`mtr`工具，如何安装和使用它？

**回答：**

## macOS上的`mtr`

`mtr` **不**随macOS预装，也无法在Apple App Store中获取。然而，它完全受支持且可以通过**Homebrew**轻松安装。

---

### 第一步 — 安装Homebrew（如果尚未安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### 第二步 — 安装`mtr`

运行以下命令通过Homebrew安装`mtr`：

```bash
brew install mtr
```

---

### 第三步 — 运行`mtr`

安装后，你可能需要使用`sudo`运行`mtr`，因为它需要原始socket访问权限，这在默认情况下仅限于root用户。

**交互（实时）模式：**
```bash
sudo mtr api.binance.com
```

**报告模式（等效于你在Linux中的命令 — 100个循环）：**
```bash
sudo mtr api.binance.com --report -c 100
```

**示例输出：**
```
HOST: mba                         Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 192.168.1.1               0.0%   100    0.7   0.9   0.4   7.9   1.0
  2.|-- 10.0.0.1                  0.0%   100    1.2   1.5   0.8  15.0   2.1
  ...
```

---

### 为什么在macOS上需要`sudo`

macOS将原始ICMP socket访问权限限制为root用户。与Linux有时可以设置setuid权限不同，在macOS上你几乎总是需要使用`sudo mtr`而非仅`mtr`。

---

### 汇总表格

| 平台           | 安装命令                     | 运行命令                                |
|----------------|------------------------------|----------------------------------------|
| Ubuntu/Debian  | `sudo apt install mtr`       | `mtr api.binance.com --report -c 100`  |
| Amazon Linux   | `sudo yum install mtr`       | `mtr api.binance.com --report -c 100`  |
| **macOS**      | `brew install mtr`           | `sudo mtr api.binance.com --report -c 100` |

---

### 替代方案：MacPorts

如果你使用MacPorts而非Homebrew，`mtr`同样在MacPorts中作为port提供。

```bash
sudo port install mtr
```

**参考资料：**

- [如何在Windows、Mac OS和Linux中执行MTR – ChemiCloud](https://chemicloud.com/kb/article/how-to-perform-a-mtr-in-windows-mac-os-and-linux/)
- [mtr — Homebrew Formulae](https://formulae.brew.sh/formula/mtr)
- [mtr on MacPorts](https://ports.macports.org/port/mtr/)