---
audio: false
generated: true
lang: zh
layout: post
title: 使用Keytool导入证书
translated: true
type: note
---

针对您关于使用 `keytool -importcert` 命令将证书导入 `jre/lib/security/cacerts` 文件时遇到"密码验证失败"错误及 `java.security.UnrecoverableException` 的问题，我们将逐步分析问题成因、解决方案以及可能的密码。

### 问题分析

`keytool` 是 Java 开发工具包（JDK）中包含的命令行工具，用于管理密钥库。密钥库是存储加密密钥和证书的文件，常用于保护 SSL/TLS 等网络通信的安全。位于 `jre/lib/security` 目录下的 `cacerts` 文件是 Java 运行时环境（JRE）自带的特定密钥库，它包含来自知名证书颁发机构（CA）的可信根证书集合，Java 应用程序默认使用这些证书来验证安全连接。

当您运行 `keytool -importcert` 命令向 `cacerts` 文件添加新证书时，需要提供正确的密钥库密码。您遇到的错误信息——"密码验证失败"及随后的 `java.security.UnrecoverableException`——表明您提供的密码（或未正确提供）与密钥库密码不匹配。该异常通常发生在密码错误导致 `keytool` 无法访问或修改密钥库时。

### 相关命令详解

您可能使用的命令形式如下：

```
keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias
```

- `-file mycert.crt`：指定要导入的证书文件
- `-keystore /path/to/jre/lib/security/cacerts`：指向 `cacerts` 密钥库
- `-alias myalias`：为密钥库中的证书分配唯一别名

执行此命令时，`keytool` 会提示输入密钥库密码。如果输入的密码错误，就会出现您描述的错误。

### 确定可能的密码

在标准 JRE 安装（如 Oracle 或 OpenJDK 发行版）中，`cacerts` 文件的**默认密码**是 **"changeit"**。这是 Java 各个版本和发行版中广泛记录的默认值。"changeit" 这个名称旨在提醒管理员可能出于安全考虑需要更改密码，但在大多数标准的未修改安装中，此密码通常保持不变。

由于您的命令因密码验证失败而报错，最可能的原因是：
1. 未正确输入 "changeit"（例如拼写错误或大小写问题——密码区分大小写）
2. 密码提示处理不当
3. 在特定环境中默认密码已被修改（虽然对于 `cacerts` 这种情况较少见，除非系统管理员明确修改）

鉴于您的查询未提及自定义配置，我们假设是标准 JRE 安装环境，此时应适用 "changeit" 密码。

### 问题解决方案

请按以下步骤解决问题：

1. **确保在提示时正确输入密码**
   重新运行命令：

   ```
   keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias
   ```

   当出现密码提示时，仔细输入 **"changeit"**（全小写，无空格）并按 Enter 键。请仔细检查拼写错误或键盘布局问题。

2. **在命令行中直接指定密码**
   为避免交互式提示问题（例如脚本执行或终端行为异常），可使用 `-storepass` 选项直接包含密码：

   ```
   keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias -storepass changeit
   ```

   这将显式传递 "changeit" 作为密码，绕过提示。如果此操作无错误执行，则问题很可能源于之前密码输入方式。

3. **检查权限设置**
   由于 `cacerts` 位于 JRE 目录（例如 Linux 上的 `/usr/lib/jvm/java-11-openjdk/lib/security/cacerts` 或 Windows 上的类似路径），请确保您具有写入权限。如需管理员权限：
   - Linux/Mac：使用 `sudo keytool ...`
   - Windows：以管理员身份运行命令提示符

   不过由于您的错误是关于密码验证而非文件访问，这很可能不是核心问题——但仍建议确认。

4. **验证密码有效性**
   如果 "changeit" 仍然失败，可能是您环境中的密码已被修改。尝试以下命令测试密码（不修改密钥库）：

   ```
   keytool -list -keystore /path/to/jre/lib/security/cacerts
   ```

   出现提示时输入 "changeit"。如果成功列出证书，则密码正确；如果出现相同错误，则密码与默认值不同。

### 如果 "changeit" 不是正确密码怎么办？

如果 "changeit" 无效，请考虑以下可能性：
- **自定义密码**：在极少数情况下，系统管理员可能修改了 `cacerts` 密码。您需要查阅系统文档或咨询管理员获取正确密码。若密码丢失无法直接恢复；如果确实无法获知，您可能需要用新 JRE 安装中的全新 `cacerts` 文件替换现有文件（这将重置密码为 "changeit"）。
- **环境特定默认值**：某些非标准 Java 发行版（如 IBM JDK）可能使用不同的默认密码，但这种情况并不常见，且您的查询表明是典型设置。

在没有额外上下文的情况下，"changeit" 仍然是标准 JRE 环境中最可能的密码。

### 最终解决方案

要解决您的问题：
- 对于标准 JRE 环境，使用此命令：

  ```
  keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias -storepass changeit
  ```

- 如果仍然失败，请使用 `-list` 命令验证密码或联系系统管理员。

基于标准 Java 规范，此场景中的**可能密码**是 **"changeit"**。只要正确输入且 `cacerts` 文件未被自定义修改，这应该能解决 `java.security.UnrecoverableException` 问题。
