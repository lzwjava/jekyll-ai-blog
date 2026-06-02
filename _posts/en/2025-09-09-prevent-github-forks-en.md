---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Preventing Repository Forks on GitHub
translated: false
type: note
---

On GitHub, **you can’t stop people from forking a public repository**. Forking is a core feature of GitHub for open collaboration. If your repo is public, anyone can make a fork.

Here are your options depending on your goal:

### 1. If you want to prevent forking altogether

* The only way is to make your repository **private**.
* Private repos cannot be forked to outside accounts.
* Inside an organization, admins can control whether private repos are forkable to other members.

### 2. If you want to reduce exposure but keep it public

* You can **restrict licensing**: add a license that doesn’t allow redistribution (e.g., “All Rights Reserved”). This won’t technically stop forks but gives you legal protection.
* You can **disable GitHub Pages** and other exposure features to reduce visibility.

### 3. If your repo has already been forked

* You cannot “unfork” someone else’s copy.
* You can only ask the fork owner to delete it, or file a **DMCA takedown request** with GitHub if they’re violating your license or rights.

---

👉 In short:

* Public repo → can always be forked.
* Private repo → fork protection, unless explicitly allowed within your org.

Do you want me to walk you through **how to set a repo private and disable internal forking**?
