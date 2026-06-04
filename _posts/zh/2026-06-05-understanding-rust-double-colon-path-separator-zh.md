---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解 Rust 双冒号路径分隔符
translated: true
type: note
---

**问题:** Rust 中的 `::` 是什么意思？

**答案:**

`::` 是**路径分隔符**——它用于在命名空间、模块和关联项之间进行导航。

## 核心用法

**1. 模块路径**
```rust
use std::collections::HashMap;  // :: 在模块树中导航
use tokio::spawn;
```

**2. 关联函数和关联类型**（非方法）
```rust
String::new()           // String 上的关联函数
Vec::<i32>::new()       // 类型特定的构造函数
std::io::Result::Ok(5)  // 枚举上的关联类型
```

**3. trait 方法（消除歧义）**
```rust
trait Speak { fn say(&self); }
struct Dog;

impl Speak for Dog {
    fn say(&self) { println!("woof"); }
}

// 如果多个 trait 实现了 `say()`，使用 Trait::method()
<Dog as Speak>::say(&dog);
```

**4. 静态路径（全局作用域）**
```rust
::mymodule::function()  // 从 crate 根开始的绝对路径
```

## 关键区别：`.` 与 `::`

```rust
let s = String::new();   // :: — 关联函数（不是实例方法）
s.len();                 // .  — 方法（在实例上调用）
```

将 `::` 理解为“作用域导航”，将 `.` 理解为“在该值上调用”。