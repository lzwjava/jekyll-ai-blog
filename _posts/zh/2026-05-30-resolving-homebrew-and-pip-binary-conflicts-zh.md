---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决Homebrew与pip二进制冲突
translated: true
type: note
---

就是这样。你已经通过 `pip` 安装了 `huggingface-hub` 0.29.3，它已经占用了 `/opt/homebrew/bin/hf` 和 `/opt/homebrew/bin/tiny-agents`。Homebrew 的 `hf` 公式提供了相同的二进制文件。

有两种方案：

**方案 1 — 干净修复：** 卸载 pip 包，然后重新链接：

```sh
pip uninstall huggingface-hub
brew link hf
```

**方案 2 — 强制覆盖：** 直接用 Homebrew 覆盖 pip 脚本：

```sh
brew link --overwrite hf
```

方案 2 虽然能解决问题，但 pip 包仍然保留——你会有两份 `huggingface-hub`（一份来自 pip，一份来自 brew），这会给维护带来麻烦。方案 1 更干净。

需要我检查一下 `hf` 公式是否应在它的 formula 文件中声明与 pip 包的冲突吗？
