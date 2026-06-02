---
audio: false
generated: true
lang: zh
layout: post
title: Chez Scheme阶乘程序
translated: true
type: note
---

这是一个简单的 Chez Scheme 程序，用于计算数字的阶乘。请保存为 `factorial.scm`：

```scheme
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(display "5 的阶乘是: ")
(display (factorial 5))
(newline)
```

运行方法：

1. 将代码保存至名为 `factorial.scm` 的文件中
2. 在终端中切换到该文件所在目录
3. 执行：`scheme --script factorial.scm`

运行后将输出：

```
5 的阶乘是: 120
```

该程序定义了递归阶乘函数并计算 5 的阶乘。如 `scheme --help` 所示，`--script` 选项支持直接运行脚本文件。
