---
audio: false
generated: true
lang: zh
layout: post
title: Java正则表达式
translated: true
type: note
---

# 如何在 Java 中使用 `java.util.regex`

Java 中的 `java.util.regex` 包提供了处理正则表达式（regex）的工具，这些模式用于匹配和操作文本。本指南将引导你了解该包的基本用法，重点介绍两个主要类：`Pattern` 和 `Matcher`。我还会通过示例介绍常见用例，帮助你入门。

## `java.util.regex` 概述

`java.util.regex` 包包括：

- **`Pattern`**：表示一个已编译的正则表达式。你可以通过正则表达式字符串创建它。
- **`Matcher`**：将模式应用于特定的输入字符串并执行匹配操作。

此外，Java 的 `String` 类提供了基于正则表达式的方法，用于处理简单任务。

## 使用 `java.util.regex` 的基本步骤

要在 Java 中使用正则表达式，请遵循以下步骤：

1. **编译模式**：将正则表达式字符串转换为 `Pattern` 对象。
2. **创建匹配器**：使用模式为输入文本创建 `Matcher`。
3. **执行操作**：使用匹配器检查匹配、查找模式或操作文本。

以下是实际应用中的操作方式。

## 示例 1：验证电子邮件地址

让我们使用一个基本的正则表达式模式 `".+@.+\\..+"` 创建一个简单的电子邮件验证器。该模式匹配在 `@` 符号前后至少有一个字符，后跟一个点和更多字符的字符串（例如 `example@test.com`）。

```java
import java.util.regex.*;

public class EmailValidator {
    public static boolean isValidEmail(String email) {
        // 定义正则表达式模式
        String regex = ".+@.+\\..+";
        // 编译模式
        Pattern pattern = Pattern.compile(regex);
        // 为输入字符串创建匹配器
        Matcher matcher = pattern.matcher(email);
        // 检查整个字符串是否匹配模式
        return matcher.matches();
    }

    public static void main(String[] args) {
        String email = "example@test.com";
        if (isValidEmail(email)) {
            System.out.println("有效的电子邮件");
        } else {
            System.out.println("无效的电子邮件");
        }
    }
}
```

### 解释

- **`Pattern.compile(regex)`**：将正则表达式字符串编译为 `Pattern` 对象。
- **`pattern.matcher(email)`**：为输入字符串 `email` 创建 `Matcher`。
- **`matcher.matches()`**：如果整个字符串匹配模式，则返回 `true`，否则返回 `false`。

**输出**：`有效的电子邮件`

注意：这是一个简化的电子邮件模式。真实的电子邮件验证需要更复杂的正则表达式（例如，遵循 RFC 5322），但这可以作为一个起点。

## 示例 2：查找字符串中的所有主题标签

假设你想从一条推文中提取所有主题标签（例如 `#java`）。使用正则表达式 `"#\\w+"`，其中 `#` 匹配字面主题标签符号，`\\w+` 匹配一个或多个单词字符（字母、数字或下划线）。

```java
import java.util.regex.*;

public class HashtagExtractor {
    public static void main(String[] args) {
        String tweet = "这是一条包含 #多个 主题标签的 #示例 推文，例如 #java";
        String regex = "#\\w+";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(tweet);

        // 查找所有匹配项
        while (matcher.find()) {
            System.out.println(matcher.group());
        }
    }
}
```

### 解释

- **`matcher.find()`**：移动到输入字符串中的下一个匹配项，如果找到匹配项则返回 `true`。
- **`matcher.group()`**：返回当前匹配项的匹配文本。

**输出**：

```
#示例
#多个
#java
```

## 示例 3：使用正则表达式替换文本

要替换一个单词的所有出现（例如，用星号审查 "badword"），你可以使用 `String.replaceAll()` 方法，该方法内部使用正则表达式。

```java
public class TextCensor {
    public static void main(String[] args) {
        String text = "这是一个包含重复 badword 的 badword 示例。";
        String censored = text.replaceAll("badword", "*******");
        System.out.println(censored);
    }
}
```

**输出**：`这是一个包含重复 ******* 的 ******* 示例。`

对于更复杂的替换，使用 `Matcher`：

```java
import java.util.regex.*;

public class ComplexReplacement {
    public static void main(String[] args) {
        String text = "联系方式：123-456-7890";
        String regex = "\\d{3}-\\d{3}-\\d{4}"; // 匹配电话号码
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(text);
        String result = matcher.replaceAll("XXX-XXX-XXXX");
        System.out.println(result);
    }
}
```

