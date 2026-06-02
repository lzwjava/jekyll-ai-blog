---
audio: false
generated: true
lang: en
layout: post
title: Mastering IntelliJ's Structural Replace
translated: false
type: note
---

Sure, let's break down IntelliJ IDEA's Structural Replace feature.

IntelliJ IDEA's Structural Replace is an incredibly powerful, yet often underutilized, feature that allows you to find and replace code patterns based on their **structure** rather than just their textual content. This goes far beyond simple text search and replace, enabling complex refactorings, code style enforcement, and bug fixes across a large codebase.

Here's a comprehensive guide:

-----

## IntelliJ IDEA Structural Replace: A Comprehensive Guide

### 1\. What is Structural Search and Replace (SSR)?

At its core, SSR in IntelliJ IDEA is about working with Abstract Syntax Trees (ASTs). Instead of searching for literal strings, you define a *pattern* that describes the structure of the code you want to find (Structural Search) and another pattern that describes how you want to transform it (Structural Replace).

This allows you to:

  * **Refactor code:** Change the way methods are called, reorder parameters, encapsulate fields, etc.
  * **Enforce coding standards:** Ensure consistent usage of specific language constructs or API calls.
  * **Fix common bugs:** Identify and correct recurring logical errors.
  * **Migrate APIs:** Update code when libraries or frameworks change.
  * **Clean up deprecated code:** Find and replace old API usages with new ones.

### 2\. Accessing Structural Search and Replace

You can access the SSR dialog in two ways:

  * **Go to Edit -\> Find -\> Search Structurally...** (for searching)
  * **Go to Edit -\> Find -\> Replace Structurally...** (for replacing directly)

The dialog for both is very similar, with "Replace Structurally" simply adding a "Replace Template" field.

### 3\. Understanding the Structural Search Dialog

The Structural Search dialog is where you define your search pattern.

#### 3.1. Search Template

This is the most crucial part. You write a code snippet that represents the *structure* you're looking for.

**Key Concepts:**

  * **Literal Code:** Any code you write directly will be matched literally.
  * **Variables:** Use variables to represent parts of the code that can vary. Variables are defined using a special syntax and then configured with constraints.
      * **Common variable syntax:** `$variableName$` (enclosed in dollar signs).
      * **Example:** `System.out.println($arg$);` will find any `System.out.println` call, where `$arg$` will match whatever is inside the parentheses.

#### 3.2. Script Constraints (on variables)

After defining variables in your "Search Template," you need to specify their constraints. This is done by selecting the variable in the template (or placing your cursor on it) and then using the "Edit variables" button (often a small pencil icon next to the template field or accessible via the "Variables" tab).

Common constraints include:

  * **Text (regexp):** A regular expression that the text content of the variable must match.
  * **Type (regexp):** A regular expression that the type of the variable must match (e.g., `java.lang.String`, `int[]`).
  * **Count:** Specifies how many times a variable element can appear (e.g., `[0, N]`, `[1, N]`, `[1, 1]`). This is especially useful for collections of statements or method parameters.
  * **Reference:** If the variable represents an identifier (like a method name or variable name), you can constrain it to refer to a specific type or declaration.
  * **Within:** Constrains the variable to be within a certain scope or declaration.
  * **Not RegExp:** Excludes matches based on a regular expression.
  * **Condition (Groovy script):** This is the most powerful constraint. You can write a Groovy script that evaluates to `true` or `false`. This script has access to the matched element and its properties, allowing for very complex logic.
      * **Example Script:** To check if an integer variable's value is greater than 10: `_target.text.toInteger() > 10` (where `_target` is the matched element for the variable).

#### 3.3. Options

Below the template, there are various options to refine your search:

  * **Context:** Defines the scope of the search (e.g., entire project, module, directory, selected files, custom scope).
  * **File type:** Restricts the search to specific file types (Java, Kotlin, XML, etc.).
  * **Case sensitive:** Standard case sensitivity toggle.
  * **Match case/whole words:** Applicable for text within the template.
  * **Match line breaks:** Important for multi-line patterns.
  * **Save Template:** Saves your current search template for future use.

### 4\. Understanding the Structural Replace Dialog

The Structural Replace dialog adds a "Replace Template" field to the "Search Template" and "Variables" you define for searching.

#### 4.1. Replace Template

This is where you define how the found code structure should be transformed.

  * **Variables from Search Template:** You can use the same variables defined in your "Search Template" within the "Replace Template." The content matched by the variable in the search will be inserted into the replace template.
  * **New Code:** You can introduce new code elements, reorder existing ones, or remove parts.
  * **Example:**
      * **Search Template:** `System.out.println($arg$);`
      * **Replace Template:** `LOGGER.info($arg$);`
      * This would change `System.out.println("Hello");` to `LOGGER.info("Hello");`.

#### 4.2. Shorten FQ Names

This option (often automatically enabled) attempts to replace fully qualified class names (e.g., `java.util.ArrayList`) with their short names (e.g., `ArrayList`) and add the necessary import statements. This is crucial for maintaining readable code.

#### 4.3. Formatting

IntelliJ IDEA will usually reformat the replaced code according to your project's code style settings, which is highly desirable.

### 5\. Practical Examples

Let's illustrate with some common scenarios.

#### Example 1: Replacing `System.out.println` with a Logger

**Goal:** Change all `System.out.println("message");` to `LOGGER.info("message");` (assuming `LOGGER` is a static final field).

