---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 08074 Python 考试样题
translated: true
type: note
---

**问题：提供广东省国家高等教育自学考试（计算机科学学士学位）08074 计算机高级程序设计考试历年 50 道样题。**

**答案：**

实际的广东省自学考试课程代码 **08074**（计算机高级程序设计）历年真题并未以完整形式免费公开在线提供（通常在付费题库、视频课程或官方渠道出售）。官方广东省自学考试真题通常通过授权平台或书店分发，许多网站显示“无历年真题”或引导购买。

然而，该考试基于教材 *Python 语言程序设计基础教程*（傅庆平 等，清华大学出版社，2022 版）。考试通常包括：

- 单选题
- 判断题
- 填空题
- 简答 / 程序阅读
- 编程题（编写代码片段/函数/程序）

以下是 **50 道代表性样题**，按照该课程的典型风格和难度编制（覆盖核心章节：基础、控制结构、数据类型、函数、OOP、文件、异常、模块、字符串/regex、GUI 基础等）。这些样题仿照常见自学考试模式、模拟题（模拟题）和 Python 高级程序设计课程教材习题。

**单选题 – 每题 1 分（约占考试 20-30%）**

1. 在 Python 中，以下哪项是不可变数据类型？
   A. list   B. dict   C. tuple   D. set

2. `print(3 ** 2 // 4)` 的输出是什么？
   A. 2   B. 2.25   C. 9   D. 1

3. Python 中用于定义函数的语句是？
   A. function   B. def   C. func   D. define

4. 在面向对象编程中，“inheritance”（继承）允许什么？
   A. 代码重复   B. 一个类从另一个类继承属性和方法   C. 仅数据隐藏   D. 多个返回值

5. Python 中常用哪个模块处理 regular expressions？
   A. os   B. sys   C. re   D. math

6. `with` 语句主要处理什么？
   A. 循环   B. 异常处理   C. 资源管理（例如文件关闭）   D. 函数定义

7. 以下哪项创建了 list comprehension？
   A. [x for x in range(5)]   B. {x for x in range(5)}   C. (x for x in range(5))   D. {x: x for x in range(5)}

8. 在 Python 3 中，`input()` 的返回值类型是什么？
   A. int   B. str   C. float   D. list

9. 用于手动 raise exception 的关键字是？
   A. throw   B. raise   C. except   D. try

10. 类中 `__init__` 方法的作用是什么？
    A. 析构函数   B. 构造函数   C. 静态方法   D. 类变量

**判断题 – 每题 1 分**

11. Python 中的 list 是可变的，而 tuple 是不可变的。（对/错）

12. 函数中没有 `return` 语句时，默认返回 `None`。（对/错）

13. 在 Python 中，所有异常必须使用 `try-except` 捕获。（对/错）

14. 在函数内部修改 global variable 时，需要使用 `global` 关键字。（对/错）

15. Python 支持 multiple inheritance。（对/错）

**填空题 – 每题 1-2 分**

16. 将元素添加到 list 末尾的方法是 ______。

17. 以读写文本模式打开文件，使用 `open('file.txt', ____)`。

18. decorator 语法在函数定义前使用 ______ 符号。

19. 在异常处理中，总是执行的块是 ______。

20. 生成 1 到 10 之间的随机整数，使用 `random.______(1, 10)`。

**程序阅读或简答题**

21. 以下代码的输出是什么？

    ```python
    def func(x, y=5):
        return x * y
    print(func(3))
    print(func(4, 2))
    ```

22. 解释 Python 中 `==` 和 `is` 操作符的区别。

23. 运行以下代码会发生什么？（识别错误）

    ```python
    try:
        x = 1 / 0
    except:
        print("Error")
    ```

24. 描述什么是 generator function，并给出其相对于普通 list 的一个优势。

25. 写出以下代码的输出：

    ```python
    s = "hello world"
    print(s.capitalize())
    print(s.upper())
    print(s.find("o"))
    ```

**编程题 – 每题 5-15 分（通常要求编写函数或小程序）**

26. 编写函数 `is_prime(n)`，如果 n 是素数则返回 True，否则返回 False。

27. 编写函数反转字符串，不使用 slicing（`[::-1]`）。

28. 编写代码读取文本文件 "data.txt" 并统计其中单词数量。

29. 定义类 `Rectangle`，具有 length 和 width 属性，以及计算面积和周长的方方法。

30. 使用 list comprehension 创建 1 到 20 中偶数的平方列表。

31. 编写程序，接受用户输入数字，使用 recursion 计算并打印其 factorial。

32. 在打开文件时处理 file not found exception，并打印友好消息。

33. 编写函数，接受一个 list，返回仅含唯一元素的新列表（保留顺序）。

34. 使用 `re` 模块检查字符串是否为有效 email 地址（简单 pattern）。

35. 创建简单 tkinter 窗口，包含一个按钮，点击时打印 "Hello"。

36. 编写代码，按键对字典列表排序（例如，按 age 对 students 排序）。

37. 实现一个 decorator，测量并打印函数执行时间。

38. 从文件中读取 CSV-like 数据，计算数值列的平均值。

39. 编写 recursive function 计算 Fibonacci sequence 前 n 项。

40. 使用 `os` 模块列出当前目录下所有 .txt 文件。

41. 创建类 `BankAccount`，包含 deposit、withdraw 和 balance check 方法。

42. 编写代码将一个文件的内容复制到另一个文件。

43. 使用 lambda 和 map() 将温度列表从 Celsius 转换为 Fahrenheit。

44. 实现 bubble sort 算法对数字列表排序。

45. 编写程序，从文本文件中找出最频繁出现的单词。

46. 使用 try-except-finally 确保处理文件后关闭文件。

47. 定义类层次：Animal → Dog 和 Cat，并重写 speak() 方法。

48. 编写代码使用 json 模块将 dictionary 序列化为 JSON 文件。

49. 创建一个 generator，无限 yield Fibonacci 数。

50. 编写完整小程序：接受学生姓名和成绩，存入 dict，按成绩降序打印。

这些样题覆盖了主要考查知识点（从 Python 基础到高级特性）。欲获取真实历年试卷或更准确模拟，请参考广东省自学考试官方资源、授权书店，或 zikaosw.cn、Bilibili 课程、淘宝学习包等包含真题和模拟题的平台。

**参考资料：**

- [08074计算机高级程序设计自考模拟试题及答案](https://www.zikaosw.cn/news/18034564.html)
- [自考08074计算机高级程序设计历年真题及答案](https://www.zikaosw.cn/lnzt/subject-2668.html)
- [2022年4月自考08074计算机高级程序设计模拟试题及答案1](https://www.zikaosw.cn/news/3947029.html)
- [gd-08074 计算机高级程序设计 - 阿福课堂- 题库](https://www.afuketang.com/tiku/%E8%AE%A1%E7%AE%97%E6%9C%BA%E9%AB%98%E7%BA%A7%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1)
- [广东教育考试院 - 教材安排 (confirming textbook)](https://eea.gd.gov.cn/attachment/0/592/592444/4769842.pdf)
