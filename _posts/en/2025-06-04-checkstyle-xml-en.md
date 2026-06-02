---
audio: false
generated: true
lang: en
layout: post
title: Checkstyle Configuration
translated: false
type: note
---

This is a Checkstyle configuration file written in XML, designed to enforce coding standards and best practices for Java code based on Sun's coding conventions, the Java Language Specification, Javadoc guidelines, and some additional best practices. Checkstyle is a static code analysis tool that checks Java source code for adherence to a set of defined rules. Below, I’ll explain the structure and key components of this configuration file.

---

### **Overview**
- **Purpose**: The file defines rules for checking Java, properties, and XML files for coding standard violations, such as formatting, naming conventions, Javadoc requirements, and code structure.
- **Structure**: The configuration is organized hierarchically using `<module>` elements, starting with a root `Checker` module, which contains other modules for specific checks or filters.
- **Standards**: It aligns with:
  - Java Language Specification (Java SE 11)
  - Sun Code Conventions
  - Javadoc guidelines
  - JDK API documentation
  - General best practices
- **Key Features**:
  - Configurable severity (set to `error`).
  - Supports file extensions: `.java`, `.properties`, `.xml`.
  - Allows suppression of specific checks via suppression files or `@SuppressWarnings` annotations.

---

### **Root Module: `<module name="Checker">`**
The `Checker` module is the top-level module that orchestrates all checks and filters.

- **Properties**:
  - `severity="error"`: Treats all violations as errors (other options include `warning` or `info`).
  - `fileExtensions="java, properties, xml"`: Applies checks to `.java`, `.properties`, and `.xml` files.

- **Submodules**:
  - **File Filters**:
    - `BeforeExecutionExclusionFileFilter`: Excludes `module-info.java` files from checks (using regex `module\-info\.java$`).
  - **Suppression Filters**:
    - `SuppressionFilter`: Loads suppression rules from a file (default: `checkstyle-suppressions.xml`). If the file is missing, it’s optional (`optional="true"`).
    - `SuppressWarningsFilter`: Enables suppression of specific checks using `@SuppressWarnings("checkstyle:...")` annotations in code.
  - **Miscellaneous Checks**:
    - `JavadocPackage`: Ensures each package has a `package-info.java` file with Javadoc.
    - `NewlineAtEndOfFile`: Checks that files end with a newline character.
    - `Translation`: Verifies that property files (e.g., for internationalization) contain the same keys across translations.
  - **Size Checks**:
    - `FileLength`: Checks the total length of a file (default limits apply unless overridden).
    - `LineLength`: Ensures lines in `.java` files do not exceed a default length (typically 80 or 120 characters, configurable).
  - **Whitespace Checks**:
    - `FileTabCharacter`: Prohibits tab characters in source files (enforces spaces for indentation).
    - `RegexpSingleline`: Detects trailing whitespace (lines ending with `\s+$`) and reports them with the message "Line has trailing spaces."
  - **Header Check** (Commented Out):
    - `Header`: If uncommented, would enforce a specific file header (e.g., a copyright notice) from a file specified in `checkstyle.header.file` for `.java` files.

---

### **Submodule: `<module name="TreeWalker">`**
The `TreeWalker` module processes the abstract syntax tree (AST) of Java source code to perform detailed checks. It contains a variety of submodules grouped by category.

#### **Javadoc Checks**
These enforce proper Javadoc comments for classes, methods, and variables:
- `InvalidJavadocPosition`: Ensures Javadoc comments are placed correctly (e.g., before a class or method, not elsewhere).
- `JavadocMethod`: Checks that methods have proper Javadoc comments, including parameters, return types, and exceptions.
- `JavadocType`: Ensures classes, interfaces, and enums have Javadoc comments.
- `JavadocVariable`: Requires Javadoc for public/protected fields.
- `JavadocStyle`: Enforces stylistic rules for Javadoc (e.g., proper HTML tags, no malformed comments).
- `MissingJavadocMethod`: Flags methods missing Javadoc comments.

