---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Centralized Configuration Management Over Multiple Files
translated: false
type: note
---

Question: In a Python script repository that dumps data from DB2 and generates files, with environments (Local dev, UAT, PROD) and three country codes (CN, TW, HK) having different configurations, is it a good idea to maintain 3 × 3 = 9 separate .ini files in the central repository?

Answer:

No, you should **not** have 9 separate .ini files in the central repository. That approach is error-prone, hard to maintain, and violates DRY principles. Here are much better alternatives (ordered from most recommended to acceptable):

### Recommended Approaches

1. **One single config file + environment variables (Best practice in 2025)**

   ```ini
   # config.ini (committed)
   [db2]
   host_template = db2-{country}-{env}.example.com
   port = 50000
   database_template = PROJ{country.upper()}

   [paths]
   output_dir = /data/output/{country}/{env}
   ```

   Then at runtime:

   ```python
   country = os.getenv("COUNTRY_CODE")      # cn, tw, hk
   env     = os.getenv("ENV", "dev")        # dev, uat, prod
   ```

   → Zero sensitive credentials in repo, only one config file.

2. **One base config + country-specific overrides (Very clean)**
   Repository structure:

   ```
   config/
     base.ini
     cn.ini
     tw.ini
     hk.ini
     env/
       dev.ini     → usually empty or logging=DEBUG
       uat.ini
       prod.ini
   ```

   Load order: `base.ini → {country}.ini → env/{env}.ini`
   Only a few lines differ per country (e.g., SSL settings, schema prefixes, date formats, encryption keys for CN).

3. **Single config with sections per country and environment**

   ```ini
   [db2:cn:prod]
   host = prod-db-cn.company.com
   ssl = true

   [db2:tw:uat]
   host = uat-db-tw.company.com
   ssl = false
   ```

   You end up with one file but still 9 sections — better than 9 files, but harder to read.

4. **Acceptable but not ideal: 3 country files × 3 env files = 9 files**
   Only if the differences are huge and you never want any shared values. Even then, use a script to generate them from a template or keep them outside version control (see below).

### What most teams actually do in real projects

- Commit only `config/base.ini` + country overrides (`cn.ini`, `tw.ini`, `hk.ini`)
- Never commit production credentials
- Use `.ini.example` files as templates
- Put real environment-specific values in environment variables or secret managers (AWS Secrets Manager, Hashicorp Vault, Azure Key Vault, etc.)
- In local dev: `local.env` file (added to .gitignore) or direnv

### Recommended final structure

```
config/
  base.ini
  cn.ini
  tw.ini
  hk.ini
  local.example.ini   ← copy to local.ini (gitignored)
scripts/
  generate_config.py  ← optional: merges base + country + env
```

This gives you maximum flexibility with only ~4 committed config files instead of 9, and no secrets in git.

**Bottom line**: 9 separate .ini files = maintenance nightmare. Use one base config + small country-specific overrides + environment variables instead.
