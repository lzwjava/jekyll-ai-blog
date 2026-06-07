---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复不可读的黄色文字
translated: true
type: note
---

**问题：** 在 Warp 终端启用浅色模式使用 Hermes 时，黄色文本输出难以阅读。如何修复？

**回答：**

按推荐顺序提供三种方法：

### 1. **禁用 Hermes 颜色输出**（最快捷）

Hermes 很可能支持 `NO_COLOR` 环境变量或有禁用 ANSI 颜色的参数：

```bash
NO_COLOR=1 hermes run

# 或查看 Hermes 帮助中的颜色参数
hermes run --help | grep -i color
```

如果它有配置文件（通常为 `~/.config/hermes/config.json` 或 `~/.hermesrc`），可添加：

```json
{
  "colors": false,
  "no_color": true
}
```

### 2. **覆盖 Warp 浅色模式配色方案**

Warp → 设置 → 主题 → 切换为终端工作专用的深色主题，或创建自定义主题，使黄色具有更高的对比度（更亮/更饱和的黄色）。

或者检查 Hermes 是否支持 `TERM_PROGRAM_VERSION` 或环境颜色覆盖：

```bash
# 强制使用 256 色模式或真彩色
export TERM=xterm-256color
hermes run
```

### 3. **若 Hermes 开源则修改源码**

如果 Hermes 位于 shell 配置文件或本地脚本中，可搜索黄色颜色代码（通常为 `\033[33m` 或 `\033[93m`）并替换：

```bash
# 查找颜色定义
grep -r "33m\|93m" ~/.config/hermes/

# 替换为更易见的颜色（例如深灰、青色）
sed -i 's/\\033\\[33m/\\033[36m/g' <文件>  # 黄色 → 青色
```

**这是什么机器？** 这是 MacBook Air M2 日常使用机。快速修复：在 Hermes 的 shell 别名中切换 `NO_COLOR=1`，或为终端工作将 Warp 切换到深色模式。

**快速测试：**

```bash
NO_COLOR=1 hermes run
# 如果有效，则添加到 ~/.zshrc 或 ~/.bashrc：
alias hermes='NO_COLOR=1 hermes'
```

`hermes --help` 显示了哪些颜色/输出选项？
