---
audio: false
generated: true
lang: en
layout: post
title: IntelliJ Structural Replacement Templates
translated: false
type: note
---

Here are 10 examples of IntelliJ's Structural Replacement templates, categorized for clarity. These can be incredibly powerful for refactoring, enforcing coding standards, and automating common code transformations.

**Basic Refactoring & Simplification:**

1. **Replace `if (condition) return true; else return false;` with `return condition;`**

      * **Search Template:**

        ```java
        if ($CONDITION$) {
            return true;
        } else {
            return false;
        }
        ```

      * **Replacement Template:**

        ```java
        return $CONDITION$;
        ```

      * **Context:** Simplifies boolean return statements.

2. **Replace `if (condition) { statement; }` with `if (!condition) { continue/break/return; }` (Guard Clause)**

      * **Search Template:**

        ```java
        if ($CONDITION$) {
            $STATEMENTS$;
        }
        ```

      * **Replacement Template:** (This one is more about suggesting a transformation, you'd manually adjust the inner part)

        ```java
        if (!$CONDITION$) {
            // Consider continue, break, or return here
        }
        $STATEMENTS$;
        ```

      * **Context:** Encourages the use of guard clauses for cleaner code flow. You'd typically use a "Replace with" action after finding the structure.

**Collection & Stream Operations:**

3. **Replace `for (Type item : collection) { if (item.getProperty() == value) { ... } }` with Stream `filter`**

      * **Search Template:**

        ```java
        for ($TYPE$ $ITEM$ : $COLLECTION$) {
            if ($ITEM$.$METHOD$($VALUE$)) {
                $STATEMENTS$;
            }
        }
        ```

      * **Replacement Template:**

        ```java
        $COLLECTION$.stream()
            .filter($ITEM$ -> $ITEM$.$METHOD$($VALUE$))
            .forEach($ITEM$ -> $STATEMENTS$); // Or .map().collect(), etc.
        ```

      * **Context:** Migrating from traditional loops to Java Streams for filtering. This is a general example; you'd likely need more specific templates for `map`, `collect`, etc.

4. **Replace `new ArrayList<>().add(item1); new ArrayList<>().add(item2);` with `List.of(item1, item2);`**

      * **Search Template:** (This might require multiple templates for varying numbers of `add` calls, or a more complex regex for `add` calls. A simpler approach for 2 items):

        ```java
        java.util.ArrayList<$TYPE$> $LIST$ = new java.util.ArrayList<>();
        $LIST$.add($ITEM1$);
        $LIST$.add($ITEM2$);
        ```

      * **Replacement Template:**

        ```java
        java.util.List<$TYPE$> $LIST$ = java.util.List.of($ITEM1$, $ITEM2$);
        ```

      * **Context:** Using Java 9+ `List.of()` for immutable lists.

**Error Handling & Resource Management:**

5. **Replace `try { ... } catch (Exception e) { e.printStackTrace(); }` with more specific logging**

      * **Search Template:**

        ```java
        try {
            $STATEMENTS$;
        } catch (java.lang.Exception $EXCEPTION$) {
            $EXCEPTION$.printStackTrace();
        }
        ```

      * **Replacement Template:**

        ```java
        try {
            $STATEMENTS$;
        } catch (java.lang.Exception $EXCEPTION$) {
            // Replace with your preferred logging framework, e.g.:
            // logger.error("An error occurred", $EXCEPTION$);
            throw new RuntimeException($EXCEPTION$); // Or rethrow a specific exception
        }
        ```

      * **Context:** Encourages proper error logging instead of just printing stack traces.

6. **Replace `try { ... } finally { closeable.close(); }` with `try-with-resources`**

      * **Search Template:**

        ```java
        java.io.Closeable $CLOSEABLE$ = null;
        try {
            $CLOSEABLE$ = $INITIALIZATION$;
            $STATEMENTS$;
        } finally {
            if ($CLOSEABLE$ != null) {
                $CLOSEABLE$.close();
            }
        }
        ```

      * **Replacement Template:**

        ```java
        try ($CLOSEABLE$ = $INITIALIZATION$) {
            $STATEMENTS$;
        }
        ```

      * **Context:** Modernizing resource management to use `try-with-resources` (Java 7+).

**Class & Method Structure:**

7. **Find fields that can be `final`**

      * **Search Template:**

        ```java
        class $CLASS$ {
            $TYPE$ $FIELD$;
        }
        ```

      * **Replacement Template:** (This is more for finding, then using a quick fix)

        ```java
        class $CLASS$ {
            // Consider making this final if it's only assigned once
            final $TYPE$ $FIELD$;
        }
        ```

      * **Context:** Identifying opportunities to improve immutability. You'd set up a filter to only show fields without multiple assignments.

8. **Replace `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);` with a custom logger utility**

      * **Search Template:**

        ```java
        private static final org.slf4j.Logger $LOGGER_VAR$ = org.slf4j.LoggerFactory.getLogger($CLASS_NAME$.class);
        ```

      * **Replacement Template:**

        ```java
        private static final org.slf4j.Logger $LOGGER_VAR$ = com.yourcompany.util.LoggerProvider.getLogger(); // Or a more specific getLogger($CLASS_NAME$.class) from your utility
        ```

      * **Context:** Enforcing a specific logging initialization pattern across your codebase.

**Annotations & Boilerplate:**

9. **Add `@Override` to methods overriding superclass methods (if missing)**

      * **Search Template:** (This is more complex and often better handled by IntelliJ's built-in inspections, but for demonstration)

        ```java
        class $CLASS$ {
            $RETURN_TYPE$ $METHOD$($PARAMS$) {
                $STATEMENTS$;
            }
        }
        ```

      * **Replacement Template:** (Again, for finding, then applying a quick fix)

        ```java
        class $CLASS$ {
            @Override // Add if it overrides a superclass method
            $RETURN_TYPE$ $METHOD$($PARAMS$) {
                $STATEMENTS$;
            }
        }
        ```

      * **Context:** Enforcing good practice and catching typos. You'd use a filter to check if the method exists in a superclass/interface.

10. **Replace repetitive `getter/setter` methods with Lombok annotations**

      * **Search Template:** (For a single getter, this would be highly repetitive for a class)

        ```java
        public $TYPE$ get$PROPERTY_NAME$() {
            return this.$FIELD_NAME$;
        }
        ```

      * **Replacement Template:** (This is conceptual, as you'd delete the getter and add `@Getter` to the field or class)

        ```java
        // Consider replacing with @lombok.Getter on the field:
        // @lombok.Getter
        // private $TYPE$ $FIELD_NAME$;
        ```

      * **Context:** Automating the transition to Lombok. For a full class, you might target the class itself and suggest `@Data` or `@Getter/@Setter` annotations based on the presence of these methods. This is one of the more advanced and potentially multi-step transformations.

**How to Use Them in IntelliJ:**

1. Go to `Analyze` -\> `Inspect Code...`
2. In the `Inspection Profile` window, click on the `...` next to the profile name to edit it.
3. Navigate to `Java` -\> `General` -\> `Structural Search Inspection`.
4. Click the `+` button to add a new search/replace template.
5. Define your `Search Template` and `Replacement Template`.
6. Use the `Variables` tab to define constraints for your variables (e.g., type, text, count).
7. Run the inspection on your code. IntelliJ will suggest replacements or highlight findings.

These examples demonstrate the versatility of Structural Search and Replace. The more specific and constrained your templates are, the more accurate and useful the replacements will be.
