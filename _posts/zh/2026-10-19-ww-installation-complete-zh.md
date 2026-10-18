---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WW安装完成
translated: true
type: note
---

已完成。以下是所安装的内容：

1. **uv** — 安装至 `~/.local/bin`（已通过 `.bashrc` 加入你的 `PATH`）
2. **Python 3.13** — 通过 uv 下载，因为系统 Python 3.14 与 `torch` 不兼容
3. **venv + 所有 230 个依赖** — 同步至 `.venv/`（包含 torch、transformers、playwright 等）
4. **全局 `ww` 命令** — 将 `~/.local/bin/ww` 符号链接至 `.venv/bin/ww`
5. **Zsh 补全** — 复制到 `~/.zsh/completions/_ww`

**验证其是否有效：**

```bash
ww
ww weather
```

**注意：**

- 你的 `.env` 文件已存在，并配置了 `OPENROUTER_API_KEY` 和 `MODEL`。
- 如果你使用 **zsh**，请运行 `autoload -Uz compinit && compinit` 以重新加载补全。
- 使用 `ww <group> <subcmd>` 从任意位置运行命令，或者使用 `uv run ww <cmd>`（如果你更倾向于不使用符号链接）。
- 某些模块（例如 `ww screenshot`、`ww macos`）仅适用于 macOS，在 Linux 上会失败。
