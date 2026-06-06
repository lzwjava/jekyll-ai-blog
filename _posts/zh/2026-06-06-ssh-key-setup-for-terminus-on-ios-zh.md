---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Terminus在iOS上的SSH密钥设置
translated: true
type: note
---

问题：如何在iOS上使用Tailscale设置Terminus，以避免每次输入密码提示？

答案：

出现密码提示是因为**Terminus使用的是密码认证而非SSH密钥认证**。每次会话都需要手动认证。通过设置基于密钥的认证来解决此问题。

## 设置：Terminus + Tailscale 的密钥认证

### 第一步：生成SSH密钥（在您的工作站上，而非iOS）

```bash
ssh-keygen -t ed25519 -f ~/.ssh/terminus_ios -C "terminus@ios"
# 不要设置密码（否则Terminus会要求输入）
```

### 第二步：将公钥添加到服务器

```bash
cat ~/.ssh/terminus_ios.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

首先在工作站上验证：

```bash
ssh -i ~/.ssh/terminus_ios user@192.168.1.36  # 应该不需要输入密码
```

### 第三步：将密钥导入Terminus（iOS）

1. **将私钥复制到iOS**（最简单的方式：通过AirDrop或邮件发送给自己）

   ```bash
   cat ~/.ssh/terminus_ios | pbcopy  # macOS：复制到剪贴板
   ```

2. **在Terminus应用中：**
   - 设置 → SSH Keys → 添加密钥
   - 粘贴**私钥**内容
   - 命名为：`terminus_ios`
   - 保存

3. **创建主机配置：**
   - 主机 → 添加
   - 主机：`workstation`（或Tailscale IP，如`100.x.x.x`）
   - 用户：`your_username`
   - 端口：`22`
   - 认证：选择`terminus_ios`密钥
   - 保存

### 第四步：通过Tailscale连接

在Terminus中，使用您的**Tailscale IP**（例如`100.97.x.x`）而不是局域网IP：

```
ssh user@100.97.x.x
```

或者如果Tailscale DNS正常，使用机器名称：

```
ssh user@lzw.tail123456.ts.net
```

---

## 为什么仍然提示输入密码

**常见原因：**

1. **在Terminus主机配置中未选择密钥**——确认“认证”设置为您的密钥而非“密码”
2. **私钥格式不匹配**——Terminus偏好OpenSSH格式（检查密钥头部：`-----BEGIN OPENSSH PRIVATE KEY-----`）
3. **服务器未重新加载`authorized_keys`**——SSH守护进程有缓存；必要时重启：

   ```bash
   sudo systemctl restart sshd  # Linux
   ```

4. **服务器权限错误**——必须设置为：

   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

---

## Terminus + Tailscale 工作流程（实用）

配置完成后：

```bash
# 在iOS的Terminus中，直接点击主机
# 或者如果使用命令行模式：
ssh workstation
# 立即连接，无需密码

# Ctrl+C 用于中断
# 长按菜单查看更多选项（复制、粘贴等）
```

**专业提示：** 如果Tailscale IP会变更（尽管通常不会），可在Terminus中设置 `StrictHostKeyChecking=no`：

```bash
# 在Terminus高级设置中，添加到SSH配置：
Host *.tail123456.ts.net
    StrictHostKeyChecking=accept-new
```

---

## 为什么不再每次都输入密码？

一旦密钥被添加到 `authorized_keys`，SSH将执行**公钥认证**——iOS客户端证明它拥有私钥但不会传输私钥。服务器使用公钥进行验证。握手完成，会话建立。无需密码。

**性能说明：** Tailscale 通过网络高效路由；通过Tailscale的iOS↔工作站连接速度几乎与直接SSH一样快。
