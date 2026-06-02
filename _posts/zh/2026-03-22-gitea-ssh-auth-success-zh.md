---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gitea SSH 认证成功详解
translated: true
type: note
---

问题：这个 Gitea SSH 认证输出是什么意思，它正常吗？

回答：

这是测试 Gitea 实例 SSH 访问时的完全**正常且预期的行为**。以下是每个部分的分解：

---

## 认证成功

```
You've successfully authenticated with the key named lzwjava@gmail.com
```

您的 SSH 密钥已被 Gitea 识别并接受。这意味着您的公钥已在 Gitea 账户设置中正确注册。

---

## “不提供 Shell 访问” — 为什么？

```
but Gitea does not provide shell access.
```

Gitea（类似于 GitHub 和 GitLab）仅将 SSH 用于 **Git 操作**（clone、push、pull），而不用于交互式终端/shell 会话。此消息是故意的 — 它是安全边界。您不应该获得 shell 提示。

---

## 调试行解释

| Line | Meaning |
|------|---------|
| `client_input_channel_req: eow@openssh.com` | 客户端发送“写入结束”信号 — SSH 会话正常拆除 |
| `channel 0: free: client-session` | SSH 会话通道正在干净释放 |
| `Transferred: sent 4840, received 4720 bytes` | 交换少量握手数据 — 测试连接正常 |
| `Bytes per second: sent 36342.9` | 传输速度统计，仅供参考 |

---

## 实际含义

- ✅ 您的 SSH 密钥**配置正确**
- ✅ 通过 SSH 的 Git 操作（`git clone`、`git push`）将**正常工作**
- ✅ 会话干净关闭，无错误
- ❌ 交互式 shell 访问被**有意阻止**（这是设计使然）

---

## 如何测试 Git 访问

您可以使用以下命令验证一切正常：

```bash
ssh -T git@<your-gitea-host>
```

成功的响应与您收到的完全相同。现在，您可以使用 SSH URL 访问仓库：

```bash
git clone git@<your-gitea-host>:lzwjava/your-repo.git
```
