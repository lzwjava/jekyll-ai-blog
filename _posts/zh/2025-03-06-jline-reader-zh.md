---
audio: false
generated: true
lang: zh
layout: post
title: Java控制台输入读取
translated: true
type: note
---

要在 Java 中使用 `org.jline.reader` 包（JLine 库的一部分，用于处理具有行编辑、历史记录和补全等高级功能的控制台输入），请按照以下步骤操作。本指南提供完整且实用的方法帮助您快速上手。

### 前置条件
确保已将 JLine 库添加到项目中。如果使用 Maven，请在 `pom.xml` 中包含以下依赖项：

```xml
<dependency>
    <groupId>org.jline</groupId>
    <artifactId>jline</artifactId>
    <version>3.21.0</version> <!-- 使用最新版本 -->
</dependency>
```

### 使用 `org.jline.reader` 的基本步骤

1. **创建 Terminal 实例**
   - 使用 `org.jline.terminal` 中的 `TerminalBuilder` 类创建 `Terminal` 对象。该对象代表将读取输入的控制台环境。
   - 示例：
     ```java
     import org.jline.terminal.Terminal;
     import org.jline.terminal.TerminalBuilder;

     Terminal terminal = TerminalBuilder.builder().build();
     ```
   - `build()` 方法创建适用于大多数环境的默认终端。您可以进一步自定义（例如设置终端类型），但默认设置通常已足够。

2. **创建 LineReader 实例**
   - 使用 `org.jline.reader` 中的 `LineReaderBuilder` 类创建 `LineReader` 对象，并将 `Terminal` 实例传递给它。
   - `LineReader` 是使用 JLine 功能读取用户输入的主要接口。
   - 示例：
     ```java
     import org.jline.reader.LineReader;
     import org.jline.reader.LineReaderBuilder;

     LineReader reader = LineReaderBuilder.builder()
         .terminal(terminal)
         .build();
     ```

3. **读取用户输入**
   - 使用 `LineReader` 的 `readLine()` 方法读取用户输入的一行文本。可以选择指定要显示的提示符。
   - 示例：
     ```java
     String line = reader.readLine("> ");
     ```
   - 这会显示 `> ` 作为提示符，等待用户输入，并在用户按下 Enter 键时返回输入的字符串。

### 简单示例
以下是一个完整的极简示例，循环读取用户输入，直到用户输入 "exit"：

```java
import org.jline.reader.LineReader;
import org.jline.reader.LineReaderBuilder;
import org.jline.terminal.Terminal;
import org.jline.terminal.TerminalBuilder;

public class ConsoleExample {
    public static void main(String[] args) throws Exception {
        // 创建 Terminal
        Terminal terminal = TerminalBuilder.builder().build();

        // 创建 LineReader
        LineReader reader = LineReaderBuilder.builder()
            .terminal(terminal)
            .build();

        // 循环读取输入
        String line;
        while ((line = reader.readLine("> ")) != null) {
            System.out.println("您输入的是: " + line);
            if (line.equals("exit")) {
                break;
            }
        }
    }
}
```

- **输出**：运行此程序时，会显示 `> ` 提示符。您可以输入文本，使用退格键或箭头键进行编辑（这是 `System.in` 不易实现的功能），然后按 Enter 键。输入 "exit" 将结束程序。

### 可选功能
您可以通过附加功能增强 `LineReader`：

#### 1. **启用命令历史记录**
   - 添加 `History` 对象以存储和调用先前的输入（例如，使用上/下箭头键）。
   - 示例：
     ```java
     import org.jline.reader.impl.history.DefaultHistory;
     import org.jline.reader.History;

     History history = new DefaultHistory();
     LineReader reader = LineReaderBuilder.builder()
         .terminal(terminal)
         .history(history)
         .build();
     ```
   - 现在，用户可以在其输入历史记录中导航。

#### 2. **添加自动补全**
   - 实现一个 `Completer`，以便在用户按下 Tab 键时建议补全选项。
   - 使用简单字符串补全器的示例：
     ```java
     import org.jline.reader.Completer;
     import org.jline.reader.impl.completer.StringsCompleter;

     Completer completer = new StringsCompleter("foo", "bar", "baz");
     LineReader reader = LineReaderBuilder.builder()
         .terminal(terminal)
         .completer(completer)
         .build();
     ```
   - 输入 "f" 并按 Tab 键会建议 "foo"。

#### 3. **读取密码（掩码输入）**
   - 使用带有掩码字符的 `readLine()` 来隐藏输入（例如，用于密码）。
   - 示例：
     ```java
     String password = reader.readLine("输入密码: ", '*');
     ```
   - 显示星号（`*`）而不是键入的字符。

### 资源管理
为了确保应用程序的健壮性，请在完成后关闭 `Terminal` 以释放资源。由于 `Terminal` 实现了 `Closeable`，可以使用 try-with-resources 块：

```java
try (Terminal terminal = TerminalBuilder.builder().build()) {
    LineReader reader = LineReaderBuilder.builder()
        .terminal(terminal)
        .build();
    String line = reader.readLine("> ");
    System.out.println("您输入的是: " + line);
}
```

### 为什么使用 `org.jline.reader`？
与使用 `System.in` 和 `BufferedReader` 的基本输入相比，`org.jline.reader` 提供：
- **行编辑**：退格键、光标移动等。
- **历史记录**：调用先前的输入。
- **补全**：自动建议选项。
- **跨平台终端处理**：在不同环境中保持一致的工作方式。

### 注意事项
- 如果未在 `LineReaderBuilder` 中指定 `Terminal`，它会在内部创建一个默认终端，因此 `LineReader reader = LineReaderBuilder.builder().build();` 适用于简单情况。
- 避免同时从多个线程调用 `readLine()`，因为 `LineReader` 对于并发读取不是线程安全的。
- 对于高级用例（例如，多行输入、自定义键绑定），请探索 JLine 的附加功能，如解析器或键映射。

这涵盖了在 Java 中有效使用 `org.jline.reader` 读取控制台输入的基本要点。从基本设置开始，并根据应用程序的需要添加历史记录或补全等功能！
