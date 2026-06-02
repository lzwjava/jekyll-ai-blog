---
audio: false
generated: true
lang: en
layout: post
title: Google Java Style Guide
translated: false
type: note
---

## 1. Source File Basics

- **File Naming**:
  - Source files are named with the case-sensitive name of the top-level class they contain
  - Files must use UTF-8 encoding
  - Special characters in file names are discouraged

## 2. Source File Structure

### Source File Organization

1. Package statement
2. Import statements
3. Exactly one top-level class

### Import Statement Rules

- No wildcard imports
- Static imports are allowed
- Imports are organized in a specific order:
  - All static imports
  - All non-static imports
  - Imports within each group are alphabetized

## 3. Formatting Guidelines

### Indentation and Braces

- Use 2 spaces for indentation (not tabs)
- Braces are used with `if`, `else`, `for`, `do`, and `while` statements, even for single-line blocks
- K&R style of brace placement is recommended

  ```java
  public void method() {
    if (condition) {
      // Code block
    }
  }
  ```

### Line Length and Wrapping

- Maximum line length is 100 characters
- Line breaks are preferred at higher-level syntax breaks
- When breaking method call chains, the break occurs before the `.`

## 4. Naming Conventions

### General Rules

- **Packages**: Lowercase, no underscores
- **Classes**: UpperCamelCase
- **Methods**: lowerCamelCase
- **Constants**: UPPER_SNAKE_CASE
- **Non-constant Fields**: lowerCamelCase
- **Parameters**: lowerCamelCase
- **Local Variables**: lowerCamelCase

### Specific Naming Practices

- Avoid abbreviations
- Exception names must end with `Exception`
- Test classes are named `TestClassName`

## 5. Programming Practices

### Java Language Rules

- **Exceptions**:
  - Catch specific exceptions
  - Avoid empty catch blocks
  - Always include a detailed error message
- **Final Keyword**:
  - Use `final` for method parameters
  - Prefer immutable objects
- **Annotations**:
  - `@Override` is mandatory for overriding methods
  - Use standard annotations appropriately

### Code Structure

- Prefer composition over inheritance
- Keep methods short and focused
- One statement per line
- Avoid deep nesting of conditionals

## 6. Comments and Documentation

### Javadoc Guidelines

- All public classes and methods must have Javadoc
- Javadoc comments start with `/**`
- Include description, parameters, return values, and exceptions
- Use `@param`, `@return`, `@throws` tags

### Inline Comments

- Use sparingly
- Explain "why", not "what"
- Keep comments concise and meaningful

## 7. Version Control Considerations

- Avoid committing commented-out code
- Use version control system features instead of code comments for tracking changes

## 8. Performance Considerations

- Prefer enhanced `for` loops
- Use `StringBuilder` for string concatenation
- Close resources using try-with-resources
- Avoid creating unnecessary objects

## 9. Testing Principles

- Write unit tests
- Aim for high code coverage
- Use JUnit for testing
- Mock external dependencies
- Test edge cases and error conditions

## 10. Additional Tools

- Google provides a Java formatter and static analysis tools
- CheckStyle and Error Prone can be used to enforce style guidelines

## Conclusion

The Google Java Style Guide provides a comprehensive set of guidelines to ensure consistent, readable, and maintainable Java code across projects.
