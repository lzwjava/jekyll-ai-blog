---
audio: false
generated: true
lang: en
layout: post
title: Git Credential Manager
translated: false
type: note
---

You're using **Git Credential Manager (GCM) version 2.6.1** on **macOS**, and you've encountered an issue where `git config --global credential.helper manager-core` throws an error:

```
warning: credential.helper has multiple values
error: cannot overwrite multiple values with a single value
```

This happens because multiple credential helpers are already set in your Git configuration. You need to **clear the existing values** before setting a new one.

---

### **🛠 Fix the Issue: Reset Credential Helper**

#### **Step 1: Check Current Credential Helpers**

Run:

```sh
git config --global --get-all credential.helper
```

This will list all configured credential helpers.

#### **Step 2: Unset Previous Credential Helpers**

Reset all credential helpers using:

```sh
git config --global --unset-all credential.helper
```

#### **Step 3: Set GCM as the Only Credential Helper**

Now, set **Git Credential Manager (GCM)** as the helper again:

```sh
git config --global credential.helper manager-core
```

#### **Step 4: Verify the Change**

Check if it's correctly set:

```sh
git config --global --get credential.helper
```

Expected output:

```
manager-core
```

---

### **🛠 Alternative: Use `--replace-all`**

If you want to overwrite existing values instead of unsetting them first, use:

```sh
git config --global --replace-all credential.helper manager-core
```

---

### **🧩 Extra Debugging**

If you're still having issues, you can check your full Git global config:

```sh
git config --global --list
```

If the issue persists, let me know! 🚀

---

Git Credential Manager (GCM) is a secure Git credential helper that stores and manages authentication credentials for HTTPS Git repositories. It works with services like GitHub, GitLab, Bitbucket, and Azure DevOps.

---

## **1. Install Git Credential Manager**

GCM is included with Git for Windows and the official Git distributions for macOS and Linux. If it's not installed, download it from:

🔗 **[Git Credential Manager on GitHub](https://github.com/GitCredentialManager/git-credential-manager)**

### **Check if GCM is installed**

Run:

```sh
git credential-manager version
```

If it's installed, you'll see a version number. If not, install it manually.

---

## **2. Configure Git to Use GCM**

Run the following command:

```sh
git config --global credential.helper manager
```

For macOS/Linux, use:

```sh
git config --global credential.helper manager-core
```

To check the current credential helper:

```sh
git config --global credential.helper
```

---

## **3. Authenticate with a Git Server**

Once configured, the first time you interact with a remote repository over HTTPS (e.g., `git clone`, `git pull`), GCM will prompt you for credentials.

- If using GitHub, GitLab, or Bitbucket, GCM will open a browser for OAuth authentication.
- If using a personal access token (PAT), enter it instead of a password.

---

## **4. Store and Manage Credentials**

GCM securely stores credentials in the OS's credential store:

- **Windows**: Windows Credential Manager
- **macOS**: macOS Keychain
- **Linux**: GPG-encrypted file (`~/.git-credentials` or `~/.gitconfig`)

To manually add a credential:

```sh
git credential approve
```

To remove a stored credential:

```sh
git credential reject https://github.com
```

To clear all credentials:

```sh
git credential reject
```

---

## **5. Using Git Credential Manager with Different Git Providers**

### **GitHub**

Use a **Personal Access Token (PAT)** instead of a password:

```sh
git credential reject https://github.com
git pull
```

You'll be prompted to log in and enter your token.

### **GitLab**

For GitLab, use OAuth or a **PAT**:

```sh
git credential reject https://gitlab.com
git pull
```

### **Azure DevOps**

Use a **PAT** or Azure authentication.

---

## **6. Debugging Issues**

If credentials are not saved or retrieved correctly:

1. Check the credential helper:

   ```sh
   git config --global credential.helper
   ```

2. Reset Git Credential Manager:

   ```sh
   git credential reject https://your-git-service.com
   ```

3. Reinstall GCM if needed.

Would you like help configuring it for a specific service? 🚀
