---
audio: false
generated: true
lang: en
layout: post
title: Reading Console Input in Java
translated: false
type: note
---

To use the `org.jline.reader` package in Java, which is part of the JLine library for handling console input with advanced features like line editing, history, and completion, follow these steps. This guide provides a complete and practical approach to get you started.

### Prerequisites
Ensure you have the JLine library added to your project. If you're using Maven, include the following dependency in your `pom.xml`:

```xml
<dependency>
    <groupId>org.jline</groupId>
    <artifactId>jline</artifactId>
    <version>3.21.0</version> <!-- Use the latest version -->
</dependency>
```

### Basic Steps to Use `org.jline.reader`

1. **Create a Terminal Instance**
   - Use the `TerminalBuilder` class from `org.jline.terminal` to create a `Terminal` object. This represents the console environment where input will be read.
   - Example:
     ```java
     import org.jline.terminal.Terminal;
     import org.jline.terminal.TerminalBuilder;

     Terminal terminal = TerminalBuilder.builder().build();
     ```
   - The `build()` method creates a default terminal suitable for most environments. You can customize it further (e.g., setting terminal type), but the default is often sufficient.

2. **Create a LineReader Instance**
   - Use the `LineReaderBuilder` class from `org.jline.reader` to create a `LineReader` object, passing the `Terminal` instance to it.
   - The `LineReader` is the main interface for reading user input with JLine's features.
   - Example:
     ```java
     import org.jline.reader.LineReader;
     import org.jline.reader.LineReaderBuilder;

     LineReader reader = LineReaderBuilder.builder()
         .terminal(terminal)
         .build();
     ```

3. **Read Input from the User**
   - Use the `readLine()` method of `LineReader` to read a line of text entered by the user. You can optionally specify a prompt to display.
   - Example:
     ```java
     String line = reader.readLine("> ");
     ```
   - This displays `> ` as a prompt, waits for user input, and returns the entered string when the user presses Enter.

### Simple Example
Here’s a complete, minimal example that reads user input in a loop until the user types "exit":

```java
import org.jline.reader.LineReader;
import org.jline.reader.LineReaderBuilder;
import org.jline.terminal.Terminal;
import org.jline.terminal.TerminalBuilder;

public class ConsoleExample {
    public static void main(String[] args) throws Exception {
        // Create Terminal
        Terminal terminal = TerminalBuilder.builder().build();

        // Create LineReader
        LineReader reader = LineReaderBuilder.builder()
            .terminal(terminal)
            .build();

        // Read input in a loop
        String line;
        while ((line = reader.readLine("> ")) != null) {
            System.out.println("You entered: " + line);
            if (line.equals("exit")) {
                break;
            }
        }
    }
}
```

- **Output**: When you run this, it displays a `> ` prompt. You can type text, use backspace or arrow keys for editing (features not easily available with `System.in`), and press Enter. Typing "exit" ends the program.

### Optional Features
You can enhance the `LineReader` with additional functionality:

#### 1. **Enable Command History**
   - Add a `History` object to store and recall previous inputs (e.g., using up/down arrow keys).
   - Example:
     ```java
     import org.jline.reader.impl.history.DefaultHistory;
     import org.jline.reader.History;

     History history = new DefaultHistory();
     LineReader reader = LineReaderBuilder.builder()
         .terminal(terminal)
         .history(history)
         .build();
     ```
   - Now, the user can navigate through their input history.

#### 2. **Add Auto-Completion**
   - Implement a `Completer` to suggest completions when the user presses Tab.
   - Example with a simple string completer:
     ```java
     import org.jline.reader.Completer;
     import org.jline.reader.impl.completer.StringsCompleter;

     Completer completer = new StringsCompleter("foo", "bar", "baz");
     LineReader reader = LineReaderBuilder.builder()
         .terminal(terminal)
         .completer(completer)
         .build();
     ```
   - Typing "f" and pressing Tab suggests "foo".

#### 3. **Read Passwords (Masked Input)**
   - Use `readLine()` with a mask character to hide input (e.g., for passwords).
   - Example:
     ```java
     String password = reader.readLine("Enter password: ", '*');
     ```
   - Displays asterisks (`*`) instead of the typed characters.

### Resource Management
For robust applications, close the `Terminal` when done to free resources. Since `Terminal` implements `Closeable`, use a try-with-resources block:

```java
try (Terminal terminal = TerminalBuilder.builder().build()) {
    LineReader reader = LineReaderBuilder.builder()
        .terminal(terminal)
        .build();
    String line = reader.readLine("> ");
    System.out.println("You entered: " + line);
}
```

### Why Use `org.jline.reader`?
Unlike basic input with `System.in` and `BufferedReader`, `org.jline.reader` provides:
- **Line Editing**: Backspace, cursor movement, etc.
- **History**: Recall previous inputs.
- **Completion**: Auto-suggest options.
- **Cross-Platform Terminal Handling**: Works consistently across different environments.

### Notes
- If you don’t specify a `Terminal` in `LineReaderBuilder`, it creates a default one internally, so `LineReader reader = LineReaderBuilder.builder().build();` works for simple cases.
- Avoid calling `readLine()` from multiple threads simultaneously, as `LineReader` is not thread-safe for concurrent reads.
- For advanced use cases (e.g., multi-line input, custom key bindings), explore additional JLine features like parsers or key maps.

This covers the essentials of using `org.jline.reader` to read console input in Java effectively. Start with the basic setup and add features like history or completion as needed for your application!
