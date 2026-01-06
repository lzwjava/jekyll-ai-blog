---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 100个Java考试核心知识点
translated: true
type: note
---

问题：在中国高等教育自学考试中，08553 Java语言程序设计考试的 100 个核心知识点有哪些？

回答：**08553 Java语言程序设计**考试重点考察 Java 语言基础、Object-Oriented Programming (OOP) 原理以及基础的 GUI/IO 操作。以下是按类别整理的 100 个核心知识点，旨在帮助你进行复习准备。

### I. Java 基础与环境

1. **Java 的起源**：由 Sun Microsystems 公司（由 James Gosling 领导）于 1995 年创建。
2. **平台无关性**：通过“一次编写，到处运行”（Write Once, Run Anywhere，简称 WORA）原则实现。
3. **JVM (Java Virtual Machine)**：解释并执行 Java Bytecode 的引擎。
4. **JRE (Java Runtime Environment)**：包含 JVM 和运行程序所需的核心类库。
5. **JDK (Java Development Kit)**：包含 JRE 以及 `javac`（编译器）等开发工具。
6. **Bytecode**：编译器生成的 `.class` 文件；它是源代码与机器码之间的中间代码。
7. **编译命令**：`javac FileName.java`。
8. **执行命令**：`java ClassName`。
9. **Main Method 签名**：`public static void main(String[] args)`。
10. **源文件规则**：一个 `.java` 文件只能有一个 `public` 类，且文件名必须与该类名匹配。
11. **注释**：单行注释 (`//`)、多行注释 (`/* ... */`) 和文档注释 (`/** ... */`)。
12. **区分大小写**：Java 严格区分大小写（例如 `Main` 和 `main` 是不同的）。
13. **Keywords**：保留字（如 `class`、`int`、`void`）不能用作标识符。

### II. 数据类型、变量与运算符

14. **8 种基本类型 (Primitive Types)**：`byte`、`short`、`int`、`long`、`float`、`double`、`char`、`boolean`。
15. **整数大小**：`byte` (8-bit)、`short` (16-bit)、`int` (32-bit)、`long` (64-bit)。
16. **浮点型**：`float` (32-bit)、`double` (64-bit)。默认字面量为 `double`。
17. **Char 类型**：使用 16-bit Unicode；可以表示中文字符。
18. **Boolean 类型**：只有两个值：`true` 或 `false`（不能为 0 或 1）。
19. **类型转换（隐式）**：小类型到大类型的自动转换（如 `int` 转 `double`）。
20. **类型转换（显式）**：强制转换（如 `(int)3.14`）。
21. **算术运算符**：`+`、`-`、`*`、`/`、`%`（取模）。
22. **关系运算符**：`==`、`!=`、`>`、`<`、`>=`、`<=`。
23. **逻辑运算符**：`&&` (AND)、`||` (OR)、`!` (NOT)。
24. **短路现象**：如果结果已确定，`&&` 和 `||` 会停止后续计算。
25. **赋值运算符**：`=`、`+=`、`-=` 等。
26. **自增/自减**：`++i`（先增后用）与 `i++`（先用后增）。

### III. 控制结构

27. **if-else**：基础条件分支。
28. **switch-case**：支持 `byte`、`short`、`char`、`int`、`String`（自 Java 7 起）及 Enum。
29. **switch 中的 break**：防止“贯穿” (fall-through) 到下一个 case。
30. **while 循环**：执行*前*检查条件。
31. **do-while 循环**：执行*后*检查条件（至少运行一次）。
32. **for 循环**：最适合已知迭代次数的情况。
33. **增强型 for 循环**：`for (Type var : collection)` 用于数组和集合。
34. **break**：完全退出当前循环。
35. **continue**：跳过当前迭代的剩余部分，进入下一次迭代。

### IV. 数组处理

36. **数组定义**：存储相同类型元素的固定大小容器。
37. **索引**：从 `0` 开始，到 `length - 1` 结束。
38. **初始化**：`int[] arr = new int[5];` 或 `int[] arr = {1, 2, 3};`。
39. **Length 属性**：`arr.length` 返回元素个数。
40. **异常**：访问 `arr[length]` 会触发 `ArrayIndexOutOfBoundsException`。
41. **多维数组**：数组的数组（如 `int[][] matrix`）。

### V. 面向对象程序设计 (OOP) 核心

