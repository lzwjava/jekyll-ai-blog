---
audio: false
generated: true
lang: en
layout: post
title: Checkstyle Rules Explained Briefly
translated: false
type: note
---

Below, I’ll explain each rule from the Checkstyle configuration file you provided, along with a small example of code that would **violate** the rule and a brief description of why it’s flagged. The rules are grouped by category as in your description, and I’ll keep the explanations concise while ensuring clarity. Each example assumes the rule is active with default settings unless specified otherwise. For rules with configurable properties (e.g., max line length), I’ll use typical defaults (e.g., 80 characters for LineLength) unless otherwise noted.

---

### Root Module: `<module name="Checker">`
The `Checker` module is the top-level orchestrator for all checks and filters. It applies to `.java`, `.properties`, and `.xml` files and sets the severity to `error`.

#### Properties
- **severity="error"**: All violations are treated as errors.
- **fileExtensions="java, properties, xml"**: Checks apply to these file types.

---

### File Filters
These filter which files are checked.

1. **BeforeExecutionExclusionFileFilter**
   - **Purpose**: Excludes files matching a regex (e.g., `module-info.java`).
   - **Example Violation**:
     ```java
     // module-info.java
     module com.example {
         requires java.base;
     }
     ```
   - **Why Flagged**: This file matches the regex `module\-info\.java$` and is excluded from checks. No violation occurs for this file, but other files are still checked.

2. **SuppressionFilter**
   - **Purpose**: Suppresses checks based on rules in a file (e.g., `checkstyle-suppressions.xml`).
   - **Example Violation**: If `checkstyle-suppressions.xml` suppresses `LineLength` for a specific file, a long line in that file won’t be flagged. Without suppression:
     ```java
     public class MyClass { // This line is very long and exceeds the default maximum length of 80 characters, causing an error.
     }
     ```
   - **Why Flagged**: Without a suppression rule, the long line violates `LineLength`.

3. **SuppressWarningsFilter**
   - **Purpose**: Allows suppression of checks using `@SuppressWarnings("checkstyle:<check-name>")`.
   - **Example Violation**:
     ```java
     public class MyClass {
         int my_field; // Violates MemberName (not camelCase)
     }
     ```
     ```java
     @SuppressWarnings("checkstyle:MemberName")
     public class MyClass {
         int my_field; // No violation due to suppression
     }
     ```
   - **Why Flagged**: Without suppression, `my_field` violates `MemberName` (expects camelCase, e.g., `myField`).

---

### Miscellaneous Checks
These apply to general file properties.

4. **JavadocPackage**
   - **Purpose**: Ensures each package has a `package-info.java` with Javadoc.
   - **Example Violation**:
     ```java
     // com/example/package-info.java (missing or no Javadoc)
     package com.example;
     ```
   - **Why Flagged**: Missing Javadoc comment (e.g., `/** Package description */`).

5. **NewlineAtEndOfFile**
   - **Purpose**: Ensures files end with a newline.
   - **Example Violation**:
     ```java
     public class MyClass {} // No newline at end
     ```
   - **Why Flagged**: File ends without a newline character.

6. **Translation**
   - **Purpose**: Verifies `.properties` files for internationalization have consistent keys.
   - **Example Violation**:
     ```properties
     # messages.properties
     key1=Hello
     key2=World
     ```
     ```properties
     # messages_fr.properties
     key1=Bonjour
     # Missing key2
     ```
   - **Why Flagged**: `messages_fr.properties` lacks `key2`, which exists in `messages.properties`.

---

### Size Checks
These enforce limits on file and line lengths.

7. **FileLength**
   - **Purpose**: Limits total lines in a file (default typically 2000 lines).
   - **Example Violation**: A 2001-line Java file.
   - **Why Flagged**: Exceeds default line limit.

8. **LineLength**
   - **Purpose**: Ensures lines don’t exceed a max length (default 80 characters).
   - **Example Violation**:
     ```java
     public class MyClass { public void myMethodWithVeryLongNameToExceedEightyCharactersInALine() {} }
     ```
   - **Why Flagged**: Line exceeds 80 characters.

---

### Whitespace Checks
These enforce consistent whitespace usage.

9. **FileTabCharacter**
   - **Purpose**: Prohibits tab characters (`\t`) in source files.
   - **Example Violation**:
     ```java
     public class MyClass {
     →    int x; // Tab character used for indentation
     }
     ```
   - **Why Flagged**: Tabs are used instead of spaces.

