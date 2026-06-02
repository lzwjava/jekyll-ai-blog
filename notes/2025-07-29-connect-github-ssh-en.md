---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connect to GitHub with SSH
translated: false
type: note
---

To connect to GitHub using SSH, follow these steps based on the provided GitHub documentation. This guide assumes you’re starting from scratch and includes checking for existing keys, generating a new key, adding it to GitHub, and testing the connection.

### 1. Check for Existing SSH Keys

Before creating a new SSH key, check if you already have one:

- Open a terminal (on macOS/Linux) or Git Bash (on Windows).
- Run:

  ```bash
  ls -al ~/.ssh
  ```

- Look for files like `id_rsa` and `id_rsa.pub` (or similar, e.g., `id_ed25519`, `id_ed25519.pub`). If they exist, you may already have a key. If you want to use an existing key, skip to step 3. If not, proceed to generate a new key.

### 2. Generate a New SSH Key

If you don’t have an SSH key or want a new one:

- In your terminal, generate a new SSH key:

  ```bash
  ssh-keygen -t ed25519 -C "your_email@example.com"
  ```

  - Replace `your_email@example.com` with the email associated with your GitHub account.
  - If your system doesn’t support `ed25519`, use:

    ```bash
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```

- When prompted, press Enter to save the key in the default location (`~/.ssh/id_ed25519` or `~/.ssh/id_rsa`).
- Optionally, enter a passphrase for extra security (or press Enter for none).

### 3. Add the SSH Key to the SSH Agent

The SSH agent manages your keys for authentication:

- Start the SSH agent:

  ```bash
  eval "$(ssh-agent -s)"
  ```

- Add your private key to the agent:

  ```bash
  ssh-add ~/.ssh/id_ed25519
  ```

  - If you used RSA, replace `id_ed25519` with `id_rsa`.
- If you set a passphrase, you’ll be prompted to enter it.

### 4. Add the SSH Key to Your GitHub Account

- Copy your public key to the clipboard:
  - On macOS:

    ```bash
    pbcopy < ~/.ssh/id_ed25519.pub
    ```

  - On Linux:

    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```

    Then manually copy the output.
  - On Windows (Git Bash):

    ```bash
    cat ~/.ssh/id_ed25519.pub | clip
    ```

  - If you used RSA, replace `id_ed25519.pub` with `id_rsa.pub`.
- Go to GitHub:
  - Log in to [GitHub](https://github.com).
  - Click your profile picture (top-right) → **Settings** → **SSH and GPG keys** → **New SSH key** or **Add SSH key**.
  - Paste your public key in the “Key” field, give it a title (e.g., “My Laptop”), and click **Add SSH key**.

### 5. Test Your SSH Connection

Verify that your SSH key works with GitHub:

- Run:

  ```bash
  ssh -T git@github.com
  ```

- If prompted, confirm by typing `yes`.
- You should see a message like:

  ```
  Hi username! You've successfully authenticated, but GitHub does not provide shell access.
  ```

  This confirms your SSH connection is working.

### 6. Configure Git to Use SSH

Ensure your Git repository uses SSH for authentication:

- Check your repository’s remote URL:

  ```bash
  git remote -v
  ```

- If the URL starts with `https://`, change it to SSH:

  ```bash
  git remote set-url origin git@github.com:username/repository.git
  ```

  - Replace `username/repository` with your GitHub username and repository name.

### 7. Optional: Manage SSH Key Passphrases

If you set a passphrase, you can configure the SSH agent to avoid reentering it:

- On macOS, add your key to the keychain:

  ```bash
  ssh-add --apple-use-keychain ~/.ssh/id_ed25519
  ```

- On Linux/Windows, the SSH agent typically prompts for the passphrase only once per session.

### 8. Optional: Use SSH Agent Forwarding or Deploy Keys

- **SSH Agent Forwarding**: If you’re deploying to a server, enable agent forwarding to use your local SSH keys securely. Add to your `~/.ssh/config`:

  ```bash
  Host example.com
      ForwardAgent yes
  ```

  Replace `example.com` with your server’s hostname.
- **Deploy Keys**: For automated scripts, generate a separate SSH key for each server and add it as a deploy key in your GitHub repository settings.

### Troubleshooting

- If `ssh -T git@github.com` fails, ensure:
  - Your public key is correctly added to GitHub.
  - The SSH agent is running and your key is added (`ssh-add -l` to list loaded keys).
  - File permissions are correct:

    ```bash
    chmod 600 ~/.ssh/id_ed25519
    chmod 644 ~/.ssh/id_ed25519.pub
    ```

- For further issues, check GitHub’s troubleshooting guide.

Now you can use SSH to interact with GitHub securely without entering credentials repeatedly.

[Connecting to GitHub with SSH - GitHub Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
