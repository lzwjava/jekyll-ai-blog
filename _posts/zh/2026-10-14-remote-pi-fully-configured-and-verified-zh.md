---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程Pi已完全配置并验证
translated: true
type: note
---

所有工作已完成并经过端到端验证。🎉

## 选项 1 已完成 — 远程 pi 已完全配置

| 步骤 | 结果 |
|---|---|
| `settings.json` 已复制 | ✅ `openrouter` / `xiaomi/mimo-v2.6-flash`，thinking `high`，theme `dark` |
| `OPENROUTER_API_KEY` → 远程 `~/.bashrc` | ✅ 已追加一次（73 个字符，值从未打印；仅在加密的 SSH 通道内传输） |
| Key 在交互式 shell 中可见 | ✅ `bash -ic` 能看到它 |
| **实时 API smoke test** | ✅ `pi -p "Reply with exactly: PI_REMOTE_OK"` → **`PI_REMOTE_OK`** |

smoke test 在远程以打印模式运行了 pi，使用了你的真实配置，通过 `OPENROUTER_API_KEY` → OpenRouter → `xiaomi/mimo-v2.6-flash` 完成认证，因此整个链路正常工作。

## 最终远程状态

```
~/.pi/agent/
├── settings.json          ← model/theme config (copied from local)
├── bin/pi                 → launcher (auto-adds standalone Node to PATH)
└── install/releases/1.2.0 ← managed install (update with: pi update)

~/.local/bin/pi            ← on PATH via ~/.profile + ~/.bashrc
~/.local/share/pi-node/    ← Node.js v22.23.3 (standalone, no sudo)
~/.bashrc                  ← PATH lines + export OPENROUTER_API_KEY
```

**用法：** `ssh lzw@192.168.1.137` 然后运行 `pi` — 它会以你的默认 model 启动并准备就绪。你可以在会话内使用 `/settings` 或 `/model` 调整任何内容（按 Ctrl+S 保存新的默认值）。