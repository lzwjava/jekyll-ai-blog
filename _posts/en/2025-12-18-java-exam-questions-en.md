---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Java Exam Questions Sample
translated: false
type: note
---

Question: Provide 30 exam questions for the course 08553 Introduction to Programming—Java in the National Higher Education Self-study Examination (Guangdong).

Answer: 

Below are 30 sample exam questions for the self-study examination course 08553 (Introduction to Programming—Java). These questions cover key topics in introductory Java programming, including basic syntax, data types, control structures, methods, arrays, classes, objects, inheritance, and simple exception handling. The questions are a mix of multiple-choice, fill-in-the-blank, short answer, code correction, code analysis, and programming questions, similar to typical self-study exam formats.

### Multiple-Choice Questions (1-10)

1. Which of the following is the correct way to declare the main method in a Java application?  
   - A. public void main(String[] args)  
   - B. static public void main(String args[])  
   - C. public static void main(String[] args)  
   - D. void main(String args)

2. In Java, which data type is used to store a single character?  
   - A. String  
   - B. char  
   - C. int  
   - D. boolean

3. What is the output of the following code?  
   ```java
   System.out.println(10 + 20 + "Hello" + 30 + 40);
   ```  
   - A. 70Hello3040  
   - B. 30Hello70  
   - C. 10 20 Hello 30 40  
   - D. Hello100

4. Which keyword is used to define a subclass in Java?  
   - A. implements  
   - B. extends  
   - C. super  
   - D. this

5. What does the `break` statement do in a switch block?  
   - A. Ends the entire program  
   - B. Skips to the next iteration  
   - C. Exits the switch statement  
   - D. Continues to the default case

6. Which of the following is NOT a valid access modifier in Java?  
   - A. public  
   - B. protected  
   - C. private  
   - D. open

7. In Java, arrays are:  
   - A. Primitive data types  
   - B. Objects  
   - C. Methods  
   - D. Interfaces

8. What is the default value of a boolean instance variable in a class?  
   - A. true  
   - B. false  
   - C. null  
   - D. 0

9. Which method is called automatically when an object is created?  
   - A. main()  
   - B. Constructor  
   - C. finalize()  
   - D. toString()

10. What exception is thrown when dividing an integer by zero?  
    - A. NullPointerException  
    - B. ArrayIndexOutOfBoundsException  
    - C. ArithmeticException  
    - D. ClassCastException

### Fill-in-the-Blank Questions (11-15)

11. The keyword used to inherit methods and fields from a parent class is ________.

12. To create an object from a class, the operator used is ________.

13. The loop that executes at least once is the ________ loop.

14. Java source files have the extension ________, and compiled bytecode files have ________.

15. The method to read input from the console using Scanner is ________.nextInt() for integers.

### Short Answer Questions (16-20)

16. Explain the difference between `==` and `.equals()` when comparing strings in Java.

17. What is method overloading? Give a simple example.

18. Describe the role of the `this` keyword in Java.

19. What is the purpose of the `final` keyword when applied to a variable, method, and class?

20. Explain the difference between `while` and `do-while` loops.

### Code Correction Questions (21-25)

21. The following code has errors. Correct it to print "Hello World":  
    ```java
    public class Test
    {
        public static void Main(string[] args) {
            system.out.println("Hello World");
        }
    }
    ```

22. Fix the array declaration and initialization to create an integer array of size 5 with values 1 to 5:  
    ```java
    int arr = new int[5];
    arr = {1,2,3,4,5};
    ```

23. Correct the constructor to properly initialize instance variables:  
    ```java
    class Person {
        String name;
        Person(String n) { name = n }
    }
    ```

24. Fix the loop to sum numbers from 1 to 10:  
    ```java
    int sum = 0;
    for(int i=1; i<10; i++) {
        sum += i
    }
    System.out.println(sum);
    ```

25. Correct the inheritance syntax:  
    ```java
    class Dog implement Animal {
        // ...
    }
    ```

### Code Analysis/Reading Questions (26-28)

26. What is the output of this code?  
    ```java
    int x = 5;
    if (x > 0) {
        System.out.println("Positive");
    } else if (x == 0) {
        System.out.println("Zero");
    } else {
        System.out.println("Negative");
    }
    ```

27. Analyze the following method and state what it returns for input 4:  
    ```java
    public static int factorial(int n) {
        if (n == 0) return 1;
        return n * factorial(n-1);
    }
    ```

28. What happens when this code runs? Describe any error.  
    ```java
    int[] arr = {1,2,3};
    System.out.println(arr[3]);
    ```

### Programming Questions (29-30)

29. Write a complete Java program to calculate the factorial of a number input from the console using a loop (not recursion).

30. Write a Java class `Rectangle` with private fields length and width, a constructor, methods to calculate area and perimeter, and a main method to test it with sample values.