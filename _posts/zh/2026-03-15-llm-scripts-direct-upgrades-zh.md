---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM 脚本优于直接升级
translated: true
type: note
---

**Question: 让 LLM 帮助编写 Ubuntu 版本升级脚本是否比让 LLM 直接执行 `do-release-upgrade` 过程更好？**

**Answer:**

是的——你的直觉完全正确。下面是对 **为什么 `do-release-upgrade` 不适合直接由 LLM 执行** 的详细分解，以及 **LLM 在此工作流程中真正闪光的地方**。

---

## 为什么 `do-release-upgrade` 不适合 LLM “直接执行”

`do-release-upgrade` 不是单个命令——它是一个 **复杂、有状态的交互式编排过程**。以下是它实际涉及的内容：

### 1. 在不可预测点出现的交互提示

在升级过程中，该工具会呈现差异并询问如何处理已修改的配置文件——例如，是保留你的 `/etc/ssh/sshd_config` 版本还是安装包维护者的版本。这些提示无法在不知道系统状态的情况下完全预测或提前自动化。

### 2. 需要监控的多阶段过程

版本升级是一个交互式过程，有时会停止并询问问题，因此你应该监控升级过程并随时准备响应。LLM 无法可靠地“持续存在”于可能持续 30–60+ 分钟的过程。

### 3. 动态依赖解析

运行命令时，它会检查是否有新版本可用、引导你完成升级、解析包依赖并移除过时或冲突的软件。这种解析是特定于环境的，无法通用预测。

### 4. 第三方 PPA 处理

第三方软件仓库和 PPA 在版本升级期间会被禁用。虽然从这些来源安装的软件不会被移除，但它们是最常见的升级问题原因。处理这些需要特定系统的知识。

### 5. 远程升级的 SSH 备份端口

如果你将 SSH 更改为非默认端口，`do-release-upgrade` 会在端口 1022 上打开第二个 SSH 服务器，作为主 SSH 服务在升级期间重启时的备份。这种运行时副作用很难让 LLM 实时管理。

### 6. 故障恢复

如果 apt 处于不良状态，你需要在重试升级前运行 `sudo dpkg --configure -a`，然后运行 `sudo apt --fix-broken install`。故障模式多种多样且特定于系统。

---

## LLM 真正有帮助的地方：脚本编写

LLM 擅长 **生成结构良好、可重复、带文档的脚本**，人类（或 CI/CD 管道）可以审查并运行。以下是 LLM 可以可靠帮助的内容：

### 升级前准备脚本
```bash
#!/bin/bash
# Pre-upgrade checklist script (LLM-generated)
set -e

echo "=== Step 1: Update current packages ==="
sudo apt update && sudo apt dist-upgrade -y

echo "=== Step 2: Check if reboot is required ==="
if [ -f /run/reboot-required ]; then
  echo "Reboot required before upgrade. Please reboot and re-run."
  exit 1
fi

echo "=== Step 3: Check disk space ==="
df -h /

echo "=== Step 4: Install upgrade manager ==="
sudo apt install -y update-manager-core

echo "=== Step 5: Backup sources.list ==="
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

echo "=== Ready for: sudo do-release-upgrade ==="
```

### 升级后清理脚本
```bash
#!/bin/bash
# Post-upgrade cleanup (LLM-generated)

echo "=== Remove obsolete packages ==="
sudo apt autoremove -y

echo "=== Re-enable PPAs (review list manually) ==="
ls /etc/apt/sources.list.d/

echo "=== Verify new release ==="
lsb_release -a

echo "=== Remove SSH backup rule if added ==="
sudo ufw delete allow 1022/tcp 2>/dev/null || true
```

---

## 正确的思维模型

| 任务 | LLM 角色 |
|---|---|
| 理解 `do-release-upgrade` 的作用 | ✅ 彻底解释 |
| 编写升级前/后 shell 脚本 | ✅ 非常适合 |
| 生成检查列表和运行手册 | ✅ 非常适合 |
| 回答配置文件冲突问题 | ✅ 提供上下文时 |
| 实际实时运行 `do-release-upgrade` | ❌ 不可靠——交互式、有状态、长时间运行 |
| 自主处理升级中故障 | ❌ 过于特定于环境 |

---

## 总结

`do-release-upgrade` 是 Canonical 构建的 **经过实战检验的编排工具**，融入了多年边缘案例处理。当你的系统有大量第三方自定义、异常包选择或自定义编译软件时，它的可预测性会降低——在这些情况下，需要对每个步骤进行更多手动审查。在此的最佳 LLM 使用方式是作为 **脚本作者、检查列表生成器和顾问**——而不是实时操作员。你运行脚本；LLM 帮助你写好它们。

**References:**

- [Ubuntu Server Upgrade Documentation](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/)
- [How to Upgrade Ubuntu Server Using do-release-upgrade](https://oneuptime.com/blog/post/2026-03-02-upgrade-ubuntu-server-do-release-upgrade/view)
- [Understanding the do-release-upgrade Command](https://knowledge.buka.sh/understanding-the-do-release-upgrade-command-in-ubuntu-a-beginners-guide/)