---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Introduction to Google Cloud Shell
translated: false
type: note
---

**Question:** Comprehensive guide to Cloud Shell in Google Cloud

**Answer:**

Cloud Shell is a free, browser-based shell environment provided by Google Cloud that allows you to manage Google Cloud resources directly from the browser without installing any software locally.

### What is Google Cloud Shell?

Cloud Shell provides a temporary **Debian-based Linux VM** (Compute Engine instance) pre-configured with:

- Google Cloud SDK (`gcloud`, `gsutil`, `bq`, etc.) — always up-to-date
- Popular tools: `docker`, `terraform`, `kubectl`, `helm`, `git`, `node`, `python`, `go`, `java`, etc.
- Authentication already handled (your Google account)
- 5 GB of persistent **home directory** storage (`/home/<your_username>`)
- Web-based code editor (Cloud Shell Editor — VS Code–like interface)
- Gemini CLI (AI assistance in terminal)

It is ideal for quick experiments, learning GCP, running gcloud commands, managing infrastructure as code, or light development.

### How to Launch Cloud Shell

1. Go to the Google Cloud Console → <https://console.cloud.google.com>
2. Click the **Cloud Shell icon** (terminal symbol) in the top-right toolbar
   → or use direct link: <https://shell.cloud.google.com>
3. First time → it provisions your machine (takes ~10–30 seconds)
4. You get a Bash terminal at the bottom of the screen (can be popped out to new tab)

Alternative launch methods:

- `cloudshell` button in many GCP docs pages ("Open in Cloud Shell")
- Direct deep-link with repo cloning: `https://shell.cloud.google.com/?show=terminal&cloudshell_git_repo=<url>`

### Persistent Storage (5 GB Home Directory)

Only `/home/$USER` is persistent across sessions.

Everything else (`/tmp`, `/usr/local`, etc.) is **ephemeral** — deleted when session ends.

Common persistent locations:

- `~/` (home)
- `~/.bashrc`, `~/.zshrc`, `~/.gitconfig`
- `~/projects/`, `~/bin/`, etc.

Tip: Store larger files in **Cloud Storage** buckets and mount them if needed.

### Session Lifetime and Machine Specs

- Idle timeout: ~**60 minutes** (configurable somewhat via settings)
- Maximum session duration: **12 hours** (then restarts)
- Machine type: usually **e2-micro** or similar (1 vCPU, ~3.75 GB RAM — can vary)
- Ephemeral disk: ~100 GB (non-persistent)

### Quotas and Limits (as of late 2025 / early 2026)

- Persistent storage: **5 GB** per user (hard limit)
- Weekly Cloud Code / Editor usage: **50 hours** (soft quota for extended editor usage)
- No custom machine type selection
- No sudo access for installing system packages (`apt install` works for user-space tools)

### Key Features and Tools Included

- Full **gcloud** CLI (authenticated automatically)
- **Cloud Shell Editor** — click pencil icon or type `cloudshell edit <file>`
- Git cloning, pushing (GitHub, Cloud Source Repositories)
- Docker (build & run containers — but no privileged mode)
- Terraform, Pulumi, Ansible, etc.
- Web preview: click port number → "Preview on port xxxx"
- File upload/download via UI (gear icon)
- Multiple tabs (in popped-out window)
- Customize prompt, install oh-my-zsh, etc.

### Best Practices

1. **Always store important data in persistent home or GCS**

   ```bash
   gsutil cp -r important-project gs://my-backup-bucket/
   ```

2. **Use .bashrc / .zshrc wisely**

   Add aliases, functions, PATH modifications.

3. **Install user tools in ~/bin or use language package managers**

   ```bash
   pip install --user awscli
   npm install -g serverless
   go install github.com/...
   ```

4. **Use Cloud Storage for larger files / shared data**

   ```bash
   gcsfuse my-bucket ~/mnt/bucket
   ```

5. **Leverage "Open in Cloud Shell" buttons in docs/tutorials**

6. **Use tmux / screen for long-running processes**

   (session survives browser close if you re-attach)

7. **Backup dotfiles**

   Push `~/.*` configs to private Git repo.

8. **For heavy development → consider Cloud Workstations or local setup**

   Cloud Shell is great for quick tasks, not full-time heavy dev.

### Common Commands to Get Started

```bash
# Show current project
gcloud config get-value project

# List projects
gcloud projects list

# Set default project
gcloud config set project my-project-id

# List buckets
gsutil ls

# Clone repo and open editor
git clone https://github.com/user/repo
cloudshell edit repo/main.py

# Preview web app
python3 -m http.server 8080   # → click "Preview on port 8080"
```

### When NOT to Use Cloud Shell

- Heavy compute (ML training, video encoding)
- Needing >5 GB persistent storage
- Requiring sudo / kernel modules
- Long-running background processes (>12h)
- Very large file handling

For those cases → use **Compute Engine**, **Cloud Run**, **Cloud Workstations**, or local machine + Cloud SDK.

Cloud Shell remains one of the fastest ways to interact with Google Cloud securely from any device with a browser.

**References:**

- [Cloud Shell documentation](https://docs.cloud.google.com/shell/docs)
- [Use Cloud Shell](https://docs.cloud.google.com/shell/docs/using-cloud-shell)
- [How Cloud Shell works](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works)
- [Launch Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell)
- [Cloud Shell Editor limitations](https://docs.cloud.google.com/code/docs/shell/limitations)
