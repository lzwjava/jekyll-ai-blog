---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust路径分隔符作用域导航
translated: true
type: note
---

**问题：** 在 Rust 中，`::` 表示什么？

**答案：**

`::` 是**路径分隔符**——它用于导航命名空间、模块和关联项。

## 核心用途

**1. 模块路径**

```rust
use std::collections::HashMap;  // :: 导航模块树
use tokio::spawn;
```

**2. 关联函数和关联类型**（非方法）

```rust
String::new()           // String 上的关联函数
Vec::<i32>::new()       // 特定类型的构造函数
std::io::Result::Ok(5)  // 枚举上的关联类型
```

**3. 特型方法（消除歧义）**

```rust
trait Speak { fn say(&self); }
struct Dog;

impl Speak for Dog {
    fn say(&self) { println!("woof"); }
}

// 如果多个特型都实现了 say()，使用 Trait::method()
<Dog as Speak>::say(&dog);
```

**4. 静态路径（全局作用域）**

```rust
::mymodule::function()  // 从 crate 根开始的绝对路径
```

## 关键区别：`.` 与 `::`

```rust
let s = String::new();   // :: — 关联函数（不是实例上的方法）
s.len();                 // .  — 方法（在实例上调用）
```

可以把 `::` 理解为“作用域导航”，而 `.` 理解为“在此值上调用”。
