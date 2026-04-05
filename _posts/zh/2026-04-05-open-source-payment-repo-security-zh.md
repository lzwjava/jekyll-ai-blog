---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源支付仓库安全
translated: true
type: note
---

问题：如果我开源 `lzwjava/live-server` 和 `lzwjava/live-mobile-web` 仓库，会有安全问题吗？如果把支付宝或微信支付的 PEM 证书放在一个闭源的独立仓库里——这是一种好方法吗？

回答：

## 开源 `live-server` 和 `live-mobile-web` 的安全风险

### 仓库内容概述

查看 `live-server` 的文件结构，其中包含：

- `config/alipay.php` — 支付宝配置
- `libraries/wx/cert/` — 微信支付证书文件（`wx` 下的 `cert/` 文件夹）
- `libraries/alipay/` — 支付宝 RSA 签名/通知逻辑
- `live-conf/` — 一个可能包含敏感信息的独立配置文件夹

这些是开源前需要重点检查的区域。

---

### 🔴 关键风险：仓库中的 PEM / 证书文件

微信支付官方文档明确警告：**切勿将你的私钥存放在任何公开可访问的位置，例如上传到 GitHub，或写在客户端代码中。** 商户私钥文件（`apiclient_key.pem`）是本地生成的，必须严格保密。

如果这些 PEM 文件或证书 **已提交到仓库的 Git 历史记录中**，即使你现在删除它们并开源仓库，**它们仍会保留在提交历史记录中**，任何克隆或分叉仓库的人都可能提取到。这是一个关键风险。

**如果 PEM 文件曾被提交，需立即采取的行动：**
- 立即在支付宝和微信支付的商户平台上撤销/重新生成证书
- 在公开仓库之前，使用 `git filter-repo` 或 BFG Repo Cleaner 从整个 Git 历史记录中彻底清除这些文件
- 轮换所有密钥（API 密钥、应用密钥、商户 ID、令牌）

---

### 🟡 开源时的其他安全风险

**1. 配置文件中的硬编码密钥**
- `config/alipay.php`、`config/database.php`、`WxPay.Config.php` 可能包含 app ID、商户 ID、应用密钥、签名密钥等
- 即使 PEM 文件单独存放，这些硬编码的配置值也是危险的

**2. 业务逻辑暴露**
- 开源会暴露付款验证方式、回调处理逻辑、订单验证流程
- 攻击者可以研究 `Charges.php`、`Rewards.php`、`Withdraws.php` 来寻找逻辑漏洞
- 研究表明，攻击者可能利用支付通知逻辑——例如，向未经正确验证签名的商户服务器发送伪造的支付宝通知——来免费获取产品

**3. 数据库结构暴露**
- `db/` 文件夹可能包含数据库迁移文件
- 攻击者可以了解你的表结构，这有助于规划 SQL 注入攻击

**4. 内部 API 文档**
- `api.md` 已包含在仓库中——这文档了你的所有 API 接口，对攻击者很有用

---

### ✅ “PEM / 配置闭源”策略——好吗？

**是的，这是正确且推荐的做法。** 以下是正确的结构方式：

#### 推荐架构

```
live-server（公开，开源）
  └── 从环境变量或外部配置文件读取配置

live-conf（私有，闭源）
  ├── alipay_private.pem
  ├── wx/cert/apiclient_cert.pem
  ├── wx/cert/apiclient_key.pem
  ├── config/database.php（包含真实凭据）
  └── config/alipay.php（包含真实的 app_id、密钥等）
```

#### 密钥管理最佳实践

| 方法 | 建议 |
|--------|---------------|
| 环境变量 | ✅ 最佳——通过 `.env` 或服务器环境变量在运行时注入密钥 |
| 配置独立的私有仓库 | ✅ 好——正如你所提议的，但要确保它从未公开过 |
| 在 `.gitignore` 中忽略 PEM/配置文件 | ✅ 必要——将 `*.pem`、`config/alipay.php`、`config/database.php` 添加到 `.gitignore` |
| 密钥管理服务 | ✅ 理想——使用阿里云 KMS、AWS Secrets Manager、HashiCorp Vault 等服务 |
| 在源代码中硬编码密钥 | ❌ 绝对不要 |
| PEM 文件在公开仓库中 | ❌ 绝对不要 |

---

### 🛡️ 开源前的检查清单

1.  **审核 Git 历史记录** — `git log --all --full-history -- "*.pem"` 检查 PEM 文件是否曾被提交
2.  **清理历史记录中的密钥** — 如果曾有密钥被提交，使用 BFG Repo Cleaner 进行清理
3.  **轮换所有密钥和证书** — 支付宝应用密钥、微信支付 API 密钥、数据库密码、七牛云令牌等
4.  **将所有真实配置移至私有仓库或环境变量** — 公开仓库应仅包含示例/模板配置文件（例如 `config/alipay.example.php`）
5.  **添加 `.gitignore` 规则** 忽略 `*.pem`、`*.p12`、`config/database.php` 及任何 `*_key*` 文件
6.  **检查 `live-conf/` 文件夹** — 此文件夹似乎是故意排除或私有的；确保它保持私有状态
7.  **检查 `fabfile.py`（部署脚本）** — 可能包含服务器 IP、SSH 凭据

---

### 总结

开源 **代码逻辑** 是可以的，在业界也很常见。安全性不在于隐藏代码，而在于 **将凭据与代码分离**。你直觉想把 PEM 文件和支付配置放在一个闭源仓库里是完全正确的——只是要绝对确保这些文件 **从未被提交** 到你计划公开的仓库中，即使是在旧的提交记录中。

参考文献：

- [微信支付：私钥与证书规则](https://pay.weixin.qq.com/doc/global/v3/en/4012357137)
- [支付宝客户端安全要求](https://docs.alipayplus.com/alipayplus/alipayplus/code_scanning_payment_standards_mpp/mpmsecurity_client)
- [研究：支付聚合中的逻辑漏洞（PDF）](https://www.xiaojingliao.com/uploads/9/7/0/2/97024238/security19-dilution.pdf)