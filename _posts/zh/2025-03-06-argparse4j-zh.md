---
audio: false
generated: true
lang: zh
layout: post
title: Java命令行参数解析
translated: true
type: note
---

要使用 `net.sourceforge.argparse4j`（这个受 Python `argparse` 启发的 Java 命令行参数解析库），请按照以下步骤操作：

---

### 1. **添加依赖**

要在项目中引入 `argparse4j`，请将其添加为依赖项。如果使用 Maven，请在 `pom.xml` 中添加以下内容：

```xml
<dependency>
    <groupId>net.sourceforge.argparse4j</groupId>
    <artifactId>argparse4j</artifactId>
    <version>0.9.0</version>
</dependency>
```

对于 Gradle 等其他构建工具，请查看 [Maven 中央仓库](https://central.sonatype.com/artifact/net.sourceforge.argparse4j/argparse4j) 获取等效配置。

---

### 2. **创建 `ArgumentParser` 对象**

首先使用 `ArgumentParsers.newFor("prog").build()` 创建 `ArgumentParser` 实例，其中 `"prog"` 是程序名称。您还可以添加描述并启用自动帮助生成。

**示例：**

```java
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;

ArgumentParser parser = ArgumentParsers.newFor("Checksum").build()
    .defaultHelp(true)  // 启用 -h/--help 选项
    .description("计算指定文件的校验和。");
```

---

### 3. **添加参数**

使用 `parser.addArgument()` 定义程序将接受的命令行参数。您可以指定：

- **可选参数**（如 `-t`、`--type`），包含标志、选项、默认值和帮助文本
- **位置参数**（如 `file`），支持使用 `.nargs("*")` 的可变长度

**示例：**

```java
parser.addArgument("-t", "--type")
    .choices("SHA-256", "SHA-512", "SHA1")  // 限制为这些选项
    .setDefault("SHA-256")                  // 未提供时的默认值
    .help("指定要使用的哈希函数");           // 帮助消息中的描述

parser.addArgument("file")
    .nargs("*")                             // 接受零个或多个参数
    .help("要计算校验和的文件");             // 帮助消息中的描述
```

---

### 4. **解析命令行参数**

使用 `parser.parseArgs()` 解析命令行参数（通常从 `main` 方法作为 `String[] args` 传入）。将其包装在 try-catch 块中以优雅处理解析错误。

**示例：**

```java
import net.sourceforge.argparse4j.inf.Namespace;
import net.sourceforge.argparse4j.inf.ArgumentParserException;

public class Checksum {
    public static void main(String[] args) {
        ArgumentParser parser = ArgumentParsers.newFor("Checksum").build()
            .defaultHelp(true)
            .description("计算指定文件的校验和。");

        parser.addArgument("-t", "--type")
            .choices("SHA-256", "SHA-512", "SHA1").setDefault("SHA-256")
            .help("指定要使用的哈希函数");
        parser.addArgument("file").nargs("*")
            .help("要计算校验和的文件");

        Namespace ns = null;
        try {
            ns = parser.parseArgs(args);  // 解析参数
        } catch (ArgumentParserException e) {
            parser.handleError(e);        // 打印错误和帮助消息
            System.exit(1);               // 出错时退出
        }
    }
}
```

---

### 5. **访问解析值**

`parseArgs()` 方法返回包含解析后参数值的 `Namespace` 对象。使用 `getString()` 或 `getList()` 等方法获取这些值。

**示例：**

```java
String hashType = ns.getString("type");  // 例如 "SHA-256"
List<String> files = ns.getList("file"); // 文件名列表

System.out.println("哈希类型：" + hashType);
System.out.println("文件：" + files);
```

---

### 完整示例

以下是一个完整示例：

```java
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;
import java.util.List;

public class Checksum {
    public static void main(String[] args) {
        // 步骤 2：创建解析器
        ArgumentParser parser = ArgumentParsers.newFor("Checksum").build()
            .defaultHelp(true)
            .description("计算指定文件的校验和。");

        // 步骤 3：添加参数
        parser.addArgument("-t", "--type")
            .choices("SHA-256", "SHA-512", "SHA1").setDefault("SHA-256")
            .help("指定要使用的哈希函数");
        parser.addArgument("file").nargs("*")
            .help("要计算校验和的文件");

        // 步骤 4：解析参数
        Namespace ns = null;
        try {
            ns = parser.parseArgs(args);
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        // 步骤 5：访问解析值
        String hashType = ns.getString("type");
        List<String> files = ns.getList("file");

        // 示例输出
        System.out.println("哈希类型：" + hashType);
        System.out.println("文件：" + files);
    }
}
```

---

### 附加功能

- **自动帮助**：使用 `-h` 或 `--help` 运行程序查看生成的帮助消息
- **子命令**：对复杂命令使用 `parser.addSubparsers()`（如 `git commit`、`git push`）
- **注解**：使用注解将参数绑定到类字段（详见用户手册）

有关高级用法，请参阅 [Argparse4j 用户手册](https://argparse4j.github.io/userguide.html)。

---

这个工作流程让您能够使用 `net.sourceforge.argparse4j` 轻松解析和处理 Java 应用程序中的命令行参数。
