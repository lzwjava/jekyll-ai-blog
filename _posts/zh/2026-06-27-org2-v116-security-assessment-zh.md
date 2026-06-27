---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ORG2 v1.1.6 安全评估
translated: true
type: note
---

现在我有足够的信息给你做一个全面的安全评估。以下是详细分析：

---

安全评估：ORG2（ORGII）v1.1.6

结论：整体设计良好，但存在一些值得关注的问题。可以使用，但需要了解其中的权衡。


## 产品概述

这是一款基于Tauri构建的桌面应用（Rust后端 + React前端），充当智能代理开发框架。它协调多个LLM提供商（OpenAI、Anthropic、Gemini、Codex、Claude Code、Copilot等），并将它们的API密钥存储在本地。


## 良好的安全实践

1. 凭据存储：密钥保存在~/.orgii/credentials.json文件中，权限设置为0o600（仅拥有者可读写）。采用原子写入模式（临时文件+重命名）防止数据损坏。

2. 敏感文件权限：在密钥库、代理CA、连接存储等场景中统一使用专用的set_sensitive_file_permissions()函数。支持跨平台（Unix 0o600，Windows icacls）。

3. MITM代理CA：自签名CA存储在~/.orgii/proxy/目录中，密钥文件权限设置正确。CA私钥不会全局可读。

4. 内容安全策略（CSP）：配置了相对严格的内容安全策略：
   - default-src 'self'
   - object-src 'none'
   - base-uri 'self'
   - connect-src限制为self、ipc、localhost和HTTPS

5. 自动更新：使用minisign公钥验证（来自GitHub的签名发布版本）。

6. 无第三方遥测/分析："analytics"模块是本地会话分析（工具使用情况、令牌数量、持续时间）——默认不会发送到外部服务。

7. 诊断上传：通过环境变量（ORGII_DIAGNOSTICS_ENDPOINT + ORGII_DIAGNOSTICS_TOKEN）选择启用。如果未配置端点，数据保留在本地。设有offline_mode标志。


## 问题点（按严重程度排序）

### 中等级别 —— 宽泛的Shell执行权限

在src-tauri/capabilities/default.json中：
```json
{
  "identifier": "shell:allow-execute",
  "allow": [
    { "name": "sh", "cmd": "sh", "args": true },
    { "name": "curl", "cmd": "curl", "args": true },
    { "name": "python3", "cmd": "python3", "args": true }
  ]
}
```
"args": true意味着参数不受限制。这实际上赋予了前端通过`sh -c "..."`执行任意shell命令的能力。虽然这是智能代理工具的设计需求，但一旦前端被攻破（XSS、恶意插件），攻击者将获得完整的shell访问权限。

### 中等级别 —— 非常宽泛的文件系统访问权限

来自capabilities/default.json：
- fs:allow-home-read-recursive —— 读取整个主目录
- fs:allow-home-write-recursive —— 写入主目录任何位置
- fs:allow-read-file with path: "**" —— 读取系统上任何文件
- fs:allow-write-text-file with path: "**" —— 写入任何文本文件

同样是代理功能的设计需求，但本质上等同于完整的文件系统访问权限。

### 中等级别 —— MITM代理拦截

对于Cursor、Copilot和Kiro等不支持自定义基础URL的代理，ORGII安装了一个本地MITM代理，使用自己的CA来拦截和重写HTTPS流量。位于src-tauri/crates/integrations/src/proxy/certificate_authority.rs的代码生成了一个根CA，可以为任何域签署证书。这对凭据注入来说是技术上必要的，但功能非常强大——如果CA密钥被泄露，所有通过代理路由的HTTPS流量都可能被拦截。

### 低级别 —— CSP允许内联样式和类似eval的结构

- style-src 'self' 'unsafe-inline' —— 允许内联CSS（通过CSS进行数据泄露的XSS向量，但限制较大）
- script-src 'self' 'wasm-unsafe-eval' —— WASM所需，但略微削弱了CSP
- connect-src包含http://127.0.0.1:*和ws://localhost:* —— 允许连接到任何本地端口

### 低级别 —— 密钥以明文JSON存储

API密钥以明文形式存储在~/.orgii/credentials.json中（受0o600权限保护）。这是桌面应用的标准做法（类似于AWS凭据的工作方式），但在共享机器上或如果恶意软件以您的用户身份运行时，密钥是可读的。

### 信息提示 —— 诊断系统

存在诊断/遥测系统，但设计合理：
- 需要显式设置ORGII_DIAGNOSTICS_ENDPOINT环境变量才能上传
- 提供offline_mode和diagnostics_level: Off选项
- 数据经过分桶/脱敏处理（CPU范围化、RAM范围化、持续时间范围化）
- 安装ID是随机UUID，不与个人身份关联
- 默认上传间隔为12小时

未设置环境变量时，不会有数据离开您的机器。


## 最终结论

是的，您可以使用它，但需要注意以下几点：

1. 这是一个代理平台——它需要shell和文件系统访问权限才能正常运行。这正是其核心功能。但请将其视为对主目录具有类似sudo级别访问权限的开发工具来对待。

2. 您的API密钥以明文形式存储在~/.orgii/credentials.json中。请确保您的用户账户安全（强密码、全盘加密）。

3. MITM代理仅在您使用Cursor/Copilot/Kiro CLI代理时激活。如果您只使用直接API密钥提供商（OpenAI、Anthropic等），它不会运行。

4. 除非您显式配置诊断端点，否则不会有数据发送到外部。

5. 代码质量可靠——Rust后端、正确的原子写入、互斥锁保护的存储、权限管理。这不是一个草率的Electron应用。

对于协调AI代理的本地优先开发工具来说，其安全态势是恰当的。广泛的权限是该产品功能的必要组成部分。