---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复NVIDIA MOK密码错误
translated: true
type: note
---

以下是完整的实际情况：

**当前状态：**
- `nvidia-driver-580` 已安装，DKMS 模块已构建 ✓
- Secure Boot **已启用** — 阻止加载未签名模块
- MOK 密钥位于 `/var/lib/shim-signed/mok/MOK.der`，但 **未注册**
- 您已进入 MokManager（蓝屏），输入密码后收到错误提示

---

## 关于密码的说明

当您通过 apt 安装 `nvidia-driver-580` 时，Ubuntu 的 DKMS 会提示您 **创建一个 MOK 注册密码**（不是您的登录密码）。MokManager 询问的正是这个密码。常见的两种失败原因：

1. **您忘记了当时输入的密码** — 这是一次性密码，很容易忘记
2. **键盘布局不匹配** — MokManager 使用美式 QWERTY 布局。如果您设密码时以为是其他布局，那么输入的实际字符就会出错

---

## 选项 A：重新创建 MOK 密钥 + 密码（这样您就知道密码了）

在工作站上执行以下命令：

```bash
sudo mokutil --reset  # 移除旧的注册请求
sudo rm /var/lib/shim-signed/mok/MOK.*
sudo dpkg-reconfigure nvidia-dkms-580
```

系统会提示您输入 **新的 MOK 密码** — 选择一个您记得住的简单密码（例如 `1234`）。然后重启：

```
sudo reboot
```

在蓝色的 MokManager 界面中：
1. **“从磁盘注册 MOK”**
2. 导航到密钥 → **继续**
3. **输入您刚设置的密码**
4. **确认/是**
5. 继续启动 → `nvidia-smi` 即可正常工作

---

## 选项 B：禁用 Secure Boot（更简单，无需密码）

在黑色 POST 画面出现时，按 **F2**（或 Del/F10，具体取决于您的主板）进入 BIOS/UEFI 设置。

然后找到：
- **Security → Secure Boot → Disabled**
- 或 **Boot → Secure Boot → Disabled**
- 或 **Authentication → Secure Boot → Disabled**

保存并退出（通常按 **F10**），正常启动即可。搞定 — 无需密码，无需 MOK，`nvidia-smi` 立即生效。

---

**我的建议：** 选项 B。只需改一个设置，重启一次，无需记住任何密码。除非您出于安全合规的需求必须启用 Secure Boot，否则对于开发工作站来说，开启它并没有实际好处。

您想怎么做 — A（重新创建 MOK）还是 B（禁用 Secure Boot）？如果是 B，我无法远程操作 BIOS 菜单 — 您需要在启动时按 F2 并找到该设置。但如果遇到困难，请告诉我您的主板型号，我可以帮您查找具体的菜单路径。