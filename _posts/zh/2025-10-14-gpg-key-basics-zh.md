---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: GPG密钥管理基础
translated: true
type: note
---

## GPG 密钥管理简介

GPG（GNU Privacy Guard）是 OpenPGP 标准的免费实现，用于安全通信，可对数据进行加密、签名和验证。其核心是**公钥密码学**，每个用户都拥有**公钥**（公开共享用于加密和验证）和**私钥**（秘密保存用于解密和签名）。密钥管理涉及创建、分发、维护和保护这些密钥，以防止篡改、泄露或滥用。管理不当可能导致密钥替换等攻击，即攻击者用其密钥替换您的密钥以拦截通信。

GPG 中的“信任网络”模型允许用户相互认证密钥，构建经过验证的身份网络。密钥存储在**钥匙环**中（公钥和私钥文件，例如旧版本中的 `pubring.kbx` 和 `secring.gpg`，或新版本中的统一文件）。请务必备份私钥并使用强密码。

## 密钥结构

GPG 密钥对不仅仅是单个密钥，而是一个组合：

- **主密钥**：主签名密钥（例如 RSA 或 DSA），用于认证（签名）其他密钥并对密钥组件进行自签名。
- **子密钥**：用于特定任务的可选从属密钥：
  - 签名子密钥：用于签名消息。
  - 加密子密钥：用于加密数据（通常定期轮换）。
  - 认证子密钥：用于 SSH 或类似用途。
- **用户标识（UID）**：字符串如“Alice（注释）<alice@example.com>”，将密钥与真实身份关联。可以为不同角色设置多个 UID。
- **自签名**：主密钥对其自身组件进行签名以防止篡改。

以交互方式查看密钥结构：

```
gpg --edit-key <密钥ID或邮箱>
```

在菜单中，使用 `check` 验证自签名，或使用 `toggle` 查看私有部分（如果可用）。

## 生成密钥

从生成主密钥对开始。初学者可使用交互式方法：

1. 运行 `gpg --full-gen-key`（或使用 `--gen-key` 使用默认设置）。
2. 选择密钥类型（默认：RSA，用于签名和加密）。
3. 选择密钥大小（例如 4096 位以增强安全性；建议最小 2048 位）。
4. 设置过期时间（例如 1y 表示一年；“0”表示永不过期——尽可能避免永不过期）。
5. 输入用户标识（姓名、邮箱）。
6. 设置强密码（20 个以上字符，混合大小写/符号）。

快速生成（非交互式）：

```
gpg --quick-generate-key "Alice <alice@example.com>" rsa default 1y
```

生成后，创建**撤销证书**（用于在密钥泄露时使其失效的文件）：

```
gpg --output revoke.asc --gen-revoke <您的密钥ID>
```

将其安全存储（例如打印存放在保险库中）——在需要之前请勿共享。

稍后添加子密钥或 UID：

- 输入 `gpg --edit-key <密钥ID>`，然后使用 `addkey`（用于子密钥）或 `adduid`（用于 UID）。这些将自动进行自签名。

## 列出和查看密钥

- 列出公钥：`gpg --list-keys`（或 `--list-public-keys`）。
- 列出私钥：`gpg --list-secret-keys`。
- 详细视图：`gpg --list-keys --with-subkey-fingerprint <密钥ID>`（显示子密钥的指纹）。

输出显示密钥 ID（短/长格式）、创建/过期日期、功能（例如 `[SC]` 表示签名/认证）和 UID。

## 导出和导入密钥

**导出**用于共享公钥或备份私钥：

- 公钥：`gpg --armor --export <密钥ID> > mykey.asc`（ASCII 编码，适用于电子邮件）。
- 私钥（仅用于备份）：`gpg --armor --export-secret-keys <密钥ID> > private.asc`。
- 上传到密钥服务器：`gpg --keyserver hkps://keys.openpgp.org --send-keys <密钥ID>`。

**导入**将其他人的密钥添加到您的公钥环：

- `gpg --import <文件.asc>`（与现有密钥合并；添加新签名/子密钥）。
- 从密钥服务器导入：`gpg --keyserver hkps://keys.openpgp.org --recv-keys <密钥ID>`。

导入后，使用 `gpg --edit-key <密钥ID>` 和 `check` 验证自签名。

## 签名和认证密钥

建立信任：

- 签名密钥（认证其有效性）：`gpg --sign-key <其他密钥ID>`（或使用 `lsign-key` 仅限本地）。
- 快速签名：`gpg --quick-sign-key <指纹> "用户标识"`。
- 设置信任级别：在 `--edit-key` 中，使用 `trust`（例如“5”表示绝对信任）。

这会在密钥上创建签名，在列表中可见。信任网络根据您对签名者的信任来计算有效性。

## 撤销密钥

撤销使密钥或组件失效而不删除它，确保其他人看到它不再有效：

- 完整密钥：导入您的撤销证书：`gpg --import revoke.asc`，然后导出/发送更新后的密钥。
- 子密钥/UID：在 `--edit-key` 中，使用 `key 1` 或 `uid 1` 选择，然后使用 `revkey` 或 `revuid`。
- 快速撤销 UID：`gpg --quick-revoke-uid <密钥ID> <要撤销的UID>`。

撤销原因：泄露、不再使用、被替换。始终发布已撤销的密钥。

## 最佳实践

- **安全**：使用硬件令牌（例如 YubiKey）存储私钥。每年轮换加密子密钥（`gpg --quick-add-key <指纹> rsa encr 1y`）。定期更改密码（`gpg --change-passphrase <密钥ID>`）。
- **过期**：设置合理的过期时间（1-2 年）以强制更新并检测泄露。
- **分发**：通过密钥服务器或直接共享公钥；亲自或通过可信渠道验证指纹以避免中间人攻击。
- **备份**：将私钥导出到加密存储。立即生成撤销证书。
- **清理**：使用 `gpg --edit-key` 和 `clean` 删除无效签名。
- **更新**：截至 2025 年，GnuPG 2.5+ 支持抗量子算法（例如 `--quick-generate-key ... pqc`）；考虑迁移以面向未来。
- **常见陷阱**：切勿共享私钥。避免永不过期。在沙盒中测试撤销。

如需实践，可在测试目录中使用 `gpg --homedir ./test-gpg` 进行实验。

[GnuPG 手册：密钥管理](https://www.gnupg.org/gph/en/manual/c235.html)
[GNU Privacy Guard 手册：OpenPGP 密钥管理](https://www.gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html)
[GnuPG 入门指南](https://www.gnupg.org/gph/en/manual/c14.html)
