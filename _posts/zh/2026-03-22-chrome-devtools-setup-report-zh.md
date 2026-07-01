---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chrome 开发者工具协议设置报告
translated: true
type: note
---

老板，这是完整的报告。

---

## 🦞 Chrome DevTools Protocol (CDP) 设置报告

**日期：** 2026-03-22 03:36–03:42 GMT+8
**主机：** `to` — Linux 6.8.0-106-generic (x64)
**OpenClaw：** 2026.3.13 (61d171a)

---

### 状态：✅ 已运行

| Component | State |
| --- | --- |
| Browser Profile | `openclaw` (default) |
| Running | **true** |
| Transport | CDP |
| Port | 18800 |
| URL | `http://127.0.0.1:18800` |
| Active Tabs | 1 |
| Snapshot Verified | ✅ (example.com) |

---

### 已完成的操作

**步骤 1 — 尝试 snap Chromium（失败）**

`sudo apt-get install chromium` 安装了 `chromium-browser 146.0.7680.80` — 但在 Ubuntu 上，这是 **snap 包装器**，不是真正的二进制文件。OpenClaw 尝试启动它并遇到：

```
Failed to create SingletonLock: Permission denied (13)
Failed to create a ProcessSingleton for your profile directory. Aborting now to avoid profile corruption.
```

**根本原因：** Snap 的 AppArmor 限制阻止 Chromium 进程写入 `~/.openclaw/browser/openclaw/user-data/`。添加 `noSandbox: true` 无济于事，因为问题是 snap/系统级别，而不是 Chrome 的渲染器沙箱。

**步骤 2 — 使用 Playwright 捆绑的 Chromium（成功）**

Playwright 1.58.2 已全局安装，并已将 Chromium 下载到 `~/.cache/ms-playwright/chromium-1208/`。这个二进制文件 **不是** snap 沙箱化的，并与 CDP 完美兼容。

**步骤 3 — 配置 OpenClaw**

将 `executablePath` 设置为 Playwright Chromium 并启动浏览器。

---

### 添加的配置

文件：`~/.openclaw/openclaw.json`

```json
"browser": {
  "enabled": true,
  "noSandbox": true,
  "headless": true,
  "executablePath": "/home/lzw/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
}
```

---

### 浏览器库存

| Binary | Version | Source | CDP Compatible |
| --- | --- | --- | --- |
| `/usr/bin/chromium-browser` | 146.0.7680.80 | snap | ❌ (AppArmor blocks it) |
| `~/.cache/ms-playwright/.../chrome` | 145.0.7632.6 | Playwright 1.58.2 | ✅ **(active)** |

---

### 活动浏览器配置文件

| Profile | Status | Notes |
| --- | --- | --- |
| `openclaw` | ✅ running (1 tab) | Managed headless, CDP on :18800 |
| `user` | ⬜ stopped | Existing-session mode (requires `--browser-profile user`) |
| `chrome-relay` | ✅ running (0 tabs) | Extension relay on :18792 |

---

### 可用功能

全部已验证并正常工作：

- `openclaw browser navigate <url>` — 页面导航
- `openclaw browser snapshot --compact` — 带元素引用的 DOM 树快照
- `openclaw browser screenshot` — 全页面或元素截图
- `openclaw browser click <ref>` — 通过引用点击元素
- `openclaw browser type <ref> <text>` — 填充表单字段
- `openclaw browser evaluate <fn>` — 在页面上下文中运行 JS
- `openclaw browser console` — 读取控制台日志
- `openclaw browser requests` — 监控网络流量
- `openclaw browser pdf` — 将页面保存为 PDF
- `openclaw browser cookies` — 读写 cookies

---

### ⚠️ 注意事项

1. **Playwright Chromium 版本落后于 snap**（145 vs 146）— 轻微，不影响 CDP 功能
2. **Playwright 更新可能更改二进制路径**（例如 `chromium-1208` → `chromium-1300`）。如果 `npx playwright install` 升级后浏览器损坏，请更新配置中的 `executablePath`
3. **`headless: true`** 表示无可见浏览器窗口 — 所有交互通过 CLI/代理命令进行。如果想看到它，请设置为 `false`（需要显示器）
4. **doctor 输出中的 Telegram 群组策略警告** 与此无关 — 那是关于 Telegram 频道配置，而不是浏览器

---

### 备选方案：安装 Google Chrome Stable

如果您想要一个能经受 Playwright 升级的更永久解决方案：

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y
```

然后将 `executablePath` 设置为 `/usr/bin/google-chrome-stable`。这是 OpenClaw 文档中官方推荐的路径。

---

还有什么其他测试或配置您想让我做吗？
