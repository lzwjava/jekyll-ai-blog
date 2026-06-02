---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java 日期转换指南 2025
translated: true
type: note
---

**问题：** 如何在 Java 中转换日期格式？LocalDate 和 SimpleDateFormat 有什么区别？

**答案：**

在现代 Java（Java 8+）中，有 **两种完全不同的日期/时间 API** 需要了解：

| 特性                     | 旧方法（Java 8 之前）             | 现代方法（Java 8+）                  | 推荐              |
|--------------------------|------------------------------------|----------------------------------------|--------------------------|
| 主要类                   | `java.util.Date`, `SimpleDateFormat` | `LocalDate`, `LocalDateTime`, `ZonedDateTime`, `DateTimeFormatter` | 使用现代 API |
| 线程安全                 | 非线程安全                         | 线程安全                               | 现代更安全     |
| 可变 / 不可变            | 可变                               | 不可变                                 | 现代更安全     |
| 时区感知                 | 差 / 混乱                          | 清晰（`LocalDate` = 无时区，`ZonedDateTime` = 有时区） | 现代更清晰     |
| 设计用于                 | 遗留代码、旧库                     | 新代码（2014+）                        | 优先现代       |

### 1. 日期转换/格式化 – 现代方法（推荐）

```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class Main {
    public static void main(String[] args) {
        // 1. String → LocalDate
        String dateStr = "2025-03-15";
        LocalDate date = LocalDate.parse(dateStr);                    // ISO format
        LocalDate date2 = LocalDate.parse("15/03/2025",
                            DateTimeFormatter.ofPattern("dd/MM/yyyy"));

        // 2. LocalDate → String (different formats)
        System.out.println(date.format(DateTimeFormatter.ISO_LOCAL_DATE));
        // 2025-03-15

        System.out.println(date.format(DateTimeFormatter.ofPattern("dd/MM/yyyy")));
        // 15/03/2025

        System.out.println(date.format(DateTimeFormatter.ofPattern("MMM d, yyyy")));
        // Mar 15, 2025

        System.out.println(date.format(DateTimeFormatter.ofPattern("EEEE, MMMM dd yyyy")));
        // Saturday, March 15 2025
    }
}
```

最常见模式：

| 模式             | 示例输出            | 含义                     |
|------------------|---------------------|--------------------------|
| `yyyy-MM-dd`     | 2025-03-15          | ISO（默认）              |
| `dd/MM/yyyy`     | 15/03/2025          | 许多国家常用             |
| `MM/dd/yyyy`     | 03/15/2025          | 美国风格                 |
| `dd MMM yyyy`    | 15 Mar 2025         | 紧凑易读                 |
| `EEEE, MMMM d yyyy` | Saturday, March 15 2025 | 非常易读             |

### 2. 旧方法 – 使用 `SimpleDateFormat`（在新代码中避免使用）

```java
import java.text.SimpleDateFormat;
import java.util.Date;

SimpleDateFormat sdf1 = new SimpleDateFormat("yyyy-MM-dd");
SimpleDateFormat sdf2 = new SimpleDateFormat("dd/MM/yyyy");

Date date = new Date();

// Date → String
String iso  = sdf1.format(date);
String euro = sdf2.format(date);

// String → Date
Date parsed = sdf1.parse("2025-03-15");   // ← can throw ParseException
```

**关于 SimpleDateFormat 的重要警告：**

- **非线程安全** → 在多线程环境中危险（Servlets、Spring、并行流等）
- 非常容易出错（yy vs yyyy、M vs MM 等）
- `java.util.Date` 表示时间瞬间（有时分 + 时区偏移混淆）

### 旧 API 和新 API 之间的快速转换

```java
// Old → New
Date oldDate = new Date();
LocalDate newDate = oldDate.toInstant()
                         .atZone(ZoneId.systemDefault())
                         .toLocalDate();

// New → Old (通常仅用于遗留 API)
Date fromLocal = Date.from(localDate.atStartOfDay(ZoneId.systemDefault()).toInstant());
```

**总结 – 2025/2026 年使用哪个？**

| 情况                               | 推荐类                          |
|------------------------------------|---------------------------------|
| 新项目/现代代码                    | `LocalDate`, `LocalDateTime`, `ZonedDateTime`, `DateTimeFormatter` |
| 读写 ISO 日期（API、JSON、数据库） | `LocalDate.parse()` + `.format(ISO_LOCAL_DATE)` |
| 需要向用户显示日期（不同国家）     | `DateTimeFormatter.ofPattern(...)` |
| 与返回 `java.util.Date` 的旧库/JDBC 合作 | 尽快转换为 `LocalDate`/`LocalDateTime` |
| 仍在维护非常旧的代码               | 可能必须保留 `SimpleDateFormat`（但需小心包装） |

**底线（2025+）：**
几乎所有情况都使用 `java.time.*` 类 + `DateTimeFormatter`。
仅在被迫处理遗留代码时才接触 `SimpleDateFormat`。

**参考资料：**

- 无需参考（这是 Java 8 引入的 java.time API 的标准 Java 知识）
