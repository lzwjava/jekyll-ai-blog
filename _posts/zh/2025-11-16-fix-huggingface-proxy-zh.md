---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 修复HuggingFace下载代理设置
translated: true
type: note
---

是的——它**可以**使用你的代理，但从你粘贴的输出来看，**你的代理目前并未被使用**。
这就是为什么下载速度会卡在**17.6字节/秒**——这是直连HuggingFace的典型症状。

让我告诉你**如何确认**以及**如何修复**这个问题。

---

# 1. 为什么当前运行*没有*使用代理

这一行：

```
78.0/630M [00:16<9947:51:33, 17.6B/s]
```

很能说明问题：如果通过`HTTP_PROXY`/`HTTPS_PROXY`设置了正确的代理（Clash、V2Ray、Shadowsocks），你应该看到类似如下的速度：

* 几百KB/秒
* 或几MB/秒
* 而不是约17字节/秒

所以Python进程没有获取到任何代理环境变量。

---

# 2. 检查代理环境变量是否存在

在你运行以下命令的**同一个终端**中：

```
python data/openwebtext_10k/prepare.py
```

运行：

```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

如果没有任何输出 → 说明这些变量未设置，因此HuggingFace无法使用它们。

---

# 3. 修复：为该终端会话设置代理

以运行在7890端口的Clash为例：

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

如果你使用SOCKS5（例如Shadowsocks）：

```bash
export HTTP_PROXY="socks5://127.0.0.1:1080"
export HTTPS_PROXY="socks5://127.0.0.1:1080"
```

**然后再次运行：**

```bash
python data/openwebtext_10k/prepare.py
```

现在你的速度应该会大幅提升。

---

# 4. 在Python内部进行额外检查

在`prepare.py`的开头添加这几行代码进行测试：

```python
import os
print("HTTP_PROXY:", os.getenv("HTTP_PROXY"))
print("HTTPS_PROXY:", os.getenv("HTTPS_PROXY"))
```

如果它们输出`None` → 你的shell没有传递这些变量 → 修复你的环境变量设置。

---

# 5. 可选：在加载数据集前用`requests`验证

运行：

```python
import requests
print(requests.get("https://api.ipify.org?format=json", timeout=5).text)
```

* 如果返回的IP来自你的VPN/代理 → 正常。
* 如果它是你的家庭ISP IP → 代理未被使用。

---

# 6. 重要细节：HuggingFace使用**HTTP**，而非SOCKS**，除非你安装了pysocks

如果你的代理是SOCKS5，某些Python安装可能无法直接使用，除非安装了`PySocks`：

```bash
pip install pysocks
```

之后SOCKS代理就能正常工作了。

---

# 7. 总结

✔ HuggingFace*会*使用代理
✔ 但前提是环境变量已设置
✘ 你的日志显示代理并未激活
✔ 解决方案：在同一个shell中设置代理环境变量

---

如果你需要，我可以：

* 调整你的shell配置（`.bashrc`或`.zshrc`）以始终使用代理
* 制作一个“代理开启”/“代理关闭”脚本
* 修改你的NanoGPT `prepare.py`以在Python内部强制使用代理

告诉我你倾向于哪种方案。
