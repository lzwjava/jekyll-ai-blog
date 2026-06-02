---
audio: false
generated: true
lang: zh
layout: post
title: Checkstyle规则简明解析
translated: true
type: note
---

下面我将逐一解释您提供的Checkstyle配置文件中的每条规则，并附上会**违反**该规则的简短代码示例及其被标记的原因。规则按照您描述中的类别分组，我会保持解释简洁明了。除非另有说明，每个示例都假设规则使用默认配置生效。对于可配置属性的规则（如行长度限制），我将使用典型默认值（例如LineLength默认为80个字符）。

---

### 根模块：`<module name="Checker">`
`Checker`模块是所有检查和筛选器的顶层协调者。它适用于`.java`、`.properties`和`.xml`文件，并将严重级别设置为`error`。

#### 属性
- **severity="error"**：所有违规行为均被视为错误。
- **fileExtensions="java, properties, xml"**：检查适用于这些文件类型。

---

### 文件筛选器
这些筛选器决定检查哪些文件。

1. **BeforeExecutionExclusionFileFilter**
   - **目的**：排除与正则表达式匹配的文件（例如`module-info.java`）。
   - **违规示例**：
     ```java
     // module-info.java
     module com.example {
         requires java.base;
     }
     ```
   - **标记原因**：此文件匹配正则表达式`module\-info\.java$`并被排除在检查之外。该文件不会产生违规，但其他文件仍会被检查。

2. **SuppressionFilter**
   - **目的**：根据文件中的规则（例如`checkstyle-suppressions.xml`）抑制检查。
   - **违规示例**：如果`checkstyle-suppressions.xml`为特定文件抑制了`LineLength`，则该文件中的长行不会被标记。若无抑制：
     ```java
     public class MyClass { // 这行非常长，超过了默认的80字符最大长度限制，导致错误。
     }
     ```
   - **标记原因**：若无抑制规则，长行违反`LineLength`。

3. **SuppressWarningsFilter**
   - **目的**：允许使用`@SuppressWarnings("checkstyle:<check-name>")`抑制检查。
   - **违规示例**：
     ```java
     public class MyClass {
         int my_field; // 违反MemberName（非驼峰命名）
     }
     ```
     ```java
     @SuppressWarnings("checkstyle:MemberName")
     public class MyClass {
         int my_field; // 因抑制而无违规
     }
     ```
   - **标记原因**：无抑制时，`my_field`违反`MemberName`（期望驼峰命名，如`myField`）。

---

### 杂项检查
这些检查适用于文件的通用属性。

4. **JavadocPackage**
   - **目的**：确保每个包都有带Javadoc的`package-info.java`。
   - **违规示例**：
     ```java
     // com/example/package-info.java（缺失或无Javadoc）
     package com.example;
     ```
   - **标记原因**：缺少Javadoc注释（例如`/** 包描述 */`）。

5. **NewlineAtEndOfFile**
   - **目的**：确保文件以换行符结尾。
   - **违规示例**：
     ```java
     public class MyClass {} // 结尾无换行
     ```
   - **标记原因**：文件结尾缺少换行符。

6. **Translation**
   - **目的**：验证国际化所需的`.properties`文件具有一致的键。
   - **违规示例**：
     ```properties
     # messages.properties
     key1=Hello
     key2=World
     ```
     ```properties
     # messages_fr.properties
     key1=Bonjour
     # 缺少key2
     ```
   - **标记原因**：`messages_fr.properties`缺少`messages.properties`中存在的`key2`。

---

### 大小检查
这些检查强制执行文件和行长度的限制。

7. **FileLength**
   - **目的**：限制文件总行数（默认通常为2000行）。
   - **违规示例**：一个2001行的Java文件。
   - **标记原因**：超过默认行数限制。

8. **LineLength**
   - **目的**：确保行不超过最大长度（默认80字符）。
   - **违规示例**：
     ```java
     public class MyClass { public void myMethodWithVeryLongNameToExceedEightyCharactersInALine() {} }
     ```
   - **标记原因**：行超过80字符。

---

### 空白检查
这些检查强制执行一致的空白使用。

