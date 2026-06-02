---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 DBeaver 中设置分隔符
translated: true
type: note
---

**Question:** 如何在 DBeaver 中设置分隔符 (delimiter)？有时在编写 BEGIN/END 存储过程调用时，我需要使用 `@` 作为结束分隔符。

**Answer:**

在 DBeaver 中，处理包含内部分号的存储过程（特别是 MySQL/MariaDB）最常用且最可靠的方法是在脚本中直接包含 `DELIMITER` 命令，并正确执行整个脚本。

### 推荐方法（适用于大多数情况）

在 SQL Editor 中按照以下方式编写脚本：

```sql
DELIMITER @

CREATE PROCEDURE your_procedure_name()
BEGIN
    SELECT 'Hello';
    INSERT INTO log VALUES ('test');
    -- 内部带有 ; 的任何语句
END @

DELIMITER ;
```

**如何执行：**

- 选中整个脚本（从第一个 `DELIMITER @` 到最后的 `DELIMITER ;`）
- 按 **Alt+X** (或右键点击 → Execute → Execute Script)
  - 这将把整个代码块作为脚本运行，使 DBeaver 能够识别 `DELIMITER` 的更改
- 或者，对选中的块使用 **Ctrl+Enter**，但对于包含分隔符更改的多语句脚本，**Alt+X** 通常更可靠

### 替代方法：在 DBeaver 设置中更改默认语句分隔符

如果你非常频繁地使用 `@`（或其他字符）而不是 `;`，可以更改 DBeaver 的解析分隔符：

1. 转到 **Window → Preferences** (macOS 上为 **DBeaver → Settings**)
2. 导航至 **Editors → SQL Editor → SQL Processing → Delimiters**
3. 将 **Statements delimiter** 设置为 `@`
4. (可选) 根据需要勾选/取消勾选 **Ignore native delimiter**
5. 点击 **Apply and Close**

更改后：

- DBeaver 将把 `@` 视为每条语句的结束
- 你不再需要编写 `DELIMITER @` —— 只需以 `@` 结束存储过程即可
- 但务必注意：此设置会影响该编辑器/连接中的 **所有** 查询

```sql
CREATE PROCEDURE your_procedure_name()
BEGIN
    SELECT 'Hello';
    -- statements
END @
```

**Warning：** 将全局/默认分隔符更改为 `@` 可能会导致普通使用 `;` 的查询出现混乱。大多数用户更喜欢第一种方法（使用 `DELIMITER` + Alt+X），因为它仅对当前脚本有效。

### 快速总结 – 通常效果最佳的方法

- 使用 `DELIMITER @` ... `END @` ... `DELIMITER ;`
- **全选** → **Alt+X** (Execute as Script)
- 这是在 DBeaver 中处理 MySQL/MariaDB 存储过程的标准方法

这种方法避免了更改全局设置，并且在不同的连接中表现一致。

**References:**

- [DBeaver SQL Execution Documentation](https://dbeaver.com/docs/dbeaver/SQL-Execution)
- [MySQL DELIMITER usage](https://www.mysqltutorial.org/mysql-stored-procedure/mysql-delimiter)
