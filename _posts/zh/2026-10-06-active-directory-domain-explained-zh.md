---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Active Directory 域详解
translated: true
type: note
---

问题：**Active Directory（AD）**中的**域**是什么意思？

回答：

在 **Active Directory** 中，**域**是**主要的管理边界和安全单元**，它将用户、计算机、服务器和策略组织在一个统一的管理体系下。

可以将 AD 域理解为一个**受管理的命名空间 + 安全数据库**。

示例：

```
公司：example.com

Active Directory 域：
    example.com

内部对象：
    用户：
        alice@example.com
        bob@example.com

    计算机：
        PC001
        Server001

    组：
        开发人员
        人力资源

    策略：
        密码规则
        软件部署
        安全设置
```

域是 AD 存储和管理以下内容的地方：

* **用户账户**
* **计算机账户**
* **组**
* **权限**
* **认证信息**
* **组策略设置**

当 Alice 登录公司笔记本电脑时：

```
Alice
  |
  | 用户名/密码
  v
域控制器
  |
  | 检查 AD 数据库
  v
example.com 域
  |
  +--> Alice 账户是否存在？
  +--> 密码是否正确？
  +--> 组成员身份？
  +--> 策略？
```

域控制器（DC）是提供此服务的服务器。

---

### 为什么称为“域”？

它源自 DNS 中的域概念。

例如：

```
example.com
```

是一个 DNS 域。

AD 通常使用相同的命名空间：

```
AD 域：
    example.com

用户：
    alice@example.com

计算机：
    laptop01.example.com
```

但 AD 域不仅仅是网站域名，它增加了身份管理和安全功能。

---

### 域 vs 工作组

在 AD 之前，Windows 使用**工作组**：

```
工作组：
    PC1
    PC2
    PC3
```

每台计算机管理自己的用户：

```
PC1：
    Alice
    Bob

PC2：
    Alice
    Bob
```

问题：

* 密码重复
* 无集中管理
* 难以管理数千台机器

AD 域：

```
             域控制器
                 |
          +------+------+
          |      |      |
        PC1    PC2    PC3
```

一个身份系统控制一切。

---

### 域 vs 林 vs 树

AD 层次结构：

```
林
 |
 +-- 树
      |
      +-- 域
            |
            +-- 组织单位（OU）
                  |
                  +-- 用户
                  +-- 计算机
                  +-- 组
```

示例：

```
林：
    Microsoft Corporation

域：
    microsoft.com
    research.microsoft.com
    europe.microsoft.com
```

**域**是基本的管理边界。

**林**是最大的信任/安全边界。

---

一个简单的类比：

* **林** = 一个国家
* **域** = 一个省份
* **OU** = 一个城市/区
* **用户/计算机** = 市民/建筑

域回答了：**“谁属于这个组织，他们被允许做什么？”**

如果您正在学习网络/安全知识，我还可以解释**AD 内部如何进行身份验证（Kerberos 票据、LDAP、NTLM）**。