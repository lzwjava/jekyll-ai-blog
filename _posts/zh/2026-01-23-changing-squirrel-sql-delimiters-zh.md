---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 更改 Squirrel SQL 定界符
translated: true
type: note
---

**Question:** 如何在 Squirrel SQL Client 中设置/更改分隔符（特别是针对使用 BEGIN … END 且需要类似 @@ 或 @ 这种不同分隔符的 stored procedures）？

**Answer:**

在 **Squirrel SQL Client** 中，默认的语句分隔符是 `;`。  
当创建或调用在主体（BEGIN … END 代码块）内包含 `;` 的 stored procedures / functions / triggers 时，你必须临时更改分隔符。

以下是在 Squirrel-SQL 中实现此操作的主要方法：

### 推荐且最常用的方法 (2024–2026 风格)

1. 进入 **SQL worksheet** (编写脚本的地方)
2. 在脚本的最顶部，写入：

```sql
--#SET TERMINATOR @@

DELIMITER @@

CREATE PROCEDURE my_proc()
BEGIN
    INSERT INTO log VALUES(NOW(), 'start');
    -- 许多使用普通 ; 的语句
    INSERT INTO log VALUES(NOW(), 'end');
END@@

DELIMITER ;
```

3. 然后执行整个脚本（Ctrl+Enter 或点击“跑步者”图标）

`--#SET TERMINATOR xx` 是一个 **SQuirreL 特殊注释**，用于更改 **当前 session/tab** 的分隔符。

常用的选项包括：

```sql
--#SET TERMINATOR @@        ← 最流行
--#SET TERMINATOR $
--#SET TERMINATOR //
--#SET TERMINATOR \G
--#SET TERMINATOR @          ← 你提到的
```

### 其他可行的方法

**方法 2 – 使用 Session Properties 菜单**

- 在左侧面板右键点击你的 session → **Session Properties**
- 转到 **SQL Execution** 选项卡 → **Delimiters**
- 将 "Statement separator" 从 `;` 更改为你想要的任何字符（例如 `@@` 或 `@`）
- → OK
- → 这将更改整个 session 的设置（直到你将其改回）

**方法 3 – 快速单行风格 (对 MySQL/MariaDB 友好)**

许多人仍然沿用“经典”写法：

```sql
DELIMITER @@

CREATE PROCEDURE example()
BEGIN
    SELECT 1;
    SELECT 2;
END @@

DELIMITER ;
```

**只要**你没有禁用 "Process SQL comments" 或 "Allow # as comment" 设置，SQuirreL 就能正确理解这种语法。

### 快速经验法则 – 2025/2026 年大多数人的做法

```sql
--#SET TERMINATOR @@

DROP PROCEDURE IF EXISTS my_proc@@

CREATE PROCEDURE my_proc(IN p_id INT)
BEGIN
    DECLARE v_name VARCHAR(100);
    SET v_name = 'test';
    INSERT INTO t1 (id, name) VALUES (p_id, v_name);
    -- 更多带有普通分号的业务逻辑
END@@

--#SET TERMINATOR ;     ← 重置是一个好习惯
```

### 总结 – 选择一种风格

风格 A (整洁且现代)

```sql
--#SET TERMINATOR @@
... 你的 procedure ...
--#SET TERMINATOR ;
```

风格 B (经典 MySQL workbench 风格)

```sql
DELIMITER @@
... 你的 procedure ...
DELIMITER ;
```

两者在当前的 SQuirreL 版本（4.x, 202x builds）中都能很好地工作。

希望这能帮你解决 "You have an error in your SQL syntax … near END" 的问题。

**References:**

- 无（信息基于截至 2025 年发布的 SQuirreL SQL client 行为和常见的社区使用模式）