#### **Naming Conventions**
These ensure that identifiers (variables, methods, classes, etc.) follow naming conventions:
- `ConstantName`: Constants (e.g., `static final`) must follow a naming pattern (typically `UPPER_CASE`).
- `LocalFinalVariableName`: Local `final` variables must follow a naming pattern (e.g., `camelCase`).
- `LocalVariableName`: Local variables must follow a naming pattern (e.g., `camelCase`).
- `MemberName`: Instance fields must follow a naming pattern (e.g., `camelCase`).
- `MethodName`: Methods must follow a naming pattern (e.g., `camelCase`).
- `PackageName`: Packages must follow a naming pattern (e.g., lowercase with dots, like `com.example`).
- `ParameterName`: Method parameters must follow a naming pattern (e.g., `camelCase`).
- `StaticVariableName`: Static (non-final) fields must follow a naming pattern.
- `TypeName`: Class/interface/enum names must follow a naming pattern (e.g., `UpperCamelCase`).

#### **Import Checks**
These regulate the use of `import` statements:
- `AvoidStarImport`: Prohibits wildcard imports (e.g., `import java.util.*`).
- `IllegalImport`: Blocks imports from restricted packages (defaults to `sun.*`).
- `RedundantImport`: Flags duplicate or unnecessary imports.
- `UnusedImports`: Detects unused imports (ignores Javadoc-related imports with `processJavadoc="false"`).

#### **Size Checks**
These limit the size of methods and parameters:
- `MethodLength`: Ensures methods do not exceed a maximum number of lines (default typically 150).
- `ParameterNumber`: Limits the number of parameters in a method (default typically 7).

#### **Whitespace Checks**
These enforce consistent use of whitespace in code:
- `EmptyForIteratorPad`: Checks padding in empty `for` loop iterators (e.g., `for (int i = 0; ; i++)`).
- `GenericWhitespace`: Ensures proper spacing around generic types (e.g., `List<String>`).
- `MethodParamPad`: Checks spacing before method parameter lists.
- `NoWhitespaceAfter`: Prohibits whitespace after certain tokens (e.g., `++` or arrays).
- `NoWhitespaceBefore`: Prohibits whitespace before certain tokens (e.g., semicolons).
- `OperatorWrap`: Ensures operators (e.g., `+`, `=`) are on the correct line.
- `ParenPad`: Checks spacing inside parentheses (e.g., `( x )` vs. `(x)`).
- `TypecastParenPad`: Ensures proper spacing in typecasts.
- `WhitespaceAfter`: Requires whitespace after certain tokens (e.g., commas, semicolons).
- `WhitespaceAround`: Ensures whitespace around operators and keywords (e.g., `if (x == y)`).

#### **Modifier Checks**
These regulate the use of Java modifiers:
- `ModifierOrder`: Ensures modifiers are in the correct order (e.g., `public static final`, per JLS).
- `RedundantModifier`: Flags unnecessary modifiers (e.g., `final` in a `final` class).

#### **Block Checks**
These enforce proper use of code blocks (`{}`):
- `AvoidNestedBlocks`: Prohibits unnecessary nested blocks (e.g., `{ { ... } }`).
- `EmptyBlock`: Flags empty blocks (e.g., `{}`) unless intentional.
- `LeftCurly`: Ensures opening braces (`{`) are placed correctly (e.g., at the end of a line).
- `NeedBraces`: Requires braces for single-statement blocks (e.g., `if (x) y();` must be `if (x) { y(); }`).
- `RightCurly`: Ensures closing braces (`}`) are placed correctly (e.g., on a new line or same line, depending on style).

