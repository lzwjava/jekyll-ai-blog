---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Scratch桌面版安装错误分析
translated: true
type: note
---

## 全面回顾：Scratch Desktop 安装

### 需求分析
用户的请求意图明确，但形式混乱 —— 一大段问答内容被直接粘贴为上下文。我准确地提取了实际任务：通过 SSH 连接到 `xiaoxin@192.168.1.47` 并安装 Scratch Desktop。

---

### 问题所在

**1. 缺少前置检查**

在安装任何软件之前，我本应运行：
```bash
ssh xiaoxin@192.168.1.47 "
  flatpak --version
  flatpak remotes --user
  flatpak list | grep -i scratch
  df -h ~
"
```
这原本可以一次性揭示：用户没有添加 flathub 远程仓库、没有已安装的 Scratch 实例，以及可用磁盘空间。

**2. 尝试以非 root 的 SSH 用户身份进行系统级安装**

这注定会失败。当你以普通用户身份 SSH 连接时，`flatpak install`（系统级）需要 root 权限。我本该立即知道应使用 `--user` 选项。

**3. 首次尝试失败导致带宽浪费**

第一次尝试在失败前下载了 7 个组件中的 6 个（约 700MB+）。由于是系统级安装，没有任何内容为用户安装缓存。第二次尝试重新下载了所有内容。这大约 **1.4GB** 的数据传输量，仅为一个约 1GB 的安装。

**4. 对 EOL（生命周期终止）运行时警告提示不足**

安装使用了 `org.freedesktop.Platform 22.08`，该版本已明确终止支持，不再接收安全更新。我仅被动提及了此事。我本应明确指出：*"Flathub 上的 Scratch Desktop 被固定在一个 EOL 运行时上 —— 这是 Flathub 打包问题，你无法在本地修复。如果这是一台共享/儿童使用的机器，这一点值得注意。"*

**5. 缺少安装后验证**

我从未确认应用程序实际能否运行：
```bash
ssh xiaoxin@192.168.1.47 "flatpak run edu.mit.Scratch --version 2>&1 | head -5"
```

**6. 未解决 XDG 路径警告**

安装过程警告 `~/.local/share/flatpak/exports/share` 不在 `XDG_DATA_DIRS` 中，因此应用程序不会出现在应用菜单里。我提到了这一点但没有修复。修复方法是在 `~/.profile` 中添加一行：
```bash
export XDG_DATA_DIRS="$HOME/.local/share/flatpak/exports/share:$XDG_DATA_DIRS"
```

---

### 本该采取的做法

```bash
# 步骤 1：前置检查
ssh xiaoxin@192.168.1.47 "flatpak list | grep -i scratch; flatpak remotes --user"

# 步骤 2：一次性执行正确命令
ssh xiaoxin@192.168.1.47 "
  flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo &&
  flatpak install --user -y flathub edu.mit.Scratch
"

# 步骤 3：修复 XDG 路径
ssh xiaoxin@192.168.1.47 "
  grep -q 'flatpak/exports' ~/.profile || echo 'export XDG_DATA_DIRS=\"\$HOME/.local/share/flatpak/exports/share:\$XDG_DATA_DIRS\"' >> ~/.profile
"

# 步骤 4：验证
ssh xiaoxin@192.168.1.47 "flatpak run edu.mit.Scratch --version 2>&1 | head -3"
```

---

### 总结

| 问题 | 严重性 |
|---|---|
| 缺少前置检查 | 中等 |
| 首次尝试使用错误的安装模式 | 高（导致约 700MB 下载浪费）|
| 未明确指出 EOL 运行时 | 低 |
| 未修复 XDG 路径 | 中等 |
| 缺少安装后验证 | 中等 |

任务最终成功完成，但花费了 3 次尝试和大约两倍于必需的带宽。