1.  **Open Structural Replace:** `Edit -> Find -> Replace Structurally...`
2.  **Search Template:**
    ```java
    System.out.println($arg$);
    ```
3.  **Variables:** Click "Edit variables" or go to the "Variables" tab.
      * Select `$arg$`.
      * **Count:** `[1, 1]` (one argument).
      * **Type (regexp):** `java.lang.String` (if you only want to replace string literals, otherwise leave it empty for any type).
4.  **Replace Template:**
    ```java
    LOGGER.info($arg$);
    ```
5.  **Run:** Click "Find" to preview the changes, then "Replace All" if you're satisfied.

#### Example 2: Swapping Method Parameters

**Goal:** Change `someMethod(paramA, paramB)` to `someMethod(paramB, paramA)`.

1.  **Search Template:**
    ```java
    someMethod($paramA$, $paramB$);
    ```
2.  **Variables:**
      * `$paramA$`: `Count: [1,1]`, `Type (regexp): .*` (any type)
      * `$paramB$`: `Count: [1,1]`, `Type (regexp): .*` (any type)
3.  **Replace Template:**
    ```java
    someMethod($paramB$, $paramA$);
    ```

#### Example 3: Encapsulating a Field (Simple Case)

**Goal:** If you have public fields like `public String name;` and want to replace direct access `obj.name` with `obj.getName()`. (This is a simplified example; often you'd use dedicated refactorings for encapsulation).

1.  **Search Template:**
    ```java
    $object$.$fieldName$;
    ```
2.  **Variables:**
      * `$object$`: `Count: [1,1]`, `Type (regexp): .*`
      * `$fieldName$`: `Count: [1,1]`, `Text (regexp): name` (specifically target the `name` field).
3.  **Replace Template:**
    ```java
    $object$.get$fieldName$();
    ```
      * **Note:** You might need to adjust the capitalization if `get$fieldName$` doesn't automatically capitalize `name` to `Name`. For this, you could use a Groovy script on `$fieldName$` within the replace template, but it gets more complex. A simpler approach for this specific case is often two SSRs or a dedicated refactoring. For `get$fieldName$()`, the IDE usually handles capitalization for common getter patterns.

#### Example 4: Finding Empty `catch` Blocks

**Goal:** Find all `catch` blocks that are empty (or only contain comments/whitespace).

1.  **Search Template:**
    ```java
    try {
        $statements$;
    } catch ($exceptionType$ $exceptionVariable$) {
        $emptyBody$;
    }
    ```
2.  **Variables:**
      * `$statements$`: `Count: [0, N]` (zero or more statements in try block)
      * `$exceptionType$`: `Count: [1,1]`
      * `$exceptionVariable$`: `Count: [1,1]`
      * `$emptyBody$`: `Count: [0, 0]` (this is the key for an empty body)

#### Example 5: Using Groovy Script for Advanced Conditions

**Goal:** Find `if` statements where the condition is a constant `true`.

1.  **Search Template:**
    ```java
    if ($condition$) {
        $thenBranch$;
    }
    ```
2.  **Variables:**
      * `$condition$`: `Count: [1,1]`
          * **Condition (Groovy script):** `_target.text == "true"` (this checks the literal text of the condition).
      * `$thenBranch$`: `Count: [0, N]`

### 6\. Tips and Best Practices

  * **Start Simple:** Begin with basic patterns and gradually add complexity.
  * **Use `Find` First:** Always use "Find" (Structural Search) before "Replace" to preview the matches and ensure your pattern is correct.
  * **Test on a Small Scope:** Before running a large-scale replacement, test your pattern on a small, isolated set of files.
  * **Save Templates:** Save frequently used or complex templates for easy reuse.
  * **Leverage Existing Templates:** IntelliJ IDEA comes with many predefined Structural Search and Replace templates. You can find them by clicking the "magnifying glass with plus" icon in the SSR dialog and Browse the existing templates. These are excellent learning resources.
  * **Groovy Script Power:** For highly specific or context-sensitive matches, Groovy scripts are invaluable. Learn the basics of how to access elements (`_target`, `_target.parent`, `_target.text`, `_target.type`, etc.) within the script.
  * **Understand Match Types:** Be aware of what your variables are matching (e.g., a statement, an expression, a type, a variable name). This influences the constraints you can apply.
  * **Regular Expressions:** A good understanding of regular expressions will significantly enhance your ability to define `Text` and `Type` constraints.
  * **Debugging:** If your pattern isn't matching as expected, simplify it. Remove constraints one by one until it starts matching, then reintroduce them to pinpoint the issue.
  * **Backup Your Code:** Before any major structural replacement operation on a large codebase, ensure you have a backup or are working within a version control system where you can easily revert changes.

### 7\. Limitations

  * **Complexity:** Very complex or highly contextual replacements might be difficult or impossible to express purely with SSR. Sometimes, a custom IntelliJ IDEA plugin or a dedicated script might be more appropriate.
  * **Performance:** Extremely broad or complex patterns run on a very large codebase can be slow.
  * **Ambiguity:** Be careful with overly general patterns, as they might unintentionally match and modify code you didn't intend to.

-----

By mastering IntelliJ IDEA's Structural Search and Replace, you gain a powerful tool for maintaining code quality, performing large-scale refactorings, and automating tedious code modifications. It's a feature that truly empowers developers to work more efficiently and consistently across their projects.
