---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale仪表盘概述
translated: true
type: note
---

**问题：** Tailscale管理面板的各个部分分别有什么作用？

**回答：**

Tailscale的管理仪表盘围绕三个层级组织：**网络可见性**（设备、用户、服务）、**访问策略**（ACL、应用）、**运维管理**（日志、DNS、设置）以及**计费**。

## 主导航

**设备**
列出所有已连接的设备（你的MacBook Air、192.168.1.36的工作站等）。显示Tailnet中的IP地址、连接状态、操作系统和最后在线时间。你可以在此处授权/取消授权设备、为设备打标签以控制访问权限，以及强制轮换密钥。

**应用**
Tailscale应用（Beta/早期访问功能）。允许你通过Tailnet公开HTTP应用，无需手动端口转发。你可以定义哪些设备上的哪些应用应当可访问，Tailscale会通过`app.tailnet-name.ts.net`域名处理DNS路由。

**服务**
通过Tailnet公开的SSH、HTTPS或自定义服务。补充了非HTTP协议的应用功能。适用于对多台设备需发现的服务进行广播。

**用户**
可访问你Tailnet的团队成员。显示邮箱、最后登录时间和MFA状态。你在此处管理邀请、移除用户并控制谁可以添加设备。

**访问控制（ACL）**
Tailnet的防火墙规则。使用HCL（HashiCorp配置语言）编写，定义了**谁可以连接什么**。例如：
```hcl
{
  "acls": [
    {
      "action": "accept",
      "src": ["tag:engineers"],
      "dst": ["tag:servers:*"]
    },
    {
      "action": "accept",
      "src": ["user:you@example.com"],
      "dst": ["tag:personal:*"]
    }
  ]
}
```
使用标签（分配给设备）和用户来制定策略。对零信任网络至关重要。

**日志**
Tailnet活动的审计轨迹——谁访问了什么、认证事件、设备注册、ACL变更。对排查连接问题或安全审计非常宝贵。

**DNS**
Tailnet的自定义DNS记录。你可以定义`internal-service.tailnet-name.ts.net`到设备IP的映射，或使用Tailscale的MagicDNS（自动解析设备名称）。同时显示全局域名服务器。

**设置 → Tailnet设置**
集群级配置：

- **通用**：Tailnet名称（自动生成）、共享设置、设备审批策略（自动批准或手动）、OIDC/OAuth提供商设置
- **用户管理**：SSO/SAML配置、基于角色的访问控制（RBAC）、谁可以添加设备
- **设备管理**：自动更新策略、设备过期时间、子网路由规则、出口节点（哪些设备充当Tailnet的出站网关）
- **策略文件管理**：ACL的Git集成——对访问规则进行版本控制
- **信任凭证**：基于证书的设备认证、用于Tailscale API调用的API密钥
- **Webhooks**：在Tailnet事件（添加设备、移除用户等）时触发外部系统
- **联系方式偏好**：电子邮件通知
- **计费**：套餐、席位限制、使用量

**设置 → 个人设置**
你的账户层级：

- **密钥**：生成**认证密钥**（用于CI/CD、无头设备配置）和**API密钥**（用于脚本化Tailscale API）。对自动化至关重要。

## 实际用例

**你的配置（MacBook Air + 工作站）：**
- 设备：两者都应出现在此处
- ACL：将工作站标记为`tag:gpu`，将GPU任务限制为仅你的用户
- DNS：添加`gpu.local`指向工作站IP
- 密钥：为无头AMD Dev Cloud实例生成认证密钥，使其自动加入Tailnet

**适用于你工作流的ACL示例：**
```hcl
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:self"],
      "dst": ["autogroup:self:*"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["tag:gpu:*"]
    }
  ]
}
```

**用于CLI自动化（ww, iclaw, zz）：**
在**设置→个人设置→密钥**中生成一个认证密钥，然后执行：
```bash
tailscale up --authkey=<密钥> --hostname=automation-box
```

你的免费套餐：6个用户、50个标记资源、无限设备。对单工程师加计算集群来说绰绰有余。