42. **Class (类)**：对象的蓝图或模板。
43. **Object (对象)**：类的实例。
44. **Encapsulation (封装)**：将数据（字段）和方法捆绑在一起；使用 `private` 实现数据隐藏。
45. **Inheritance (继承)**：使用 `extends` 从父类继承属性。
46. **Polymorphism (多态)**：一个对象采取多种形式的能力（Overloading 与 Overriding）。
47. **Abstraction (抽象)**：使用 `abstract` 类和 `interface` 定义“做什么”而非“怎么做”。
48. **Constructor (构造方法)**：初始化对象的特殊方法；无返回值类型，且与类名相同。
49. **默认构造方法**：若未定义构造方法，Java 会自动提供。
50. **this 关键字**：指向当前对象实例。
51. **super 关键字**：指向父类实例或构造方法。
52. **Method Overloading (方法重载)**：同名但参数不同（在同一个类中）。
53. **Method Overriding (方法重写)**：子类中具有相同的名称和参数（配合 `@Override` 使用）。
54. **访问修饰符**：`public`、`protected`、`default`（无修饰符）和 `private`。
55. **private**：仅在同类中可见。
56. **public**：随处可见。
57. **protected**：在同包和子类中可见。
58. **final (变量)**：常量值。
59. **final (方法)**：不能被重写。
60. **final (类)**：不能被继承（例如 `String` 类）。
61. **static (字段)**：由类的所有实例共享。
62. **static (方法)**：属于类而非对象；不能访问非静态成员。

### VI. 接口与抽象类

63. **Abstract Class**：不能被实例化；可以有抽象方法和具体方法。
64. **Interface**：一种契约；（Java 8 之前）仅包含常量和抽象方法。
65. **多重继承**：一个类可以实现多个 Interface，但只能继承一个父类。
66. **implements 关键字**：用于实现接口。

### VII. 字符串处理

67. **String**：Immutable（创建后值不可更改）。
68. **StringBuffer**：Mutable，线程安全（同步）。
69. **StringBuilder**：Mutable，速度更快，但非线程安全。
70. **字符串比较**：内容比较始终使用 `.equals()`，而非 `==`（后者比较内存地址）。
71. **常用方法**：`length()`、`charAt()`、`substring()`、`indexOf()`、`trim()`。

### VIII. 异常处理

72. **Throwable**：所有 Error 和 Exception 的根类。
73. **Error**：程序不应尝试捕获的严重问题（如 `OutOfMemoryError`）。
74. **Exception**：分为 Checked 和 Unchecked。
75. **Checked Exceptions**：编译时检查（如 `IOException`）。必须使用 `try-catch` 或 `throws`。
76. **Unchecked (Runtime) Exceptions**：运行时发生（如 `NullPointerException`）。
77. **try 块**：包含可能抛出异常的代码。
78. **catch 块**：处理异常。
79. **finally 块**：无论是否发生异常都会执行的代码（用于关闭资源）。
80. **throw**：用于手动触发异常。
81. **throws**：在方法签名中声明，表示该方法可能抛出异常。

### IX. Java I/O 系统

82. **Stream (流)**：数据的序列。
83. **Byte Streams**：`InputStream`、`OutputStream`（用于图像、二进制文件）。
84. **Character Streams**：`Reader`、`Writer`（用于文本文件）。
85. **File 类**：用于操作文件属性和目录。
86. **Buffered Streams**：通过减少 I/O 操作次数来提高性能。
87. **Serialization (序列化)**：使用 `Serializable` 接口将对象转换为字节流。

### X. GUI 与事件处理 (AWT/Swing)

88. **AWT (Abstract Window Toolkit)**：重量级、平台相关的组件。
89. **Swing**：轻量级、平台无关的组件（以 'J' 开头，如 `JButton`）。
90. **JFrame**：GUI 应用程序的主窗口。
91. **Layout Managers (布局管理器)**：`FlowLayout`、`BorderLayout`、`GridLayout`。
92. **事件源 (Event Source)**：产生事件的组件（如按钮）。
93. **事件监听器 (Event Listener)**：处理事件的接口（如 `ActionListener`）。
94. **事件处理器 (Event Handler)**：监听器内部的方法（如 `actionPerformed`）。

### XI. 多线程与集合

95. **线程创建**：继承 `Thread` 类或实现 `Runnable` 接口。
96. **线程启动**：调用 `.start()` 方法，这会触发 `.run()`。
97. **Synchronization (同步)**：使用 `synchronized` 关键字防止数据竞态。
98. **Collection 接口**：集合层次结构的根（List, Set）。
99. **ArrayList**：动态数组，允许重复，保持顺序。
100. **HashMap**：存储键值对；不允许重复的键。