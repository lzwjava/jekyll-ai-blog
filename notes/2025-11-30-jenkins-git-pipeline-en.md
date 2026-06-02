---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Configuring Jenkins Pipeline from Internal Git
translated: false
type: note
---

Here’s how to configure a Jenkins Pipeline that loads the `Jenkinsfile` from an internal (enterprise) GitHub server (like GitHub Enterprise or self-hosted GitLab/Stash/Bitbucket Server, etc.).

### There are two main ways

  1. Pipeline script from SCM (recommended for real projects)
  2. Pipeline script (inline) – not what you want

### 1. Create / Edit a “Pipeline” job

- Job type → Pipeline
- In the Pipeline section choose:
  **Definition**: Pipeline script from SCM
- SCM → Git

### 2. Fill the Git configuration

| Field                              | What to put (example for GitHub Enterprise)                              |
|------------------------------------|--------------------------------------------------------------------------|
| Repository URL                     | `https://github.internal.company.com/org/repo.git`  or  `git@github.internal.company.com:org/repo.git` (SSH) |
| Credentials                        | Choose or create the credential (see below)                              |
| Branches to build                  | `*/main` or `*/master` or `feature/*` etc.                                       |
| Script Path                        | Usually `Jenkinsfile` (or `ci/Jenkinsfile` if it's in a subfolder)     |

### 3. Add credentials for the internal GitHub

Go to Jenkins → Manage Jenkins → Credentials → System → Global credentials (unrestricted) → Add Credentials

Most common scenarios:

#### A. HTTPS with Personal Access Token (recommended for GitHub Enterprise)

| Field               | Value                                                                 |
|---------------------|-----------------------------------------------------------------------|
| Kind                | Username with password                                                |
| Scope               | Global                                                                |
| Username            | Your GitHub username (or any string, e.g. `git`)                      |
| Password            | Personal Access Token (PAT) from your admin created on the internal GHE |
| ID                  | Something meaningful, e.g. `internal-ghe-pat`                         |
| Description         | Internal GitHub Enterprise PAT                                        |

Then select this credential in the job’s “Credentials” dropdown.

#### B. SSH private key (also very common)

| Field               | Value                                                                 |
|---------------------|-----------------------------------------------------------------------|
| Kind                | SSH Username with private key                                         |
| Scope               | Global                                                                |
| Username            | `git`                                                                 |
| Private Key         | Paste the private key (-----BEGIN OPENSSH PRIVATE KEY----- …)         |
| Passphrase          | If the key has a passphrase, put it here                     |
| ID                  | e.g. `internal-ghe-ssh-key`                                           |
| Description         | Internal GitHub Enterprise SSH key                                     |

Repository URL must then be the SSH form:
`git@github.internal.company.com:org/repo.git`

### 4. Additional useful options (inside the Git section of the job)

| Option                                          | Recommended value for enterprise environments                                                                                           |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Additional Behaviors → Checkout to specific local branch | Branch name: `**` (makes the workspace branch name match the remote branch name)                                                        |
| Additional Behaviors → Wipe out repository…     | Usually enable for clean builds                                                                                                         |
| Lightweight checkout                            | Leave unchecked (you need the full Jenkinsfile, not the lightweight version that Jenkins does for Pipeline CPS)                        |
| Poll SCM / GitHub hook trigger for GITScm polling | Enable if you want webhooks or polling                                                                                               |

### 5. Webhook setup on the internal GitHub (optional but recommended)

- On GitHub Enterprise → Repository → Settings → Webhooks → Add webhook
- Payload URL: `https://your-jenkins.company.com/github-webhook/` (Jenkins has a built-in endpoint)
- Content type: application/json
- Events: Just the push event (or “Send me everything”)
- Make sure Jenkins is reachable from the internal GitHub (firewall / reverse proxy)

Then in the Jenkins job enable:
Pipeline → Build Triggers → GitHub hook trigger for GITScm polling

That’s it. Once saved, Jenkins will clone the repo using the credential you selected and execute whatever is in the `Jenkinsfile` at the root (or the path you specified).

### Quick summary of the most common working configuration

```
Pipeline
 └ Definition: Pipeline script from SCM
     └ SCM: Git
         Repository URL: https://github.internal.company.com/myorg/myrepo.git
         Credentials: internal-ghe-pat (Username + PAT)
         Branches to build: */main
         Script Path: Jenkinsfile
```

or with SSH

```
Repository URL: git@github.internal.company.com:myorg/myrepo.git
Credentials: internal-ghe-ssh-key (SSH private key)
```

Both work perfectly with internal enterprise GitHub instances.
