---
audio: false
generated: true
lang: zh
layout: post
title: Scheme编程教程
translated: true
type: note
---

Scheme 是一种极简主义的 Lisp 方言，以其简洁优雅而闻名。本教程将涵盖基础知识，助您快速入门。

## 1. 基础语法与概念

### 运行 Scheme

- 您需要一个 Scheme 解释器（如 Racket、Guile 或 Chez Scheme）
- 代码通常写在 `.scm` 文件中，或在 REPL（读取-求值-输出循环）中输入

### 表达式与括号

- Scheme 中的所有内容都是返回值的表达式
- 括号用于函数调用和分组
- 格式：`(函数 参数1 参数2 ...)`

## 2. 基础数据类型

```scheme
; 数字
42          ; 整数
3.14        ; 浮点数
1/2         ; 有理数

; 布尔值
#t          ; 真
#f         ; 假

; 字符串
"hello"     ; 字符串字面量

; 符号
'hello      ; 符号（用 ' 引用）
```

## 3. 基础运算

```scheme
; 算术运算
(+ 2 3)        ; 5
(- 10 4)       ; 6
(* 3 4)        ; 12
(/ 15 3)       ; 5

; 比较运算
(= 5 5)        ; #t
(< 3 7)        ; #t
(> 10 5)       ; #t
```

## 4. 定义变量

```scheme
; 定义全局变量
(define x 10)

; 使用变量
(+ x 5)        ; 15
```

## 5. 函数

### 定义函数

```scheme
; 基础函数定义
(define square
  (lambda (x)    ; lambda 创建匿名函数
    (* x x)))

(square 4)     ; 16
```

### 多参数函数

```scheme
(define add
  (lambda (x y)
    (+ x y)))

(add 3 5)      ; 8
```

### 简写定义

```scheme
; 替代语法（语法糖）
(define (multiply x y)
  (* x y))

(multiply 2 3) ; 6
```

## 6. 条件判断

### If 语句

```scheme
(define (is-positive? n)
  (if (> n 0)
      #t
      #f))

(is-positive? 5)   ; #t
(is-positive? -2)  ; #f
```

### Cond（多条件判断）

```scheme
(define (number-type n)
  (cond
    ((> n 0) "正数")
    ((< n 0) "负数")
    (else "零")))

(number-type 5)    ; "正数"
(number-type 0)    ; "零"
```

## 7. 列表

### 创建列表

```scheme
; 使用引号
'(1 2 3)          ; 数字列表

; 使用 list 函数
(list 1 2 3)      ; 同上

; 使用 cons（构造）
(cons 1 '(2 3))   ; 同上
```

### 列表操作

```scheme
(car '(1 2 3))    ; 1（首元素）
(cdr '(1 2 3))    ; (2 3)（剩余列表）
(null? '())       ; #t（检查是否为空）
(length '(1 2 3)) ; 3
```

## 8. 递归

### 简单递归

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(factorial 5)     ; 120 (5 * 4 * 3 * 2 * 1)
```

### 列表递归

```scheme
(define (sum-list lst)
  (if (null? lst)
      0
      (+ (car lst) (sum-list (cdr lst)))))

(sum-list '(1 2 3 4))  ; 10
```

## 9. 高阶函数

### 映射

```scheme
(map square '(1 2 3 4))    ; (1 4 9 16)
(map + '(1 2 3) '(4 5 6))  ; (5 7 9)
```

### 过滤

```scheme
(define (even? n) (= (remainder n 2) 0))
(filter even? '(1 2 3 4 5 6))  ; (2 4 6)
```

## 10. Let 绑定

```scheme
; 局部变量绑定
(define (circle-area r)
  (let ((pi 3.14159))
    (* pi (square r))))

(circle-area 2)    ; 12.56636
```

## 11. 输入/输出

```scheme
; 显示输出
(display "Hello, Scheme!")
(newline)

; 读取输入（具体实现可能有所不同）
(define name (read))
(display "Hello, ")
(display name)
```

## 12. 示例程序

这是一个结合多个概念的完整程序：

```scheme
; 计算数字列表平均值的程序
(define (average lst)
  (define (sum lst)
    (if (null? lst)
        0
        (+ (car lst) (sum (cdr lst)))))
  (define len (length lst))
  (if (= len 0)
      0
      (/ (sum lst) len)))

; 测试程序
(display (average '(1 2 3 4 5)))  ; 3
(newline)
(display (average '()))           ; 0
```

## Scheme 的主要特性

1. **极简主义**：核心语言小巧但功能强大
2. **函数式**：强调纯函数和不可变性
3. **前缀表示法**：所有操作使用前缀语法
4. **一等函数**：函数可以作为参数传递
5. **尾调用优化**：高效的递归处理

## 学习建议

1. 在 REPL 中练习以查看即时结果
2. 从简单函数开始，逐步构建复杂功能
3. 对列表处理使用递归思维
4. 使用适当的缩进来管理括号
5. 尝试使用高阶函数

本教程涵盖了 Scheme 的核心概念。要加深理解，请尝试：

- 编写更复杂的递归函数
- 探索宏系统（高级主题）
- 构建小型项目，如计算器或列表处理器
- 学习 Scheme 的标准库（因实现而异）

需要我详细说明任何特定部分或提供更多示例吗？