#### **Coding Problem Checks**
These identify common coding issues:
- `EmptyStatement`: Flags empty statements (e.g., `;;`).
- `EqualsHashCode`: Ensures that if `equals()` is overridden, `hashCode()` is also overridden.
- `HiddenField`: Detects fields shadowed by local variables or parameters.
- `IllegalInstantiation`: Prohibits instantiation of certain classes (e.g., `java.lang` classes like `String`).
- `InnerAssignment`: Disallows assignments within expressions (e.g., `if (x = y)`).
- `MagicNumber`: Flags hardcoded numeric literals (e.g., `42`) unless in specific contexts.
- `MissingSwitchDefault`: Requires a `default` case in `switch` statements.
- `MultipleVariableDeclarations`: Prohibits declaring multiple variables in a single line (e.g., `int x, y;`).
- `SimplifyBooleanExpression`: Flags overly complex boolean expressions (e.g., `if (x == true)`).
- `SimplifyBooleanReturn`: Simplifies boolean return statements (e.g., `if (x) return true; else return false;`).

#### **Class Design Checks**
These enforce good class design practices:
- `DesignForExtension`: Ensures non-final classes have protected or abstract methods for extensibility.
- `FinalClass`: Flags classes with only private constructors as candidates for `final`.
- `HideUtilityClassConstructor`: Ensures utility classes (with only static members) have private constructors.
- `InterfaceIsType`: Prohibits interfaces used solely as marker interfaces (without methods).
- `VisibilityModifier`: Enforces proper visibility for fields (e.g., prefers private fields with getters/setters).

#### **Miscellaneous Checks**
- `ArrayTypeStyle`: Enforces consistent array declaration style (e.g., `int[]` vs. `int []`).
- `FinalParameters`: Requires method parameters to be `final` where possible.
- `TodoComment`: Flags `TODO` comments in code (useful for tracking incomplete work).
- `UpperEll`: Ensures the letter `L` is used for long literals (e.g., `100L` instead of `100l`).

#### **Suppression Filters (Inside TreeWalker)**
- `SuppressionXpathFilter`: Allows suppression of checks using XPath expressions defined in a file (default: `checkstyle-xpath-suppressions.xml`, optional).
- `SuppressWarningsHolder`: Supports `@SuppressWarnings("checkstyle:...")` annotations for suppressing specific checks within the AST.

---

### **Key Points**
- **Configurability**: Most modules have default settings but can be customized via properties (e.g., `LineLength` can set a specific `max` length).
- **Suppression**: The configuration supports flexible suppression of checks via external files (`checkstyle-suppressions.xml`, `checkstyle-xpath-suppressions.xml`) or annotations.
- **Extensibility**: Additional checks can be added, and existing ones can be disabled by commenting them out or removing them.
- **Documentation**: The configuration references Checkstyle’s documentation (e.g., `https://checkstyle.org`) for details on each module.
- **Header Check**: The `Header` module is commented out, so it’s not active unless uncommented and configured with a header file.

---

### **How It’s Used**
1. **Integration**: This file is typically used with a build tool like Maven, Gradle, or an IDE plugin to run Checkstyle during the build process or in development.
2. **Violation Reporting**: When code violates a rule (e.g., a line exceeds the maximum length), Checkstyle reports it as an error (due to `severity="error"`).
3. **Suppression**: Developers can suppress specific violations using `@SuppressWarnings("checkstyle:<check-name>")` or by defining rules in suppression files.
4. **Customization**: Properties like `basedir`, `checkstyle.header.file`, or suppression file paths can be set externally (e.g., via build tool configurations).

---

### **Example Violations**
- **JavadocMethod**: A public method without Javadoc will trigger an error.
- **LineLength**: A line in a `.java` file exceeding the default max (e.g., 80 characters) will be flagged.
- **AvoidStarImport**: Using `import java.util.*` will cause an error.
- **MagicNumber**: Writing `int x = 42;` without a named constant will be flagged.

---

If you need a deeper explanation of a specific module, examples of violations, or guidance on customizing this configuration, let me know!
