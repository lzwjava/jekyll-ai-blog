---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复VSCode代理弹窗
translated: true
type: note
---

**问题：** 为什么在企业环境中即使配置了代理设置，VSCode 仍持续弹出代理对话框？

**回答：**

VSCode 的代理处理分散在多个层级，任何一层的配置错误都会导致重复提示。以下是实际原因及正确修复方法。

## 根本问题

VSCode 并非只有单一的代理设置——不同组件独立处理代理：

1. **VSCode 自身**（Electron）
2. **Node.js 进程**（扩展、语言服务器）
3. **Git**（用于源代码管理）
4. **扩展**（可能包含自己的代理逻辑）

如果只配置了其中一层，其他层会失败并提示输入凭据。

## 正确的代理配置方法

### 1. **VSCode 设置**（`settings.json`）

```json
{
  "http.proxy": "http://<代理主机>:<端口>",
  "https.proxy": "http://<代理主机>:<端口>",
  "http.proxyStrictSSL": false,
  "http.proxyAuthorization": true,
  "http.proxySupport": "override"
}
```

关键细节：如果代理需要认证，**不要将凭据直接嵌入 settings.json**。VSCode 会提示一次，然后将其缓存到凭据存储中。

### 2. **环境变量**（对 Node/Git 至关重要）

在启动 VSCode 前设置：

```bash
export HTTP_PROXY="http://<代理主机>:<端口>"
export HTTPS_PROXY="http://<代理主机>:<端口>"
export NO_PROXY="localhost,127.0.0.1"
export NODE_TLS_REJECT_UNAUTHORIZED=0  # 仅当使用自签名证书时
```

如果代理需要认证：

```bash
export HTTP_PROXY="http://<用户名>:<密码>@<代理主机>:<端口>"
export HTTPS_PROXY="http://<用户名>:<密码>@<代理主机>:<端口>"
```

**更好的方法**——使用无需嵌入凭据的代理（NTLM/域认证由操作系统处理），或将凭据存储在 `~/.netrc` 中：

```
machine <代理主机>
login <用户名>
password <密码>
```

然后启动 VSCode：

```bash
code  # 会读取环境变量和 .netrc
```

### 3. **Git 配置**

企业环境中的 Git 代理问题常常独立存在：

```bash
git config --global http.proxy "http://<代理主机>:<端口>"
git config --global https.proxy "http://<代理主机>:<端口>"
git config --global http.sslVerify false
```

或者如果企业使用 NTLM/域认证：

```bash
git config --global http.proxy "http://<域>\\<用户名>:<密码>@<代理主机>:<端口>"
```

### 4. **针对企业 HTTPS 检查（中间人代理）**

如果你的企业会检查 HTTPS 流量（中间人解密），请导入企业 CA 证书：

```bash
# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /path/to/corporate-ca.crt

# Linux
sudo cp /path/to/corporate-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Windows（PowerShell）
Import-Certificate -FilePath "C:\path\to\corporate-ca.crt" -CertStoreLocation "Cert:\CurrentUser\Root"
```

然后 VSCode 可以安全地验证 SSL，同时设置 `"http.proxyStrictSSL": true`。

### 5. **对特定主机禁用代理**（如需要）

```json
{
  "http.proxyAuthorization": true,
  "http.noProxy": "*.internal.company.com,localhost,127.0.0.1,192.168.x.x"
}
```

## 调试清单

如果弹窗持续出现：

1. **检查 VSCode 实际看到的内容：**

   ```bash
   code --verbose 2>&1 | grep -i proxy
   ```

2. **确认环境变量已加载：**

   ```bash
   env | grep -i proxy
   ```

3. **直接测试代理：**

   ```bash
   curl -x http://<代理主机>:<端口> https://api.github.com
   ```

4. **禁用扩展**（某些扩展会覆盖代理逻辑）——通过命令面板以安全模式重新加载 VSCode。

5. **清除缓存的凭据：**
   - macOS：钥匙串 → 删除 VSCode 条目
   - Linux：`~/.config/Code/User/globalStorage` → 删除凭据缓存
   - Windows：凭据管理器 → 删除 VSCode 条目

## 终极方案

如果以上方法均失败，且你在自己控制的机器上，可以使用本地代理隧道（更易于调试）：

```bash
# 使用本地 SOCKS 代理或 tinyproxy
# 将全部流量通过企业代理转发
tinyproxy -r <代理主机> -p 8888

# 然后在 VSCode 中设置：
# "http.proxy": "http://127.0.0.1:8888"
```

这样可将 VSCode 与企业代理的复杂性隔离开，并提供一个单一控制点。

---

**参考链接：**

- [VSCode HTTP 代理设置](https://code.visualstudio.com/docs/setup/network)
- [Node.js 代理配置](https://nodejs.org/en/docs/guides/nodejs-behind-a-corporate-proxy/)
