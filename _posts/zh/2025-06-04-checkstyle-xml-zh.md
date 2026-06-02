---
audio: false
generated: true
lang: zh
layout: post
title: Checkstyle配置
translated: true
type: note
---

这是一个用 XML 编写的 Checkstyle 配置文件，旨在基于 Sun 编码规范、Java 语言规范、Javadoc 指南以及一些额外的最佳实践来强制执行 Java 代码的编码标准和最佳实践。Checkstyle 是一个静态代码分析工具，用于检查 Java 源代码是否遵守一组定义的规则。下面，我将解释此配置文件的结构和关键组成部分。

---

### **概述**
- **目的**：该文件定义了检查 Java、properties 和 XML 文件编码标准违规的规则，例如格式、命名约定、Javadoc 要求和代码结构。
- **结构**：配置使用 `<module>` 元素按层次结构组织，从根模块 `Checker` 开始，该模块包含用于特定检查或过滤器的其他模块。
- **标准**：它遵循：
  - Java 语言规范（Java SE 11）
  - Sun 代码约定
  - Javadoc 指南
  - JDK API 文档
  - 通用最佳实践
- **关键特性**：
  - 可配置的严重性（设置为 `error`）。
  - 支持文件扩展名：`.java`、`.properties`、`.xml`。
  - 允许通过抑制文件或 `@SuppressWarnings` 注解来抑制特定检查。

---

### **根模块：`<module name="Checker">`**
`Checker` 模块是协调所有检查和过滤器的顶级模块。

- **属性**：
  - `severity="error"`：将所有违规视为错误（其他选项包括 `warning` 或 `info`）。
  - `fileExtensions="java, properties, xml"`：对 `.java`、`.properties` 和 `.xml` 文件应用检查。

- **子模块**：
  - **文件过滤器**：
    - `BeforeExecutionExclusionFileFilter`：从检查中排除 `module-info.java` 文件（使用正则表达式 `module\-info\.java$`）。
  - **抑制过滤器**：
    - `SuppressionFilter`：从文件加载抑制规则（默认：`checkstyle-suppressions.xml`）。如果文件缺失，则为可选（`optional="true"`）。
    - `SuppressWarningsFilter`：支持使用代码中的 `@SuppressWarnings("checkstyle:...")` 注解来抑制特定检查。
  - **杂项检查**：
    - `JavadocPackage`：确保每个包都有一个带有 Javadoc 的 `package-info.java` 文件。
    - `NewlineAtEndOfFile`：检查文件是否以换行符结尾。
    - `Translation`：验证属性文件（例如，用于国际化）在翻译中包含相同的键。
  - **大小检查**：
    - `FileLength`：检查文件的总长度（除非被覆盖，否则应用默认限制）。
    - `LineLength`：确保 `.java` 文件中的行不超过默认长度（通常为 80 或 120 个字符，可配置）。
  - **空白检查**：
    - `FileTabCharacter`：禁止在源文件中使用制表符（强制使用空格进行缩进）。
    - `RegexpSingleline`：检测尾随空白（以 `\s+$` 结尾的行）并报告消息“行尾有空格”。
  - **头检查**（已注释掉）：
    - `Header`：如果取消注释，将为 `.java` 文件强制执行特定的文件头（例如，版权声明），该文件头来自 `checkstyle.header.file` 中指定的文件。

---

### **子模块：`<module name="TreeWalker">`**
`TreeWalker` 模块处理 Java 源代码的抽象语法树（AST）以执行详细检查。它包含按类别分组的各种子模块。

#### **Javadoc 检查**
这些检查强制执行类、方法和变量的正确 Javadoc 注释：
- `InvalidJavadocPosition`：确保 Javadoc 注释放置正确（例如，在类或方法之前，而不是其他地方）。
- `JavadocMethod`：检查方法是否有正确的 Javadoc 注释，包括参数、返回类型和异常。
- `JavadocType`：确保类、接口和枚举有 Javadoc 注释。
- `JavadocVariable`：要求对公共/受保护字段进行 Javadoc 注释。
- `JavadocStyle`：强制执行 Javadoc 的样式规则（例如，正确的 HTML 标签，无格式错误的注释）。
- `MissingJavadocMethod`：标记缺少 Javadoc 注释的方法。

