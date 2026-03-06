---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust 借用检查器简单解释
translated: true
type: note
---

## Rust Borrow Checker —— 全面介绍

---

### 1. 什么是 Borrow Checker？

Borrow checker 是 Rust 编译器的一个静态分析组件，它会验证程序中的每一个引用。它的任务是防止其他系统语言中常见的几种内存错误，例如 use-after-free（在内存被释放后访问它）和 data races。

当我们查看编译阶段——解析、语义分析（borrow checker 在此阶段发挥作用）、优化和代码生成——borrow checker 在语义分析阶段运行，在生成任何可执行二进制文件之前进行。

Borrow checker 执行的所有分析都在编译时完成。您不会为此支付任何运行时成本。然而，这个系统确实有一定的成本：学习曲线。许多 Rust 新手用户会经历一种称为“与 borrow checker 斗争”的情况，此时 Rust 编译器拒绝编译作者认为有效的程序。

---

### 2. Ownership —— 基础

Borrow checker 帮助您管理 ownership。正如 *The Rust Programming Language* 一书所述，“Ownership 是 Rust 最独特的功能，它使 Rust 能够在不需要垃圾回收器的情况下提供内存安全保证。”

在实践中，当传递变量时，您可以做三件事之一：移动数据本身并放弃 ownership，创建数据的副本并传递它，或者传递数据的引用并保留 ownership——让接收者暂时 borrow 它。

---

### 3. Borrowing 和 References

与其直接传递值，您可以获取一个引用（`&T`）。它不拥有资源，而是 borrow ownership。一个 borrow 某物的绑定在超出作用域时不会释放资源。这意味着在使用引用调用函数后，您可以再次使用原始绑定。

有三种方式访问 Rust 项的内容：通过项的所有者（`item`）、共享引用（`&item`）或可变引用（`&mut item`）。所有者可以创建、读取、更新和 drop 该项。可变引用可以读取和更新底层项。普通引用只能从中读取。

---

### 4. 两大核心规则

Borrow checker 强制执行两条基本规则：

#### 规则 1：引用不能比它借用的值存活得更久

Rust 的 borrow checker 对借用值的方式施加了约束。引用不能比它借用的值存活得更久——例如，您不能存储一个指向超出作用域的值的引用，然后再尝试使用该引用。

#### 规则 2：别名规则（Shared XOR Mutable）

对于给定的值，在任何时候：您可以有一个或多个对该值的共享引用，**或者**恰好有一个独占的（可变）引用到该值——绝不能同时两者都有。

```rust
fn main() {
    let mut a = 10;
    let b = &a;       // immutable borrow
    {
        let c = &mut a;   // mutable borrow — ERROR: conflicts with b
        *c = 20;
    }
    println!("{}", b); // b used here
}
```

上面的代码失败是因为 `a` 同时被可变借用（通过 `c`）和不可变借用（通过 `b`）。

---

### 5. 为什么别名规则重要：Data Races

Data race 发生在两个或多个指针同时访问同一内存位置，其中至少有一个在写入，并且操作未同步时发生。对于共享引用，您可以拥有任意多个，因为它们都不在写入。但是，由于您一次只能有一个 `&mut T`，因此不可能发生 data race。这是 Rust 如何在编译时防止 data races。

---

### 6. Iterator 失效预防

Borrow checker 防止的一个例子是“iterator invalidation”，即尝试变异您正在迭代的集合时发生的情况。如果您尝试在用不可变引用迭代 `Vec` 时向其 push，编译器会发出错误：`cannot borrow 'v' as mutable because it is also borrowed as immutable`。

---

### 7. Lifetimes

Lifetimes 是 borrow checker 跟踪引用有效期长短的机制。

每当您创建一个 borrow，编译器就会为生成的引用分配一个 lifetime。这个 lifetime 对应于引用可以使用的那段代码范围。编译器推断这个 lifetime 为仍涵盖引用所有使用的最小 lifetime。

当编译器无法推断输入和输出 lifetimes 之间的关系时，需要在函数签名中使用显式 lifetime 注解：

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

这里的 `'a` 表示：“返回的引用至少与两个输入一样长寿。”

---

### 8. Non-Lexical Lifetimes (NLL)

