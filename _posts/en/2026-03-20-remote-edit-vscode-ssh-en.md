---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Edit Files Using VS Code SSH
translated: false
type: note
---

Question: How to use VS Code to remotely edit files on a server?

Answer:

The best and most popular way to remotely edit files on a server using **Visual Studio Code** is the official **Remote - SSH** extension. It gives you a full VS Code experience on the remote machine (IntelliSense, debugging, terminal, extensions, etc.).

### Step-by-step guide (2025–2026 method)

1. **Prerequisites**
   - VS Code installed on your local computer
   - SSH server running on the remote machine (almost all Linux servers have it)
   - You can already connect via terminal using `ssh user@server-ip` (very important to test first!)

2. **Install the Remote - SSH extension**
   - Open VS Code
   - Go to Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on Mac)
   - Search for **Remote - SSH**
   - Install the one published by **Microsoft** (ms-vscode-remote.remote-ssh)

3. **(Recommended) Set up SSH key authentication**
   Password login works, but keys are much more convenient and secure.

   On your **local** machine:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location & no passphrase (or set one)
   ```

   Copy public key to server (easiest way):
   ```bash
   ssh-copy-id user@your-server-ip
   ```

   Or manually:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # copy output → paste into server's ~/.ssh/authorized_keys
   ```

4. **Configure SSH connection in VS Code**
   Two main ways:

   **Way A – Quick (recommended for most people)**

   - Press `Ctrl+Shift+P` → type **Remote-SSH: Connect to Host...**
   - Select **Add New SSH Host...**
   - Enter: `ssh user@server-ip -p 22` (or just `user@server-ip` if port 22)
   - Choose config file location (usually `~/.ssh/config` on Linux/Mac or `%USERPROFILE%\.ssh\config` on Windows)
   - VS Code adds an entry like this:

     ```text
     Host my-server
         HostName 192.168.1.150     # or domain.com
         User yourusername
         Port 22
         # Optional: IdentityFile ~/.ssh/id_ed25519
     ```

   **Way B – Manual edit** (more control)

   Open/create file `~/.ssh/config` and add:

   ```text
   Host myserver
       HostName 123.45.67.89
       User devuser
       Port 2222                # only if not default 22
       IdentityFile ~/.ssh/id_ed25519
   ```

5. **Connect**
   - `Ctrl+Shift+P` → **Remote-SSH: Connect to Host...**
   - Select your host (e.g. `myserver` or `user@ip`)
   - First time: VS Code installs its server component on the remote machine (~/.vscode-server)
   - Wait 30–90 seconds (only first time)

6. **Open folder and start editing**
   - After connection → you see green bar at bottom left ("SSH: myserver")
   - `File → Open Folder...` → browse remote filesystem → select project folder
   - Or drag folder from Remote Explorer sidebar
   - Now edit files normally — save = saved directly on server

7. **Useful features once connected**
   - Integrated terminal (`Ctrl+``) → runs on server
   - Install extensions remotely (look for "Install in SSH" button)
   - Debugging, Git, tasks.json, etc. all work on remote
   - Multiple hosts → use Remote Explorer sidebar

### Quick Troubleshooting Tips

- Connection fails? → Test `ssh user@server` in terminal first
- Very slow? → Check network, or add to `settings.json`:
  ```json
  "remote.SSH.useLocalServer": true,
  "remote.SSH.connectTimeout": 60
  ```
- Permission denied? → Fix SSH keys or password
- VS Code server install fails? → Server needs ~150–300 MB disk space + internet (to download once)

### Alternative (if you cannot install anything on server)

Use **SSH FS** extension — it mounts remote folder via SFTP/SSHFS. Less powerful (no full remote extensions/debugging), but zero installation on server.

References:

- [Official VS Code Remote - SSH documentation](https://code.visualstudio.com/docs/remote/ssh)
- [Remote SSH tutorial](https://code.visualstudio.com/docs/remote/ssh-tutorial)
