---
audio: false
generated: true
lang: en
layout: post
title: Oracle's Code Conventions for the Java Programming Language
translated: false
type: note
---

## 1. File Organization

### 1.1 File Names

- Source files must have the `.java` extension
- Source filenames must exactly match the public class name in the file
- Examples:
  - `MyClass.java` contains a public class named `MyClass`
  - `CircleShape.java` contains a public class named `CircleShape`

### 1.2 File Structure

1. Beginning comments
2. Package statement
3. Import statements
4. Class and interface declarations

## 2. Formatting and Indentation

### 2.1 Indentation

- Use 4 spaces for indentation (not tabs)
- Indent continuation lines by 8 spaces
- Braces should align vertically

### 2.2 Line Length

- Recommended maximum line length is 80 characters
- For long statements, break lines at a higher logical level

### 2.3 Wrapping Lines

- Break line before an operator
- Align the new line with the beginning of the expression at the same level

## 3. Comments

### 3.1 File Comments

- Every source file should start with a comment block:

  ```java
  /*
   * Classname
   *
   * Version information
   *
   * Date
   *
   * Copyright notice
   */
  ```

### 3.2 Implementation Comments

- Use `/* */` for multi-line comments
- Use `//` for single-line comments
- Comments should explain "why", not "what"

### 3.3 Documentation Comments

- Use Javadoc-style comments for classes, interfaces, methods
- Include:
  - Brief description
  - `@param` for method parameters
  - `@return` for return values
  - `@throws` for exceptions

## 4. Declarations

### 4.1 Number Per Line

- One declaration per line
- Recommended:

  ```java
  int level;        // Correct
  int size;         // Correct

  // Avoid:
  int level, size;  // Not recommended
  ```

### 4.2 Initialization

- Initialize variables at declaration when possible
- Group related declarations together

## 5. Statements

### 5.1 Simple Statements

- One statement per line
- Use a space after commas
- Use spaces around operators

### 5.2 Compound Statements

- Braces are used with `if`, `else`, `for`, `while`, `do` statements, even for single-line blocks

### 5.3 Return Statements

- Prefer explicit return
- Avoid unnecessary `else` after `return`

## 6. Naming Conventions

### 6.1 Package Names

- All lowercase
- Unique prefix, often company domain reversed
- Example: `com.company.project`

### 6.2 Class Names

- UpperCamelCase
- Noun or noun phrases
- Examples: `DataProcessor`, `HttpClient`

### 6.3 Interface Names

- Similar to class names
- Consider describing behavior
- Examples: `Runnable`, `Serializable`

### 6.4 Method Names

- lowerCamelCase
- Verb or verb phrases
- Examples: `calculateTotal()`, `sendMessage()`

### 6.5 Variable Names

- lowerCamelCase
- Meaningful and descriptive
- Avoid single-letter names except for temporary variables

### 6.6 Constant Names

- ALL_UPPERCASE with underscores
- Example: `MAX_VALUE`, `COLOR_RED`

## 7. Programming Practices

### 7.1 Visibility

- Use the lowest possible visibility
- Prefer `private` over `public`
- Use accessor methods for class fields

### 7.2 Variable Scope

- Declare variables in the smallest scope possible
- Initialize variables close to their first use

### 7.3 Exception Handling

- Always include a message in exceptions
- Catch specific exceptions
- Use try-catch-finally appropriately

## 8. Best Practices

### 8.1 Avoid Magic Numbers

- Use named constants instead of literal numbers
- Improve code readability and maintainability

### 8.2 Prefer Immutability

- Use `final` for variables that don't change
- Create immutable classes when possible

## Conclusion

These conventions aim to improve code readability, maintainability, and consistency across Java projects.
