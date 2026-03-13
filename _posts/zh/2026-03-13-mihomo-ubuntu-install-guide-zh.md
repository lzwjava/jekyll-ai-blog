---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Ubuntu 上安装 Mihomo 指南
translated: true
type: note
---

**问题：** 如何在 Ubuntu 上安装 `mihomo-linux-amd64-v3-alpha-0317d9f.deb`？

**答案：**

这个 `.deb` 文件是一个 Debian 软件包，Ubuntu 原生支持使用 `dpkg` 或 `apt` 安装它。以下是完整的逐步指南：

---

## 步骤 1：确保文件已下载

确保 `.deb` 文件位于当前目录。如果不是，请导航到保存位置：

```bash
cd ~/Downloads
ls mihomo*.deb
```

---

## 步骤 2：安装 `.deb` 软件包

**方法 A — 使用 `dpkg`（直接且简单）：**

```bash
sudo dpkg -i mihomo-linux-amd64-v3-alpha-0317d9f.deb
```

如果此步骤后有缺失依赖，请使用以下命令修复：

```bash
sudo apt --fix-broken install
```

**方法 B — 使用 `apt`（自动处理依赖）：**

```bash
sudo apt install ./mihomo-linux-amd64-v3-alpha-0317d9f.deb
```

> 注意：`./` 前缀是必需的，用于告诉 `apt` 使用本地文件而不是在线仓库搜索。

---

## 步骤 3：验证安装

安装后，检查 mihomo 是否可用：

```bash
mihomo -v
# 或
which mihomo
```

---

## 步骤 4：设置配置目录

Mihomo 需要配置文件才能工作：

```bash
sudo mkdir -p /etc/mihomo
# 将您的 config.yaml 放置在此目录中
sudo nano /etc/mihomo/config.yaml
```

---

## 步骤 5：将 Mihomo 启用并作为系统服务启动

MetaCubeX 的 `.deb` 软件包通常会安装 systemd 服务。使用以下命令启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable mihomo
sudo systemctl start mihomo
```

检查服务状态：

```bash
sudo systemctl status mihomo
```

---

## 关于 `-amd64-v3` 变体的说明

文件名中的 `amd64-v3` 表示此二进制文件针对支持 **x86-64-v3** 指令集的 CPU 进行了优化（例如 Intel Haswell 或更新版本、AMD Ryzen 或更新版本）。如果您的 CPU 较旧且不支持这些指令，二进制文件可能会因 **Illegal instruction** 错误而崩溃。在这种情况下，请下载兼容所有 64 位 x86 CPU 的 `-amd64-v1` 版本。

检查您的 CPU 级别支持：

```bash
/lib64/ld-linux-x86-64.so.2 --help | grep "x86-64-v"
```

如果 `x86-64-v3` 显示为 **(supported)**，则可以使用。

---

**参考资料：**

- [MetaCubeX/mihomo GitHub Releases](https://github.com/MetaCubeX/mihomo/releases)
- [https://deepwiki.com/MetaCubeX/Meta-Docs/2-installation-and-setup](https://deepwiki.com/MetaCubeX/Meta-Docs/2-installation-and-setup)
- [https://reajason.eu.org/writing/ubuntu2004mihomotunmode/](https://reajason.eu.org/writing/ubuntu2004mihomotunmode/)