---
audio: false
generated: true
image: false
lang: en
layout: post
title: Preventing Forks on Public GitHub Repositories
translated: false
type: note
---

**Question:** In a GitHub public repository, how do you prevent or ban forking?

**Answer:**

You can't fully prevent forking on a **public** GitHub repo — it's a core GitHub feature and part of the open-source social contract. GitHub does not provide a native setting to disable forking on public repos.

However, there are a few real options depending on your actual goal:

---

### Option 1: Make the repo private (only real technical block)

Private repos support fork restriction:

- **Org repos → Settings → Member privileges → Repository forking** — uncheck it
- This works only for private repos within an org

For public repos, this control doesn't exist.

---

### Option 2: Use a restrictive license

You can't block the GitHub UI fork button, but you can legally restrict what people do with forks:

- **AGPL-3.0** — forces derivative works to open-source
- **BSL (Business Source License)** — used by HashiCorp, restricts commercial use
- **Custom proprietary license** — "no redistribution, no forking" clause
- **No license** — under Berne Convention, default copyright applies; no one legally has the right to redistribute

```
# In LICENSE file:
Copyright (c) 2026 Zhiwei Li. All rights reserved.
No part of this software may be reproduced or distributed without permission.
```

This doesn't block the button — but it makes forks legally infringing.

---

### Option 3: GitHub Enterprise / Organization setting (for org public repos)

If you're on **GitHub Enterprise**, organizations have more control. But even then, public repo forking restriction is not a standard feature.

---

### The Honest Answer

| Goal | Solution |
|---|---|
| Block the fork button entirely | ❌ Not possible on public repos |
| Prevent legal reuse | ✅ Restrictive license |
| Prevent forks within your org | ✅ Make private + disable fork in org settings |
| Prevent forking completely | ✅ Make the repo private |

If your goal is to share code publicly but restrict usage (common for commercial open-core projects), the **BSL or a custom proprietary license** is the industry standard move — it's what HashiCorp did with Terraform before OpenTofu forked it.