10. **RegexpSingleline**
    - **Purpose**: Detects trailing whitespace (lines ending with `\s+$`).
    - **Example Violation**:
      ```java
      public class MyClass {   // Trailing spaces
      }
      ```
    - **Why Flagged**: Line ends with whitespace.

---

### Header Check (Commented Out)
11. **Header**
    - **Purpose**: Enforces a specific file header (e.g., copyright notice) from `checkstyle.header.file`.
    - **Example Violation** (if enabled):
      ```java
      // Missing header
      public class MyClass {}
      ```
    - **Why Flagged**: Lacks required header (e.g., `// Copyright 2025 Example Inc.`).

---

### Submodule: `<module name="TreeWalker">`
The `TreeWalker` processes the Java AST for detailed checks.

#### Javadoc Checks
These enforce proper Javadoc comments.

12. **InvalidJavadocPosition**
    - **Purpose**: Ensures Javadoc comments are before classes/methods, not elsewhere.
    - **Example Violation**:
      ```java
      public class MyClass {
          /** This is misplaced Javadoc */
          int x;
      }
      ```
    - **Why Flagged**: Javadoc is not before a class/method declaration.

13. **JavadocMethod**
    - **Purpose**: Checks methods for proper Javadoc (parameters, return, exceptions).
    - **Example Violation**:
      ```java
      public int add(int a, int b) { return a + b; }
      ```
    - **Why Flagged**: Missing Javadoc for public method.

14. **JavadocType**
    - **Purpose**: Ensures classes/interfaces/enums have Javadoc.
    - **Example Violation**:
      ```java
      public class MyClass {}
      ```
    - **Why Flagged**: Missing Javadoc for class.

15. **JavadocVariable**
    - **Purpose**: Requires Javadoc for public/protected fields.
    - **Example Violation**:
      ```java
      public class MyClass {
          public int x;
      }
      ```
    - **Why Flagged**: Missing Javadoc for public field.

16. **JavadocStyle**
    - **Purpose**: Enforces Javadoc style (e.g., valid HTML, no malformed comments).
    - **Example Violation**:
      ```java
      /** Missing period at end */
      public class MyClass {}
      ```
    - **Why Flagged**: Javadoc lacks a period at the end.

17. **MissingJavadocMethod**
    - **Purpose**: Flags methods missing Javadoc.
    - **Example Violation**:
      ```java
      public void myMethod() {}
      ```
    - **Why Flagged**: Public method lacks Javadoc.

---

#### Naming Conventions
These enforce naming patterns.

18. **ConstantName**
    - **Purpose**: Constants (`static final`) must be `UPPER_CASE`.
    - **Example Violation**:
      ```java
      public class MyClass {
          static final int myConstant = 42;
      }
      ```
    - **Why Flagged**: `myConstant` should be `MY_CONSTANT`.

19. **LocalFinalVariableName**
    - **Purpose**: Local `final` variables must be `camelCase`.
    - **Example Violation**:
      ```java
      public void myMethod() {
          final int MY_VAR = 1;
      }
      ```
    - **Why Flagged**: `MY_VAR` should be `myVar`.

20. **LocalVariableName**
    - **Purpose**: Local variables must be `camelCase`.
    - **Example Violation**:
      ```java
      public void myMethod() {
          int MY_VAR = 1;
      }
      ```
    - **Why Flagged**: `MY_VAR` should be `myVar`.

21. **MemberName**
    - **Purpose**: Instance fields must be `camelCase`.
    - **Example Violation**:
      ```java
      public class MyClass {
          int my_field;
      }
      ```
    - **Why Flagged**: `my_field` should be `myField`.

22. **MethodName**
    - **Purpose**: Methods must be `camelCase`.
    - **Example Violation**:
      ```java
      public void MyMethod() {}
      ```
    - **Why Flagged**: `MyMethod` should be `myMethod`.

23. **PackageName**
    - **Purpose**: Packages must be lowercase with dots (e.g., `com.example`).
    - **Example Violation**:
      ```java
      package com.Example;
      ```
    - **Why Flagged**: `Example` should be `example`.

24. **ParameterName**
    - **Purpose**: Method parameters must be `camelCase`.
    - **Example Violation**:
      ```java
      public void myMethod(int MY_PARAM) {}
      ```
    - **Why Flagged**: `MY_PARAM` should be `myParam`.

