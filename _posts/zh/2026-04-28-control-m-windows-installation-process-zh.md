---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Control-M Windows 安装流程
translated: true
type: note
---

问题：Control-M v9.0.21在Windows上的安装流程是什么？是否需要输入Web主机和端口？

答案：

## Control-M v9.0.21（v921）在Windows上的安装——完整概述

Control-M v9.0.21是BMC公司的一款工作负载自动化产品。在Windows上，它可以进行**完整安装**（所有组件集成一体），也可以按组件分别安装（企业管理器、服务器、代理）。以下是详细解析：

---

### 1. 安装选项

Control-M v9.0.21支持完整安装，通过交互式或自动安装方式，在Windows上安装包括应用程序插件和附加组件在内的所有组件。您可以使用默认设置安装，或选择自定义安装来配置数据库服务器、数据库名称、用户名、主机名和端口设置。

两种安装模式如下：
- **交互式安装** — 通过屏幕上的图形用户界面向导逐步引导
- **自动（静默）安装** — 使用预先生成的XML参数文件进行无人值守安装

---

### 2. 运行Setup.exe前的先决条件

在Windows上开始安装之前，您必须：
- 确认操作系统和数据库软件与当前版本的Control-M兼容（参见Control-M完整安装系统要求）。
- 确认满足Java要求（Control-M外部Java安装）。
- 确认目标计算机干净，未安装任何旧版Control-M。
- 确认已下载正确的安装文件。
- 如果在集群环境中安装，请先完成Control-M集群配置步骤。

---

### 3. 运行Windows安装程序（Setup.exe）

开始安装步骤：
1. 使用具有管理员权限的用户ID登录计算机。
2. 在命令提示符窗口中运行：`<source_path>\Setup.exe`
3. 选择**Control-M 9.0.21.100 - Full Installation**选项，并按照屏幕上的指示继续操作，直至安装完成。

---

### 4. 是否需要输入Web主机和端口？是的——在自定义安装过程中

是的，当您选择**自定义**安装路径（而非默认安装）时，安装程序**确实会**提示输入主机名和端口。

**Web服务器端口：**
在自服务和Web组件设置过程中，您必须确认默认的Web服务器端口**18080**或您希望使用的其他已配置端口是开放的。安装完成后，您可以打开Control-M配置管理器，选择“所有组件”下的Web服务器，并查看Web服务器URL，以访问Control-M Web组件。

**企业管理和服务器通信端口：**
防火墙规则和双向通信所需的关键端口包括：
- Control-M/EM TCP/IP端口：**2370**
- 配置代理端口：**2369**
- 代理到服务器端口：**7005**
- 高可用性端口：**2368**

**数据库端口：**
如果您在已安装带有PostgreSQL数据库的Control-M/EM的同一台计算机上安装带有PostgreSQL数据库的Control-M/Server，则必须为第二个数据库实例使用**不同的端口**。

**Zookeeper/Kafka端口（如果位于同一主机）：**
如果在同一台计算机上安装Control-M/EM和Control-M/Server，则必须配置Zookeeper和Kafka服务，以便在Control-M/EM和附加的Control-M/Server实例上使用不同的端口。

---

### 5. 自动（静默）安装

对于自动安装，您需要向导操作直至摘要窗口，点击**生成**以创建XML参数文件，然后运行：
```
<source_path>\Setup.exe -silent <xml_path>\<filename.xml>
```
要在安装过程中加密密码，请运行：
```
<source_path>\Setup.exe -encrypt <password>
```
安装日志保存在：
```
<installFolder>\BMCINSTALL\log\BMC_Control-M_Install_<date-time>.log
```
注意：生成的XML参数文件仅适用于具有相同代理实例名称的计算机。对于具有不同名称的每台计算机，必须单独创建或手动修改该文件。

---

### 6. 在Windows上安装Control-M/代理（单独组件）

在Windows上安装Control-M/代理：
1. 使用管理员权限登录。
2. 将安装文件复制到主目录。
3. 在命令提示符中运行`<source_path>\setup.exe`。
4. 按照屏幕指示（交互式）操作，或生成XML文件进行自动安装。
代理安装日志位于：`<installFolder>\BMCINSTALL\log\BMC_Control-M_AGENT_Install<date-time>.log`

---

### 摘要表格

| 参数 | 默认值 | 备注 |
|---|---|---|
| Web服务器端口 | 18080 | 可在自定义安装时配置 |
| EM TCP/IP端口 | 2370 | 防火墙需开放 |
| 配置代理端口 | 2369 | 防火墙需开放 |
| 代理到服务器端口 | 7005 | 防火墙需开放 |
| HA端口 | 2368 | 用于高可用性设置 |
| PostgreSQL端口 | 默认（5432） | 若EM与Server同主机，则需使用不同端口 |

---

### 关键要点

是的——在Windows上安装Control-M v9.0.21时，如果选择自定义安装选项，安装程序**确实需要您确认或输入Web主机和端口设置**。默认选项使用预设值（例如，Web服务器端口18080）。主可执行文件是`Setup.exe`，需要通过具有管理员权限的命令提示符启动。

参考资料：

- [Control-M在Windows上的完整安装（BMC文档）](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Installing_Control-M_on_Windows.htm)
- [Control-M v9.0.21安装简介](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Introduction_to_Control-M_Installation.htm)
- [Control-M/代理在Windows上的安装](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/Installing_Control-M_Agent_on_Windows.htm)
- [Control-M/服务器安装](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Control-M_Server_installation.htm)
- [Control-M系统配置 / 端口](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/System_Configuration.htm)
- [Control-M自服务安装（Web端口）](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/Control-M_Self_Service_installation.htm)