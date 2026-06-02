---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-pro-preview
title: 更新WebSphere Liberty中的SSL证书
translated: true
type: note
---

在 IBM WebSphere Liberty Profile (WLP) 中更新 SSL 证书主要涉及替换配置的 **keystore** 文件中的密钥条目，并在涉及新证书颁发机构 (CA) 或中间证书时更新信任库。

您提到的 `.sth` 文件通常是传统 WebSphere Application Server 中与 **CMS（证书管理系统）密钥库**（`.kdb` 格式）关联的 **存储文件**，用于安全存储密钥库密码。**IBM WebSphere Liberty Profile** 通常使用 **PKCS12**（`.p12`）或 **JKS**（`.jks`）格式的密钥库，其密码可能直接以编码形式存储在 `server.xml` 中，**通常不使用单独的 `.sth` 文件**，除非为其他组件或旧版本/配置特别配置。

以下是续订、密钥库管理和备份的通用分步流程。

-----

## 1. 备份现有密钥库和配置

**这是最关键的一步。** 在进行任何更改之前，请备份您的现有文件。

1.  **停止 Liberty 服务器：**
    ```bash
    wlp/bin/server stop <server_name>
    ```
2.  **备份密钥库文件：**
      * 默认密钥库通常名为 **`key.p12`**（或在旧版本中为 `key.jks`），位于：
        `wlp/usr/servers/<server_name>/resources/security/`
      * **将整个 `security` 目录** 复制到 WLP 安装目录之外的安全位置。
3.  **备份服务器配置：**
      * 复制 **`server.xml`** 文件：
        `wlp/usr/servers/<server_name>/server.xml`

-----

## 2. 获取并准备新证书

您应从证书颁发机构 (CA) 收到您的新证书以及中间/根 CA 证书。它们通常以 `.pem`、`.cer` 或 PKCS12 捆绑包 (`.p12`) 的形式提供。

如果您是从现有密钥库生成的证书签名请求 (CSR) 开始的，则需要将签名的证书使用相同的私钥导入回该密钥库。

-----

## 3. 使用新证书更新密钥库

**`keytool`** 实用程序是 Liberty 使用的 Java 运行时环境 (JRE/JDK) 的一部分，是管理密钥库的标准工具。

`server.xml` 中的默认密钥库配置通常如下所示（您需要 `location` 和 `password`）：

```xml
<keyStore id="defaultKeyStore"
          location="${server.config.dir}/resources/security/key.p12"
          password="{xor}..." />
```

### 选项 A：替换现有密钥库中的证书

当您拥有与密钥库中**现有私钥**对应的、由 **CA 签名的新证书**时，使用此方法。您必须先导入 CA 的根证书和中间证书，然后再导入您的新个人证书。

1.  **导入根/中间 CA 证书（到密钥/信任库）：**
    ```bash
    # 导航到 JRE/JDK bin 目录，例如 wlp/java/jre/bin
    keytool -importcert -file <ca_root_cert_file>.cer -alias <root_alias> -keystore <keystore_location> -storepass <keystore_password> -storetype PKCS12
    # 对任何中间证书重复此操作
    keytool -importcert -file <intermediate_cert_file>.cer -alias <intermediate_alias> -keystore <keystore_location> -storepass <keystore_password> -storetype PKCS12
    ```
2.  **导入新的个人（签名）证书：**
    ```bash
    keytool -importcert -file <new_signed_cert_file>.cer -alias <private_key_alias> -keystore <keystore_location> -storepass <keystore_password> -storetype PKCS12
    ```
      * `<private_key_alias>` **必须与用于生成 CSR 的私钥别名匹配**。如果是 Liberty 默认值，别名通常是 **`default`**。

### 选项 B：创建新的密钥库文件

如果您在旧密钥库之外生成了全新的密钥对（或收到了新的 `.p12` 捆绑包），或者续订过程复杂，您可以创建一个新的密钥库并替换旧的。

1.  **将新密钥/证书导入到新文件中：**（这在很大程度上取决于您收到新证书的方式——CA 提供的 `.p12` 捆绑包是最简单的）。
2.  **替换旧文件：** 重命名旧的 `key.p12` 文件（例如，改为 `key.p12.old`），并将您新的、正确命名的密钥库文件 (`key.p12`) 放入 `resources/security/` 目录。

-----

## 4. 续订自签名证书

如果您使用的是由 Liberty 的 `securityUtility` 创建的**自签名证书**，过程很简单，只需删除旧的，然后让 Liberty 创建一个新的，或者直接使用 `keytool` 命令生成一个新的。

1.  **停止 Liberty 服务器。**
2.  **从 `wlp/usr/servers/<server_name>/resources/security/` 中删除现有的密钥库文件** (`key.p12`)。
3.  **启动 Liberty 服务器。**
    ```bash
    wlp/bin/server start <server_name>
    ```
    如果您的 `server.xml` 中有 `<keyStore id="defaultKeyStore" ... />` 元素，Liberty 将自动调用 `securityUtility` 来生成**新的自签名证书**和密钥库。

-----

## 5. 重启并验证

1.  **启动 Liberty 服务器**（如果它尚未从续订步骤开始运行）。
    ```bash
    wlp/bin/server start <server_name>
    ```
2.  **检查日志：** 查看 `messages.log` 中是否有任何 SSL 或密钥库相关的错误。
3.  **在浏览器中验证：** 通过 HTTPS 访问您的应用程序，并在浏览器中检查证书详细信息，以确保**新的到期日期**正确且证书链受信任。

您是否需要我为您查找特定证书文件类型（例如 P7B、PEM、PKCS12）的 **`keytool`** 命令，或者为您的 `server.xml` **编码新密钥库密码**的命令？