25. **StaticVariableName**
    - **Purpose**: Static (non-final) fields must follow a naming pattern.
    - **Example Violation**:
      ```java
      public class MyClass {
          static int MY_FIELD;
      }
      ```
    - **Why Flagged**: `MY_FIELD` should be `myField` (assuming camelCase).

26. **TypeName**
    - **Purpose**: Class/interface/enum names must be `UpperCamelCase`.
    - **Example Violation**:
      ```java
      public class myClass {}
      ```
    - **Why Flagged**: `myClass` should be `MyClass`.

---

#### Import Checks
These regulate import statements.

27. **AvoidStarImport**
    - **Purpose**: Prohibits wildcard imports (e.g., `import java.util.*`).
    - **Example Violation**:
      ```java
      import java.util.*;
      ```
    - **Why Flagged**: Uses `*` instead of specific imports (e.g., `import java.util.List`).

28. **IllegalImport**
    - **Purpose**: Blocks imports from restricted packages (e.g., `sun.*`).
    - **Example Violation**:
      ```java
      import sun.misc.Unsafe;
      ```
    - **Why Flagged**: `sun.misc.Unsafe` is in a restricted package.

29. **RedundantImport**
    - **Purpose**: Flags duplicate or unnecessary imports.
    - **Example Violation**:
      ```java
      import java.util.List;
      import java.util.List;
      ```
    - **Why Flagged**: Duplicate import of `List`.

30. **UnusedImports**
    - **Purpose**: Detects unused imports.
    - **Example Violation**:
      ```java
      import java.util.List;
      public class MyClass {}
      ```
    - **Why Flagged**: `List` is imported but not used.

---

#### Size Checks
These limit method and parameter counts.

31. **MethodLength**
    - **Purpose**: Limits method length (default typically 150 lines).
    - **Example Violation**: A method with 151 lines.
    - **Why Flagged**: Exceeds default line limit.

32. **ParameterNumber**
    - **Purpose**: Limits method parameters (default typically 7).
    - **Example Violation**:
      ```java
      public void myMethod(int a, int b, int c, int d, int e, int f, int g, int h) {}
      ```
    - **Why Flagged**: 8 parameters exceed the default limit of 7.

---

#### Whitespace Checks
These enforce consistent whitespace in code.

33. **EmptyForIteratorPad**
    - **Purpose**: Checks padding in empty `for` loop iterators.
    - **Example Violation**:
      ```java
      for (int i = 0; ; i++) {}
      ```
    - **Why Flagged**: Empty iterator section should have space (e.g., `for (int i = 0; ; i++)`).

34. **GenericWhitespace**
    - **Purpose**: Ensures spacing around generic types (e.g., `List<String>`).
    - **Example Violation**:
      ```java
      List<String>list;
      ```
    - **Why Flagged**: No space between `>` and `list`.

35. **MethodParamPad**
    - **Purpose**: Checks spacing before method parameter lists.
    - **Example Violation**:
      ```java
      public void myMethod (int x) {}
      ```
    - **Why Flagged**: Space before `(int x)` is incorrect.

36. **NoWhitespaceAfter**
    - **Purpose**: Prohibits whitespace after certain tokens (e.g., `++`).
    - **Example Violation**:
      ```java
      int x = y ++ ;
      ```
    - **Why Flagged**: Space after `++`.

37. **NoWhitespaceBefore**
    - **Purpose**: Prohibits whitespace before certain tokens (e.g., `;`).
    - **Example Violation**:
      ```java
      int x = 1 ;
      ```
    - **Why Flagged**: Space before `;`.

38. **OperatorWrap**
    - **Purpose**: Ensures operators are on the correct line.
    - **Example Violation**:
      ```java
      int x = 1 +
          2;
      ```
    - **Why Flagged**: `+` should be at the end of the first line.

39. **ParenPad**
    - **Purpose**: Checks spacing inside parentheses.
    - **Example Violation**:
      ```java
      if ( x == y ) {}
      ```
    - **Why Flagged**: Spaces inside `(` and `)` are incorrect.

40. **TypecastParenPad**
    - **Purpose**: Ensures spacing in typecasts.
    - **Example Violation**:
      ```java
      Object o = ( String ) obj;
      ```
    - **Why Flagged**: Spaces inside `( String )` are incorrect.

