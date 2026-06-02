---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: C Programming Exam Guide
translated: false
type: note
---

## "Computer Programming Fundamentals (Practice)" Course Examination Outline
**Course Code: 13794**

---

## I. Assessment Objectives

This course aims to cultivate students' computational thinking and programming skills, laying a solid programming foundation for subsequent specialized courses (such as "Advanced Programming Language" and "Data Structures").

**Specific assessment objectives:**

- Ability to write simple programs using C language basic syntax rules to implement basic operations and input/output functions
- Ability to use three basic control structures to solve practical problems and select appropriate control structures based on problem requirements
- Ability to conduct modular programming, reasonably define and call functions, and achieve code reuse and preliminary encapsulation
- Ability to use arrays to process batch data, including numerical computation and string processing
- Ability to use pointers to complete simple memory access and data operations
- Master basic program debugging methods and be able to identify and correct syntax errors and logic errors in programs
- Master simple data structures and algorithms in programming, and be able to comprehensively apply learned knowledge to design and implement complete simple application programs to solve practical problems

---

## II. Reference Textbook

**"Computer Programming Fundamentals"**
Edited by Sun Jianzhi, Xiao Yuanyuan, and Zhang Yingxin
Mechanical Industry Press, 2024 edition

---

## III. Assessment Content

The assessment content focuses on core knowledge points with practical significance that can be verified through hands-on operations, specifically divided into **6 modules:**

### 1. Data Types, Operators, and Input/Output

**(1) Basic data types:**
- Definition and use of int (integer), char (character), float (single-precision floating-point), double (double-precision floating-point)

