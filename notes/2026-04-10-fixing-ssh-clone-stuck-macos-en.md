---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing SSH Clone Stuck on macOS
translated: false
type: note
---

Question: Why is the Hermes Agent Installer stuck at "Trying SSH clone..." on macOS?

Answer:

The Hermes Agent Installer is stuck at the "Trying SSH clone..." step because the script is attempting to clone the Hermes repository using Git over SSH, but the SSH clone is failing (likely due to authentication issues, missing SSH keys, or GitHub SSH access problems), and the installer is not handling the failure gracefully. It appears to be hanging while waiting for an SSH prompt, SSH passphrase, or a timeout that never triggers properly.

### Common causes on macOS:
- **No SSH key set up for GitHub**: Git is trying to use SSH (git@github.com:...), but you don't have an SSH key added to your GitHub account or ssh-agent.
- **SSH agent not running or key not loaded**: Even if you have keys, they might not be loaded.
- **Firewall / network / VPN issues**: SSH connections to GitHub are being blocked or delayed.
- **Git configuration preferring SSH**: The installer or your global Git config forces SSH instead of HTTPS.
- **The script has a bug**: It tries SSH first and falls back to HTTPS, but the SSH attempt is hanging indefinitely (common if it's waiting for user input that isn't shown properly due to terminal issues).

### How to fix it:

1. **Quickest fix - Force HTTPS clone** (recommended):
   - Cancel the current installation (press Ctrl+C a few times).
   - Delete the partial install folder:
     ```
     rm -rf /Users/lzwjava/.hermes/hermes-agent
     ```
   - Then manually clone using HTTPS instead:
     ```
     git clone https://github.com/NousResearch/Hermes-Agent.git /Users/lzwjava/.hermes/hermes-agent
     ```
   - After cloning, continue the installation by running the installer again or following any remaining setup steps.

2. **Set up SSH properly** (if you prefer SSH):
   - Generate an SSH key if you don't have one:
     ```
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```
   - Add the key to ssh-agent:
     ```
     eval "$(ssh-agent -s)"
     ssh-add ~/.ssh/id_ed25519
     ```
   - Copy the public key and add it to your GitHub account (Settings → SSH and GPG keys).
   - Test SSH:
     ```
     ssh -T git@github.com
     ```
   - Then retry the installer.

3. **Other troubleshooting steps**:
   - Make sure Git is configured with your credentials:
     ```
     git config --global user.name "Your Name"
     git config --global user.email "your_email@example.com"
     ```
   - Update Git:
     ```
     brew upgrade git
     ```
   - Run the installer with more verbose output if possible (check if there's a `--verbose` flag or look at the installer script).
   - Temporarily disable SSH and force HTTPS by setting:
     ```
     git config --global url."https://github.com/".insteadOf git@github.com:
     ```

After fixing the clone, the installer should continue past that step.

If it still gets stuck, share the full installer output or the content of the installer script for more specific help.

References:  
- None (based on common Git/SSH issues on macOS)