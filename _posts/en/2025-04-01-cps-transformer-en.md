---
audio: false
generated: true
lang: en
layout: post
title: CPS Transformer
translated: false
type: note
---

```scheme
;; A simple CPS transformer which does proper tail-call and does not
;; duplicate contexts for if-expressions.
;; author: Yin Wang (yw21@cs.indiana.edu)
(load "pmatch.scm") ; Loads a pattern matching library for Scheme, making it easier to handle different expression structures.

(define cps
  (lambda (exp)
    (letrec
        ([trivial? (lambda (x) (memq x '(zero? add1 sub1)))] ; Checks if a given symbol is one of the primitive operators: zero?, add1, sub1. These are treated specially in the transformation.
         [id (lambda (v) v)] ; The identity function, used as the initial continuation for the top-level expression.
         [ctx0 (lambda (v) `(k ,v))]      ; tail context. This creates a continuation that simply applies the current continuation 'k' to a value 'v'. It's used when the current call is in tail position.
         [fv (let ([n -1]) ; Creates a generator for fresh variable names.
               (lambda ()
                 (set! n (+ 1 n))
                 (string->symbol (string-append "v" (number->string n)))))]
         [cps1
          (lambda (exp ctx) ; The core recursive function that performs the CPS transformation. It takes an expression 'exp' and a continuation 'ctx' as arguments. The continuation represents what to do with the result of evaluating 'exp'.
            (pmatch exp ; Uses pattern matching to analyze the structure of the expression.
              [,x (guard (not (pair? x))) (ctx x)] ; Base case: If the expression 'x' is not a pair (i.e., it's a literal or a variable), it means it's already a value. Apply the current continuation 'ctx' to this value.

              [(if ,test ,conseq ,alt) ; Matches an 'if' expression with a test, consequent, and alternative.
               (cps1 test ; Recursively transform the 'test' expression.
                     (lambda (t) ; The continuation for the 'test' expression. It takes the result of the test (which will be a boolean value) as 't'.
                       (cond
                        [(memq ctx (list ctx0 id)) ; If the current context 'ctx' is either the tail context 'ctx0' or the initial identity context 'id', it means the 'if' expression itself is in a tail position.
                         `(if ,t ,(cps1 conseq ctx) ,(cps1 alt ctx))] ; In this case, the 'if' expression remains an 'if' expression in the CPSed code. The consequent and alternative are CPSed with the same context 'ctx'. This avoids duplicating contexts.
                        [else ; If the current context is not a tail context, it means the result of the 'if' expression needs to be passed to some further computation.
                         (let ([u (fv)]) ; Generate a fresh variable name 'u' to hold the result of the 'if' expression.
                           `(let ([k (lambda (,u) ,(ctx u))]) ; Create a new continuation 'k' that takes the result 'u' and applies the original context 'ctx' to it.
                              (if ,t ,(cps1 conseq ctx0) ,(cps1 alt ctx0))))])))] ; The 'if' expression is wrapped in a 'let' that introduces the new continuation 'k'. The consequent and alternative are CPSed with the tail context 'ctx0', as their results will be immediately passed to 'k'.

              [(lambda (,x) ,body) ; Matches a lambda expression with a single argument 'x' and a body.
               (ctx `(lambda (,x k) ,(cps1 body ctx0)))] ; The lambda expression is transformed into a new lambda expression that takes an additional argument 'k' (the continuation). The body of the original lambda is CPSed with the tail context 'ctx0', as its result will be passed to this continuation 'k'.

              [(,op ,a ,b) ; Matches an expression with a binary operator 'op' and two operands 'a' and 'b'.
               (cps1 a ; Recursively transform the first operand 'a'.
                     (lambda (v1) ; The continuation for 'a'. It takes the result 'v1'.
                       (cps1 b ; Recursively transform the second operand 'b'.
                             (lambda (v2) ; The continuation for 'b'. It takes the result 'v2'.
                                   (ctx `(,op ,v1 ,v2))))))] ; Apply the original context 'ctx' to the expression formed by the operator 'op' and the CPSed results of the operands 'v1' and 'v2'.

              [(,rator ,rand) ; Matches a function application with a rator (the function) and a rand (the argument).
               (cps1 rator ; Recursively transform the rator.
                     (lambda (r) ; The continuation for the rator. It takes the result 'r' (the function).
                       (cps1 rand ; Recursively transform the operand.
                             (lambda (d) ; The continuation for the operand. It takes the result 'd' (the argument).
                               (cond
                                [(trivial? r) (ctx `(,r ,d))] ; If the rator 'r' is a trivial operator (like zero?, add1, sub1), apply the current context 'ctx' to the application of the operator to the operand.
                                [(eq? ctx ctx0) `(,r ,d k)]  ; tail call. If the current context is the tail context 'ctx0', it means this function application is in a tail position. The CPSed function 'r' is called with the CPSed argument 'd' and the current continuation 'k'.
                                [else ; If the function application is not in a tail position.
                                 (let ([u (fv)]) ; Generate a fresh variable name 'u' for the result.
                                   `(,r ,d (lambda (,u) ,(ctx u))))])))))]))]) ; The CPSed function 'r' is called with the CPSed argument 'd' and a new continuation that takes the result 'u' and applies the original context 'ctx' to it.

      (cps1 exp id))));; Starts the CPS transformation by calling 'cps1' with the input expression 'exp' and the initial identity continuation 'id'.

;;; tests
;; var
(cps 'x) ; Transforms the variable 'x'. The result will be '(k x)' because the initial context is 'id', and 'id' is applied to 'x'.

(cps '(lambda (x) x)) ; Transforms a simple identity lambda function. The result will be '(lambda (x k) (k x))'.

(cps '(lambda (x) (x 1))) ; Transforms a lambda function that applies its argument to 1. The result will be '(lambda (x k) (x 1 k))'.

;; no lambda (will generate identity functions to return to the toplevel)
(cps '(if (f x) a b)) ; Transforms an if expression where the test is a function call.

(cps '(if x (f a) b)) ; Transforms an if expression where the test is a variable.

;; if stand-alone (tail)
(cps '(if x (f a) b)) ; Here, the 'if' is at the top level, so it's in a tail context.

;; if inside if-test (non-tail)
(cps '(lambda (x) (if (f x) a b))) ; The 'if' is inside a lambda, and its result is used by the lambda (implicitly returned), so it's not in a tail context.

(cps '(lambda (x) (if (if x (f a) b) c d))) ; Nested 'if' expressions. The inner 'if' is in the test of the outer 'if'.

;; both branches are trivial, should do some more optimizations
(cps '(lambda (x) (if (if x (zero? a) b) c d)))

;; if inside if-branch (tail)
(cps '(lambda (x) (if t (if x (f a) b) c))) ; The inner 'if' is in the consequent branch of the outer 'if'. If the outer 'if' is in a tail context, the inner one will also be.

;; if inside if-branch, but again inside another if-test (non-tail)
(cps '(lambda (x) (if (if t (if x (f a) b) c) e w)))

;; if as operand (non-tail)
(cps '(lambda (x) (h (if x (f a) b)))) ; The result of the 'if' expression is used as an argument to 'h'.

;; if as operator (non-tail)
(cps '(lambda (x) ((if x (f g) h) c))) ; The result of the 'if' expression is used as the function to be called.

;; why we need more than two names
(cps '(((f a) (g b)) ((f c) (g d)))) ; This example likely demonstrates the need for the fresh variable name generator ('fv') to avoid naming conflicts when transforming complex nested expressions.

;; factorial
(define fact-cps
  (cps
   '(lambda (n)
      ((lambda (fact)
         ((fact fact) n))
       (lambda (fact)
         (lambda (n)
           (if (zero? n)
               1
               (* n ((fact fact) (sub1 n))))))))));; print out CPSed function

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

**Explanation of the CPS Transformer:**

This Scheme code implements a Continuation-Passing Style (CPS) transformation for a simple subset of the Scheme language. Here's a breakdown of the key concepts and how the code works:

**1. Continuation-Passing Style (CPS):**

* In CPS, a function doesn't return a value directly. Instead, it takes an extra argument called a **continuation**.
* The continuation is a function that represents the rest of the computation to be performed with the result of the current function.
* When a CPS function finishes its computation, it calls the continuation with the result.

**Why use CPS?**

* **Explicit Control Flow:** CPS makes the flow of control explicit. Function calls and returns are replaced by calls to continuations.
* **Tail-Call Optimization:** CPS enables easy implementation of proper tail-call optimization. In the transformed code, function calls in tail position become the last operation, allowing for efficient execution without increasing the stack depth.
* **Implementing Advanced Control Structures:** CPS can be used as an intermediate representation in compilers to implement features like exceptions, coroutines, and backtracking.

**2. The `cps` Function:**

* The main entry point for the transformation. It takes an expression `exp` as input.
* It uses `letrec` to define several mutually recursive helper functions.
* It initializes the transformation by calling `cps1` with the input expression and the identity function `id` as the initial continuation. This means that the final result of the transformed expression will be returned directly.

**3. Helper Functions:**

* **`trivial?`:** Identifies primitive operators like `zero?`, `add1`, and `sub1`. These are handled specially in the transformation.
* **`id`:** The identity function `(lambda (v) v)`. It's the initial continuation, meaning "just return the value".
* **`ctx0`:** Creates a "tail context". Given a value `v`, it returns `(k v)`, where `k` is the current continuation. This signifies that the current computation is in a tail position, and the result should be passed directly to the awaiting continuation.
* **`fv`:** Generates fresh variable names (e.g., `v0`, `v1`, `v2`, ...). This is crucial to avoid variable capture when introducing new continuations.

**4. The `cps1` Function (The Core Transformation):**

* This function recursively traverses the input expression and transforms it into CPS.
* It takes two arguments: the expression `exp` to be transformed and the current continuation `ctx`.
* It uses the `pmatch` library for pattern matching to handle different types of expressions:

  * **Literals and Variables:** If the expression is not a pair (a literal or a variable), it's already a value. The current continuation `ctx` is applied to this value: `(ctx x)`.

  * **`if` Expressions:** This is a key part of the transformer that handles tail calls and avoids context duplication.
    * It first transforms the `test` expression with a continuation that takes the result of the test (`t`).
    * If the current context `ctx` is a tail context (`ctx0`) or the initial identity context (`id`), it means the `if` expression itself is in a tail position. In this case, the `if` structure is preserved, and the `conseq` and `alt` branches are CPSed with the same context `ctx`.
    * If the current context is not a tail context, it means the result of the `if` expression needs to be used later. A new continuation `k` is created that takes the result of the `if` and applies the original context `ctx` to it. The `conseq` and `alt` branches are then CPSed with the tail context `ctx0`, and the entire `if` expression is wrapped in a `let` that introduces `k`.

  * **`lambda` Expressions:** A `lambda` expression `(lambda (x) body)` is transformed into a new `lambda` expression that takes an additional argument `k` (the continuation): `(lambda (x k) (cps1 body ctx0))`. The body of the original lambda is CPSed with the tail context `ctx0`.

  * **Binary Operations (`op a b`):** The operands `a` and `b` are CPSed sequentially. The continuation for `a` takes its result `v1`, and then CPSes `b` with a continuation that takes its result `v2`. Finally, the original context `ctx` is applied to the expression formed by the operator `op` and the CPSed results `v1` and `v2`.

  * **Function Applications (`rator rand`):** The `rator` (function) and `rand` (argument) are CPSed sequentially.
    * If the `rator` is a `trivial?` operator, the current context `ctx` is directly applied to the result of applying the operator to the operand.
    * If the current context is a tail context (`ctx0`), the CPSed function `r` is called with the CPSed argument `d` and the current continuation `k`. This ensures proper tail calls.
    * Otherwise (non-tail call), a new continuation is created that takes the result of the function call and applies the original context `ctx` to it. The CPSed function `r` is called with the CPSed argument `d` and this new continuation.

**5. Tests:**

* The code includes several test cases that demonstrate the transformation of different types of expressions, including variables, lambda functions, `if` expressions in various contexts, and function applications.

**6. Factorial Example:**

* The `fact-cps` definition shows how the CPS transformer can be applied to a recursive factorial function.
* The `pretty-print` output shows the CPSed version of the factorial function, which now takes an extra continuation argument `k`.
* The final line evaluates the CPSed factorial function with the input `5` and a top-level continuation `(lambda (v) v)` that simply returns the final value.

**In summary, this code implements a CPS transformation that aims to:**

* Convert expressions into continuation-passing style.
* Ensure proper tail-call optimization by passing the current continuation explicitly.
* Handle `if` expressions efficiently without duplicating the surrounding context when the `if` itself is in a tail position. This is achieved by keeping the `if` structure and CPSing the branches with the same context. When the `if` is not in a tail position, it introduces a new continuation to handle the result.