**输出**：`联系方式：XXX-XXX-XXXX`

## 示例 4：使用分组解析结构化数据

正则表达式分组，用括号 `()` 定义，允许你捕获匹配的部分。例如，解析像 `123-45-6789` 这样的社会安全号码（SSN）：

```java
import java.util.regex.*;

public class SSNParser {
    public static void main(String[] args) {
        String ssn = "123-45-6789";
        String regex = "(\\d{3})-(\\d{2})-(\\d{4})"; // 区域号、组号、序列号的分组
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(ssn);

        if (matcher.matches()) {
            System.out.println("区域号码：" + matcher.group(1));
            System.out.println("组号码：" + matcher.group(2));
            System.out.println("序列号码：" + matcher.group(3));
        }
    }
}
```

### 解释

- **`"(\\d{3})-(\\d{2})-(\\d{4})"`**：定义三个分组：
  - 分组 1：`\\d{3}`（三位数字）
  - 分组 2：`\\d{2}`（两位数字）
  - 分组 3：`\\d{4}`（四位数字）
- **`matcher.group(n)`**：检索分组 `n` 匹配的文本（基于 1 的索引）。

**输出**：

```
区域号码：123
组号码：45
序列号码：6789
```

你也可以使用**命名分组**以提高清晰度：

```java
String regex = "(?<area>\\d{3})-(?<group>\\d{2})-(?<serial>\\d{4})";
Pattern pattern = Pattern.compile(regex);
Matcher matcher = pattern.matcher("123-45-6789");
if (matcher.matches()) {
    System.out.println("区域：" + matcher.group("area"));
    System.out.println("组：" + matcher.group("group"));
    System.out.println("序列：" + matcher.group("serial"));
}
```

## 附加功能和提示

### 标志

在 `Pattern.compile()` 中使用标志修改模式行为：

- **`Pattern.CASE_INSENSITIVE`**：匹配时忽略大小写。

  ```java
  Pattern pattern = Pattern.compile("hello", Pattern.CASE_INSENSITIVE);
  Matcher matcher = pattern.matcher("HELLO");
  System.out.println(matcher.matches()); // true
  ```

### 字符串方法

对于简单任务，使用 `String` 方法：

- **`matches()`**：检查整个字符串是否匹配正则表达式。

  ```java
  String text = "cat";
  System.out.println(text.matches("\\w{3}")); // true
  ```

- **`split()`**：按正则表达式模式分割字符串。

  ```java
  String data = "apple, banana, cherry";
  String[] fruits = data.split("\\s*,\\s*");
  // 输出：apple, banana, cherry
  ```

### 转义特殊字符

正则表达式使用特殊字符，如 `.`、`*` 和 `?`。要字面匹配它们，使用 `\\` 转义：

- 匹配句点：`"\\."`
- 在 Java 字符串中，转义反斜杠：`"\\d"` 表示数字，`"\\\\"` 表示字面反斜杠。

### 性能

编译模式代价高昂。尽可能重用 `Pattern` 对象：

```java
Pattern pattern = Pattern.compile("\\d+"); // 编译一次
for (String input : new String[]{"123", "456"}) {
    Matcher matcher = pattern.matcher(input);
    if (matcher.matches()) {
        System.out.println("数字：" + input);
    }
}
```

### 错误处理

无效的正则表达式模式会抛出 `PatternSyntaxException`。在生产代码中处理它：

```java
try {
    Pattern pattern = Pattern.compile("["); // 无效的正则表达式
} catch (PatternSyntaxException e) {
    System.err.println("无效的正则表达式：" + e.getMessage());
}
```

## 总结

- **编译模式**：`Pattern.compile(regex)`
- **创建匹配器**：`pattern.matcher(input)`
- **关键操作**：
  - `matches()`：全字符串匹配
  - `find()`：查找下一个匹配项
  - `group()`：提取匹配文本
  - `replaceAll()`：替换匹配项
- **便利性**：对于简单任务，使用 `String` 方法。
- **最佳实践**：转义特殊字符，重用模式，并处理异常。

这涵盖了 `java.util.regex` 的基本要点。对于高级主题，如前瞻或字符类，请查阅 [Java 文档](https://docs.oracle.com/en/java/javase/17/docs/api/java.util.regex/package-summary.html) 或针对特定用例进行实验！