9. **FileTabCharacter**
   - **目的**：禁止源文件中使用制表符（`\t`）。
   - **违规示例**：
     ```java
     public class MyClass {
     →    int x; // 使用制表符缩进
     }
     ```
   - **标记原因**：使用了制表符而非空格。

10. **RegexpSingleline**
    - **目的**：检测行尾空白（以`\s+$`结尾的行）。
    - **违规示例**：
      ```java
      public class MyClass {   // 尾部空格
      }
      ```
    - **标记原因**：行尾有空白。

---

### 头部检查（已注释）
11. **Header**
    - **目的**：强制执行特定的文件头部（例如版权声明），从`checkstyle.header.file`读取。
    - **违规示例**（若启用）：
      ```java
      // 缺少头部
      public class MyClass {}
      ```
    - **标记原因**：缺少必需的头部（例如`// Copyright 2025 Example Inc.`）。

---

### 子模块：`<module name="TreeWalker">`
`TreeWalker`处理Java抽象语法树以进行详细检查。

#### Javadoc检查
这些检查强制执行正确的Javadoc注释。

12. **InvalidJavadocPosition**
    - **目的**：确保Javadoc注释位于类/方法之前，而非其他地方。
    - **违规示例**：
      ```java
      public class MyClass {
          /** 这是 misplaced Javadoc */
          int x;
      }
      ```
    - **标记原因**：Javadoc不在类/方法声明之前。

13. **JavadocMethod**
    - **目的**：检查方法是否具有正确的Javadoc（参数、返回值、异常）。
    - **违规示例**：
      ```java
      public int add(int a, int b) { return a + b; }
      ```
    - **标记原因**：公共方法缺少Javadoc。

14. **JavadocType**
    - **目的**：确保类/接口/枚举具有Javadoc。
    - **违规示例**：
      ```java
      public class MyClass {}
      ```
    - **标记原因**：类缺少Javadoc。

15. **JavadocVariable**
    - **目的**：要求公共/受保护字段具有Javadoc。
    - **违规示例**：
      ```java
      public class MyClass {
          public int x;
      }
      ```
    - **标记原因**：公共字段缺少Javadoc。

16. **JavadocStyle**
    - **目的**：强制执行Javadoc样式（例如有效的HTML、无格式错误的注释）。
    - **违规示例**：
      ```java
      /** 结尾缺少句点 */
      public class MyClass {}
      ```
    - **标记原因**：Javadoc结尾缺少句点。

17. **MissingJavadocMethod**
    - **目的**：标记缺少Javadoc的方法。
    - **违规示例**：
      ```java
      public void myMethod() {}
      ```
    - **标记原因**：公共方法缺少Javadoc。

---

#### 命名约定
这些检查强制执行命名模式。

18. **ConstantName**
    - **目的**：常量（`static final`）必须为`UPPER_CASE`。
    - **违规示例**：
      ```java
      public class MyClass {
          static final int myConstant = 42;
      }
      ```
    - **标记原因**：`myConstant`应为`MY_CONSTANT`。

19. **LocalFinalVariableName**
    - **目的**：局部`final`变量必须为`camelCase`。
    - **违规示例**：
      ```java
      public void myMethod() {
          final int MY_VAR = 1;
      }
      ```
    - **标记原因**：`MY_VAR`应为`myVar`。

20. **LocalVariableName**
    - **目的**：局部变量必须为`camelCase`。
    - **违规示例**：
      ```java
      public void myMethod() {
          int MY_VAR = 1;
      }
      ```
    - **标记原因**：`MY_VAR`应为`myVar`。

21. **MemberName**
    - **目的**：实例字段必须为`camelCase`。
    - **违规示例**：
      ```java
      public class MyClass {
          int my_field;
      }
      ```
    - **标记原因**：`my_field`应为`myField`。

22. **MethodName**
    - **目的**：方法必须为`camelCase`。
    - **违规示例**：
      ```java
      public void MyMethod() {}
      ```
    - **标记原因**：`MyMethod`应为`myMethod`。

23. **PackageName**
    - **目的**：包名必须为小写带点（例如`com.example`）。
    - **违规示例**：
      ```java
      package com.Example;
      ```
    - **标记原因**：`Example`应为`example`。

