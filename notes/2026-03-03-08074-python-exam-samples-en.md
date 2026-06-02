---
audio: false
generated: true
image: false
lang: en
layout: post
title: 08074 Python Exam Sample Questions
translated: false
type: note
---

**Question: Provide 50 sample exam questions from past years for the 08074 Advanced Computer Programming exam in the Guangdong National Higher Education Self-study Examination (Computer Science bachelor's degree).**

**Answer:**

Actual past exam papers (历年真题) for course code **08074** (计算机高级程序设计) in Guangdong self-study exams are not freely and publicly available online in full form (they are often sold in paid question banks, video courses, or official channels). Official Guangdong self-study exam true questions are typically distributed through authorized platforms or bookstores, and many sites indicate "no past questions available" or redirect to purchase.

However, the exam is based on the textbook *Python 语言程序设计基础教程* (Fu Qingping et al., Tsinghua University Press, 2022 edition). Exams usually include:

- Multiple-choice questions (单选题)
- True/False questions (判断题)
- Fill-in-the-blank (填空题)
- Short answer / code analysis (简答 / 程序阅读)
- Programming problems (编程题: write code snippets/functions/programs)

Below are **50 representative sample questions** compiled in the typical style and difficulty of this course (covering core chapters: basics, control structures, data types, functions, OOP, files, exceptions, modules, strings/regex, GUI basics, etc.). These are modeled after common self-study exam patterns, simulation tests (模拟题), and textbook exercises for Python-based advanced programming courses.

**Multiple Choice / Single Selection (单选题) – 1 point each (approx. 20-30% of exam)**

1. In Python, which of the following is an immutable data type?
   A. list   B. dict   C. tuple   D. set

2. What is the output of `print(3 ** 2 // 4)`?
   A. 2   B. 2.25   C. 9   D. 1

3. Which statement is used to define a function in Python?
   A. function   B. def   C. func   D. define

4. In object-oriented programming, what does "inheritance" allow?
   A. Code duplication   B. A class to inherit attributes and methods from another class   C. Data hiding only   D. Multiple return values

5. Which module is commonly used for regular expressions in Python?
   A. os   B. sys   C. re   D. math

6. What does the `with` statement primarily handle?
   A. Loops   B. Exception handling   C. Resource management (e.g., file closing)   D. Function definition

7. Which of the following creates a list comprehension?
   A. [x for x in range(5)]   B. {x for x in range(5)}   C. (x for x in range(5))   D. {x: x for x in range(5)}

8. In Python 3, what is the type of `input()` return value?
   A. int   B. str   C. float   D. list

9. Which keyword is used to raise an exception manually?
   A. throw   B. raise   C. except   D. try

10. What is the purpose of `__init__` method in a class?
    A. Destructor   B. Constructor   C. Static method   D. Class variable

**True/False (判断题) – 1 point each**

11. Python lists are mutable, while tuples are immutable. (True/False)

12. A function without a `return` statement returns `None` by default. (True/False)

13. In Python, all exceptions must be caught using `try-except`. (True/False)

14. The `global` keyword is required to modify a global variable inside a function. (True/False)

15. Python supports multiple inheritance. (True/False)

**Fill-in-the-Blank (填空题) – 1-2 points each**

16. The method to add an element to the end of a list is ______.

17. To open a file for reading and writing (text mode), use `open('file.txt', ____)`.

18. The decorator syntax uses the ______ symbol before a function definition.

19. In exception handling, the block that always executes is ______.

20. To generate random integers between 1 and 10, use `random.______(1, 10)`.

**Code Analysis / Short Answer (程序阅读或简答题)**

21. What is the output of the following code?
    ```python
    def func(x, y=5):
        return x * y
    print(func(3))
    print(func(4, 2))
    ```

22. Explain the difference between `==` and `is` operators in Python.

23. What will happen if you run this code? (Identify the error)
    ```python
    try:
        x = 1 / 0
    except:
        print("Error")
    ```

24. Describe what a generator function is and give one advantage over a normal list.

25. Write the output of:
    ```python
    s = "hello world"
    print(s.capitalize())
    print(s.upper())
    print(s.find("o"))
    ```

**Programming Questions (编程题) – 5-15 points each (often require writing functions or small programs)**

26. Write a function `is_prime(n)` that returns True if n is a prime number, False otherwise.

27. Write a function to reverse a string without using slicing (`[::-1]`).

28. Write code to read a text file "data.txt" and count the number of words in it.

29. Define a class `Rectangle` with attributes length and width, and methods to calculate area and perimeter.

30. Use list comprehension to create a list of squares of even numbers from 1 to 20.

31. Write a program that takes user input for a number and prints its factorial using recursion.

32. Handle file not found exception when opening a file and print a friendly message.

33. Write a function that takes a list and returns a new list with unique elements only (preserve order).

34. Use the `re` module to check if a string is a valid email address (simple pattern).

35. Create a simple tkinter window with a button that prints "Hello" when clicked.

36. Write code to sort a list of dictionaries by a key (e.g., sort students by age).

37. Implement a decorator that measures and prints the execution time of a function.

38. Read CSV-like data from a file and calculate the average of a numeric column.

39. Write a recursive function to compute the Fibonacci sequence up to n terms.

40. Use `os` module to list all .txt files in the current directory.

41. Create a class `BankAccount` with deposit, withdraw, and balance check methods.

42. Write code to copy contents from one file to another.

43. Use lambda and map() to convert a list of temperatures from Celsius to Fahrenheit.

44. Implement bubble sort algorithm for a list of numbers.

45. Write a program that finds the most frequent word in a text file.

46. Use try-except-finally to ensure a file is closed after processing.

47. Define a class hierarchy: Animal → Dog and Cat, with a speak() method overridden.

48. Write code to serialize a dictionary to a JSON file using json module.

49. Create a generator that yields Fibonacci numbers indefinitely.

50. Write a complete small program: Accept student names and scores, store in dict, print sorted by score descending.

These samples cover the main knowledge points tested (basics to advanced Python features). For real past papers or more accurate simulations, refer to Guangdong self-study exam official resources, authorized bookstores, or platforms like zikaosw.cn, Bilibili courses, or Taobao study packs that include true questions and mocks.

**References:**

- [08074计算机高级程序设计自考模拟试题及答案](https://www.zikaosw.cn/news/18034564.html)
- [自考08074计算机高级程序设计历年真题及答案](https://www.zikaosw.cn/lnzt/subject-2668.html)
- [2022年4月自考08074计算机高级程序设计模拟试题及答案1](https://www.zikaosw.cn/news/3947029.html)
- [gd-08074 计算机高级程序设计 - 阿福课堂- 题库](https://www.afuketang.com/tiku/%E8%AE%A1%E7%AE%97%E6%9C%BA%E9%AB%98%E7%BA%A7%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1)
- [广东教育考试院 - 教材安排 (confirming textbook)](https://eea.gd.gov.cn/attachment/0/592/592444/4769842.pdf)
