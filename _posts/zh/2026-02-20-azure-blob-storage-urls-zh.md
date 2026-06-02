---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Azure Blob 存储 URL 解析
translated: true
type: note
---

是的，您提供的 URL 表明该图像存储在 **Microsoft Azure Blob Storage** 中。以下是 URL 及其参数的详细解析，说明其工作原理：

---

### **1. URL 结构**

```
https://mistralaichatupprodswe.blob.core.windows.net/chat-images/assistant/be/75/da/be75da1d-cd84-46ef-a1a5-0fb7427ad357/01a20d1d-beff-430b-a263-55670cb3cc4f/3435c442-534e-4046-8238-4cf1e062d038/5b528d38-7a4a-495a-a832-9ca833506521.webp
```

- **`mistralaichatupprodswe.blob.core.windows.net`**：这是 Azure Blob Storage 的端点，格式为 `<账户名称>.blob.core.windows.net`。
- **`chat-images/assistant/...`**：这是容器中 blob（文件）的路径。Azure Blob Storage 将文件组织在容器中，此路径代表虚拟目录结构。

---

### **2. 查询参数（SAS 令牌）**

问号 `?` 后的查询字符串是 **Shared Access Signature (SAS) 令牌**，提供对 blob 的安全、限时访问权限。以下是各参数的含义：

| 参数 | 值 | 用途 |
|------|----|------|
| `sv` | `2025-01-05` | SAS 版本（生成令牌时使用的 API 版本） |
| `st` | `2026-02-19T18:46:54Z` | SAS 令牌生效的起始时间（UTC） |
| `se` | `2026-02-19T19:46:54Z` | SAS 令牌失效的到期时间（UTC） |
| `sr` | `b` | 资源类型：`b` = blob（文件） |
| `sp` | `rade` | 权限：`r` = 读取，`a` = 添加，`d` = 删除，`e` = 列出（但此处仅 `r` 和 `d` 相关） |
| `sig` | `NmXKg4mPgJtSswAcsOyt4O%2FdTaMctjMyRa8Cc5V9Td4%3D` | 用于身份验证的 HMAC-SHA256 签名 |

---

### **3. 工作原理**

- **访问控制**：SAS 令牌允许在不提供 Azure 凭据的情况下，临时、受控地访问 blob。任何拥有此 URL 的人都可在指定时间窗口（`st` 至 `se`）内访问 blob。
- **安全性**：`sig` 参数是使用存储账户密钥生成的加密签名，确保令牌未被篡改。
- **权限**：`sp=rade` 参数授予 **读取** 和 **删除** 权限，但实际共享图像时通常仅使用 **读取** 权限。

---

### **4. 为何使用 Azure Blob Storage？**

- **可扩展性**：Azure Blob Storage 旨在处理海量非结构化数据（如图像、视频等）。
- **全球访问**：文件可通过 HTTP/HTTPS 在任何地方访问。
- **成本效益**：仅按实际使用的存储空间和带宽付费。

---

### **5. 实际影响**

- **临时访问**：该 URL 将在 `2026-02-19T19:46:54Z`（生成后 1 小时）后失效。
- **无需身份验证**：任何拥有该 URL 的人都可在有效时间窗口内访问图像。

---

**总结**：这是一个通过 SAS 令牌进行身份验证和权限控制的 Azure Blob Storage 图像访问 URL，具有安全性和时效性。若需在令牌过期后继续访问图像，则需生成新的 SAS 令牌。
