---
audio: false
generated: true
lang: en
layout: post
title: Regular Expressions in Java
translated: false
type: note
---

# How to Use `java.util.regex` in Java

The `java.util.regex` package in Java provides tools for working with regular expressions (regex), which are patterns used to match and manipulate text. This guide will walk you through the basics of using this package, focusing on the two main classes: `Pattern` and `Matcher`. I'll also cover common use cases with examples to help you get started.

## Overview of `java.util.regex`

The `java.util.regex` package includes:

- **`Pattern`**: Represents a compiled regular expression. You create it from a regex string.
- **`Matcher`**: Applies the pattern to a specific input string and performs matching operations.

Additionally, Java's `String` class offers regex-based methods for simpler tasks.

## Basic Steps to Use `java.util.regex`

To use regular expressions in Java, follow these steps:

1. **Compile a Pattern**: Convert your regex string into a `Pattern` object.
2. **Create a Matcher**: Use the pattern to create a `Matcher` for your input text.
3. **Perform Operations**: Use the matcher to check for matches, find patterns, or manipulate text.

Here’s how it works in practice.

## Example 1: Validating an Email Address

Let’s create a simple email validator using a basic regex pattern: `".+@.+\\..+"`. This pattern matches strings with at least one character before and after an `@` symbol, followed by a dot and more characters (e.g., `example@test.com`).

```java
import java.util.regex.*;

public class EmailValidator {
    public static boolean isValidEmail(String email) {
        // Define the regex pattern
        String regex = ".+@.+\\..+";
        // Compile the pattern
        Pattern pattern = Pattern.compile(regex);
        // Create a matcher for the input string
        Matcher matcher = pattern.matcher(email);
        // Check if the entire string matches the pattern
        return matcher.matches();
    }

    public static void main(String[] args) {
        String email = "example@test.com";
        if (isValidEmail(email)) {
            System.out.println("Valid email");
        } else {
            System.out.println("Invalid email");
        }
    }
}
```

### Explanation
- **`Pattern.compile(regex)`**: Compiles the regex string into a `Pattern` object.
- **`pattern.matcher(email)`**: Creates a `Matcher` for the input string `email`.
- **`matcher.matches()`**: Returns `true` if the entire string matches the pattern, `false` otherwise.

**Output**: `Valid email`

Note: This is a simplified email pattern. Real email validation requires a more complex regex (e.g., per RFC 5322), but this serves as a starting point.

## Example 2: Finding All Hashtags in a String

Suppose you want to extract all hashtags (e.g., `#java`) from a tweet. Use the regex `"#\\w+"`, where `#` matches the literal hashtag symbol and `\\w+` matches one or more word characters (letters, digits, or underscores).

```java
import java.util.regex.*;

public class HashtagExtractor {
    public static void main(String[] args) {
        String tweet = "This is a #sample tweet with #multiple hashtags like #java";
        String regex = "#\\w+";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(tweet);

        // Find all matches
        while (matcher.find()) {
            System.out.println(matcher.group());
        }
    }
}
```

### Explanation
- **`matcher.find()`**: Moves to the next match in the input string and returns `true` if a match is found.
- **`matcher.group()`**: Returns the matched text for the current match.

**Output**:
```
#sample
#multiple
#java
```

## Example 3: Replacing Text with Regex

To replace all occurrences of a word (e.g., censoring "badword" with asterisks), you can use the `String.replaceAll()` method, which uses regex internally.

```java
public class TextCensor {
    public static void main(String[] args) {
        String text = "This is a badword example with badword repeated.";
        String censored = text.replaceAll("badword", "*******");
        System.out.println(censored);
    }
}
```

**Output**: `This is a ******* example with ******* repeated.`

For more complex replacements, use `Matcher`:

```java
import java.util.regex.*;

public class ComplexReplacement {
    public static void main(String[] args) {
        String text = "Contact: 123-456-7890";
        String regex = "\\d{3}-\\d{3}-\\d{4}"; // Matches phone numbers
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(text);
        String result = matcher.replaceAll("XXX-XXX-XXXX");
        System.out.println(result);
    }
}
```

