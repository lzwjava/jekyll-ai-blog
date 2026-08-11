---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu 26.04 下 Fcitx5 双拼设置
translated: true
type: note
---

## 您的系统

- **Ubuntu 26.04 LTS (Resolute Raccoon)**，GNOME 运行在 **Wayland** 上
- 默认安装了 IBus，但没有 `ibus-pinyin`
- 软件源中 **有** Fcitx5 包（版本 5.1.19）
- ⚠️ 注意：在 26.04 上，`fcitx5-configtool` 已不再作为一个独立的包存在——现在它叫 **`fcitx5-config-qt`**（GUI 配置工具仍可通过 `fcitx5-configtool` 启动）

## 安装（选项 1：Fcitx5 + 双拼）

我写了一个脚本存放在 `/tmp/install-fcitx5-shuangpin.sh`。在终端中运行它：

```bash
bash /tmp/install-fcitx5-shuangpin.sh
```

或者手动安装：

```bash
sudo apt update
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-config-qt
im-config -n fcitx5
```

然后 **注销并重新登录**（必须操作——Wayland 会话无法热切换输入框架）。

## 配置双拼

1. 启动 **Fcitx 5 配置**（应用菜单，或运行 `fcitx5-configtool`）
2. **添加输入法 → 汉语 → Pinyin**
3. 选中 Pinyin 条目 → 点击齿轮图标 → **双拼 (Shuangpin)** 选项卡
4. 选择您的方案——**小鹤双拼 (Xiaohe)** 最流行；**微软双拼 (Microsoft)** 和 **自然码 (Ziranma)** 也在列表中
5. 开启 **双拼模式**；可选择保留全拼作为后备

您会看到一个托盘图标；`Ctrl+Space` 切换中英文。在双拼模式下，`xiaoming` → `xm`。

## 针对您系统的注意事项/潜在问题

- **Wayland**：Fcitx5 通过 `text-input-v3` 原生支持。除非某些应用（极少）无法接收输入，否则无需设置 `GTK_IM_MODULE` / `QT_IM_MODULE` 环境变量——仅在遇到问题时才添加。
- **IBus 冲突**：我保留了 ibus 的安装（GNOME 依赖它来处理自身快捷键），但已将其从自动启动中屏蔽。如果出现双重预编辑，`sudo apt remove ibus` 可彻底解决问题。
- **Rime（选项 3）**：可通过 `fcitx5-rime` 包安装——如果您需要带完整自定义词典的小鹤双拼，之后运行 `sudo apt install fcitx5-rime` 即可。

需要查看特定双拼方案布局（小鹤 vs 微软键位映射）？或者希望我在您登录一次后预先配置好 `~/.config/fcitx5/conf/pinyin.conf`？