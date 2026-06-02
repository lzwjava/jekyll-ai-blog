---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fixing GitHub Actions Push Authentication Errors
translated: false
type: note
---

That 403 means the push is authenticating as **`lzwjava` without a token that has write access** (often because the job is still using the default `GITHUB_TOKEN`, which can’t push to another repo). Fix it by **injecting a real credential for the destination checkout/push**.

Here are three solid ways—pick one. I’ll show the quickest first.

---

### Option A — Use a PAT and embed it in the remote (quickest)

1. Create a **classic PAT** with `repo` scope (or a fine-grained PAT with **Contents: Read & Write** to `lzwjava/lzwjava.github.io`). Save it in the source repo as `DEPLOY_TOKEN`.

2. Update your workflow’s deploy step to **force the remote to use that token**:

{% raw %}
```yaml
- name: Check out destination repo
  uses: actions/checkout@v4
  with:
    repository: lzwjava/lzwjava.github.io
    token: ${{ secrets.DEPLOY_TOKEN }}
    path: destination
    fetch-depth: 0

- name: Push built site to destination
  run: |
    rsync -av --delete _site/ destination/
    cd destination
    touch .nojekyll

    git config user.name  "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"

    # Force the remote to use PAT explicitly (avoids credential-helper conflicts)
    git remote set-url origin https://${{ secrets.DEPLOY_TOKEN }}@github.com/lzwjava/lzwjava.github.io.git

    if [ -n "$(git status --porcelain)" ]; then
      git add -A
      git commit -m "deploy: ${GITHUB_SHA}"
      git push origin HEAD:main
    else
      echo "No changes to deploy."
    fi
```
{% endraw %}

If you still see 403, your PAT is missing scopes or (if the repo were in an org) needs SSO authorization. Regenerate with `repo` scope and try again.

---

### Option B — Avoid credential bleed: disable default credentials on the first checkout

Sometimes the **first checkout** writes the default `GITHUB_TOKEN` into the credential helper and it gets reused later. Disable it:

```yaml
- name: Check out source repo
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
    persist-credentials: false   # <- important
```

Then keep the destination checkout with your PAT as shown in Option A (you can skip the `remote set-url` line if things already work, but it’s harmless).

---

### Option C — SSH deploy key (very robust)

1. On your machine: `ssh-keygen -t ed25519 -C "deploy@actions" -f deploy_key`
2. Add **public key** (`deploy_key.pub`) as a **Deploy key** in `lzwjava/lzwjava.github.io` with **Write access**.
3. Add the **private key** (`deploy_key`) as `ACTIONS_DEPLOY_KEY` secret in the **source** repo.

Workflow:

{% raw %}
```yaml
- name: Check out destination repo via SSH
  uses: actions/checkout@v4
  with:
    repository: lzwjava/lzwjava.github.io
    ssh-key: ${{ secrets.ACTIONS_DEPLOY_KEY }}
    path: destination
    fetch-depth: 0

- name: Push built site (SSH)
  run: |
    rsync -av --delete _site/ destination/
    cd destination
    touch .nojekyll
    git config user.name  "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    if [ -n "$(git status --porcelain)" ]; then
      git add -A
      git commit -m "deploy: ${GITHUB_SHA}"
      git push origin HEAD:main
    else
      echo "No changes to deploy."
    fi
```
{% endraw %}

---

### Quick diagnostics if it fails again

Run these right before pushing to see what auth is actually configured:

```bash
cd destination
git remote -v
git config --get user.name
git config --get user.email
git config --get url.https://github.com/.insteadof || true
git config --global --list | sed -n 's/^credential\.helper.*/&/p'
```

If `remote -v` shows a plain `https://github.com/...` **without** your PAT injected (Option A) or `git@github.com:` (Option C), you’re still using the wrong credential.

---

### Common gotchas

* **Fine-grained PAT** must explicitly grant **Contents: Read & Write** **to that exact repo**.
* **Branch protection** on `main` can block bot pushes (required checks/signatures). If so, deploy to an unprotected branch (e.g., `gh-pages`) or adjust rules.
* **Expired PAT** → regenerate.
* **Org SSO** (not your case if it’s a user repo) → authorize the PAT for the org.

Do one of the three options above and the 403 will go away.