24. **ParameterName**
    - **目的**：方法参数必须为`camelCase`。
    - **违规示例**：
      ```java
      public void myMethod(int MY_PARAM) {}
      ```
    - **标记原因**：`MY_PARAM`应为`myParam`。

25. **StaticVariableName**
    - **目的**：静态（非final）字段必须遵循命名模式。
    - **违规示例**：
      ```java
      public class MyClass {
          static int MY_FIELD;
      }
      ```
    - **标记原因**：`MY_FIELD`应为`myField`（假设驼峰命名）。

26. **TypeName**
    - **目的**：类/接口/枚举名称必须为`UpperCamelCase`。
    - **违规示例**：
      ```java
      public class myClass {}
      ```
    - **标记原因**：`myClass`应为`MyClass`。

---

#### 导入检查
这些检查规范import语句。

27. **AvoidStarImport**
    - **目的**：禁止通配符导入（例如`import java.util.*`）。
    - **违规示例**：
      ```java
      import java.util.*;
      ```
    - **标记原因**：使用了`*`而非具体导入（例如`import java.util.List`）。

28. **IllegalImport**
    - **目的**：阻止从受限包导入（例如`sun.*`）。
    - **违规示例**：
      ```java
      import sun.misc.Unsafe;
      ```
    - **标记原因**：`sun.misc.Unsafe`在受限包中。

29. **RedundantImport**
    - **目的**：标记重复或不必要的导入。
    - **违规示例**：
      ```java
      import java.util.List;
      import java.util.List;
      ```
    - **标记原因**：重复导入`List`。

30. **UnusedImports**
    - **目的**：检测未使用的导入。
    - **违规示例**：
      ```java
      import java.util.List;
      public class MyClass {}
      ```
    - **标记原因**：导入了`List`但未使用。

---

#### 大小检查
这些检查限制方法和参数数量。

31. **MethodLength**
    - **目的**：限制方法长度（默认通常为150行）。
    - **违规示例**：一个151行的方法。
    - **标记原因**：超过默认行数限制。

32. **ParameterNumber**
    - **目的**：限制方法参数数量（默认通常为7个）。
    - **违规示例**：
      ```java
      public void myMethod(int a, int b, int c, int d, int e, int f, int g, int h) {}
      ```
    - **标记原因**：8个参数超过默认限制7个。

---

#### 空白检查
这些检查强制执行代码中一致的空白。

33. **EmptyForIteratorPad**
    - **目的**：检查空`for`循环迭代器中的填充。
    - **违规示例**：
      ```java
      for (int i = 0; ; i++) {}
      ```
    - **标记原因**：空迭代器部分应有空格（例如`for (int i = 0; ; i++)`）。

34. **GenericWhitespace**
    - **目的**：确保泛型类型周围的间距（例如`List<String>`）。
    - **违规示例**：
      ```java
      List<String>list;
      ```
    - **标记原因**：`>`和`list`之间无空格。

35. **MethodParamPad**
    - **目的**：检查方法参数列表前的间距。
    - **违规示例**：
      ```java
      public void myMethod (int x) {}
      ```
    - **标记原因**：`(int x)`前的空格不正确。

36. **NoWhitespaceAfter**
    - **目的**：禁止特定标记后的空白（例如`++`）。
    - **违规示例**：
      ```java
      int x = y ++ ;
      ```
    - **标记原因**：`++`后有空格。

37. **NoWhitespaceBefore**
    - **目的**：禁止特定标记前的空白（例如`;`）。
    - **违规示例**：
      ```java
      int x = 1 ;
      ```
    - **标记原因**：`;`前有空格。

38. **OperatorWrap**
    - **目的**：确保操作符在正确的行上。
    - **违规示例**：
      ```java
      int x = 1 +
          2;
      ```
    - **标记原因**：`+`应在第一行末尾。

39. **ParenPad**
    - **目的**：检查圆括号内的间距。
    - **违规示例**：
      ```java
      if ( x == y ) {}
      ```
    - **标记原因**：`(`和`)`内的空格不正确。

40. **TypecastParenPad**
    - **目的**：确保类型转换中的间距。
    - **违规示例**：
      ```java
      Object o = ( String ) obj;
      ```
    - **标记原因**：`( String )`内的空格不正确。

