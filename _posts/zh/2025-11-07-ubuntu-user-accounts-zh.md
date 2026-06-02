---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 创建Ubuntu用户账户
translated: true
type: note
---

### 在 Ubuntu Linux 中创建新用户

Ubuntu 提供了命令行和图形界面两种创建用户的方式。命令行方法简单直接，适用于所有版本（包括服务器版），而图形界面方法仅适用于桌面版。

#### 命令行方法（推荐）
1. 打开终端（Ctrl+Alt+T）
2. 运行以下命令，将 `username` 替换为期望的用户名：
   ```
   sudo adduser username
   ```
   - 系统将提示为新用户设置强密码
   - 随后会询问可选信息（如全名、房间号、工作电话等），按 Enter 跳过或按需填写
3. （可选）授予新用户管理员权限：
   ```
   sudo usermod -aG sudo username
   ```
   - 该命令将用户加入 `sudo` 用户组，使其能够执行需要提升权限的命令

新用户的家目录将位于 `/home/username`，并可立即登录系统。

#### 图形界面方法（仅限桌面版）
1. 打开**设置**应用（可通过活动概览搜索）
2. 在侧边栏中进入**用户**选项
3. 点击右上角的**解锁**按钮并输入管理员密码
4. 点击**添加用户**
5. 填写账户类型（标准用户或管理员）、全名、用户名和密码
6. 点击**添加**

#### 验证操作
- 使用 `su - username` 切换用户，或注销后重新登录
- 通过 `cat /etc/passwd | grep username` 查看用户信息

本操作指南适用于 Ubuntu 24.04 LTS 及后续版本。

[用户管理 - Ubuntu 服务器文档](https://documentation.ubuntu.com/server/how-to/security/user-management/)
[添加新用户账户 - Ubuntu 官方文档](https://help.ubuntu.com/stable/ubuntu-help/user-add.html.en)
