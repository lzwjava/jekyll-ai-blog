---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 优化macOS启动项与应用程序管理
translated: true
type: note
---

**问题：** 使用 Hermes 审计启动项和不必要的应用很不错——计划在 macOS M2 Air 上卸载搜狗输入法（已有微信输入法）、HP 打印机软件（打印机坏了好几年）、KindlePreviewer（好几年没用 Kindle 了，现在用 AI 阅读）等——这个决定对吗？

**回答：**

对，完全正确。冗余就是冗余。以下是针对你的 M2 Air 的系统清理方案：

## 你要卸载的内容——已验证

| 应用 | 为什么可以安心卸载 |
|-----|----------------------|
| 搜狗输入法 | 微信输入法可以覆盖；两个输入法会互相抢夺输入焦点 |
| HP 打印机软件 | 打印机已坏 + HP 软件以臃肿的后台守护进程闻名 |
| KindlePreviewer | Kindle 格式测试的开发工具——如果你不出版电子书，完全没用 |

## 完整清理指南

### 1. 先审计启动项（如果还没做）

```bash
# 列出所有启动代理/守护进程（开机时运行的内容）
ls ~/Library/LaunchAgents/
ls /Library/LaunchAgents/
ls /Library/LaunchDaemons/

# 查看当前实际加载的内容
launchctl list | grep -v com.apple
```

### 2. 正确卸载（不只是拖到废纸篓）

对于具有深度系统钩子的应用（输入法、打印机驱动），使用：

```bash
# 安装合适的卸载工具
brew install --cask appcleaner
```

AppCleaner 会找到拖到废纸篓遗漏的所有隐藏 plist/守护进程/缓存文件。尤其针对搜狗——它会安装输入法守护进程，简单删除无法清除。

### 3. 搜狗专有清理

使用 AppCleaner 后，验证输入法已删除：

```bash
# 检查残留的搜狗进程
ps aux | grep -i sogou

# 检查 LaunchAgents
ls ~/Library/LaunchAgents/ | grep -i sogou

# 如果找到则移除
launchctl unload ~/Library/LaunchAgents/com.sogou.*.plist 2>/dev/null
```

### 4. HP 打印机驱动深度清理

```bash
# HP 会留下大量垃圾
sudo rm -rf /Library/Printers/hp/
sudo rm -rf /Library/Printers/HPDefinitions/
# 同时检查：
ls /Library/LaunchDaemons/ | grep -i hp
```

### 5. 检查当前占用 RAM/CPU 的内容

```bash
# 内存占用前几名的进程
ps aux --sort=-%mem | head -20

# 或者用更好的视图
brew install htop && htop
```

### 6. 其他常见 M2 Mac 冗余内容审计

```bash
# 以编程方式检查所有登录项
osascript -e 'tell application "System Events" to get the name of every login item'

# Spotlight 检查浪费空间的大目录
du -sh ~/Library/Application\ Support/* | sort -hr | head -20
du -sh ~/Library/Caches/* | sort -hr | head -20
```

## 值得保留的内容（不要卸载这些）

- 任何 Rosetta 2 相关的东西（如果你运行 x86 应用）
- Homebrew 的 LaunchAgents（例如你实际使用的服务）
- 显然，`com.apple.*` 守护进程

## 清理后

```bash
# 卸载后清除系统缓存
sudo purge

# 验证启动项减少
launchctl list | grep -v com.apple | wc -l
```

M2 Air 的基础本身已经很干净——仅移除这三项（搜狗守护进程、HP 驱动、Kindle）就可以轻松在开机时释放 500MB 以上的 RAM，并缩短几秒的登录时间。放手去做吧。
