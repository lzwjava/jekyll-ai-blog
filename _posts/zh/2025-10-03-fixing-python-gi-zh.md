---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 修复损坏的Python GI绑定
translated: true
type: note
---

### 更新后的诊断
根据最新信息，您安装的 Python 3.13.7（可能是手动安装或通过 PPA/源码安装）破坏了系统的 GObject Introspection (GI) 绑定。`gi` 模块的 `_gi` C 扩展是针对系统默认 Python（很可能是 3.10 或 3.11，根据 `/usr/lib/python` 中的目录判断）编译的，而不是 3.13。当 `gnome-terminal`（一个 Python 脚本）尝试加载时，就会引发循环导入错误。`/usr/lib/python` 中的多版本设置证实了这种不匹配——像 `python3-gi` 这样的系统软件包尚未针对 3.13 构建（截至 2025 年，对大多数发行版来说这个版本太新了）。

UFW 日志仍然是无关的干扰信息。

### 推荐修复方案：恢复系统默认 Python
最干净的解决方案是将 `/usr/bin/python3` 切换回发行版默认版本（例如 3.10），然后重新安装 GI 绑定。这可以避免复制 .so 文件等可能引发不一致性的临时方案。

1. **识别并切换到默认 Python 版本**（如果配置了 `update-alternatives` 则使用该工具，否则手动创建符号链接）：
   ```
   # 检查是否配置了 alternatives
   sudo update-alternatives --config python3
   ```
   - 如果列出选项，请选择优先级最低的选项（通常是发行版默认版本，如 3.10）。
   - 如果没有配置 alternatives（原生 Ubuntu 常见情况），手动恢复：
     ```
     # 假设默认版本为 3.10（Ubuntu 22.04 常见情况；如果基础版本是 3.11 请相应调整）
     sudo rm /usr/bin/python3
     sudo ln -s /usr/bin/python3.10 /usr/bin/python3
     ```
   - 验证：`python3 --version` 现在应显示 3.10.x（或您的默认版本）。

2. **重新安装 GI 和 GNOME Terminal 软件包**：
   ```
   sudo apt update
   sudo apt install --reinstall python3-gi gir1.2-glib-2.0 gnome-terminal
   ```

3. **测试**：
   ```
   python3 -c "from gi.repository import GLib, Gio; print('GI OK')"
   gnome-terminal
   ```
   - 如果 Python 测试通过但终端仍无法启动，重置其配置：`dconf reset -f /org/gnome/terminal/`。

### 如需保留 Python 3.13
- 这种方法更复杂，因为官方尚未提供针对 3.13 的 `python3-gi`。您需要从源码编译 PyGObject：
  1. 安装构建依赖：`sudo apt install libgirepository1.0-dev libcairo2-dev pkg-config python3.13-dev`。
  2. 下载并构建 PyGObject：按照[官方指南](https://pygobject.gnome.org/install.html)操作，使用 `--prefix=/usr/local` 参数。
  3. 但此举可能破坏其他系统工具——如果出现问题请恢复原状。
- 或者，临时复制 `_gi` 扩展（不推荐长期使用）：
  ```
  cd /usr/lib/python3/dist-packages/gi/
  sudo cp _gi.cpython-3[01]m*.so _gi.cpython-313m-x86_64-linux-gnu.so  # 将 '3[01]' 调整为您的默认版本（3.10 或 3.11）
  ```
  然后按上述方法重新安装 `python3-gi`。

### 预防措施
- 不要手动覆盖 `/usr/bin/python3`——对于需要 3.13 的项目请使用虚拟环境（`python3 -m venv myenv`）。
- 如果通过 deadsnakes PPA 安装了 3.13，请移除该 PPA 并坚持使用发行版 Python。

如果问题仍未解决，请运行 `ls -l /usr/bin/python*` 和 `dpkg -l | grep python3 | grep -E 'gi|default'` 并分享输出结果。

[尝试安装新版 Python 3 后 gnome-terminal 无法启动](https://askubuntu.com/questions/880188/gnome-terminal-will-not-start-after-trying-to-install-newer-version-of-python-3)
[ImportError: cannot import name '_gi' from partially initialized module 'gi'](https://stackoverflow.com/questions/59838238/importerror-cannot-import-name-gi-from-partially-initialized-module-gi-mo)
[为什么终端无法打开？](https://www.reddit.com/r/Ubuntu/comments/1f9qh0a/why_wont_terminal_open/)