41. **WhitespaceAfter**
    - **Purpose**: Requires whitespace after certain tokens (e.g., commas).
    - **Example Violation**:
      ```java
      int[] arr = {1,2,3};
      ```
    - **Why Flagged**: Missing space after commas.

42. **WhitespaceAround**
    - **Purpose**: Ensures whitespace around operators/keywords.
    - **Example Violation**:
      ```java
      if(x==y) {}
      ```
    - **Why Flagged**: Missing spaces around `==` and `if`.

---

#### Modifier Checks
These regulate Java modifiers.

43. **ModifierOrder**
    - **Purpose**: Ensures modifiers are in correct order (per JLS).
    - **Example Violation**:
      ```java
      static public final int x = 1;
      ```
    - **Why Flagged**: Incorrect order; should be `public static final`.

44. **RedundantModifier**
    - **Purpose**: Flags unnecessary modifiers.
    - **Example Violation**:
      ```java
      public final class MyClass {
          public final void myMethod() {}
      }
      ```
    - **Why Flagged**: `final` on method in a `final` class is redundant.

---

#### Block Checks
These enforce proper use of code blocks.

45. **AvoidNestedBlocks**
    - **Purpose**: Prohibits unnecessary nested blocks.
    - **Example Violation**:
      ```java
      public void myMethod() {
          { int x = 1; }
      }
      ```
    - **Why Flagged**: Unnecessary nested block.

46. **EmptyBlock**
    - **Purpose**: Flags empty blocks.
    - **Example Violation**:
      ```java
      if (x == 1) {}
      ```
    - **Why Flagged**: Empty `if` block.

47. **LeftCurly**
    - **Purpose**: Ensures opening braces are placed correctly.
    - **Example Violation**:
      ```java
      public class MyClass
      {
      }
      ```
    - **Why Flagged**: `{` should be on the same line as `class`.

48. **NeedBraces**
    - **Purpose**: Requires braces for single-statement blocks.
    - **Example Violation**:
      ```java
      if (x == 1) y = 2;
      ```
    - **Why Flagged**: Missing braces; should be `{ y = 2; }`.

49. **RightCurly**
    - **Purpose**: Ensures closing braces are placed correctly.
    - **Example Violation**:
      ```java
      public class MyClass {
      }
      ```
    - **Why Flagged**: `}` should be on a new line (depending on style).

---

#### Coding Problem Checks
These identify common coding issues.

50. **EmptyStatement**
    - **Purpose**: Flags empty statements.
    - **Example Violation**:
      ```java
      int x = 1;; // Extra semicolon
      ```
    - **Why Flagged**: Extra `;` creates an empty statement.

51. **EqualsHashCode**
    - **Purpose**: Ensures `equals()` and `hashCode()` are both overridden.
    - **Example Violation**:
      ```java
      public class MyClass {
          @Override
          public boolean equals(Object o) { return true; }
      }
      ```
    - **Why Flagged**: Missing `hashCode()` override.

52. **HiddenField**
    - **Purpose**: Detects fields shadowed by local variables/parameters.
    - **Example Violation**:
      ```java
      public class MyClass {
          int x;
          public void setX(int x) { this.x = x; }
      }
      ```
    - **Why Flagged**: Parameter `x` shadows field `x`.

53. **IllegalInstantiation**
    - **Purpose**: Prohibits instantiation of certain classes.
    - **Example Violation**:
      ```java
      String s = new String("test");
      ```
    - **Why Flagged**: Unnecessary instantiation of `String`.

54. **InnerAssignment**
    - **Purpose**: Disallows assignments in expressions.
    - **Example Violation**:
      ```java
      if (x = 1) {}
      ```
    - **Why Flagged**: Assignment `x = 1` in expression.

55. **MagicNumber**
    - **Purpose**: Flags hardcoded numeric literals.
    - **Example Violation**:
      ```java
      int x = 42;
      ```
    - **Why Flagged**: `42` should be a named constant (e.g., `static final int MY_CONST = 42;`).

56. **MissingSwitchDefault**
    - **Purpose**: Requires a `default` case in `switch` statements.
    - **Example Violation**:
      ```java
      switch (x) {
          case 1: break;
      }
      ```
    - **Why Flagged**: Missing `default` case.

57. **MultipleVariableDeclarations**
    - **Purpose**: Prohibits multiple variables in one declaration.
    - **Example Violation**:
      ```java
      int x, y;
      ```
    - **Why Flagged**: Should be `int x; int y;`.

