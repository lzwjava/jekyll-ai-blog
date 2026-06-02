---
audio: false
generated: true
lang: en
layout: post
title: Scheme Programming Tutorial
translated: false
type: note
---

Scheme is a minimalist dialect of Lisp known for its simplicity and elegance. This tutorial will cover the basics to get you started.

## 1. Basic Syntax and Concepts

### Running Scheme

- You'll need a Scheme interpreter (like Racket, Guile, or Chez Scheme)
- Code is typically written in a `.scm` file or entered in a REPL (Read-Eval-Print Loop)

### Expressions and Parentheses

- Everything in Scheme is an expression that returns a value
- Parentheses are used for function calls and grouping
- Format: `(function arg1 arg2 ...)`

## 2. Basic Data Types

```scheme
; Numbers
42          ; Integer
3.14        ; Floating-point
1/2         ; Rational

; Booleans
#t          ; True
#f         ; False

; Strings
"hello"     ; String literal

; Symbols
'hello      ; Symbol (quoted with ')
```

## 3. Basic Operations

```scheme
; Arithmetic
(+ 2 3)        ; 5
(- 10 4)       ; 6
(* 3 4)        ; 12
(/ 15 3)       ; 5

; Comparisons
(= 5 5)        ; #t
(< 3 7)        ; #t
(> 10 5)       ; #t
```

## 4. Defining Variables

```scheme
; Define a global variable
(define x 10)

; Use the variable
(+ x 5)        ; 15
```

## 5. Functions

### Defining Functions

```scheme
; Basic function definition
(define square
  (lambda (x)    ; lambda creates an anonymous function
    (* x x)))

(square 4)     ; 16
```

### Multiple Parameters

```scheme
(define add
  (lambda (x y)
    (+ x y)))

(add 3 5)      ; 8
```

### Shorthand Definition

```scheme
; Alternative syntax (syntactic sugar)
(define (multiply x y)
  (* x y))

(multiply 2 3) ; 6
```

## 6. Conditionals

### If Statement

```scheme
(define (is-positive? n)
  (if (> n 0)
      #t
      #f))

(is-positive? 5)   ; #t
(is-positive? -2)  ; #f
```

### Cond (Multiple Conditions)

```scheme
(define (number-type n)
  (cond
    ((> n 0) "positive")
    ((< n 0) "negative")
    (else "zero")))

(number-type 5)    ; "positive"
(number-type 0)    ; "zero"
```

## 7. Lists

### Creating Lists

```scheme
; Using quote
'(1 2 3)          ; List of numbers

; Using list function
(list 1 2 3)      ; Same as above

; Using cons (construct)
(cons 1 '(2 3))   ; Same as above
```

### List Operations

```scheme
(car '(1 2 3))    ; 1 (first element)
(cdr '(1 2 3))    ; (2 3) (rest of list)
(null? '())       ; #t (check if empty)
(length '(1 2 3)) ; 3
```

## 8. Recursion

### Simple Recursion

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(factorial 5)     ; 120 (5 * 4 * 3 * 2 * 1)
```

### List Recursion

```scheme
(define (sum-list lst)
  (if (null? lst)
      0
      (+ (car lst) (sum-list (cdr lst)))))

(sum-list '(1 2 3 4))  ; 10
```

## 9. Higher-Order Functions

### Mapping

```scheme
(map square '(1 2 3 4))    ; (1 4 9 16)
(map + '(1 2 3) '(4 5 6))  ; (5 7 9)
```

### Filtering

```scheme
(define (even? n) (= (remainder n 2) 0))
(filter even? '(1 2 3 4 5 6))  ; (2 4 6)
```

## 10. Let Bindings

```scheme
; Local variable bindings
(define (circle-area r)
  (let ((pi 3.14159))
    (* pi (square r))))

(circle-area 2)    ; 12.56636
```

## 11. Input/Output

```scheme
; Display output
(display "Hello, Scheme!")
(newline)

; Read input (implementation may vary)
(define name (read))
(display "Hello, ")
(display name)
```

## 12. Example Program

Here's a complete program that combines several concepts:

```scheme
; Program to calculate average of a list of numbers
(define (average lst)
  (define (sum lst)
    (if (null? lst)
        0
        (+ (car lst) (sum (cdr lst)))))
  (define len (length lst))
  (if (= len 0)
      0
      (/ (sum lst) len)))

; Test the program
(display (average '(1 2 3 4 5)))  ; 3
(newline)
(display (average '()))           ; 0
```

## Key Features of Scheme

1. **Minimalist**: Small core language with powerful features
2. **Functional**: Emphasis on pure functions and immutability
3. **Prefix Notation**: All operations use prefix syntax
4. **First-class Functions**: Functions can be passed as arguments
5. **Tail-call Optimization**: Efficient recursion

## Learning Tips

1. Practice in a REPL to see immediate results
2. Start with simple functions and build complexity
3. Think recursively for list processing
4. Use proper indentation to manage parentheses
5. Experiment with higher-order functions

This tutorial covers the core concepts of Scheme. To deepen your understanding, try:

- Writing more complex recursive functions
- Exploring macro systems (advanced topic)
- Building small projects like calculators or list processors
- Studying Scheme's standard libraries (varies by implementation)

Would you like me to elaborate on any specific section or provide more examples?