41. **WhitespaceAfter**
    - **目的**：要求特定标记后必须有空白（例如逗号）。
    - **违规示例**：
      ```java
      int[] arr = {1,2,3};
      ```
    - **标记原因**：逗号后缺少空格。

42. **WhitespaceAround**
    - **目的**：确保操作符/关键字周围的空白。
    - **违规示例**：
      ```java
      if(x==y) {}
      ```
    - **标记原因**：`==`和`if`周围缺少空格。

---

#### 修饰符检查
这些检查规范Java修饰符。

43. **ModifierOrder**
    - **目的**：确保修饰符顺序正确（符合JLS）。
    - **违规示例**：
      ```java
      static public final int x = 1;
      ```
    - **标记原因**：顺序错误；应为`public static final`。

44. **RedundantModifier**
    - **目的**：标记不必要的修饰符。
    - **违规示例**：
      ```java
      public final class MyClass {
          public final void myMethod() {}
      }
      ```
    - **标记原因**：`final`类中的`final`方法是冗余的。

---

#### 代码块检查
这些检查强制执行代码块的正确使用。

45. **AvoidNestedBlocks**
    - **目的**：禁止不必要的嵌套块。
    - **违规示例**：
      ```java
      public void myMethod() {
          { int x = 1; }
      }
      ```
    - **标记原因**：不必要的嵌套块。

46. **EmptyBlock**
    - **目的**：标记空块。
    - **违规示例**：
      ```java
      if (x == 1) {}
      ```
    - **标记原因**：空的`if`块。

47. **LeftCurly**
    - **目的**：确保左大括号位置正确。
    - **违规示例**：
      ```java
      public class MyClass
      {
      }
      ```
    - **标记原因**：`{`应与`class`在同一行。

48. **NeedBraces**
    - **目的**：要求单语句块使用大括号。
    - **违规示例**：
      ```java
      if (x == 1) y = 2;
      ```
    - **标记原因**：缺少大括号；应为`{ y = 2; }`。

49. **RightCurly**
    - **目的**：确保右大括号位置正确。
    - **违规示例**：
      ```java
      public class MyClass {
      }
      ```
    - **标记原因**：`}`应在新行上（取决于样式）。

---

#### 编码问题检查
这些检查识别常见的编码问题。

50. **EmptyStatement**
    - **目的**：标记空语句。
    - **违规示例**：
      ```java
      int x = 1;; // 多余分号
      ```
    - **标记原因**：多余`;`创建了空语句。

51. **EqualsHashCode**
    - **目的**：确保同时重写`equals()`和`hashCode()`。
    - **违规示例**：
      ```java
      public class MyClass {
          @Override
          public boolean equals(Object o) { return true; }
      }
      ```
    - **标记原因**：缺少`hashCode()`重写。

52. **HiddenField**
    - **目的**：检测被局部变量/参数遮蔽的字段。
    - **违规示例**：
      ```java
      public class MyClass {
          int x;
          public void setX(int x) { this.x = x; }
      }
      ```
    - **标记原因**：参数`x`遮蔽了字段`x`。

53. **IllegalInstantiation**
    - **目的**：禁止实例化特定类。
    - **违规示例**：
      ```java
      String s = new String("test");
      ```
    - **标记原因**：不必要的`String`实例化。

54. **InnerAssignment**
    - **目的**：不允许在表达式中赋值。
    - **违规示例**：
      ```java
      if (x = 1) {}
      ```
    - **标记原因**：表达式中的赋值`x = 1`。

55. **MagicNumber**
    - **目的**：标记硬编码的数字字面量。
    - **违规示例**：
      ```java
      int x = 42;
      ```
    - **标记原因**：`42`应为命名常量（例如`static final int MY_CONST = 42;`）。

56. **MissingSwitchDefault**
    - **目的**：要求`switch`语句有`default`分支。
    - **违规示例**：
      ```java
      switch (x) {
          case 1: break;
      }
      ```
    - **标记原因**：缺少`default`分支。

57. **MultipleVariableDeclarations**
    - **目的**：禁止在单个声明中声明多个变量。
    - **违规示例**：
      ```java
      int x, y;
      ```
    - **标记原因**：应为`int x; int y;`。