通过在 Rust 2018 中引入的 Non-Lexical Lifetimes (NLL)，borrow checker 变得更灵活和直观。Rust 现在可以检测引用在作用域中真正不再被使用的时间，而不是强制它们存活到词法块结束。这减少了“borrow checker 斗争”，并确保您只关注真正的 lifetime 冲突。

在 NLL 之前，即使先前的不可变 borrow 已在变异之前结束，编译器也会抱怨您无法可变借用数据。有了 NLL，编译器会跟踪引用的实际使用位置，并在可能时更早结束它们的 lifetime。

从 Rust 1.63 开始，NLL 默认启用于所有 Rust editions，完成了旧的基于 AST 的 borrow checker 的移除。

---

### 9. Struct 中的字段 Borrowing

Struct 的字段可以独立于彼此被 borrow，但对 struct 调用方法会 borrow 整个 struct，可能使对单个字段的引用失效。

---

### 10. 逃生舱：Interior Mutability

当单写入者规则过于严格时，Rust 提供了 **interior mutability** 模式：

- **`Cell<T>`** —— 对于 `Copy` 类型，通过共享引用允许变异。
- **`RefCell<T>`** —— 在运行时而非编译时强制执行 borrow 规则。
- **`Mutex<T>` / `RwLock<T>`** —— 适用于并发代码的线程安全等价物。
- **`Rc<T>` / `Arc<T>`** —— 使用引用计数的共享 ownership。

对于从 C++ 转过来的程序员，最常见的工具是 `Rc<T>`（及其线程安全变体 `Arc<T>`），通常与 `RefCell`（或线程安全的替代 `Mutex`）结合使用。然而，这种方法意味着您会失去 Rust 的一些保护——同一项在存在另一个引用时被可变借用的情况会导致运行时 panic 而非编译时错误。

---

### 11. 自引用 Struct —— 已知限制

来自其他语言的程序员与 borrow checker 的一个特定战斗是尝试创建自引用数据结构——包含 owned 数据及其内部引用的 struct。Rust 中的数据结构可以从栈移动到堆再返回，这使得内部引用本质上不安全。

---

### 12. 未来：Polonius

Rust borrow checking 的下一个前沿是 Polonius —— 从 2018 年的 NLL 工作中分离出的下一代 borrow checker。它的最重要贡献是修复已知限制，即 borrow checker 拒绝涉及条件返回引用的有效代码。

---

### 13. 总结表格

 

| Concept | Rule |
|---|---|
| Ownership | 每个值恰好有一个所有者 |
| Move | Ownership 转移；原始绑定变为无效 |
| Immutable borrow (`&T`) | 可同时允许多个 |
| Mutable borrow (`&mut T`) | 一次仅一个；不允许其他借用 |
| Lifetime | 跟踪引用有效期长短 |
| NLL | 在最后使用处结束借用，而非作用域边界 |
| Interior mutability | 通过 `RefCell`、`Mutex` 等运行时检查变异 |

---

### 14. 与 Borrow Checker 协作的提示

当遇到 borrow checker 错误时，仔细阅读错误消息——Rust 的错误会解释违反了哪条规则，并经常建议修复。识别冲突的借用，追踪 lifetimes，并应用如 cloning、重组或 interior mutability 等模式。大多数时候，borrow checker 错误表明设计可以改进，而无需立即求助 `unsafe` 或 `RefCell`。

References:

- [Borrow Checking — Comprehensive Rust](https://google.github.io/comprehensive-rust/borrowing/borrowck.html)
- [References and Borrowing — The Rust Book (MIT mirror)](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/references-and-borrowing.html)
- [Understanding the Rust Borrow Checker — LogRocket](https://blog.logrocket.com/introducing-rust-borrow-checker/)
- [Understanding and Implementing Rust's Borrow Checker — Reintech](https://reintech.io/blog/understanding-implementing-rust-borrow-checker)
- [Item 15: Understand the Borrow Checker — Effective Rust](https://www.lurklurk.org/effective-rust/borrows.html)
- [NLL RFC 2094 — Rust RFC Book](https://rust-lang.github.io/rfcs/2094-nll.html)
- [NLL Fully Stable — Rust Blog](https://blog.rust-lang.org/2022/08/05/nll-by-default/)
- [The Rust Borrow Checker — A Deep Dive (InfoQ)](https://www.infoq.com/presentations/rust-borrow-checker/)
- [Borrow Checker — DeepWiki](https://deepwiki.com/rust-lang/rust/3.2-borrow-checker)