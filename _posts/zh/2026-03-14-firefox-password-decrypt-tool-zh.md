---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Firefox 保存密码解密工具
translated: true
type: note
---

**问题：** firefox-decrypt 工具是什么，它是如何工作的？

**答案：**

**firefox-decrypt**（最常指 <https://github.com/unode/firefox_decrypt）是一个流行的开源> Python 脚本，旨在从基于 Mozilla 的浏览器/邮件配置文件中提取和解密保存的密码。

它支持：

- Firefox
- Waterfox
- Thunderbird
- SeaMonkey
- 以及各种衍生产品

### 它实际做了什么

Firefox（以及相关应用）将保存的登录信息存储在配置文件文件夹内的文件中：

- `logins.json` — 包含网站列表 + 加密的用户名 + 加密的密码
- `key4.db`（较新版本的 Firefox）或较旧的 `key3.db` — 包含加密密钥

所有密码都使用对称加密（历史上为 3DES-CBC，后续版本转向 AES）。

加密密钥以两种方式受保护：

1. **无主密码** → 密钥以可解密形式存储（仅受 OS 登录/文件权限保护）
2. **设置了主密码** → 密钥本身使用从主密码派生的密钥加密（使用 3DES 或较新版本的 PBKDF2 + AES）

**firefox-decrypt** 读取这些文件并：

- 如果未使用主密码 → 立即显示所有密码
- 如果存在主密码 → 提示输入它，然后解密所有内容

它**不会**执行任何暴力破解、字典攻击或主密码破解 — 你必须知道它。

### 基本用法

```bash
# Clone the repo
git clone https://github.com/unode/firefox_decrypt.git
cd firefox_decrypt

# Run it (Python 3.9+ required in recent versions)
python3 firefox_decrypt.py
```

典型输出流程：

1. 列出检测到的配置文件（如果存在多个）
2. 你选择一个（或它自动选择默认的）
3. 如果设置了主密码 → 提示：`Master Password:`
4. 打印表格，包含：hostname、username、password（有时还有更多字段）

你也可以直接指向配置文件文件夹：

```bash
python3 firefox_decrypt.py /path/to/your/profile
```

### 重要说明（2025–2026 时代）

- 在 Firefox 版本 ~120–130 上运行良好，无重大问题
- Firefox 144+ 据报道在某些情况下引入了 AES-256-CBC 更改 — 原始 firefox-decrypt 可能需要更新或 fork 以实现完美兼容
- 许多人现在使用 **LaZagne**、**HackBrowserData**、**firepwd.py** 或 **browser password dumpers**，这些工具包含 Firefox 支持并更可靠地处理较新格式
- 仅用于合法与合规的取证/恢复用途（自己的机器、授权的事故响应、CTF 挑战等）

### 值得了解的替代方案

- **firepwd.py** (<https://github.com/lclevy/firepwd>) — 纯 Python，无 NSS 依赖，非常适合学习
- **NSS-based tools** — 使用真实的 Mozilla NSS 库（pwdecrypt、modutil 等）
- **LaZagne** — 多浏览器密码提取器（包含 Firefox 模块）
- GUI 工具：PasswordFox (NirSoft)、Browser Password Recovery 工具

简而言之：**firefox-decrypt** 是经典的、轻量级的命令行方式，许多人（渗透测试人员、取证分析师、CTF 玩家、健忘用户）在过去 ~10 年中使用它来读取保存的 Firefox 密码，前提是有配置文件访问权限，并且 — 如需要 — 知道主密码。

**参考：**

- [https://github.com/unode/firefox_decrypt](https://github.com/unode/firefox_decrypt)
- [https://github.com/lclevy/firepwd](https://github.com/lclevy/firepwd)