58. **SimplifyBooleanExpression**
    - **目的**：标记复杂的布尔表达式。
    - **违规示例**：
      ```java
      if (x == true) {}
      ```
    - **标记原因**：应为`if (x)`。

59. **SimplifyBooleanReturn**
    - **目的**：简化布尔返回语句。
    - **违规示例**：
      ```java
      if (x) return true; else return false;
      ```
    - **标记原因**：应为`return x;`。

---

#### 类设计检查
这些检查强制执行良好的类设计。

60. **DesignForExtension**
    - **目的**：确保非final类具有protected/abstract方法。
    - **违规示例**：
      ```java
      public class MyClass {
          public void myMethod() {}
      }
      ```
    - **标记原因**：非final类具有非protected/abstract方法。

61. **FinalClass**
    - **目的**：将具有私有构造函数的类标记为`final`候选。
    - **违规示例**：
      ```java
      public class MyClass {
          private MyClass() {}
      }
      ```
    - **标记原因**：应为`final`，因为无法被继承。

62. **HideUtilityClassConstructor**
    - **目的**：确保工具类具有私有构造函数。
    - **违规示例**：
      ```java
      public class MyUtils {
          public static void doSomething() {}
      }
      ```
    - **标记原因**：工具类缺少私有构造函数。

63. **InterfaceIsType**
    - **目的**：禁止标记接口（无方法）。
    - **违规示例**：
      ```java
      public interface MyMarker {}
      ```
    - **标记原因**：接口无方法。

64. **VisibilityModifier**
    - **目的**：强制执行正确的字段可见性（优先私有并带有getter/setter）。
    - **违规示例**：
      ```java
      public class MyClass {
          public int x;
      }
      ```
    - **标记原因**：字段`x`应为`private`并带有访问器。

---

#### 杂项检查
代码质量的额外检查。

65. **ArrayTypeStyle**
    - **目的**：强制执行一致的数组声明样式（`int[]` vs. `int []`）。
    - **违规示例**：
      ```java
      int x[];
      ```
    - **标记原因**：应为`int[] x`。

66. **FinalParameters**
    - **目的**：要求方法参数尽可能为`final`。
    - **违规示例**：
      ```java
      public void myMethod(int x) {}
      ```
    - **标记原因**：参数`x`应为`final int x`。

67. **TodoComment**
    - **目的**：标记`TODO`注释。
    - **违规示例**：
      ```java
      // TODO: 修复此问题
      public void myMethod() {}
      ```
    - **标记原因**：检测到`TODO`注释。

68. **UpperEll**
    - **目的**：确保长整型字面量使用`L`（而非`l`）。
    - **违规示例**：
      ```java
      long x = 100l;
      ```
    - **标记原因**：`100l`应为`100L`。

---

#### 抑制筛选器（TreeWalker内部）
这些允许在AST内抑制检查。

69. **SuppressionXpathFilter**
    - **目的**：使用来自文件（例如`checkstyle-xpath-suppressions.xml`）的XPath表达式抑制检查。
    - **违规示例**：类似于`SuppressionFilter`但使用XPath（例如抑制特定方法的`JavadocMethod`）。

70. **SuppressWarningsHolder**
    - **目的**：在AST中支持`@SuppressWarnings("checkstyle:...")`。
    - **违规示例**：
      ```java
      public class MyClass {
          int MY_FIELD; // 违反MemberName
      }
      ```
      ```java
      @SuppressWarnings("checkstyle:MemberName")
      public class MyClass {
          int MY_FIELD; // 无违规
      }
      ```
    - **标记原因**：无抑制时，`MY_FIELD`违反`MemberName`。

---

### 关键说明
- **可配置性**：如`LineLength`或`MethodLength`等规则可具有自定义阈值（例如`LineLength`的`max="120"`）。
- **抑制**：使用`@SuppressWarnings("checkstyle:<check-name>")`或抑制文件绕过特定检查。
- **集成**：通过Maven/Gradle或IDE插件运行；错误在构建过程中报告。
- **头部检查**：除非取消注释并使用`checkstyle.header.file`配置，否则处于非活动状态。

如果您需要具体的自定义示例（例如将`LineLength`改为120）、违规修复方法或集成细节，请告知我！
