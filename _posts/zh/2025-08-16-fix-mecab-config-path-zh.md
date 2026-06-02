---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复MeCab配置文件路径
translated: true
type: note
---

```
RuntimeError: param.cpp(70) [ifs] no such file or directory: /usr/local/etc/mecabrc
```

这个错误意味着 **MeCab 找不到配置文件** (`mecabrc`)。
在 macOS 上，如果你最近通过 Homebrew 安装了 MeCab，它很可能被安装在 `/opt/homebrew/` 目录下而非 `/usr/local/`，但 Python 绑定仍在寻找旧的 `/usr/local/etc/mecabrc` 路径。

以下是解决方法：

---

### 1. 查找 `mecabrc` 的实际位置

运行：

```bash
brew list mecab
```

或：

```bash
find /opt/homebrew -name mecabrc
```

你可能会看到类似这样的路径：

```
/opt/homebrew/etc/mecabrc
```

---

### 2. 为 MeCab 指定正确的配置文件路径

可以在 Python 代码中指定路径：

```python
import MeCab

t = MeCab.Tagger(f"-r /opt/homebrew/etc/mecabrc -d /opt/homebrew/lib/mecab/dic/ipadic")
print(t.parse("すもももももももものうち"))
```

---

### 3. 或者设置环境变量

```bash
export MECABRC=/opt/homebrew/etc/mecabrc
```

然后正常运行脚本：

```bash
python try_mecab.py
```

---

### 4. 如果需要让 `/usr/local/etc/mecabrc` 生效

可以创建符号链接：

```bash
sudo mkdir -p /usr/local/etc
sudo ln -s /opt/homebrew/etc/mecabrc /usr/local/etc/mecabrc
```

但使用环境变量是更清晰的方法。

---

如果你需要，我也可以提供 **Homebrew 重装 + ipadic 词典配置** 的完整命令，这样就不需要每次都指定 `-r` 参数，你的 `try_mecab.py` 也能保持简洁。
