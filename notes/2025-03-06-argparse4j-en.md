---
audio: false
generated: true
lang: en
layout: post
title: Parsing Command-line Arguments in Java
translated: false
type: note
---

To use `net.sourceforge.argparse4j`, a Java library for parsing command-line arguments inspired by Python's `argparse`, follow these steps:

---

### 1. **Add the Dependency**

To include `argparse4j` in your project, add it as a dependency. If you're using Maven, update your `pom.xml` with the following:

```xml
<dependency>
    <groupId>net.sourceforge.argparse4j</groupId>
    <artifactId>argparse4j</artifactId>
    <version>0.9.0</version>
</dependency>
```

For other build tools like Gradle, check the [Maven Central Repository](https://central.sonatype.com/artifact/net.sourceforge.argparse4j/argparse4j) for the equivalent configuration.

---

### 2. **Create an `ArgumentParser` Object**

Start by creating an `ArgumentParser` instance using `ArgumentParsers.newFor("prog").build()`, where `"prog"` is the name of your program. You can also add a description and enable automatic help generation.

**Example:**

```java
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;

ArgumentParser parser = ArgumentParsers.newFor("Checksum").build()
    .defaultHelp(true)  // Enables -h/--help option
    .description("Calculate checksum of given files.");
```

---

### 3. **Add Arguments**

Define the command-line arguments your program will accept using `parser.addArgument()`. You can specify:

- **Optional arguments** (e.g., `-t`, `--type`) with flags, choices, defaults, and help text.
- **Positional arguments** (e.g., `file`) with optional variable-length support using `.nargs("*")`.

**Example:**

```java
parser.addArgument("-t", "--type")
    .choices("SHA-256", "SHA-512", "SHA1")  // Restrict to these options
    .setDefault("SHA-256")                  // Default value if not provided
    .help("Specify hash function to use");  // Description for help message

parser.addArgument("file")
    .nargs("*")                             // Accepts zero or more arguments
    .help("File to calculate checksum");    // Description for help message
```

---

### 4. **Parse Command-Line Arguments**

Parse the command-line arguments (typically passed as `String[] args` from your `main` method) using `parser.parseArgs()`. Wrap this in a try-catch block to handle parsing errors gracefully.

**Example:**

```java
import net.sourceforge.argparse4j.inf.Namespace;
import net.sourceforge.argparse4j.inf.ArgumentParserException;

public class Checksum {
    public static void main(String[] args) {
        ArgumentParser parser = ArgumentParsers.newFor("Checksum").build()
            .defaultHelp(true)
            .description("Calculate checksum of given files.");

        parser.addArgument("-t", "--type")
            .choices("SHA-256", "SHA-512", "SHA1").setDefault("SHA-256")
            .help("Specify hash function to use");
        parser.addArgument("file").nargs("*")
            .help("File to calculate checksum");

        Namespace ns = null;
        try {
            ns = parser.parseArgs(args);  // Parse the arguments
        } catch (ArgumentParserException e) {
            parser.handleError(e);        // Print error and help message
            System.exit(1);               // Exit on error
        }
    }
}
```

---

### 5. **Access Parsed Values**

The `parseArgs()` method returns a `Namespace` object containing the parsed argument values. Use methods like `getString()` or `getList()` to retrieve them.

**Example:**

```java
String hashType = ns.getString("type");  // e.g., "SHA-256"
List<String> files = ns.getList("file"); // List of file names

System.out.println("Hash Type: " + hashType);
System.out.println("Files: " + files);
```

---

### Putting It All Together

Here’s a complete example:

```java
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;
import java.util.List;

public class Checksum {
    public static void main(String[] args) {
        // Step 2: Create parser
        ArgumentParser parser = ArgumentParsers.newFor("Checksum").build()
            .defaultHelp(true)
            .description("Calculate checksum of given files.");

        // Step 3: Add arguments
        parser.addArgument("-t", "--type")
            .choices("SHA-256", "SHA-512", "SHA1").setDefault("SHA-256")
            .help("Specify hash function to use");
        parser.addArgument("file").nargs("*")
            .help("File to calculate checksum");

        // Step 4: Parse arguments
        Namespace ns = null;
        try {
            ns = parser.parseArgs(args);
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        // Step 5: Access parsed values
        String hashType = ns.getString("type");
        List<String> files = ns.getList("file");

        // Example output
        System.out.println("Hash Type: " + hashType);
        System.out.println("Files: " + files);
    }
}
```

---

### Additional Features

- **Automatic Help**: Run your program with `-h` or `--help` to see a generated help message.
- **Subcommands**: Use `parser.addSubparsers()` for complex commands (e.g., `git commit`, `git push`).
- **Annotations**: Bind arguments to class fields using annotations (see the user manual for details).

For more advanced usage, consult the [Argparse4j User Manual](https://argparse4j.github.io/userguide.html).

---

This workflow lets you easily parse and handle command-line arguments in your Java application using `net.sourceforge.argparse4j`.
