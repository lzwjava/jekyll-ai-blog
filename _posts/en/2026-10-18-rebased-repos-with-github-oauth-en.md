---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rebased Repos with GitHub OAuth
translated: false
type: note
---

Both repos are committed and pushed. Each remote had new commits from another machine, so I rebased on top instead of force-pushing.

## `live-mobile-web` → pushed `0c72414..e7225fd`

| Commit | Contents |
|---|---|
| `ea7176d` feat: center the app column and polish avatar/user list layout | your pre-existing WIP (`App.vue`, `Tabbar.vue`, `variables.styl`, `IntroView.vue`, `UsersView.vue`, `user-avatar.vue`) |
| `e7225fd` feat: add GitHub login | `src/common/github.js`, `src/views/GithubCallbackView.vue`, router, `LoginOptionsForm`, `WeiboForm`, `.env.production`, README |

- Rebased cleanly onto remote `0c72414` (Fun Live icon assets — no file overlap).

## `live-server` → pushed `9564196..d282dbc`

| Commit | Contents |
|---|---|
| `d282dbc` feat: return the GitHub OAuth code to the calling SPA | `app/Controllers/Github.php`, `app/Config/Constants.php`, `.env.example` |

- Rebase hit one conflict in `app/Config/Constants.php`: your remote GCS migration had rewritten the `QINIU_FILE_HOST*` values (now `storage.googleapis.com/qulive`) in the same spot where I added `GITHUB_LOGIN_REDIRECT_ORIGINS`. Resolution kept **both** — remote's GCS hosts plus the redirect allow-list — and `php -l` passed before continuing.
- `Github.php` auto-merged; the redirect/allow-list logic verified intact after rebase (`.env.example` also auto-merged).

Working trees are clean in both repos, and remote's other new commits (GCS image storage, `api.funlive.io` nginx vhost, DB URL rewriter) are untouched beneath mine.

Reminder for deploying: push is done, but **live-server must be deployed before this frontend build**, otherwise clicking GitHub login ends on the old JSON callback page.