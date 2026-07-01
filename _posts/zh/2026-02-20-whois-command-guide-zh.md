---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whois 命令必备指南
translated: true
type: note
---

**`whois`** 命令是一种广泛使用的网络管理工具，用于查询存储互联网资源（如域名、IP 地址块或自治系统号）注册用户或分配者信息的数据库。以下是 `whois` 命令的全面介绍：

---

## **1. `whois` 的用途**

- **域名查询**：获取域名所有者、注册日期、到期日期和名称服务器等信息。
- **IP 地址查询**：识别负责某个 IP 地址或地址块的组织或 ISP。
- **网络故障排除**：通过识别特定资源的负责方帮助诊断网络问题。
- **安全研究**：调查可疑域名或 IP 地址的潜在威胁。

---

## **2. `whois` 的工作原理**

- `whois` 命令查询由**注册机构**（如 ICANN、RIPE、ARIN、APNIC）和**注册管理机构**（如 `.com` 域名的 Verisign）维护的 **WHOIS 数据库**。
- 响应内容包括：
  - 注册人（所有者）信息
  - 管理和技术联系方式
  - 注册和到期日期
  - 名称服务器
  - 域名状态（如活动、过期、锁定）

---

## **3. 基本语法**

```bash
whois [选项] <域名或IP>
```

### 常用选项

| 选项 | 描述 |
| ------ | ------ |
| `-h <服务器>` | 查询特定 WHOIS 服务器（如 `-h whois.verisign-grs.com`）。 |
| `-v` | 详细输出（显示更多细节）。 |
| `-H` | 隐藏法律免责声明。 |
| `-r` | 禁用递归查询（仅显示顶级注册机构）。 |

---

## **4. 示例**

### **域名查询**

```bash
whois example.com
```

**输出**：

- 注册机构：GoDaddy/Namecheap 等
- 创建/到期日期
- 名称服务器
- 注册人联系信息（如未隐私保护）

### **IP 地址查询**

```bash
whois 8.8.8.8
```

**输出**：

- 组织：Google LLC
- 网络范围：8.8.8.0 - 8.8.8.255
- 滥用联系方式

### **查询特定 WHOIS 服务器**

```bash
whois -h whois.ripe.net 193.0.0.0
```

**输出**：

- RIPE NCC 数据库中的详细信息（适用于欧洲 IP 范围）。

---

## **5. WHOIS 隐私（GDPR/代理服务）**

- 许多注册机构提供 **WHOIS 隐私**服务（如 Domains By Proxy）以隐藏注册人详情。
- 自 **GDPR（2018）** 以来，欧盟域名的 WHOIS 记录中个人数据通常被隐去。
- 如需完整详情，可能需要：
  - 直接联系注册机构。
  - 使用 **RDAP**（注册数据访问协议），这是 WHOIS 的现代替代方案。

---

## **6. WHOIS 替代方案**

- **RDAP**：结构化且符合隐私法规（如 `curl https://rdap.verisign.com/com/v1/domain/example.com`）。
- **在线工具**：[ICANN 查询](https://lookup.icann.org/) 或 [ARIN](https://www.arin.net/) 等网站。
- **编程 API**：WhoisXML API 或 DomainTools 等服务。

---

## **7. 限制**

- **数据不完整**：部分注册机构会隐去或省略详情。
- **查询限制**：频繁查询可能被封锁。
- **非实时**：数据可能过时。

---

## **8. 实际应用场景**

- **网络安全**：调查恶意域名或 IP。
- **域名获取**：检查域名是否可用或即将到期。
- **网络调试**：识别 ISP 或托管提供商。

---

## **9. 安装 `whois`**

- **Linux/macOS**：通常预装。如未安装：

  ```bash
  sudo apt install whois  # Debian/Ubuntu
  brew install whois      # macOS
  ```

- **Windows**：使用第三方工具（如 [Sysinternals WHOIS](https://learn.microsoft.com/en-us/sysinternals/)）或在线服务。

---

是否需要深入了解某些特定方面，如以编程方式解析 WHOIS 输出或使用 RDAP？
