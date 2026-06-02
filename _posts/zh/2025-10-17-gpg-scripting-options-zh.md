---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GPG脚本命令选项
translated: true
type: note
---

### GPG 命令选项解析

`--batch`、`--yes`、`-o` 和 `--pinentry-mode` 是 `gpg`（GNU 隐私卫士）命令中用于非交互式或脚本化操作的常用标志，例如加密、解密或签名场景。以下是各选项的详细说明：

- **`--batch`**：启用批处理模式，阻止 `gpg` 提出任何交互式问题或允许交互命令。这在无法进行用户输入的脚本或自动化场景中非常实用。可通过 `--no-batch` 禁用此模式。

- **`--yes`**：自动对多数确认提示（如文件覆盖）应答“是”。这能避免因是/否类问题导致执行中断。

- **`-o`（或 `--output`）**：指定操作输出的目标文件。后接文件名参数，例如 `-o output.txt`。若未指定，输出可能默认指向标准输出流或其他默认位置。

- **`--pinentry-mode`**：控制 GPG 代理处理 PIN 码输入（口令提示）的方式。可选模式包括 `ask`（默认：弹出图形或控制台提示）、`loopback`（允许通过标准输入传递口令，适用于无弹窗的脚本场景）、`cancel`（取消需要 PIN 码的操作）或 `error`（返回错误而非提示）。在批处理脚本中常配合 `loopback` 模式实现安全的非交互式口令输入。

这些选项常组合运用于脚本场景，例如 `gpg --batch --yes -o decrypted.txt --pinentry-mode loopback --decrypt encrypted.gpg` 可实现全自动化运行。

#### 参考文档
- [GPG 手册页](https://linux.die.net/man/1/gpg)
- [GnuPG 代理选项](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html)
- [GnuPG 官方手册](https://www.gnupg.org/documentation/manuals/gnupg/index.html)