#### **命名约定**
这些检查确保标识符（变量、方法、类等）遵循命名约定：
- `ConstantName`：常量（例如，`static final`）必须遵循命名模式（通常为 `UPPER_CASE`）。
- `LocalFinalVariableName`：局部 `final` 变量必须遵循命名模式（例如，`camelCase`）。
- `LocalVariableName`：局部变量必须遵循命名模式（例如，`camelCase`）。
- `MemberName`：实例字段必须遵循命名模式（例如，`camelCase`）。
- `MethodName`：方法必须遵循命名模式（例如，`camelCase`）。
- `PackageName`：包必须遵循命名模式（例如，小写带点，如 `com.example`）。
- `ParameterName`：方法参数必须遵循命名模式（例如，`camelCase`）。
- `StaticVariableName`：静态（非 final）字段必须遵循命名模式。
- `TypeName`：类/接口/枚举名称必须遵循命名模式（例如，`UpperCamelCase`）。

#### **导入检查**
这些检查规范 `import` 语句的使用：
- `AvoidStarImport`：禁止通配符导入（例如，`import java.util.*`）。
- `IllegalImport`：阻止从受限包导入（默认为 `sun.*`）。
- `RedundantImport`：标记重复或不必要的导入。
- `UnusedImports`：检测未使用的导入（忽略与 Javadoc 相关的导入，`processJavadoc="false"`）。

#### **大小检查**
这些检查限制方法和参数的大小：
- `MethodLength`：确保方法不超过最大行数（默认通常为 150）。
- `ParameterNumber`：限制方法中的参数数量（默认通常为 7）。

#### **空白检查**
这些检查强制执行代码中空白的一致使用：
- `EmptyForIteratorPad`：检查空 `for` 循环迭代器中的填充（例如，`for (int i = 0; ; i++)`）。
- `GenericWhitespace`：确保泛型类型周围的间距正确（例如，`List<String>`）。
- `MethodParamPad`：检查方法参数列表前的间距。
- `NoWhitespaceAfter`：禁止在某些标记后使用空白（例如，`++` 或数组）。
- `NoWhitespaceBefore`：禁止在某些标记前使用空白（例如，分号）。
- `OperatorWrap`：确保运算符（例如，`+`、`=`）位于正确的行上。
- `ParenPad`：检查括号内的间距（例如，`( x )` 与 `(x)`）。
- `TypecastParenPad`：确保类型转换中的间距正确。
- `WhitespaceAfter`：要求在某些标记后使用空白（例如，逗号、分号）。
- `WhitespaceAround`：确保运算符和关键字周围的空白（例如，`if (x == y)`）。

#### **修饰符检查**
这些检查规范 Java 修饰符的使用：
- `ModifierOrder`：确保修饰符顺序正确（例如，`public static final`，符合 JLS）。
- `RedundantModifier`：标记不必要的修饰符（例如，`final` 类中的 `final`）。

#### **块检查**
这些检查强制执行代码块（`{}`）的正确使用：
- `AvoidNestedBlocks`：禁止不必要的嵌套块（例如，`{ { ... } }`）。
- `EmptyBlock`：标记空块（例如，`{}`），除非是故意的。
- `LeftCurly`：确保左大括号（`{`）放置正确（例如，在一行的末尾）。
- `NeedBraces`：要求单语句块使用大括号（例如，`if (x) y();` 必须为 `if (x) { y(); }`）。
- `RightCurly`：确保右大括号（`}`）放置正确（例如，在新行或同一行，取决于样式）。

