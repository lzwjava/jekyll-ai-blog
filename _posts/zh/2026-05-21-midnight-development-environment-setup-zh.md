---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 午夜开发环境设置
translated: true
type: note
---

以下是你这台 Linux Mint 22.3 机器在过去约 2 小时（午夜到凌晨 1 点）内的完整活动记录：

---

## 已安装的软件

**Ghostty 1.3.1** — 终端模拟器，通过 apt 从 `ppa:mkasberg/ghostty-ubuntu` 安装。GPU 加速的 GTK4 终端，内置 350+ 主题。后续通过 apt 自动更新。

**VS Code 1.121.0** — 添加了微软官方 apt 仓库，通过 apt 安装。占用约 726 MB 磁盘空间。已预装 54 个扩展，包括完整的 Python、Java、C/C++、Rust、Go、Kotlin、PHP 支持，以及 Raspberry Pi Pico / 嵌入式 MCU 工具链。

**GitHub Desktop 3.4.13-linux1** — 通过 `dpkg -i` 从 shiftkey 分支的 `.deb` 包安装。这是事实上 Linux 上的 GitHub Desktop 移植版，因为官方没有推出 Linux 版本。二进制文件位于 `/usr/bin/github-desktop`。

---

## 系统配置

**Caps Lock ↔ 左 Ctrl 互换** — 从损坏的 `~/.Xmodmap`（基于 keysym，不起作用）清理后，改用基于 keycode 的规则重写。添加了 `~/.xprofile` 作为后备方案，包含 `setxkbmap -option ctrl:swapcaps`。两种方法现已一致。

**Hermes YOLO 模式** — 在 `~/.hermes/config.yaml` 中设置 `approvals.mode: off`，这样每次执行命令时就不会提示确认。

---

## Hermes / LLM 修复（在你的 `ww` 项目中）

**推理模型 token 限制** — DeepSeek v4 Flash 是推理模型，`max_tokens=60` 太小（推理过程消耗了全部预算）。已提升至 300，修改位置：

- `ww/note/create_note_utils.py`
- `ww/note/screenshot_log.py`

**增强 LLM 错误诊断** — 在 `ww/llm/openrouter_client.py` 中添加了代理连通性检查以及更丰富的错误信息，这样空内容响应和非 200 错误会包含模型名称、max_tokens、finish_reason 和代理状态。

---

## 杂项

- 阅读了王垠的一篇微博文章，比较了 MITM 攻击与组织功能失调——已保存为笔记。
- `.gitignore` 清理：经历过一些反复回退，但最终保留了原始规则加上 `.env`。

---

### 当前要紧事项

1. **测试 `ww note`** —— token 限制修复后应该能正常工作。试试看。
2. **Ghostty 配置** —— 终端已安装但还没有配置文件。配置文件位于 `~/.config/ghostty/config`，可以设置主题、字体或透明度。
3. **GitHub Desktop** —— 运行 `github-desktop` 启动一次，通过 OAuth 登录，克隆一个仓库以验证密钥链集成是否正常。
4. **VS Code 扩展** —— 预装了 54 个扩展，你可能想审核一下哪些真正有用、哪些是冗余，特别是如果有重复或过时的。

需要我帮你处理以上任何一项，或者设置其他内容吗？
