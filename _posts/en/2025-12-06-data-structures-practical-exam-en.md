---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Data Structures Practical Exam Syllabus
translated: false
type: note
---

Question: Guangdong Higher Education Self-Examination Syllabus for "Data Structures (Practical)" Course (Course Code: 13182) – Translated to English and Formatted

Answer:

# Guangdong Higher Education Self-Examination

## Data Structures (Practical Assessment) Course Syllabus

**(Course Code: 13182)**

### I. Assessment Objectives

"Data Structures" is a core professional course for the Higher Education Self-Examination Computer Application (Associate Degree) program. The practical component aims to develop candidates' ability to apply data structures to solve real-world problems through theoretical study and hands-on experiments.

Candidates are required to:

- Start from practical problems and requirements
- Select appropriate storage structures
- Design corresponding algorithms
- Implement and verify algorithms using the C language
- Solve general and moderately complex application problems
- Deepen understanding of data structures theory
- Master fundamental algorithm implementation techniques and enhance comprehensive application skills

### II. Prescribed Textbook

《Data Structures》
Edited by the National Higher Education Self-Examination Guidance Committee
Authored by Xin Yunwei and Chen Shuoying
Published by China Machine Press, 2023 Edition

### III. Assessment Content

Candidates must master the following:

1. Structure and operations of linked lists; solve application problems using linked list operations
2. Sequential stack and circular queue storage characteristics and basic operations
3. Two-dimensional array storage and random access by subscript; solve problems using 2D arrays
4. Binary tree storage using binary linked lists; implement tree creation, traversal, and Huffman algorithm
5. Graph storage using adjacency matrix and adjacency list; implement graph creation, traversal, and applications
6. Implement basic sorting algorithms and compare the number of key comparisons and element moves
7. Understand sequential and binary search principles and implement the search process

### IV. Exam Structure

Closed-book written exam, 120 minutes, total 100 points

| Question Type           | Description                                                                 | Number of Questions | Points |
|-------------------------|-----------------------------------------------------------------------------|---------------------|--------|
| Multiple Choice         | Choose the best answer from 4 options                                       | 10 questions        | 20     |
| Code Fill-in-the-Blank  | Complete missing parts in given programs                                    | 2 questions (10 blanks total) | 20     |
| Function Writing        | Write required functions based on provided interface and main function     | 2 questions         | 20     |
| Programming             | Write complete programs according to requirements                           | 3 questions         | 40     |
| **Total**               |                                                                             |                     | **100** |

### V. Exam Requirements

1. Closed-book, paper-based exam only
2. Duration: 120 minutes
3. Must cover all knowledge points in Section III
4. Difficulty distribution: Easy 20%, Moderately Easy 35%, Moderately Difficult 35%, Difficult 10%

### VI. Network Environment

None required (offline paper exam)

### VII. Important Notes

1. Answers must be written in black or blue ink pen (pencil not allowed)
2. All code (fill-in, function, and programming questions) must be written in **C language**

### VIII. Sample Questions

#### 1. Multiple Choice (10 questions, 20 points)

**Q1.** To check whether parentheses in an expression are properly matched, the most suitable data structure is:
A. Linear list B. Queue C. Tree D. Stack
**Answer:** D

#### 2. Code Fill-in-the-Blank (2 questions, 20 points)

**Q1.** Complete the circular queue implementation (10 points)

```c
// Key blanks and answers:
(1) (q->rear + 1) % MAX_SIZE == q->front
(2) isFull(q)
(3) (q->rear + 1) % MAX_SIZE
(4) q->data[i]
(5) initQueue(&q)
```

#### 3. Function Question (2 questions, 20 points)

**Q1.** Delete the node at position `i` in a singly linked list with a head node (10 points)

```c
int deli(Node* head, int i) {
    if (head == NULL || i < 1) return 0;
    Node* p = head->next;
    Node* q = head;
    int j = 1;
    while (p != NULL && j < i) {
        q = p;
        p = p->next;
        j++;
    }
    if (p != NULL && j == i) {
        q->next = p->next;
        free(p);
        return 1;
    }
    return 0;
}
```

#### 4. Programming Questions (3 questions, 40 points total)

**Q1.** Direct Insertion Sort – Output the array after each pass (15 points)

```c
#include <stdio.h>
#define MAX_SIZE 100

void printArray(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) printf("%d ", arr[i]);
    printf("%d\n", arr[n-1]);
}

void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int temp = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > temp) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = temp;
        printArray(arr, n);
    }
}

int main() {
    int arr[MAX_SIZE], n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);
    insertionSort(arr, n);
    return 0;
}
```

This document is the official English translation and cleanly formatted version of the original Chinese syllabus for the Guangdong Self-Examination "Data Structures (Practical)" course (Code 13182).
