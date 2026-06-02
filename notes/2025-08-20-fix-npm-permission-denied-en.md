---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix npm Permission Denied Error
translated: false
type: note
---

The error you're encountering, `EACCES: permission denied`, means your current user does **not have write permissions** to the `/usr/local/lib/node_modules` directory. This is a common issue when installing global npm packages on Linux or macOS.

### **How to Fix This Issue**

#### **Option 1: Use `sudo` (Not Recommended for Regular Use)**

You can use `sudo` to run the command as the root user, but this is **not recommended** for regular use, as it can lead to permission issues with npm packages later.

```bash
sudo npm install -g @anthropic-ai/claude-code
```

#### **Option 2: Change npm's Default Directory (Recommended)**

The best practice is to configure npm to use a directory in your home folder where you have write permissions.

1. **Create a global npm directory in your home folder:**

   ```bash
   mkdir ~/.npm-global
   ```

2. **Configure npm to use this directory:**

   ```bash
   npm config set prefix '~/.npm-global'
   ```

3. **Add the new directory to your `PATH`:**
   Open your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`, or `~/.profile`) and add this line:

   ```bash
   export PATH=~/.npm-global/bin:$PATH
   ```

   Then, reload your shell:

   ```bash
   source ~/.bashrc  # or ~/.zshrc, ~/.profile
   ```

4. **Retry the installation:**

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

#### **Option 3: Fix Permissions for `/usr/local` (Advanced)**

If you want to keep using `/usr/local`, you can change its ownership to your user:

```bash
sudo chown -R $(whoami) /usr/local/lib/node_modules
```

Then retry the installation.

---

**Recommendation:** Use **Option 2** to avoid permission issues in the future.
