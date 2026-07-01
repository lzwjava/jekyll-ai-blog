---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pushing to GitHub and Gitea Simultaneously
translated: false
type: note
---

**Question:** How do I push a Git repository to both GitHub and a local Gitea server on the LAN at the same time, and what is the sync mechanism behind it?

---

**Answer:**

## Overview of the Sync Mechanism

Git is designed to be decentralized. When your project exists as a repo on Gitea and as a repo on GitHub, it is like the project existing on two separate servers — there is no contradiction. You can make changes to your local copy, commit them, then push to either Gitea, GitHub, or both simultaneously.

There is **no automatic two-way sync** between GitHub and Gitea by default. The sync is **push-based and one-directional from your local machine** — you are the source of truth, and both remotes receive your commits when you push. Git's internal mechanism (pack objects, delta compression) is identical for both remotes; it just sends the same commit objects to two different endpoints.

---

## Method 1: Two Separate Named Remotes (Most Flexible)

This is the cleanest approach — explicit and easy to manage.

```bash
# Add GitHub as remote named "github"
git remote add github git@github.com:username/repo.git

# Add local Gitea as remote named "gitea"
git remote add gitea http://192.168.1.x:3000/username/repo.git
# or via SSH: git@192.168.1.x:username/repo.git
```

Git lets you have multiple remotes, each with its own name. Adding GitHub and Gitea as separate remotes means you can push to both at the same time. `git push github main` sends commits from local main to the GitHub remote, and the same applies for Gitea.

Push to both manually:

```bash
git push github main
git push gitea main
```

Or create a **Git alias** to push both with one command:

```bash
git config --global alias.pushall '!git push github main && git push gitea main'
# Then just run:
git pushall
```

---

## Method 2: Single Remote with Multiple Push URLs (One `git push` command)

You can define a git remote that points to multiple push URLs. For example, create one called `all`, add the first URL, then add the second URL:

```bash
# Create "all" remote pointing to GitHub
git remote add all git@github.com:username/repo.git

# Add GitHub as 1st push URL
git remote set-url --add --push all git@github.com:username/repo.git

# Add Gitea as 2nd push URL
git remote set-url --add --push all http://192.168.1.x:3000/username/repo.git
```

Verify with:

```bash
git remote -v
# Output:
# all  git@github.com:username/repo.git (fetch)
# all  git@github.com:username/repo.git (push)
# all  http://192.168.1.x:3000/username/repo.git (push)
```

A `git fetch` or `git pull` will use the first URL in the list, while `git push` will push to **all** push URLs configured for that remote.

Now a single command pushes to both:

```bash
git push all main
```

---

## Method 3: Modify `origin` to Push to Both (If `origin` already exists)

If you already have `origin` pointing to GitHub:

```bash
# Keep existing origin fetch URL (GitHub)
# Add Gitea as an additional push-only URL
git remote set-url --add --push origin http://192.168.1.x:3000/username/repo.git
```

Now `origin` will still **fetch** from GitHub, but will **push** to both GitHub and Gitea.

---

## Method 4: Automate via Git Post-Commit Hook

You can use a `post-commit` hook to automatically push to both remotes after every commit. Navigate to `.git/hooks/`, create a file named `post-commit`, and add the following script:

```bash
#!/bin/sh
# Push changes to Gitea
git push gitea main
# Push changes to GitHub
git push github main
```

Then make it executable:

```bash
chmod +x .git/hooks/post-commit
```

---

## Sync Mechanism Summary

| Aspect | Detail |
| --- | --- |
| **Direction** | Local → both remotes (push-based) |
| **Atomicity** | Pushes are sequential, not atomic — one can succeed while the other fails |
| **Fetch/Pull** | Only fetches from **one** remote (the fetch URL, usually GitHub) |
| **Conflict handling** | Must be resolved locally; both remotes should ideally stay in sync |
| **LAN vs Internet** | Gitea on LAN is fast; GitHub push goes over internet separately |

---

## Authentication Tips

- **SSH keys** are recommended for both remotes for password-less operation. Add your public key to both GitHub and your Gitea instance.
- **HTTPS with token**: For GitHub, use a Personal Access Token (PAT); for Gitea, also use a PAT or basic auth.
- If on LAN, SSH to Gitea typically works as: `git@192.168.1.x:username/repo.git` (ensure port 22 is open on your Gitea host).

---

**References:**

- [Pushing to multiple Git remotes (jeffkreeftmeijer.com)](https://jeffkreeftmeijer.com/git-multiple-remotes/)
- [How to push to multiple git remotes at once (gist.github.com)](https://gist.github.com/rvl/c3f156e117e22a25f242)
- [Git: Push to multiple remotes at once (leighm.cc)](https://leighm.cc/posts/git-push-to-multiple-remotes-at-once/)
- [Push to Multiple Repositories Using Git Hooks (dev.to)](https://dev.to/nguonodave/push-to-multiple-repositories-simultaneously-using-git-hooks-4cmf)
- [Working with multiple Git remotes (jigarius.com)](https://jigarius.com/blog/multiple-git-remote-repositories)
- [Setting Up a Self-Hosted Github Clone with Gitea (charlesreid1.github.io)](https://charlesreid1.github.io/setting-up-a-self-hosted-github-clone-with-gitea.html)