**Output**: `Contact: XXX-XXX-XXXX`

## Example 4: Using Groups to Parse Structured Data

Regex groups, defined with parentheses `()`, allow you to capture parts of a match. For example, to parse a Social Security Number (SSN) like `123-45-6789`:

```java
import java.util.regex.*;

public class SSNParser {
    public static void main(String[] args) {
        String ssn = "123-45-6789";
        String regex = "(\\d{3})-(\\d{2})-(\\d{4})"; // Groups for area, group, serial
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(ssn);

        if (matcher.matches()) {
            System.out.println("Area number: " + matcher.group(1));
            System.out.println("Group number: " + matcher.group(2));
            System.out.println("Serial number: " + matcher.group(3));
        }
    }
}
```

### Explanation
- **`"(\\d{3})-(\\d{2})-(\\d{4})"`**: Defines three groups:
  - Group 1: `\\d{3}` (three digits)
  - Group 2: `\\d{2}` (two digits)
  - Group 3: `\\d{4}` (four digits)
- **`matcher.group(n)`**: Retrieves the text matched by group `n` (1-based index).

**Output**:
```
Area number: 123
Group number: 45
Serial number: 6789
```

You can also use **named groups** for clarity:

```java
String regex = "(?<area>\\d{3})-(?<group>\\d{2})-(?<serial>\\d{4})";
Pattern pattern = Pattern.compile(regex);
Matcher matcher = pattern.matcher("123-45-6789");
if (matcher.matches()) {
    System.out.println("Area: " + matcher.group("area"));
    System.out.println("Group: " + matcher.group("group"));
    System.out.println("Serial: " + matcher.group("serial"));
}
```

## Additional Features and Tips

### Flags
Modify pattern behavior with flags in `Pattern.compile()`:
- **`Pattern.CASE_INSENSITIVE`**: Ignores case when matching.
  ```java
  Pattern pattern = Pattern.compile("hello", Pattern.CASE_INSENSITIVE);
  Matcher matcher = pattern.matcher("HELLO");
  System.out.println(matcher.matches()); // true
  ```

### String Methods
For simple tasks, use `String` methods:
- **`matches()`**: Checks if the entire string matches a regex.
  ```java
  String text = "cat";
  System.out.println(text.matches("\\w{3}")); // true
  ```
- **`split()`**: Splits a string by a regex pattern.
  ```java
  String data = "apple, banana, cherry";
  String[] fruits = data.split("\\s*,\\s*");
  // Outputs: apple, banana, cherry
  ```

### Escaping Special Characters
Regex uses special characters like `.`, `*`, and `?`. To match them literally, escape with `\\`:
- Match a period: `"\\."`
- In Java strings, escape backslashes: `"\\d"` for digits, `"\\\\"` for a literal backslash.

### Performance
Compiling a pattern is costly. Reuse `Pattern` objects when possible:
```java
Pattern pattern = Pattern.compile("\\d+"); // Compile once
for (String input : new String[]{"123", "456"}) {
    Matcher matcher = pattern.matcher(input);
    if (matcher.matches()) {
        System.out.println("Number: " + input);
    }
}
```

### Error Handling
Invalid regex patterns throw `PatternSyntaxException`. Handle it in production code:
```java
try {
    Pattern pattern = Pattern.compile("["); // Invalid regex
} catch (PatternSyntaxException e) {
    System.err.println("Invalid regex: " + e.getMessage());
}
```

## Summary

- **Compile a Pattern**: `Pattern.compile(regex)`
- **Create a Matcher**: `pattern.matcher(input)`
- **Key Operations**:
  - `matches()`: Full string match
  - `find()`: Find next match
  - `group()`: Extract matched text
  - `replaceAll()`: Replace matches
- **Convenience**: Use `String` methods for simple tasks.
- **Best Practices**: Escape special characters, reuse patterns, and handle exceptions.

This covers the essentials of `java.util.regex`. For advanced topics like lookaheads or character classes, consult the [Java documentation](https://docs.oracle.com/en/java/javase/17/docs/api/java.util.regex/package-summary.html) or experiment with specific use cases!
