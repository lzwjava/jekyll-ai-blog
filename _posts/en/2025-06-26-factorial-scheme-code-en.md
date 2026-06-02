---
audio: false
generated: true
lang: en
layout: post
title: Chez Scheme Factorial Program
translated: false
type: note
---

Here's a simple Chez Scheme program that calculates the factorial of a number. Save it as `factorial.scm`:

```scheme
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(display "Factorial of 5 is: ")
(display (factorial 5))
(newline)
```

To run it:
1. Save the code in a file named `factorial.scm`.
2. In your terminal, navigate to the directory containing the file.
3. Run: `scheme --script factorial.scm`

This will output:
```
Factorial of 5 is: 120
```

The program defines a recursive `factorial` function and computes the factorial of 5. The `--script` option (as shown in the `scheme --help` output) allows you to run the file directly.
