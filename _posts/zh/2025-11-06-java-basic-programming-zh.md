---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Java基础编程指南
translated: true
type: note
---

以下是针对**08553 程序设计导论——Java**课程**第二部分：基础编程**的精要指南，专为**全国高等教育自学考试**编写。本部分训练编写小型、正确的Java程序，并理解Java处理数据和表达式的方式。

---

## 1. 从控制台读取输入

### 1.1 使用 `Scanner`

Java通过`java.util`包中的`Scanner`类读取输入。

```java
import java.util.Scanner;

public class InputExample {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("请输入您的姓名：");
        String name = sc.nextLine();
        System.out.print("请输入您的年龄：");
        int age = sc.nextInt();
        System.out.println("你好 " + name + "，您今年 " + age + " 岁。");
        sc.close();
    }
}
```

**关键点：**

* 始终需要`import java.util.Scanner;`
* 根据数据类型使用`nextInt()`、`nextDouble()`、`nextLine()`
* 关闭`Scanner`以释放资源
* 注意：`nextLine()`会读取整行内容，与`nextInt()`混用时可能导致输入跳过

---

## 2. 标识符、变量、表达式、赋值和常量

### 2.1 标识符

为变量、方法或类命名的名称。
**规则：**

* 必须以字母、`_`或`$`开头
* 不能以数字开头
* 区分大小写（`score` ≠ `Score`）
* 不能是关键字（`int`、`class`、`if`等）

**示例：**
`studentName`、`_total`、`$price`

### 2.2 变量

变量存储特定**类型**的数据。
声明示例：

```java
int age = 20;
double price = 12.5;
char grade = 'A';
boolean passed = true;
```

### 2.3 赋值语句

使用`=`进行赋值（从右到左）：

```java
x = 5;
y = x + 2;
```

### 2.4 常量

使用`final`声明，后续不可更改：

```java
final double PI = 3.14159;
```

常量名称建议使用大写。

---

## 3. 数值数据类型与运算

### 3.1 常用数值类型

* `byte`（8位整数）
* `short`（16位）
* `int`（32位，最常用）
* `long`（64位）
* `float`（32位小数）
* `double`（64位小数，精度更高）

**示例：**

```java
int count = 5;
double price = 19.99;
```

### 3.2 基本算术运算符

`+`、`-`、`*`、`/`、`%`

示例：

```java
int a = 10, b = 3;
System.out.println(a / b);  // 3（整数除法）
System.out.println(a % b);  // 1
System.out.println((double)a / b); // 3.3333（类型转换）
```

---

## 4. 类型转换（强制转换）

### 4.1 自动转换（拓宽）

小类型→大类型自动转换：
`int` → `long` → `float` → `double`

示例：

```java
int i = 10;
double d = i;  // 自动转换
```

### 4.2 手动转换（强制转换）

显式将大类型→小类型：

```java
double d = 9.7;
int i = (int) d; // i = 9（小数部分丢失）
```

注意**精度损失**。

---

## 5. 表达式求值与运算符优先级

### 5.1 运算顺序

Java遵循既定顺序：

1. 括号`( )`
2. 一元运算符`+`、`-`、`++`、`--`
3. 乘除取模`* / %`
4. 加减`+ -`
5. 赋值`=`

示例：

```java
int x = 2 + 3 * 4;   // 14，不是20
int y = (2 + 3) * 4; // 20
```

### 5.2 混合表达式

若有一个操作数为`double`，结果即为`double`：

```java
double result = 5 / 2;     // 2.0（先进行整数除法）
double result2 = 5.0 / 2;  // 2.5（浮点数除法）
```

---

## 6. 复合赋值与自增/自减

### 6.1 复合赋值

快捷运算符：

```java
x += 3;  // 等同于 x = x + 3
y *= 2;  // 等同于 y = y * 2
```

### 6.2 自增与自减

`++`增加1，`--`减少1。
两种形式：

```java
int a = 5;
System.out.println(a++); // 输出5，然后a = 6
System.out.println(++a); // a = 7，然后输出7
```

**记住：**

* 后缀（`a++`）→ 先使用后增加
* 前缀（`++a`）→ 先增加后使用

---

## 7. 常见错误避免

* 在比较中使用`=`而非`==`
* 期望小数结果时使用整数除法
* 使用变量前未初始化
* 类型转换时数据丢失（如`(int) 3.9` → 3）

---

## 8. 典型考题示例

**例题1：**

> 以下代码输出什么？
>
> ```java
> int x = 5, y = 2;
> double z = x / y;
> System.out.println(z);
> ```

**答案：** `2.0`（赋值前先进行整数除法）

**例题2：**

> 哪个运算符优先级最高？
> A. `+`
> B. `*`
> C. `=`
> D. `++`
> **答案：** D

**例题3：**

> 以下代码输出什么？
>
> ```java
> int a = 3;
> int b = ++a + a++;
> System.out.println(b);
> ```

**解析：**
`++a`使`a = 4`，加上`4`，然后`a++`使用`4`并自增至`5`
因此`b = 8`

---

是否需要继续学习**第三部分：控制结构（选择与循环语句）**？该部分涵盖`if`、`switch`、`for`、`while`，是Java考试中过程逻辑的核心内容。