58. **SimplifyBooleanExpression**
    - **Purpose**: Flags complex boolean expressions.
    - **Example Violation**:
      ```java
      if (x == true) {}
      ```
    - **Why Flagged**: Should be `if (x)`.

59. **SimplifyBooleanReturn**
    - **Purpose**: Simplifies boolean return statements.
    - **Example Violation**:
      ```java
      if (x) return true; else return false;
      ```
    - **Why Flagged**: Should be `return x;`.

---

#### Class Design Checks
These enforce good class design.

60. **DesignForExtension**
    - **Purpose**: Ensures non-final classes have protected/abstract methods.
    - **Example Violation**:
      ```java
      public class MyClass {
          public void myMethod() {}
      }
      ```
    - **Why Flagged**: Non-final class has non-protected/abstract method.

61. **FinalClass**
    - **Purpose**: Flags classes with private constructors as candidates for `final`.
    - **Example Violation**:
      ```java
      public class MyClass {
          private MyClass() {}
      }
      ```
    - **Why Flagged**: Should be `final` since it can’t be extended.

62. **HideUtilityClassConstructor**
    - **Purpose**: Ensures utility classes have private constructors.
    - **Example Violation**:
      ```java
      public class MyUtils {
          public static void doSomething() {}
      }
      ```
    - **Why Flagged**: Missing private constructor for utility class.

63. **InterfaceIsType**
    - **Purpose**: Prohibits marker interfaces (without methods).
    - **Example Violation**:
      ```java
      public interface MyMarker {}
      ```
    - **Why Flagged**: Interface has no methods.

64. **VisibilityModifier**
    - **Purpose**: Enforces proper field visibility (prefers private with getters/setters).
    - **Example Violation**:
      ```java
      public class MyClass {
          public int x;
      }
      ```
    - **Why Flagged**: Field `x` should be `private` with accessors.

---

#### Miscellaneous Checks
Additional checks for code quality.

65. **ArrayTypeStyle**
    - **Purpose**: Enforces consistent array declaration style (`int[]` vs. `int []`).
    - **Example Violation**:
      ```java
      int x[];
      ```
    - **Why Flagged**: Should be `int[] x`.

66. **FinalParameters**
    - **Purpose**: Requires method parameters to be `final` where possible.
    - **Example Violation**:
      ```java
      public void myMethod(int x) {}
      ```
    - **Why Flagged**: Parameter `x` should be `final int x`.

67. **TodoComment**
    - **Purpose**: Flags `TODO` comments.
    - **Example Violation**:
      ```java
      // TODO: Fix this
      public void myMethod() {}
      ```
    - **Why Flagged**: `TODO` comment detected.

68. **UpperEll**
    - **Purpose**: Ensures `L` for long literals (not `l`).
    - **Example Violation**:
      ```java
      long x = 100l;
      ```
    - **Why Flagged**: `100l` should be `100L`.

---

#### Suppression Filters (Inside TreeWalker)
These allow suppression within the AST.

69. **SuppressionXpathFilter**
    - **Purpose**: Suppresses checks using XPath expressions from a file (e.g., `checkstyle-xpath-suppressions.xml`).
    - **Example Violation**: Similar to `SuppressionFilter` but uses XPath (e.g., suppress `JavadocMethod` for a specific method).

70. **SuppressWarningsHolder**
    - **Purpose**: Supports `@SuppressWarnings("checkstyle:...")` in the AST.
    - **Example Violation**:
      ```java
      public class MyClass {
          int MY_FIELD; // Violates MemberName
      }
      ```
      ```java
      @SuppressWarnings("checkstyle:MemberName")
      public class MyClass {
          int MY_FIELD; // No violation
      }
      ```
    - **Why Flagged**: Without suppression, `MY_FIELD` violates `MemberName`.

---

### Key Notes
- **Configurability**: Rules like `LineLength` or `MethodLength` can have custom thresholds (e.g., `max="120"` for `LineLength`).
- **Suppression**: Use `@SuppressWarnings("checkstyle:<check-name>")` or suppression files to bypass specific checks.
- **Integration**: Run with Maven/Gradle or IDE plugins; errors are reported during builds.
- **Header Check**: Inactive unless uncommented and configured with `checkstyle.header.file`.

If you need specific customization examples (e.g., changing `LineLength` to 120), violation fixes, or integration details, let me know!
