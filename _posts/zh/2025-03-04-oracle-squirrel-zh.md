---
audio: false
generated: true
lang: zh
layout: post
title: 在Squirrel SQL客户端中添加Oracle JDBC驱动
translated: true
type: note
---

要为 Squirrel SQL Client 添加 Oracle JDBC 驱动程序，请按照以下详细步骤操作。该过程包括配置驱动程序和设置 Oracle 数据库的连接别名。

### 步骤 1：定位所需文件
您需要 Oracle JDBC 驱动文件，特别是 `ojdbc.jar`。该文件包含使 Squirrel SQL Client 能够连接 Oracle 数据库的必要类。请确保您已下载此文件（例如从 Oracle 网站或数据库管理员处获取），并知晓其在系统中的存储位置。

### 步骤 2：启动 Squirrel SQL Client
在计算机上打开 Squirrel SQL Client 应用程序。

### 步骤 3：访问驱动程序选项卡
在 Squirrel SQL Client 界面左侧，找到并单击 **Drivers** 选项卡。此部分允许您管理应用程序可用的 JDBC 驱动程序。

### 步骤 4：添加新驱动程序
- 在驱动程序选项卡中，单击 **"+"** 按钮打开"添加驱动程序"对话框。

### 步骤 5：命名驱动程序
- 在"添加驱动程序"对话框的"名称"字段中，输入 **Oracle Thin Driver**。这是用于在 Squirrel SQL Client 中识别 Oracle 驱动程序的描述性名称。

### 步骤 6：添加 `ojdbc.jar` 文件
- 在"添加驱动程序"对话框中切换到 **Extra Class Path** 选项卡。
- 单击 **Add** 按钮。
- 导航至系统中 `ojdbc.jar` 文件的存储位置，选择该文件并确认将其添加到驱动程序的类路径中。

### 步骤 7：指定 Java 驱动类
- 在"类名称"字段中输入 Java 驱动类：**oracle.jdbc.OracleDriver**。这会告知 Squirrel SQL Client 使用 `ojdbc.jar` 文件中的哪个类来处理 Oracle 数据库连接。

### 步骤 8：提供示例 URL
- 您可以选择指定用于连接 Oracle 数据库的示例 URL 格式：
  - **通过 SID 连接**：`jdbc:oracle:thin:@HOST[:PORT]:DB`
  - **通过服务名连接**：`jdbc:oracle:thin:@//HOST[:PORT]/DB`
- 在后续设置连接时（在别名配置中），请将 `HOST`、`PORT` 和 `DB` 替换为实际值。

### 步骤 9：保存驱动程序配置
- 单击 **OK** 保存驱动程序设置并关闭"添加驱动程序"对话框。"Oracle Thin Driver"现在应出现在驱动程序选项卡中，并带有绿色对勾标记，表示已正确配置。

### 步骤 10：为数据库创建别名
- 切换到 Squirrel SQL Client 左侧的 **Aliases** 选项卡。
- 单击 **"+"** 按钮打开"添加别名"对话框。

### 步骤 11：配置别名
- 在"添加别名"对话框中：
  - **名称**：输入此连接的名称（例如"My Oracle DB"）。
  - **驱动程序**：从下拉菜单中选择 **Oracle Thin Driver**。
  - **URL**：输入特定 Oracle 数据库的连接 URL：
    - 通过 SID：`jdbc:oracle:thin:@HOST[:PORT]:DB`
    - 通过服务名：`jdbc:oracle:thin:@//HOST[:PORT]/DB`
    - 将 `HOST`（例如 localhost 或 IP 地址）、`PORT`（默认为 1521）和 `DB`（SID 或服务名）替换为数据库的实际详细信息。
  - **用户名**：输入数据库用户名。
  - **密码**：输入数据库密码。

### 步骤 12：测试连接
- 单击"添加别名"对话框中的 **Test** 按钮，验证 Squirrel SQL Client 是否可以使用提供的详细信息连接到您的 Oracle 数据库。如果成功，您将看到确认消息。

### 步骤 13：保存别名
- 如果测试连接成功，单击 **OK** 保存别名。新别名现在将出现在别名选项卡中。

### 步骤 14：连接到数据库
- 在别名选项卡中，选择您新创建的别名（例如"My Oracle DB"）。
- 单击 **Connect** 按钮建立与 Oracle 数据库的连接。连接成功后，您即可开始使用 Squirrel SQL Client 查询数据库。

### 关键信息摘要
- **所需文件**：`ojdbc.jar`
- **Java 驱动类**：`oracle.jdbc.OracleDriver`
- **URL 格式**：
  - SID：`jdbc:oracle:thin:@HOST[:PORT]:DB`
  - 服务名：`jdbc:oracle:thin:@//HOST[:PORT]/DB`

通过遵循这些步骤，您将成功将 Oracle JDBC 驱动程序添加到 Squirrel SQL Client 并配置好与 Oracle 数据库的连接。请确保所有详细信息（文件路径、URL、凭据）准确无误，以避免连接问题。
