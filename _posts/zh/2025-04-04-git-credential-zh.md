---
audio: false
generated: true
lang: zh
layout: post
title: Git 凭据管理器
translated: true
type: note
---

你正在 **macOS** 上使用 **Git Credential Manager (GCM) 2.6.1 版本**，并且遇到了执行 `git config --global credential.helper manager-core` 时报错的问题：

```
warning: credential.helper has多个值
error: 无法用单个值覆盖多个值
```

这是因为你的 Git 配置中已经设置了多个凭据助手。在设置新的助手之前，你需要**清除现有的值**。

---

### **🛠 修复问题：重置凭据助手**

#### **步骤 1：检查当前的凭据助手**

运行：

```sh
git config --global --get-all credential.helper
```

这将列出所有已配置的凭据助手。

#### **步骤 2：取消设置之前的凭据助手**

使用以下命令重置所有凭据助手：

```sh
git config --global --unset-all credential.helper
```

#### **步骤 3：将 GCM 设置为唯一的凭据助手**

现在，重新将 **Git Credential Manager (GCM)** 设置为助手：

```sh
git config --global credential.helper manager-core
```

#### **步骤 4：验证更改**

检查是否正确设置：

```sh
git config --global --get credential.helper
```

预期输出：

```
manager-core
```

---

### **🛠 替代方法：使用 `--replace-all`**

如果你想直接覆盖现有值而不是先取消设置，可以使用：

```sh
git config --global --replace-all credential.helper manager-core
```

---

### **🧩 额外调试**

如果问题仍然存在，你可以检查完整的 Git 全局配置：

```sh
git config --global --list
```

如果问题持续，请告诉我！🚀

---

Git Credential Manager (GCM) 是一个安全的 Git 凭据助手，用于存储和管理 HTTPS Git 仓库的身份验证凭据。它支持 GitHub、GitLab、Bitbucket 和 Azure DevOps 等服务。

---

## **1. 安装 Git Credential Manager**

GCM 已包含在 Git for Windows 以及官方的 macOS 和 Linux Git 发行版中。如果未安装，请从以下地址下载：

🔗 **[Git Credential Manager on GitHub](https://github.com/GitCredentialManager/git-credential-manager)**

### **检查 GCM 是否已安装**

运行：

```sh
git credential-manager version
```

如果已安装，你将看到版本号。如果未安装，请手动安装。

---

## **2. 配置 Git 使用 GCM**

运行以下命令：

```sh
git config --global credential.helper manager
```

对于 macOS/Linux，使用：

```sh
git config --global credential.helper manager-core
```

检查当前的凭据助手：

```sh
git config --global credential.helper
```

---

## **3. 与 Git 服务器进行身份验证**

配置完成后，首次通过 HTTPS 与远程仓库交互时（例如 `git clone`、`git pull`），GCM 将提示你输入凭据。

- 如果使用 GitHub、GitLab 或 Bitbucket，GCM 将打开浏览器进行 OAuth 身份验证。
- 如果使用个人访问令牌 (PAT)，请输入令牌而不是密码。

---

## **4. 存储和管理凭据**

GCM 将凭据安全地存储在操作系统的凭据存储中：

- **Windows**：Windows 凭据管理器
- **macOS**：macOS 钥匙串
- **Linux**：GPG 加密文件 (`~/.git-credentials` 或 `~/.gitconfig`)

手动添加凭据：

```sh
git credential approve
```

删除存储的凭据：

```sh
git credential reject https://github.com
```

清除所有凭据：

```sh
git credential reject
```

---

## **5. 在不同 Git 提供商中使用 Git Credential Manager**

### **GitHub**

使用**个人访问令牌 (PAT)** 而不是密码：

```sh
git credential reject https://github.com
git pull
```

系统将提示你登录并输入令牌。

### **GitLab**

对于 GitLab，使用 OAuth 或 **PAT**：

```sh
git credential reject https://gitlab.com
git pull
```

### **Azure DevOps**

使用 **PAT** 或 Azure 身份验证。

---

## **6. 调试问题**

如果凭据未正确保存或检索：

1. 检查凭据助手：

   ```sh
   git config --global credential.helper
   ```

2. 重置 Git Credential Manager：

   ```sh
   git credential reject https://your-git-service.com
   ```

3. 如有需要，重新安装 GCM。

需要为特定服务配置帮助吗？🚀
