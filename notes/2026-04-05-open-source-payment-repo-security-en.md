---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Source Payment Repository Security
translated: false
type: note
---

Question: If I open source the `lzwjava/live-server` and `lzwjava/live-mobile-web` repositories, will there be security issues? What if the Alipay or WeChat Pay PEM certificates are kept in a closed-source separate repo — is that a good approach?

Answer:

## Security Risks of Open Sourcing `live-server` and `live-mobile-web`

### Overview of What's in the Repos

Looking at the `live-server` file structure, it contains:

- `config/alipay.php` — Alipay configuration
- `libraries/wx/cert/` — WeChat Pay certificate files (the `cert/` folder under `wx`)
- `libraries/alipay/` — Alipay RSA signing/notification logic
- `live-conf/` — a separate config folder that may contain sensitive secrets

These are significant areas to examine before open sourcing.

---

### 🔴 Critical Risk: PEM / Certificate Files in the Repo

WeChat Pay's official documentation explicitly warns: **never put your private key on any publicly-accessible location, for example, uploading it to GitHub, or writing it in the client-side code.** The merchant private key file (`apiclient_key.pem`) is generated locally and must be kept strictly confidential.

If these PEM files or certificates are **committed in the repo's Git history**, even if you delete them now and open source the repo, **they remain in the commit history** and can be extracted by anyone who clones or forks the repo. This is a critical risk.

**Immediate action if PEM files were ever committed:**

- Revoke/regenerate your Alipay and WeChat Pay certificates immediately on their respective merchant platforms
- Use `git filter-repo` or BFG Repo Cleaner to purge the files from the entire git history before making public
- Rotate all secrets (API keys, app secrets, merchant IDs, tokens)

---

### 🟡 Other Security Risks When Open Sourcing

**1. Hardcoded Secrets in Config Files**

- `config/alipay.php`, `config/database.php`, `WxPay.Config.php` likely contain app IDs, merchant IDs, app secrets, signing keys
- Even if PEM files are separate, these config values are dangerous if hardcoded

**2. Business Logic Exposure**

- Open sourcing reveals how payments are validated, how callbacks are handled, and how orders are verified
- Attackers can study `Charges.php`, `Rewards.php`, `Withdraws.php` to find logic vulnerabilities
- Research has shown that attackers can exploit payment notification logic — for example, sending fake Alipay notifications to a merchant server that isn't verifying signatures properly — to obtain products for free

**3. Database Schema Exposure**

- The `db/` folder likely contains schema migrations
- Attackers can learn your table structures, which helps with SQL injection planning

**4. Internal API Documentation**

- `api.md` is included in the repo — this documents all your endpoints, which is useful for attackers

---

### ✅ The "Closed Source PEM / Config" Strategy — Is It Good?

**Yes, this is the correct and recommended approach.** Here's how to structure it properly:

#### Recommended Architecture

```
live-server (public, open source)
  └── reads config from environment variables or external config path

live-conf (private, closed source)
  ├── alipay_private.pem
  ├── wx/cert/apiclient_cert.pem
  ├── wx/cert/apiclient_key.pem
  ├── config/database.php (with real credentials)
  └── config/alipay.php (with real app_id, keys)
```

#### Best Practices for Secrets Management

| Method | Recommendation |
| -------- | --------------- |
| Environment Variables | ✅ Best — inject secrets at runtime via `.env` or server env vars |
| Separate Private Repo for Configs | ✅ Good — as you propose, but make sure it was NEVER public |
| `.gitignore` for PEM/config files | ✅ Necessary — add `*.pem`, `config/alipay.php`, `config/database.php` to `.gitignore` |
| Secrets Management Services | ✅ Ideal — use Alibaba Cloud KMS, AWS Secrets Manager, HashiCorp Vault |
| Hardcoded secrets in source code | ❌ Never |
| PEM files in public repo | ❌ Never |

---

### 🛡️ Checklist Before Open Sourcing

1. **Audit git history** — `git log --all --full-history -- "*.pem"` to check if PEM files were ever committed
2. **Scrub secrets from history** — use BFG Repo Cleaner if any secrets were committed
3. **Rotate all keys and certificates** — Alipay app secret, WeChat Pay API key, database passwords, Qiniu tokens
4. **Move all real configs to a private repo or environment variables** — the public repo should only contain example/template config files (e.g., `config/alipay.example.php`)
5. **Add `.gitignore` rules** for `*.pem`, `*.p12`, `config/database.php`, any `*_key*` files
6. **Review `live-conf/` folder** — this folder appears to be intentionally excluded or private; ensure it stays that way
7. **Check `fabfile.py`** (deployment script) — may contain server IPs, SSH credentials

---

### Summary

Open sourcing the **code logic** is fine and common in the industry. The security lies not in hiding the code, but in **separating credentials from code**. Your instinct to keep PEM files and payment configs in a closed-source repo is exactly right — just make absolutely sure those files were **never committed** to the repo you plan to make public, even in old commits.

References:

- [WeChat Pay: Private Key and Certificate Rules](https://pay.weixin.qq.com/doc/global/v3/en/4012357137)
- [Alipay Client Security Requirements](https://docs.alipayplus.com/alipayplus/alipayplus/code_scanning_payment_standards_mpp/mpmsecurity_client)
- [Research: Logic Vulnerabilities in Payment Syndication (PDF)](https://www.xiaojingliao.com/uploads/9/7/0/2/97024238/security19-dilution.pdf)
