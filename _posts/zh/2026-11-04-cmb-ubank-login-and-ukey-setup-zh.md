---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 招商银行UBank登录与UKey设置
translated: true
type: note
---

**问题：** 招商银行UBank企业银行的登录用户名格式是什么，以及如何设置U盾？

**答案：**

## 登录用户名格式

对于招商银行UBank企业银行，登录标识并不是字面上的“公司名+用户名”的自由文本。实际格式是：

- **企业编号 (Company Code)** — 公司在开立企业银行账户时由招商银行分配的数字代码
- **操作员编号 / 用户名 (Operator Code / Username)** — 为每个用户（管理员、制单员、审批员）分配

这两个字段在UBank登录界面中是分开的。公司代码和用户代码均在分行开户过程中设置——银行会将其打印在与UKey一起交付的密码信封中。

> 如果不确定公司代码或用户名，请检查随UKey一起提供的**密码信封**，或联系招商银行客户经理。

---

## U盾 (UKey) 设置步骤

所需的UBank客户端版本为10.3.9.656或更高。下载地址：招商银行主页 → 企业业务 → U-BANK软件下载。

**步骤1 — 进入注册页面**
启动UBank并插入管理员的UKey。系统会自动弹出“注册新证书”窗口。

**步骤2 — 填写证书信息**
系统自动检测UKey证书编号，并将其与任何未注册的管理员用户匹配。设置一个**8位证书密码**（不能有重复或连续数字）。

**步骤3 — 填写管理员用户信息**
身份证号码的最后4位是开立企业银行账户时提交的申请表上写的那4位。设置一个**8位登录密码**（不能有重复或连续数字）。

**步骤4 — 获取验证码**
点击“获取验证码”——验证码发送至管理员注册的手机或邮箱。有效期为5分钟。

**步骤5 — 完成注册**
确认信息并点击“确认”以完成证书和管理员注册。之后即可登录UBank。

---

**需仔细核对的要点：**
- 插入UKey时指示灯应亮起（表示硬件已被识别）
- 使用带有IE兼容浏览器的Windows PC或专用UBank桌面客户端
- 如果未检测到UKey，请检查Windows服务中的Smart Card服务是否设置为**自动**

**参考资料：**
- [招商银行网上企业银行初次使用指南 (PDF)](https://market.cmbchina.com/mpage/online/220516150452657/wyccsyzn/wyccsyzn.pdf)
- [CMB English Corporate Internet Banking](https://english.cmbchina.com/Corporate/Internet/Default.aspx)