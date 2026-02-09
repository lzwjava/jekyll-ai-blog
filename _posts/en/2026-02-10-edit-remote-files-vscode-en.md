---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Edit Remote Files in VS Code
translated: false
type: note
---

**Question:** How to use VS Code to edit server files by connecting to a host, like Andrej Karpathy did in his video?

**Answer:**

Andrej Karpathy has mentioned in interviews (e.g., Lex Fridman podcast) that he likes to use **VS Code locally** (on his Mac) but connects via **Remote-SSH** to edit files directly on a remote Linux server/cluster. This gives a full local-quality VS Code experience (IntelliSense, debugging, extensions, terminal, etc.) while the actual files live on the remote machine.

This is the standard and most common way developers (including many AI/ML researchers) edit code on remote servers today.

### Step-by-step setup (2026 current best practice)

1. **Install VS Code**  
   Download and install from: https://code.visualstudio.com/ (if not already installed).

2. **Install the Remote - SSH extension**  
   - Open VS Code  
   - Go to Extensions view (Ctrl+Shift+X or Cmd+Shift+X on Mac)  
   - Search for **Remote - SSH**  
   - Install the official one by Microsoft (ms-vscode-remote.remote-ssh)

3. **Set up SSH access to your server**  
   Make sure you can already connect via terminal with:  
   ```
   ssh username@your-server-ip-or-domain
   ```  
   Best practice: Use SSH key authentication (strongly recommended):  
   - Generate key pair if you don't have one: `ssh-keygen -t ed25519`  
   - Copy public key to server: `ssh-copy-id username@your-server-ip-or-domain`  
   - Or manually add `~/.ssh/id_ed25519.pub` content to server's `~/.ssh/authorized_keys`

   Optional but very useful: Create an entry in your local `~/.ssh/config` file:  
   ```
   Host my-server
       HostName your-server-ip-or-domain
       User your-username
       Port 22                # change if using non-standard port
       IdentityFile ~/.ssh/id_ed25519
   ```  
   → Then you can simply use `ssh my-server` instead of typing full details every time.

4. **Connect from VS Code**  
   Two easiest ways:

   **Way A – Command Palette (recommended)**  
   - Press Ctrl+Shift+P (Cmd+Shift+P on Mac) → type **Remote-SSH: Connect to Host...**  
   - Select **+ Add New SSH Host...** (first time) or pick existing host  
   - Enter: `username@your-server-ip-or-domain` (or just `my-server` if you used ssh config)  
   - Choose which config file to update (usually pick the default ~/.ssh/config)  
   - VS Code connects → it will install VS Code Server on the remote machine (automatic, one-time ~30-60 seconds)  
   - After connected, open any folder: **File → Open Folder...** and navigate to your project path on the server (e.g. `/home/username/projects/my-repo`)

   **Way B – From status bar**  
   - Bottom-left corner click the green **><** remote indicator  
   - Choose **Connect to Host...**

5. **You're now editing remotely**  
   - All files you open/edit/save are physically on the server  
   - Terminal (Ctrl+`) runs on the server  
   - Extensions (Python, GitLens, Jupyter, etc.) can be installed remotely  
   - Debugging, tasks, git operations all work as if local  
   - You get full IntelliSense, auto-format on save, etc.

### Tips & Common Gotchas

- First connection may take 1–2 minutes (installs VS Code Server on remote)  
- Make sure remote server has internet (needs to download VS Code Server once)  
- If connection drops → just reconnect (VS Code usually recovers well)  
- For very large projects, consider excluding folders via `.vscode/settings.json` → `"files.exclude"` or `"search.exclude"`  
- Want even faster experience? Use **Remote - Tunnels** or **GitHub Codespaces** if your workflow allows it  
- Alternative (if you really don't want VS Code Server on remote): sshfs + SFTP extension, but it's slower and less reliable than Remote-SSH

This is exactly the setup Karpathy described — local VS Code window + remote folder via SSH. It's extremely productive for working on GPU servers, clusters, cloud VMs, etc.

**References:**  

- [Remote Development using SSH - Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh)  
- [Remote - SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)