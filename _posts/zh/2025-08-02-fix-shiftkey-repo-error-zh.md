---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复APT GPG签名错误
translated: true
type: note
---

您遇到的这个错误意味着 APT 拒绝从 ShiftKey 仓库更新，因为它无法验证其 GPG 签名。您可以通过以下两种简单方法解决此问题：

---

## 1. **移除或禁用损坏的仓库**

如果您实际上不需要 `https://apt.packages.shiftkey.dev/ubuntu`，直接禁用它即可：

```bash
# 查找定义该仓库的文件（位于 /etc/apt/sources.list.d/ 目录下）
ls /etc/apt/sources.list.d/shiftkey*

# 删除该文件（请替换为实际文件名）
sudo rm /etc/apt/sources.list.d/shiftkey.packages.shiftkey.dev.list

# 然后更新并安装
sudo apt update
sudo apt install pkg-config libssl-dev
```

---

## 2. **导入仓库的签名密钥**

如果您确实需要继续使用 ShiftKey 的软件包，需要获取并安装其公钥：

```bash
# 下载 GPG 密钥并解码后存入 APT 的密钥环
curl -fsSL https://apt.packages.shiftkey.dev/ubuntu/pubkey.gpg \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/shiftkey-archive-keyring.gpg > /dev/null

# 编辑仓库文件使其引用该密钥环
# 用编辑器打开 /etc/apt/sources.list.d/shiftkey*.list，将 deb 行改为：
#   deb [signed-by=/usr/share/keyrings/shiftkey-archive-keyring.gpg] https://apt.packages.shiftkey.dev/ubuntu any main

# 然后更新并安装
sudo apt update
sudo apt install pkg-config libssl-dev
```

---

当 APT 能够无 GPG 错误地更新后，您就可以自由安装 `pkg-config` 和 `libssl-dev`，然后重新构建：

```bash
cargo clean
cargo run
```