#### **编码问题检查**
这些检查识别常见的编码问题：
- `EmptyStatement`：标记空语句（例如，`;;`）。
- `EqualsHashCode`：确保如果重写了 `equals()`，则也要重写 `hashCode()`。
- `HiddenField`：检测被局部变量或参数遮蔽的字段。
- `IllegalInstantiation`：禁止实例化某些类（例如，`java.lang` 类如 `String`）。
- `InnerAssignment`：不允许在表达式内进行赋值（例如，`if (x = y)`）。
- `MagicNumber`：标记硬编码的数字字面量（例如，`42`），除非在特定上下文中。
- `MissingSwitchDefault`：要求 `switch` 语句中有 `default` 情况。
- `MultipleVariableDeclarations`：禁止在单行中声明多个变量（例如，`int x, y;`）。
- `SimplifyBooleanExpression`：标记过于复杂的布尔表达式（例如，`if (x == true)`）。
- `SimplifyBooleanReturn`：简化布尔返回语句（例如，`if (x) return true; else return false;`）。

#### **类设计检查**
这些检查强制执行良好的类设计实践：
- `DesignForExtension`：确保非 final 类具有受保护或抽象方法以实现可扩展性。
- `FinalClass`：将仅具有私有构造函数的类标记为 `final` 的候选。
- `HideUtilityClassConstructor`：确保工具类（仅具有静态成员）具有私有构造函数。
- `InterfaceIsType`：禁止仅用作标记接口（无方法）的接口。
- `VisibilityModifier`：强制执行字段的正确可见性（例如，倾向于使用带有 getter/setter 的私有字段）。

#### **杂项检查**
- `ArrayTypeStyle`：强制执行一致的数组声明样式（例如，`int[]` 与 `int []`）。
- `FinalParameters`：要求方法参数尽可能为 `final`。
- `TodoComment`：标记代码中的 `TODO` 注释（用于跟踪未完成的工作）。
- `UpperEll`：确保对 long 字面量使用字母 `L`（例如，`100L` 而不是 `100l`）。

#### **抑制过滤器（在 TreeWalker 内部）**
- `SuppressionXpathFilter`：允许使用文件中定义的 XPath 表达式来抑制检查（默认：`checkstyle-xpath-suppressions.xml`，可选）。
- `SuppressWarningsHolder`：支持使用 `@SuppressWarnings("checkstyle:...")` 注解来抑制 AST 中的特定检查。

---

### **关键点**
- **可配置性**：大多数模块具有默认设置，但可以通过属性进行自定义（例如，`LineLength` 可以设置特定的 `max` 长度）。
- **抑制**：配置支持通过外部文件（`checkstyle-suppressions.xml`、`checkstyle-xpath-suppressions.xml`）或注解灵活地抑制检查。
- **可扩展性**：可以添加额外的检查，并且可以通过注释掉或删除现有检查来禁用它们。
- **文档**：配置参考了 Checkstyle 的文档（例如，`https://checkstyle.org`）以获取每个模块的详细信息。
- **头检查**：`Header` 模块被注释掉，因此除非取消注释并使用头文件进行配置，否则它不会激活。

---

### **使用方式**
1. **集成**：此文件通常与构建工具（如 Maven、Gradle）或 IDE 插件一起使用，以在构建过程或开发期间运行 Checkstyle。
2. **违规报告**：当代码违反规则时（例如，一行超过最大长度），Checkstyle 会将其报告为错误（由于 `severity="error"`）。
3. **抑制**：开发人员可以使用 `@SuppressWarnings("checkstyle:<check-name>")` 或通过在抑制文件中定义规则来抑制特定违规。
4. **自定义**：诸如 `basedir`、`checkstyle.header.file` 或抑制文件路径等属性可以在外部设置（例如，通过构建工具配置）。

---

### **违规示例**
- **JavadocMethod**：没有 Javadoc 的公共方法将触发错误。
- **LineLength**：`.java` 文件中超过默认最大值（例如，80 个字符）的行将被标记。
- **AvoidStarImport**：使用 `import java.util.*` 将导致错误。
- **MagicNumber**：编写 `int x = 42;` 而没有命名常量将被标记。

---

如果您需要特定模块的更深入解释、违规示例或自定义此配置的指导，请告诉我！