**(2) Constants and variables:**
- Declaration of literal constants and symbolic constants (#define)
- Declaration, initialization, and assignment rules for variables

**(3) Operators and expressions:**
- Priority and associativity of arithmetic operators (+, -, *, /, %)
- Relational operators (>, <, ==, etc.)
- Logical operators (&&, ||, !)
- Legal writing and calculation of expressions

**(4) Input/output:**
- Correct use of scanf (input format control for different data types)
- printf (output format control for different data types, such as %d, %c, %f)
- Note: no space between % and format character

### 2. Structured Programming

**(1) Conditional statements:**
- Syntax and logic implementation of if statements (single branch)
- if-else statements (double branch)
- switch-case statements (multiple branches)
- Ability to handle nested conditional logic

**(2) Loop statements:**
- Syntax and applicable scenarios of for loop, while loop, do-while loop
- Ability to implement batch data processing through loops (such as accumulation, counting)

**(3) Jump statements:**
- Correct use of break (exit loop/switch)
- continue (skip current loop iteration)

**(4) Compound structures:**
- Nesting of conditional statements and loop statements
- Ability to implement complex logic (such as multi-condition data filtering)

### 3. Arrays and Strings

**(1) One-dimensional arrays:**
- Array definition (such as int arr[10])
- Initialization (complete initialization, partial initialization)
- Accessing array elements through subscripts
- Traversing arrays using loops

**(2) Two-dimensional arrays:**
- Basic definition (such as int mat[3][4])
- Initialization and element access
- Ability to complete simple two-dimensional array operations

**(3) Strings:**
- Definition and initialization of character arrays (such as char str[20] = "hello")
- Use of common string processing functions:
  - strlen (length)
  - strcpy (copying)
  - strcmp (comparison)
  - strcat (concatenation)
- Attention to the role of string terminator '\0'

### 4. Function Basics

**(1) Function definition and declaration:**
- Writing standards for function return value type, parameter list (formal parameters), and function body
- Position of function declaration (prototype)

**(2) Function calls:**
- Syntax of function calls
- Matching rules between actual parameters and formal parameters (type, quantity)
- Difference between parameterless and parameterized function calls

**(3) Variable scope:**
- Scope of local variables (defined inside functions) and global variables (defined outside functions)
- Avoiding variable name conflicts

**(4) Simple function implementation:**
- Ability to write functions that implement specific functions (such as summation, finding maximum)
- Understanding the passing of function return values

### 5. Pointer Basics

**(1) Pointer definition and initialization:**
- Declaration of pointer variables (such as int *p)
- Syntax of pointers pointing to variables (such as p = &a)
- Concept of NULL pointer

**(2) Pointers and arrays:**
- Methods of accessing array elements through pointers (such as *(p+i) equivalent to arr[i])
- Understanding the relationship between array names and pointers

**(3) Pointers and variables:**
- Syntax for modifying variable values through pointers (such as *p = 10)
- Where * is the pointer dereference symbol
- This statement is equivalent to a = 10, provided that p = &a

**(4) Pointer operation precautions:**
- Avoid using uninitialized wild pointers
- Understand the risk of pointer out-of-bounds access

### 6. File Operations

**(1) Opening and closing files:**
- Opening files (fopen function)
- Closing files (fclose function)

**(2) File reading and writing:**
- Character reading/writing (fgetc, fputc functions)
- String reading/writing (fgets, fputs functions)

**(3) File operation process:**
- Must follow the order of "open file → perform read/write operations → close file"
- Avoid resource leaks caused by unclosed files

**(4) File opening failure handling:**
- Check the return value of fopen function
- If it is NULL (indicating opening failure), provide a prompt (such as printf("File opening failed\n");)

---

## IV. Test Paper Structure

**Total Score: 100 points**

**Question Types:**

1. **Program fill-in-the-blank questions** - 2 questions, 20 points
   - Given incomplete program code, candidates complete missing parts according to requirements

2. **Function questions** - 1 question, 15 points
   - Given main function, candidates implement specified function without modifying main function

3. **Programming design questions** - 3 questions, 65 points
   - Given specific problem requirements, candidates design and write complete program code

---

## V. Question Setting Requirements

1. All exams use an online programming evaluation system (OJ)
2. Candidates can submit code multiple times
3. System returns evaluation results in real-time
4. Final answer is the candidate's last submission for each question
5. **Exam time: 90 minutes**
6. Questions cover knowledge points of each module
7. **Difficulty ratio:**
   - Easy: 20%
   - Relatively easy: 35%
   - Relatively difficult: 35%
   - Difficult: 10%

---

## VI. Exam Network Environment Requirements

The exam environment must meet:
- Ability to access the online programming evaluation platform (pintia.cn)
- Provide C language integrated development environment (Dev C++ or VS Code)

---

## VII. Notes

- Candidates can modify code multiple times based on results returned by the online programming evaluation platform
- The candidate's answer is based on the last submission of each question

---

## VIII. Question Type Examples

### 1. Program Fill-in-the-Blank Question

**Question Description:**

The following code intends to implement "input 5 integers into an array, calculate the average of array elements and output (retain 1 decimal place)". Please complete the missing code to ensure the program functions correctly.

**Fill-in-the-blank program:**

```c
#include <stdio.h>
int main() {
    int arr[5];
    int i;
    float avg, sum = 0.0;

    // Blank 1: Loop to input 5 integers into array arr
    for (i = 0; i < 5; i++) {
        ____________________;
    }

    // Blank 2: Loop to accumulate array elements into sum
    for (i = 0; i < 5; i++) {
        ____________________;
    }

    // Blank 3: Calculate average (sum divided by number of elements 5)
    avg = ____________________;

    // Blank 4: Output average, retain 1 decimal place
    ____________________;

    return 0;
}
```

**Reference Answer:**

- **Blank 1:** `scanf("%d", &arr[i]);`
- **Blank 2:** `sum += arr[i];` (or `sum = sum + arr[i];`)
- **Blank 3:** `sum / 5.0` (need to use 5.0 to ensure floating-point division, avoid integer truncation)
- **Blank 4:** `printf("Average: %.1f\n", avg);`

---

### 2. Function Question

**Question Description:**

Given the main function code, implement the function `countOdd` with the following functionality: count the number of odd numbers among the first n elements of array arr and return that count.

**Main function as follows:**

```c
#include <stdio.h>
#define N 50

// Function declaration
int countOdd(int arr[], int n);

int main() {
    int arr[N], n, cnt;

    // Input number of array elements
    scanf("%d", &n);

    // Input n integers into array
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    // Call function to count odd numbers
    cnt = countOdd(arr, n);

    // Output result
    printf("Number of odd numbers: %d\n", cnt);

    return 0;
}

/* Please write the countOdd function here */
```

**Reference Answer:**

```c
int countOdd(int arr[], int n) {
    int count = 0; // Initialize odd number counter to 0

    // Traverse the first n elements of the array
    for (int i = 0; i < n; i++) {
        // Check if current element is odd (remainder not 0 when divided by 2)
        if (arr[i] % 2 != 0) {
            count++; // Increment odd number counter by 1
        }
    }

    return count; // Return number of odd numbers
}
```

---

### 3. Programming Question

**Question Description:**

Write a complete program to implement "student grade level judgment" function.

**Specific requirements:**

- **Input:** Input the names (string, length ≤10) and scores (integer, 0-100) of 3 students in sequence
- **Processing:** Divide grades according to scores:
  - 90-100 is A
  - 80-89 is B
  - 70-79 is C
  - 60-69 is D
  - 0-59 is E
- **Output:** Output each student's 'Name: Score - Grade' line by line (such as 'Zhang San: 95-A')

**Reference Answer:**

```c
#include <stdio.h>
#include <string.h> // For string processing (can be omitted in this question, but kept for standards)

int main() {
    // Define arrays to store names and scores of 3 students
    char name[3][11]; // 3 strings, each maximum 10 characters (plus '\0')
    int score[3];
    char grade; // Store individual student's grade

    // Input information for 3 students
    for (int i = 0; i < 3; i++) {
        printf("Please enter the name and score of student %d (separated by space): ", i+1);
        scanf("%s %d", name[i], &score[i]); // Name without spaces, use %s for input
    }

    // Process and output results
    for (int i = 0; i < 3; i++) {
        // Determine grade based on score
        if (score[i] >= 90 && score[i] <= 100) {
            grade = 'A';
        } else if (score[i] >= 80 && score[i] <= 89) {
            grade = 'B';
        } else if (score[i] >= 70 && score[i] <= 79) {
            grade = 'C';
        } else if (score[i] >= 60 && score[i] <= 69) {
            grade = 'D';
        } else {
            grade = 'E';
        }

        // Output result
        printf("%s: %d-%c\n", name[i], score[i], grade);
    }

    return 0;
}
```
