---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DMIT 防火墙 ACL 位置指南
translated: true
type: note
---

**问题：** 为什么在 DMIT.io 控制面板中找不到 firewall / ACL 部分来开放端口 13000-14000，即使我已经在 UFW 中允许了它们？

**回答：**

DMIT.io 宣传所有云 VM 实例都配备可自定义的前端（外部）firewall，支持 ACL rules，但根据当前公开信息和用户报告，客户端控制面板中管理这些 ACL rules 的确切位置和界面可能并不显眼，或者使用与预期不同的标签（例如，并非总是在主实例页面直接称为“Firewall”或“ACL Rules”）。

以下是您找不到它的最可能原因及解决步骤：

1. **检查控制面板中的正确位置**
   - 登录 <https://www.dmit.io/> 或您的计费/客户端区域（SolusVM、自定义面板或基于 WHMCS 的门户）。
   - 转到 **Services** → **My Services** → 选择您的特定云实例/VM。
   - 查找以下标签或部分：
     - "Firewall"
     - "Security"
     - "Network"
     - "ACL"
     - "Protection" / "DDoS Protection" / "Front Firewall"
     - "Advanced" 或 "Additional Features"
   - 一些提供商将高级 firewall 选项隐藏在“Manage”或“Console”按钮下，或在单独的“Security Group”区域中。如果不在那里，它可能仅在满足某些条件后出现（例如，启用 DDoS protection 后或特定计划）。

2. **外部 firewall 可能默认禁用或最小化**
   - 在某些 DMIT 计划中，前端 firewall 以非常宽松的规则启动（允许大多数入站流量）或主要用于 DDoS 过滤，而不是细粒度端口控制。
   - 如果没有显示自定义 ACL 界面，提供商可能不提供超出基本 DDoS 设置的用户可配置入站端口限制功能——这意味着外部端口默认开放，除非被其反 DDoS 层阻塞。

3. **您的问题几乎肯定不是 DMIT 外部 firewall**
   - 您已经运行：

     ```
     sudo ufw allow 13000:14000/tcp
     sudo ufw allow 13000:14000/udp
     sudo ufw reload
     ```

     但看到：**Firewall not enabled (skipping reload)**
   - 这意味着 **UFW 当前在您的 VPS 上处于禁用/非活动状态**。没有规则（即使是允许的规则）被强制执行，因为 firewall 未运行。
   - **首先修复这个问题**——这是即使添加规则后端口仍被阻塞的最常见原因：

     ```
     sudo ufw enable
     ```

     对提示回答“y”（它警告可能中断 SSH——确保您通过 DMIT 面板有控制台访问权限，以防锁死）。
     然后重新加载：

     ```
     sudo ufw reload
     ```

     验证状态：

     ```
     sudo ufw status verbose
     ```

     现在您应该看到 13000:14000 规则列为 ALLOW，并且 firewall 显示为“active”。

4. **启用 UFW 后测试连通性**
   - 从外部机器尝试：
     `telnet your-vps-ip 13000`（或使用 `nc -zv your-vps-ip 13000` 测试 TCP）
     如果连接成功，则端口已开放。
   - 如果仍关闭 → 仔细检查您测试的是正确的公网 IP（在 VPS 上运行 `curl ifconfig.me`）。

5. **如果您仍需要/想要配置 DMIT 前端 firewall**
   - 通过客户端区域直接提交支持工单（在“Support”或“Open Ticket”下）。询问：
     “如何访问并配置我的实例的可自定义前端 firewall ACL rules，以允许/拒绝特定入站端口或范围？”
   - DMIT 支持团队通常对这些问题很乐于助人，可以指导您找到确切的面板部分（或确认您的计划是否不可用户编辑）。

**总结**

- 首先启用 UFW（`sudo ufw enable`）——这是目前阻塞您端口的原因，而不是 DMIT 那边。
- DMIT 外部 ACL 界面按其网站存在，但可能难以找到或受限；如需使用支持团队。
- 向 0.0.0.0/0 开放像 1000 个端口这样的大范围很危险——如果您的应用允许，请限制源 IP。

**参考资料：**

- [DMIT 官方网站（提及可自定义 ACL 前端 firewall）](https://www.dmit.io/)
