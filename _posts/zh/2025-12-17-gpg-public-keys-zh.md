---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 将 GPG 公钥存储在 Git 中
translated: true
type: note
---

问题：我们可以在Git仓库中保存.gpg公钥文件吗？

回答：

可以，将GPG **公钥**文件（通常导出为`.asc`或`.gpg` ASCII-armored文件）存储在Git仓库中是安全且通常推荐的做法。

GPG公钥的设计初衷就是为了广泛共享——这是非对称加密工作原理的基础。分发您的公钥可以让其他人加密数据给您或验证您的签名。无论是公共还是私有Git仓库，将公钥提交到其中并没有重大的安全风险：

- 没有敏感信息被暴露（私钥仍然保密）。
- 它有助于团队工作流程，例如验证已签名的提交/标签，或者允许像`git-secret`这样的工具使用团队成员的公钥加密秘密。
- 常见的做法包括将维护者/开发者的公钥存储在仓库中，以用于离线或防火墙环境，或者将其嵌入为Git对象/blob以进行验证。

**重要警告**：
- 绝不要提交**私钥**（或秘密密钥环）——这将是一个严重的安全漏洞。
- 如果仓库是公共的，广泛分发公钥没有问题，但要确保公钥关联的电子邮件/身份符合您的需求。
- 对于关键项目，应通过其指纹来固定公钥，而不是仅仅依赖文件，以避免潜在的篡改（尽管这在实践中很少见）。

这在开源项目中是标准做法，并得到GitHub/GitLab等平台的支援，这些平台会定期共享或上传公钥以进行提交验证。

参考资料：

- [关于在仓库中存储PGP公钥的Reddit讨论](https://www.reddit.com/r/github/comments/1kn1hzu/is_it_safe_to_keep_a_pgp_key_in_a_public_repo_i/)
- [Stack Overflow：在Git仓库中共享公钥以进行签名验证](https://stackoverflow.com/questions/46318599/should-we-share-the-public-key-for-checking-signing-in-the-git-repository)
- [GitHub文档：添加GPG密钥](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account)
- [信息安全Stack Exchange：公开存储GPG加密数据](https://security.stackexchange.com/questions/193864/is-it-safe-to-store-gpg-encrypted-data-publicly-eg-on-github)