---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Path Separator Scope Navigation
translated: false
type: note
---

**Question:** What does `::` mean in Rust?

**Answer:**

`::` is the **path separator** — it navigates through namespaces, modules, and associated items.

## Core Uses

**1. Module paths**

```rust
use std::collections::HashMap;  // :: navigates the module tree
use tokio::spawn;
```

**2. Associated functions & types** (not methods)

```rust
String::new()           // Associated function on String
Vec::<i32>::new()       // Type-specific constructor
std::io::Result::Ok(5)  // Associated type on enum
```

**3. Trait methods (disambiguate)**

```rust
trait Speak { fn say(&self); }
struct Dog;

impl Speak for Dog {
    fn say(&self) { println!("woof"); }
}

// If multiple traits implement `say()`, use Trait::method()
<Dog as Speak>::say(&dog);
```

**4. Static paths (global scope)**

```rust
::mymodule::function()  // Absolute path from crate root
```

## Key Difference: `.` vs `::`

```rust
let s = String::new();   // :: — associated function (not a method on an instance)
s.len();                 // .  — method (called on instance)
```

Think of `::` as "scope navigation" and `.` as "call on this value."
