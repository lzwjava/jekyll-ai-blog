---
audio: false
generated: true
lang: zh
layout: post
title: 使用Apache Commons Lang生成随机字符串
translated: true
type: note
---

`RandomStringUtils` 是 Apache Commons Lang 库中一个非常实用的类，提供了多种生成随机字符串的静态方法。包括生成特定长度的字符串、仅包含字母、仅包含数字、字母数字字符，甚至是从自定义字符集中生成字符串。

以下是使用方法及所需的 Maven 依赖：

## 如何使用 `org.apache.commons.lang3.RandomStringUtils;`

首先，需要在 Java 文件中导入该类：

```java
import org.apache.commons.lang3.RandomStringUtils;
```

然后就可以使用其静态方法。以下是一些常见示例：

1.  **生成指定长度的随机字母数字字符串：**

    ```java
    String randomAlphaNumeric = RandomStringUtils.randomAlphanumeric(10);
    System.out.println("随机字母数字: " + randomAlphaNumeric); // 例如："aB5cY2x9Pq"
    ```

2.  **生成指定长度的随机字母字符串：**

    ```java
    String randomAlphabetic = RandomStringUtils.randomAlphabetic(8);
    System.out.println("随机字母: " + randomAlphabetic); // 例如："GhJkLmNo"
    ```

3.  **生成指定长度的随机数字字符串：**

    ```java
    String randomNumeric = RandomStringUtils.randomNumeric(6);
    System.out.println("随机数字: " + randomNumeric); // 例如："123456"
    ```

4.  **生成混合字母和数字的随机字符串，指定标志位：**

    ```java
    String randomLettersAndNumbers = RandomStringUtils.random(12, true, true);
    System.out.println("随机字母和数字: " + randomLettersAndNumbers); // 例如："abC123DeF456"
    ```

5.  **从自定义字符集生成随机字符串：**

    ```java
    String chars = "abcdefg";
    String randomFromCustomSet = RandomStringUtils.random(5, chars);
    System.out.println("自定义字符集随机: " + randomFromCustomSet); // 例如："gcfae"
    ```

## 在 `pom.xml` 中使用哪个库

要在 Maven 项目中使用 `RandomStringUtils`，需要将 `commons-lang3` 依赖项添加到 `pom.xml` 文件中。

以下是依赖代码片段：

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.14.0</version> </dependency>
```

**重要提示：**

  * **版本：** 请务必检查 [Maven Central](https://mvnrepository.com/artifact/org.apache.commons/commons-lang3) 以获取 `commons-lang3` 的最新稳定版本。据我上次更新，`3.14.0` 或更高版本是不错的选择，但最好始终使用可用的绝对最新稳定版本。
  * **作用域：** 依赖项的默认作用域是 `compile`，这通常是像这样的工具库所需要的。这意味着该 JAR 在编译、测试和运行时都可用。如果仅用于测试，可以使用 `<scope>test</scope>`。
  * **弃用说明：** 请注意，Apache Commons Lang 3 的较新版本中已弃用了一些旧方法，例如 `RandomStringUtils.randomAlphabetic(int count)`。相反，建议使用 `secure()`、`secureStrong()` 或 `insecure()` 方法，这些方法能更好地控制随机源。例如：`RandomStringUtils.secure().nextAlphanumeric(10)`。然而，对于许多用例，旧方法仍然有效。
