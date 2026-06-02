---
audio: false
generated: true
lang: zh
layout: post
title: CPS转换器
translated: true
type: note
---

```scheme
;; 一个简单的CPS转换器，能正确处理尾调用且不为if表达式复制上下文。
;; 作者：王垠 (yw21@cs.indiana.edu)
(load "pmatch.scm") ; 加载Scheme的模式匹配库，便于处理不同的表达式结构。

(define cps
  (lambda (exp)
    (letrec
        ([trivial? (lambda (x) (memq x '(zero? add1 sub1)))] ; 检查给定符号是否为基本操作符：zero?、add1、sub1。这些在转换中会特殊处理。
         [id (lambda (v) v)] ; 恒等函数，用作顶层表达式的初始延续。
         [ctx0 (lambda (v) `(k ,v))]      ; 尾上下文。创建一个延续，仅将当前延续'k'应用于值'v'。当当前调用处于尾位置时使用。
         [fv (let ([n -1]) ; 生成新鲜变量名的生成器。
               (lambda ()
                 (set! n (+ 1 n))
                 (string->symbol (string-append "v" (number->string n)))))]
         [cps1
          (lambda (exp ctx) ; 执行CPS转换的核心递归函数。接收表达式'exp'和延续'ctx'作为参数。延续表示如何处理'exp'的求值结果。
            (pmatch exp ; 使用模式匹配分析表达式结构。
              [,x (guard (not (pair? x))) (ctx x)] ; 基础情况：如果表达式'x'不是序对（即字面量或变量），说明它已是值。将当前延续'ctx'应用于该值。

              [(if ,test ,conseq ,alt) ; 匹配带有测试、 consequent和alternative的'if'表达式。
               (cps1 test ; 递归转换'test'表达式。
                     (lambda (t) ; 'test'表达式的延续。接收测试结果（布尔值）作为't'。
                       (cond
                        [(memq ctx (list ctx0 id)) ; 如果当前上下文'ctx'是尾上下文'ctx0'或初始恒等上下文'id'，说明'if'表达式本身处于尾位置。
                         `(if ,t ,(cps1 conseq ctx) ,(cps1 alt ctx))] ; 此时，'if'表达式在CPS化代码中仍保持'if'结构。consequent和alternative用相同上下文'ctx'进行CPS化。这避免了上下文重复。
                        [else ; 如果当前上下文不是尾上下文，说明'if'表达式的结果需要传递给后续计算。
                         (let ([u (fv)]) ; 生成新鲜变量名'u'来保存'if'表达式的结果。
                           `(let ([k (lambda (,u) ,(ctx u))]) ; 创建新延续'k'，接收结果'u'并对其实施原始上下文'ctx'。
                              (if ,t ,(cps1 conseq ctx0) ,(cps1 alt ctx0))))]))] ; 将'if'表达式包装在引入新延续'k'的'let'中。consequent和alternative用尾上下文'ctx0'进行CPS化，因为它们的结果将立即传递给'k'。

              [(lambda (,x) ,body) ; 匹配带有单个参数'x'和函数体的lambda表达式。
               (ctx `(lambda (,x k) ,(cps1 body ctx0)))] ; lambda表达式被转换为新的lambda表达式，额外接收参数'k'（延续）。原始lambda的函数体用尾上下文'ctx0'进行CPS化，因为其结果将传递给该延续'k'。

              [(,op ,a ,b) ; 匹配带有二元操作符'op'和两个操作数'a'、'b'的表达式。
               (cps1 a ; 递归转换第一个操作数'a'。
                     (lambda (v1) ; 'a'的延续。接收结果'v1'。
                       (cps1 b ; 递归转换第二个操作数'b'。
                             (lambda (v2) ; 'b'的延续。接收结果'v2'。
                                   (ctx `(,op ,v1 ,v2))))))] ; 将原始上下文'ctx'应用于由操作符'op'和操作数CPS化结果'v1'、'v2'构成的表达式。

              [(,rator ,rand) ; 匹配函数应用，包含rator（函数）和rand（参数）。
               (cps1 rator ; 递归转换rator。
                     (lambda (r) ; rator的延续。接收结果'r'（函数）。
                       (cps1 rand ; 递归转换操作数。
                             (lambda (d) ; 操作数的延续。接收结果'd'（参数）。
                               (cond
                                [(trivial? r) (ctx `(,r ,d))] ; 如果rator'r'是简单操作符（如zero?、add1、sub1），将当前上下文'ctx'应用于操作符对操作数的应用。
                                [(eq? ctx ctx0) `(,r ,d k)]  ; 尾调用。如果当前上下文是尾上下文'ctx0'，说明此函数应用处于尾位置。CPS化函数'r'以CPS化参数'd'和当前延续'k'进行调用。
                                [else ; 如果函数应用不处于尾位置。
                                 (let ([u (fv)]) ; 生成新鲜变量名'u'用于保存结果。
                                   `(,r ,d (lambda (,u) ,(ctx u))))])))))]))]) ; CPS化函数'r'以CPS化参数'd'和新延续进行调用，该延续接收结果'u'并对其实施原始上下文'ctx'。

      (cps1 exp id))));; 通过以输入表达式'exp'和初始恒等延续'id'调用'cps1'来启动CPS转换。

;;; 测试
;; 变量
(cps 'x) ; 转换变量'x'。结果将是'(k x)'，因为初始上下文是'id'，且'id'被应用于'x'。

(cps '(lambda (x) x)) ; 转换简单恒等lambda函数。结果将是'(lambda (x k) (k x))'。

(cps '(lambda (x) (x 1))) ; 转换将其参数应用于1的lambda函数。结果将是'(lambda (x k) (x 1 k))'。

;; 无lambda（将生成恒等函数以返回顶层）
(cps '(if (f x) a b)) ; 转换测试部分为函数调用的if表达式。

(cps '(if x (f a) b)) ; 转换测试部分为变量的if表达式。

;; 独立if（尾位置）
(cps '(if x (f a) b)) ; 此处'if'位于顶层，故处于尾上下文。

;; if位于if测试内部（非尾位置）
(cps '(lambda (x) (if (f x) a b))) ; 'if'位于lambda内部，且其结果被lambda使用（隐式返回），故不处于尾上下文。

(cps '(lambda (x) (if (if x (f a) b) c d))) ; 嵌套'if'表达式。内部'if'位于外部'if'的测试部分。

;; 两个分支都是简单操作，应进行更多优化
(cps '(lambda (x) (if (if x (zero? a) b) c d)))

;; if位于if分支内部（尾位置）
(cps '(lambda (x) (if t (if x (f a) b) c))) ; 内部'if'位于外部'if'的consequent分支。若外部'if'处于尾上下文，内部亦然。

;; if位于if分支内部，但再次位于另一个if测试中（非尾位置）
(cps '(lambda (x) (if (if t (if x (f a) b) c) e w)))

;; if作为操作数（非尾位置）
(cps '(lambda (x) (h (if x (f a) b)))) ; 'if'表达式的结果被用作'h'的参数。

;; if作为操作符（非尾位置）
(cps '(lambda (x) ((if x (f g) h) c))) ; 'if'表达式的结果被用作要调用的函数。

;; 为何需要多于两个名称
(cps '(((f a) (g b)) ((f c) (g d)))) ; 此示例可能展示在转换复杂嵌套表达式时，需要新鲜变量名生成器（'fv'）以避免命名冲突。

;; 阶乘
(define fact-cps
  (cps
   '(lambda (n)
      ((lambda (fact)
         ((fact fact) n))
       (lambda (fact)
         (lambda (n)
           (if (zero? n)
               1
               (* n ((fact fact) (sub1 n))))))))));; 打印CPS化后的函数

(pretty-print fact-cps);; =>
;; '(lambda (n k)
;;    ((lambda (fact k) (fact fact (lambda (v0) (v0 n k))))
;;     (lambda (fact k)
;;       (k
;;        (lambda (n k)
;;          (if (zero? n)
;;            (k 1)
;;            (fact
;;             fact
;;             (lambda (v1) (v1 (sub1 n) (lambda (v2) (k (* n v2))))))))));
;;     k))

((eval fact-cps) 5 (lambda (v) v));; => 120
```

**CPS转换器说明：**

此Scheme代码实现了Scheme语言简单子集的 Continuation-Passing Style（CPS）转换。以下是关键概念及代码工作原理的解析：

**1. Continuation-Passing Style（CPS）：**

* 在CPS中，函数不直接返回值，而是接收一个称为**延续**的额外参数。
* 延续是一个函数，表示要对当前函数结果执行的剩余计算。
* 当CPS函数完成计算时，它会使用结果调用该延续。

**为何使用CPS？**

* **显式控制流：** CPS使控制流显式化。函数调用和返回被替换为对延续的调用。
* **尾调用优化：** CPS便于实现正确的尾调用优化。在转换后的代码中，尾位置的函数调用成为最后操作，无需增加栈深度即可高效执行。
* **实现高级控制结构：** CPS可用作编译器的中间表示，以实现异常、协程和回溯等功能。

**2. `cps`函数：**

* 转换的主入口点。接收表达式`exp`作为输入。
* 使用`letrec`定义多个相互递归的辅助函数。
* 通过以输入表达式和恒等函数`id`作为初始延续调用`cps1`来初始化转换。这意味着转换后表达式的最终结果将直接返回。

**3. 辅助函数：**

* **`trivial?`：** 识别基本操作符如`zero?`、`add1`和`sub1`。这些在转换中会特殊处理。
* **`id`：** 恒等函数`(lambda (v) v)`。是初始延续，意为"直接返回值"。
* **`ctx0`：** 创建"尾上下文"。给定值`v`，返回`(k v)`，其中`k`是当前延续。表示当前计算处于尾位置，结果应直接传递给等待的延续。
* **`fv`：** 生成新鲜变量名（如`v0`、`v1`、`v2`等）。在引入新延续时，这对避免变量捕获至关重要。

**4. `cps1`函数（核心转换）：**

* 此函数递归遍历输入表达式并将其转换为CPS形式。
* 接收两个参数：要转换的表达式`exp`和当前延续`ctx`。
* 使用`pmatch`库进行模式匹配以处理不同类型的表达式：

    * **字面量和变量：** 如果表达式不是序对（字面量或变量），它已是值。将当前延续`ctx`应用于该值：`(ctx x)`。

    * **`if`表达式：** 这是处理尾调用和避免上下文重复的转换器关键部分。
        * 首先转换`test`表达式，其延续接收测试结果（`t`）。
        * 如果当前上下文`ctx`是尾上下文（`ctx0`）或初始恒等上下文（`id`），说明`if`表达式本身处于尾位置。此时保留`if`结构，并用相同上下文`ctx`对`conseq`和`alt`分支进行CPS化。
        * 如果当前上下文不是尾上下文，说明`if`表达式的结果后续会被使用。创建新延续`k`来接收`if`的结果并对其实施原始上下文`ctx`。然后用尾上下文`ctx0`对`conseq`和`alt`分支进行CPS化，并将整个`if`表达式包装在引入`k`的`let`中。

    * **`lambda`表达式：** lambda表达式`(lambda (x) body)`被转换为新的lambda表达式，额外接收参数`k`（延续）：`(lambda (x k) (cps1 body ctx0))`。原始lambda的函数体用尾上下文`ctx0`进行CPS化。

    * **二元操作（`op a b`）：** 操作数`a`和`b`被顺序CPS化。`a`的延续接收其结果`v1`，然后用接收结果`v2`的延续对`b`进行CPS化。最后将原始上下文`ctx`应用于由操作符`op`和CPS化结果`v1`、`v2`构成的表达式。

    * **函数应用（`rator rand`）：** `rator`（函数）和`rand`（参数）被顺序CPS化。
        * 如果`rator`是`trivial?`操作符，直接将当前上下文`ctx`应用于操作符对操作数的应用结果。
        * 如果当前上下文是尾上下文（`ctx0`），CPS化函数`r`以CPS化参数`d`和当前延续`k`进行调用。这确保了正确的尾调用。
        * 否则（非尾调用），创建新延续来接收函数调用结果并对其实施原始上下文`ctx`。CPS化函数`r`以CPS化参数`d`和该新延续进行调用。

**5. 测试：**

* 代码包含多个测试用例，展示不同类型表达式的转换，包括变量、lambda函数、不同上下文中的`if`表达式和函数应用。

**6. 阶乘示例：**

* `fact-cps`定义展示CPS转换器如何应用于递归阶乘函数。
* `pretty-print`输出显示阶乘函数的CPS化版本，现在额外接收延续参数`k`。
* 最后一行以输入`5`和顶层延续`(lambda (v) v)`（直接返回最终值）评估CPS化阶乘函数。

**总结，此代码实现的CPS转换旨在：**

* 将表达式转换为 continuation-passing style。
* 通过显式传递当前延续来确保正确的尾调用优化。
* 当`if`本身处于尾位置时，高效处理`if`表达式而不复制周围上下文。这是通过保留`if`结构并用相同上下文对分支进行CPS化实现的。当`if`不处于尾位置时，会引入新延续来处理结果。
