---
audio: false
generated: true
lang: zh
layout: post
title: 使用DBeaver检查Oracle数据库表数据的步骤
translated: true
type: note
---

我理解您是基于之前关于在Oracle数据库中查找有数据的表的问题，现在想了解如何使用DBeaver来实现这一目的。DBeaver是一款流行、免费、跨平台的数据库工具，能很好地支持Oracle及其他数据库。下面我将逐步指导您如何使用DBeaver检查Oracle模式并识别包含数据的表。

---

#### 1. **设置Oracle数据库连接**
   - **安装DBeaver**：如果尚未安装，请从[dbeaver.io](https://dbeaver.io/)下载并安装DBeaver（社区版即可）。
   - **创建新连接**：
     1. 打开DBeaver，点击菜单中的**数据库** > **新建数据库连接**。
     2. 从列表中选择**Oracle**，点击**下一步**。
     3. 输入连接信息：
        - **主机**：Oracle服务器的主机名或IP地址
        - **端口**：通常为1521（Oracle默认端口）
        - **数据库/SID或服务名**：根据您的设置（例如Express Edition的SID为`XE`，或服务名）
        - **用户名**和**密码**：您的Oracle凭据
     4. 点击**测试连接**验证是否成功。如果提示需要下载Oracle JDBC驱动，DBeaver可自动完成。
     5. 点击**完成**保存连接。

#### 2. **在数据库导航器中探索模式**
   - 在**数据库导航器**（左侧窗格）中展开您的Oracle连接。
   - 您将看到模式列表（例如您的用户名或其他有访问权限的模式）。展开要检查的目标模式。
   - 在每个模式下展开**表**节点查看所有数据表。

#### 3. **通过图形界面检查表数据**
   - **查看表数据**：
     1. 双击表名或右键点击选择**编辑表**。
     2. 在打开的编辑器中切换到**数据**标签页。
     3. 如果表包含数据，将显示数据行；如果为空，则无数据行（或显示“无数据”提示）。
     - 默认情况下DBeaver最多获取200行。要获取全部数据，可点击数据标签页底部工具栏的**获取所有行**按钮（小箭头图标）。
   - **快速统计行数**：
     1. 在数据库导航器中右键点击目标表。
     2. 选择**导航** > **行数统计**。
     3. DBeaver将执行`SELECT COUNT(*)`查询并在弹窗中显示结果。如果结果为0，则该表为空。

#### 4. **使用SQL查询检查多个表**
   - 如需批量检查多个表（比逐个点击更高效），可使用SQL编辑器：
     1. 点击**SQL编辑器** > **新建SQL脚本**（或按`Ctrl + [`）。
     2. 设置模式上下文：
        - 在SQL编辑器顶部的下拉列表选择目标模式，或执行：
          ```sql
          ALTER SESSION SET CURRENT_SCHEMA = schema_name;
          ```
          将`schema_name`替换为目标模式（如`HR`）。
     3. 查询所有表的行数统计：
        - 使用以下SQL列出包含数据的表（类似我之前提供的方案）：
          ```sql
          SELECT table_name, num_rows
          FROM user_tables
          WHERE num_rows > 0
          ORDER BY num_rows DESC;
          ```
        - 按`Ctrl + Enter`执行查询，结果将显示在下方的**结果**标签页中。
        - `USER_TABLES`仅显示当前模式下的表。如需跨模式访问，使用`ALL_TABLES`：
          ```sql
          SELECT owner, table_name, num_rows
          FROM all_tables
          WHERE num_rows > 0
          AND owner = UPPER('schema_name');
          ```
     4. **注意**：`NUM_ROWS`是基于上次统计更新得到的估算值。如需更新统计信息可执行：
        ```sql
        EXEC DBMS_STATS.GATHER_SCHEMA_STATS('schema_name');
        ```
