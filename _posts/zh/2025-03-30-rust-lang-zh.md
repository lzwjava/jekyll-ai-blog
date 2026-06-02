---
audio: false
generated: true
lang: zh
layout: post
title: Rust编程语言
translated: true
type: note
---

好的，这是一份关于 Rust 编程语言的综合指南，涵盖了其核心概念、语法和高级特性。Rust 是一门专注于安全性、速度和并发性的系统编程语言。

**I. Rust 简介**

* **什么是 Rust？**
  * Rust 是一门多范式、静态类型、编译型编程语言，专为性能和安全性而设计，尤其适用于系统编程、游戏引擎、Web 汇编和嵌入式系统等领域。
  * 它通过所有权、借用和生命周期的系统，在没有垃圾回收器的情况下实现了内存安全。
  * Rust 强调零成本抽象，意味着你可以获得高级特性而无需显著的运行时开销。
* **主要特性与设计原则：**
  * **内存安全：** 在编译时防止常见错误，如空指针解引用、数据竞争和缓冲区溢出。
  * **无畏并发：** 所有权系统使得编写安全的并发代码更加容易。
  * **高性能：** 底层控制、零成本抽象和高效编译带来了卓越的性能，通常可与 C++ 相媲美。
  * **富有表现力的类型系统：** 强大的类型推断、泛型、Trait（类似于接口或类型类）和代数数据类型。
  * **卓越的工具链：** Cargo（构建系统和包管理器）、rustfmt（代码格式化工具）、clippy（代码 lint 工具）。
  * **不断发展的生态系统：** 拥有一个充满活力且活跃的社区，库和框架的数量不断增长。
* **使用场景：**
  * 操作系统
  * 游戏引擎
  * Web 汇编 (Wasm)
  * 嵌入式系统
  * 命令行工具
  * 网络编程
  * 加密货币
  * 高性能计算

**II. 设置 Rust 开发环境**

* **安装：**
  * 推荐使用 `rustup`（官方的 Rust 工具链安装器）来安装 Rust。
  * 访问 [https://rustup.rs/](https://rustup.rs/) 并按照您操作系统的说明进行操作。
  * 在类 Unix 系统上，通常运行类似这样的命令：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
* **验证安装：**
  * 打开终端或命令提示符并运行：
    * `rustc --version`：显示 Rust 编译器版本。
    * `cargo --version`：显示 Cargo 版本。
* **Cargo：Rust 构建系统与包管理器：**
  * Cargo 对于管理 Rust 项目至关重要。它负责：
    * 构建你的代码。
    * 管理依赖项（crate）。
    * 运行测试。
    * 发布库。
  * **创建新项目：** `cargo new <项目名称>`（创建一个二进制项目）。 `cargo new --lib <库名称>`（创建一个库项目）。
  * **项目结构：** 一个典型的 Cargo 项目包含：
    * `Cargo.toml`：包含项目元数据和依赖项的清单文件。
    * `src/main.rs`：二进制项目的入口点。
    * `src/lib.rs`：库项目的入口点。
    * `Cargo.lock`：记录项目中使用的依赖项的确切版本。
  * **构建：** `cargo build`（在调试模式下构建项目）。 `cargo build --release`（为发布版本进行优化构建）。
  * **运行：** `cargo run`（构建并运行二进制文件）。
  * **添加依赖项：** 将 crate 名称和版本添加到 `Cargo.toml` 的 `[dependencies]` 部分。Cargo 会自动下载并构建它们。
  * **更新依赖项：** `cargo update`。

**III. 基础 Rust 语法与概念**

* **Hello, World!**

    ```rust
    fn main() {
        println!("Hello, world!");
    }
    ```

  * `fn main()`：程序开始执行的主函数。
  * `println!()`：一个宏（由 `!` 表示），用于向控制台打印文本。
* **变量与可变性：**
  * 变量默认是不可变的。要使变量可变，请使用 `mut` 关键字。
  * 声明：`let 变量名 = 值;`（类型推断）。 `let 变量名: 类型 = 值;`（显式类型标注）。
  * 可变变量：`let mut counter = 0; counter = 1;`
  * 常量：使用 `const` 声明，必须有类型标注，且其值必须在编译时已知。`const MAX_POINTS: u32 = 100_000;`
  * 遮蔽：你可以声明一个与之前变量同名的新变量；新变量会遮蔽旧变量。
* **数据类型：**
  * **标量类型：** 表示单个值。
    * **整数：** `i8`, `i16`, `i32`, `i64`, `i128`, `isize`（指针大小的有符号整数）；`u8`, `u16`, `u32`, `u64`, `u128`, `usize`（指针大小的无符号整数）。整数字面值可以有后缀（例如 `10u32`）。
    * **浮点数：** `f32`（单精度）, `f64`（双精度）。
    * **布尔值：** `bool` (`true`, `false`)。
    * **字符：** `char`（Unicode 标量值，4 字节）。
    * **单元类型：** `()`（表示空元组或没有值）。
  * **复合类型：** 将多个值组合在一起。
    * **元组：** 固定大小的有序元素序列，元素类型可以不同。`let my_tuple = (1, "hello", 3.14); let (x, y, z) = my_tuple; let first = my_tuple.0;`
    * **数组：** 固定大小的相同类型元素的集合。`let my_array = [1, 2, 3, 4, 5]; let months: [&str; 12] = ["...", "..."]; let first = my_array[0];`
    * **切片：** 对数组或另一个切片中连续元素序列的动态大小视图。`let slice = &my_array[1..3];`
  * **其他重要类型：**
    * **字符串：**
      * `String`：可增长、可变、拥有所有权的字符串数据。使用 `String::from("...")` 创建，或通过转换其他字符串类型创建。
      * `&str`：字符串切片，对字符串数据的不可变视图。当直接嵌入代码中时（例如 `"hello"`），通常被称为"字符串字面值"。
    * **向量 (`Vec<T>`)：** 可调整大小的数组，可以增长或缩小。`let mut my_vec: Vec<i32> = Vec::new(); my_vec.push(1); let another_vec = vec![1, 2, 3];`
    * **哈希映射 (`HashMap<K, V>`)：** 存储键值对，其中键是唯一的且为可哈希类型。需要 `use std::collections::HashMap;`。
* **运算符：**
  * **算术：** `+`, `-`, `*`, `/`, `%`。
  * **比较：** `==`, `!=`, `>`, `<`, `>=`, `<=`。
  * **逻辑：** `&&` (AND), `||` (OR), `!` (NOT)。
  * **位运算：** `&` (AND), `|` (OR), `^` (XOR), `!` (NOT), `<<` (左移), `>>` (右移)。
  * **赋值：** `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`。
* **控制流：**
  * **`if`, `else if`, `else`：** 条件执行。

        ```rust
        let number = 7;
        if number < 5 {
            println!("condition was true");
        } else if number == 7 {
            println!("number is seven");
        } else {
            println!("condition was false");
        }
        ```

  * **`loop`：** 无限循环（使用 `break` 退出）。

        ```rust
        loop {
            println!("again!");
            break;
        }
        ```

  * **`while`：** 只要条件为真就继续循环。

        ```rust
        let mut counter = 0;
        while counter < 5 {
            println!("counter is {}", counter);
            counter += 1;
        }
        ```

  * **`for`：** 遍历集合。

        ```rust
        let a = [10, 20, 30, 40, 50];
        for element in a.iter() {
            println!("the value is: {}", element);
        }

        for number in 1..5 { // 从 1 迭代到（但不包括）5
            println!("{}", number);
        }
        ```

  * **`match`：** 强大的控制流构造，将值与一系列模式进行比较。

        ```rust
        let number = 3;
        match number {
            1 => println!("one"),
            2 | 3 => println!("two or three"),
            4..=6 => println!("four, five, or six"),
            _ => println!("something else"), // 通配模式
        }
        ```

  * **`if let`：** 一种更简洁的方式来处理枚举或 `Option`，当你只关心一个或少数几个变体时。

        ```rust
        let some_value = Some(5);
        if let Some(x) = some_value {
            println!("The value is: {}", x);
        }
        ```

**IV. 所有权、借用与生命周期**

这是 Rust 内存安全保证的核心。

* **所有权：**
  * Rust 中的每个值都有一个变量作为其*所有者*。
  * 一个值在任意时刻只能有一个所有者。
  * 当所有者离开作用域时，该值将被丢弃（其内存被释放）。
* **借用：**
  * 无需转移所有权，你可以创建对值的引用。这称为*借用*。
  * **不可变借用 (`&`):** 你可以同时拥有对某个值的多个不可变引用。不可变借用不允许修改被借用的值。
  * **可变借用 (`&mut`):** 你一次最多只能拥有一个对某个值的可变引用。可变借用允许修改被借用的值。
  * **借用规则：**
        1. 在任意给定时间，你*要么*只能有一个可变引用，*要么*只能有任意数量的不可变引用。
        2. 引用必须始终有效。
* **生命周期：**
  * 生命周期是描述引用有效范围的注解。Rust 编译器使用生命周期信息来确保引用不会比它们所指向的数据存活得更久（悬垂指针）。
  * 在许多情况下，编译器可以自动推断生命周期（生命周期省略）。
  * 当引用的生命周期不明确时，你可能需要在函数签名或结构体定义中显式标注生命周期。
  * 显式生命周期注解示例：

        ```rust
        fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
            if x.len() > y.len() {
                x
            } else {
                y
            }
        }
        ```

        `'a` 表示返回的字符串切片将至少与两个输入字符串切片活得一样久。

**V. 结构体、枚举与模块**

* **结构体：** 将命名字段组合在一起的自定义数据类型。

    ```rust
    struct User {
        active: bool,
        username: String,
        email: String,
        sign_in_count: u64,
    }

    fn main() {
        let mut user1 = User {
            active: true,
            username: String::from("someusername123"),
            email: String::from("someone@example.com"),
            sign_in_count: 1,
        };

        user1.email = String::from("another@example.com");

        let user2 = User {
            email: String::from("another@example.com"),
            ..user1 // 结构体更新语法，剩余字段来自 user1
        };
    }
    ```

  * 元组结构体：没有命名字段的命名元组。`struct Color(i32, i32, i32);`
  * 单元结构体：没有字段的结构体。`struct AlwaysEqual;`
* **枚举：** 通过列举其可能的变体来定义类型。

    ```rust
    enum Message {
        Quit,
        Move { x: i32, y: i32 }, // 匿名结构体
        Write(String),
        ChangeColor(i32, i32, i32), // 类元组
    }

    fn main() {
        let q = Message::Quit;
        let m = Message::Move { x: 10, y: 5 };
        let w = Message::Write(String::from("hello"));

        match m {
            Message::Quit => println!("Quit"),
            Message::Move { x, y } => println!("Move to x={}, y={}", x, y),
            Message::Write(text) => println!("Write: {}", text),
            Message::ChangeColor(r, g, b) => println!("Change color to r={}, g={}, b={}", r, g, b),
        }
    }
    ```

  * 枚举可以直接在其变体中保存数据。
* **模块：** 在 crate（包）内组织代码。
  * 使用 `mod` 关键字定义模块。
  * 模块可以包含其他模块、结构体、枚举、函数等。
  * 使用 `pub`（公开）和私有（默认）控制可见性。
  * 使用模块路径访问模块内的项（例如 `my_module::my_function()`）。
  * 使用 `use` 关键字将项引入当前作用域（例如 `use std::collections::HashMap;`）。
  * 将模块分离到不同的文件中（约定：名为 `my_module` 的模块放在 `src/my_module.rs` 或 `src/my_module/mod.rs` 中）。

**VI. Trait 与泛型**

* **Trait：** 类似于其他语言中的接口或类型类。它们定义了一组方法，类型必须实现这些方法才能满足特定契约。

    ```rust
    pub trait Summary {
        fn summarize(&self) -> String;
    }

    pub struct NewsArticle {
        pub headline: String,
        pub location: String,
        pub author: String,
        pub content: String,
    }

    impl Summary for NewsArticle {
        fn summarize(&self) -> String {
            format!("{}, by {} ({})", self.headline, self.author, self.location)
        }
    }

    pub struct Tweet {
        pub username: String,
        pub content: String,
        pub reply: bool,
        pub retweet: bool,
    }

    impl Summary for Tweet {
        fn summarize(&self) -> String {
            format!("{}: {}", self.username, self.content)
        }
    }

    fn main() {
        let tweet = Tweet {
            username: String::from("horse_ebooks"),
            content: String::from("of course, as you probably already know, people"),
            reply: false,
            retweet: false,
        };

        println!("New tweet available! {}", tweet.summarize());
    }
    ```

  * Trait 可以为方法提供默认实现。
  * Trait 可以用作泛型类型的约束。
* **泛型：** 编写可以在编译时处理多种类型而无需知道具体类型的代码。

    ```rust
    fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
        let mut largest = list[0];

        for &item in list.iter() {
            if item > largest {
                largest = item;
            }
        }

        largest
    }

    fn main() {
        let number_list = vec![34, 50, 25, 100, 65];
        let result = largest(&number_list);
        println!("The largest number is {}", result);

        let char_list = vec!['y', 'm', 'a', 'q'];
        let result = largest(&char_list);
        println!("The largest char is {}", result);
    }
    ```

  * 类型参数在尖括号 `<T>` 中声明。
  * Trait 约束 (`T: PartialOrd + Copy`) 指定了泛型类型必须实现的功能。
  * `PartialOrd` 允许使用 `>` 进行比较，`Copy` 表示该类型可以通过值复制。

**VII. 错误处理**

Rust 强调显式的错误处理。

* **`Result` 枚举：** 表示成功 (`Ok`) 或失败 (`Err`)。

    ```rust
    enum Result<T, E> {
        Ok(T),
        Err(E),
    }
    ```

  * `T` 是成功值的类型。
  * `E` 是错误值的类型。
  * 通常用于可能失败的操作（例如，文件 I/O，网络请求）。
  * `?` 运算符是处理 `Result` 值的语法糖。如果 `Result` 是 `Ok`，则解包其值；如果是 `Err`，则从当前函数提早返回错误。
* **`panic!` 宏：** 导致程序立即崩溃。通常用于不可恢复的错误。

    ```rust
    fn main() {
        let v = vec![1, 2, 3];
        // v[99]; // 这会在运行时导致 panic
        panic!("Crash and burn!");
    }
    ```

* **`Option` 枚举：** 表示可能存在也可能不存在的值。

    ```rust
    enum Option<T> {
        Some(T),
        None,
    }
    ```

  * 用于避免空指针。
  * 使用 `unwrap()`, `unwrap_or()`, `map()`, `and_then()` 等方法来处理 `Option` 值。

    ```rust
    fn divide(a: i32, b: i32) -> Option<i32> {
        if b == 0 {
            None
        } else {
            Some(a / b)
        }
    }

    fn main() {
        let result1 = divide(10, 2);
        match result1 {
            Some(value) => println!("Result: {}", value),
            None => println!("Cannot divide by zero"),
        }

        let result2 = divide(5, 0);
        println!("Result 2: {:?}", result2.unwrap_or(-1)); // 如果为 None 则返回 -1
    }
    ```

**VIII. 闭包与迭代器**

* **闭包：** 可以捕获其周围环境变量的匿名函数。

    ```rust
    fn main() {
        let x = 4;
        let equal_to_x = |z| z == x; // 捕获了 x 的闭包

        println!("Is 5 equal to x? {}", equal_to_x(5));
    }
    ```

  * 闭包语法：`|参数| -> 返回类型 { 函数体 }`（返回类型通常可以推断）。
  * 闭包可以通过引用 (`&`)、可变引用 (`&mut`) 或通过值（移动所有权）来捕获变量。Rust 推断捕获方式。使用 `move` 关键字强制转移所有权。
* **迭代器：** 提供处理元素序列的方法。
  * 通过对向量、数组和哈希映射等集合调用 `iter()` 方法创建（用于不可变迭代），`iter_mut()` 用于可变迭代，`into_iter()` 用于消费集合并获取其元素的所有权。
  * 迭代器是惰性的；只有在显式消费时才会产生值。
  * 常见的迭代器适配器（转换迭代器的方法）：`map()`, `filter()`, `take()`, `skip()`, `zip()`, `enumerate()` 等。
  * 常见的迭代器消费者（产生最终值的方法）：`collect()`, `sum()`, `product()`, `fold()`, `any()`, `all()` 等。

    ```rust
    fn main() {
        let v1 = vec![1, 2, 3];

        let v1_iter = v1.iter(); // 创建 v1 的迭代器

        for val in v1_iter {
            println!("Got: {}", val);
        }

        let v2: Vec<_> = v1.iter().map(|x| x + 1).collect(); // 转换并收集
        println!("v2: {:?}", v2);

        let sum: i32 = v1.iter().sum(); // 消费迭代器以获得总和
        println!("Sum of v1: {}", sum);
    }
    ```

**IX. 智能指针**

智能指针是行为类似于指针但具有额外元数据和功能的数据结构。它们强制执行与常规引用不同的规则集。

* **`Box<T>`：** 最简单的智能指针。它在堆上分配内存并提供值的所有权。当 `Box` 离开作用域时，堆上的值将被丢弃。适用于：
  * 编译时大小未知的数据。
  * 转移大量数据的所有权。
  * 创建递归数据结构。
* **`Rc<T>`（引用计数）：** 使程序的多个部分能够对同一数据具有只读访问权限。只有当最后一个 `Rc` 指针离开作用域时，数据才会被清理。非线程安全。
* **`Arc<T>`（原子引用计数）：** 类似于 `Rc<T>`，但线程安全，可用于并发场景。与 `Rc<T>` 相比有一些性能开销。
* **`Cell<T>` 和 `RefCell<T>`（内部可变性）：** 允许在存在对数据的不可变引用时修改数据。这违反了 Rust 通常的借用规则，用于特定的、受控的情况。
  * `Cell<T>`：适用于 `Copy` 类型。允许设置和获取值。
  * `RefCell<T>`：适用于非 `Copy` 类型。提供运行时借用检查（如果在运行时违反借用规则则 panic）。
* **`Mutex<T>` 和 `RwLock<T>`（并发原语）：** 提供跨线程安全共享可变访问的机制。
  * `Mutex<T>`：一次只允许一个线程持有锁并访问数据。
  * `RwLock<T>`：允许多个读取者或一个写入者访问数据。

**X. 并发**

Rust 具有出色的内置并发支持。

* **线程：** 使用 `std::thread::spawn` 生成新的操作系统线程。

    ```rust
    use std::thread;
    use std::time::Duration;

    fn main() {
        let handle = thread::spawn(|| {
            for i in 1..10 {
                println!("hi number {} from the spawned thread!", i);
                thread::sleep(Duration::from_millis(1));
            }
        });

        for i in 1..5 {
            println!("hi number {} from the main thread!", i);
            thread::sleep(Duration::from_millis(1));
        }

        handle.join().unwrap(); // 等待生成的线程完成
    }
    ```

* **消息传递：** 使用通道（由 `std::sync::mpsc` 提供）在线程间发送数据。

    ```rust
    use std::sync::mpsc;
    use std::thread;
    use std::time::Duration;

    fn main() {
        let (tx, rx) = mpsc::channel();

        thread::spawn(move || {
            let val = String::from("hi");
            tx.send(val).unwrap();
            // println!("val is {}", val); // 错误：val 已被移动
        });

        let received = rx.recv().unwrap();
        println!("Got: {}", received);
    }
    ```

* **共享状态并发：** 使用像 `Mutex<T>` 和 `Arc<T>` 这样的智能指针，在多个线程之间实现安全的共享可变访问。

**XI. 宏**

宏是 Rust 中的一种元编程形式。它们允许你编写生成其他代码的代码。

* **声明宏 (`macro_rules!`)：** 匹配模式并将其替换为其他代码。对于减少样板代码非常强大。

    ```rust
    macro_rules! vec {
        ( $( $x:expr ),* ) => {
            {
                let mut temp_vec = Vec::new();
                $(
                    temp_vec.push($x);
                )*
                temp_vec
            }
        };
    }

    fn main() {
        let my_vec = vec![1, 2, 3, 4];
        println!("{:?}", my_vec);
    }
    ```

* **过程宏：** 比声明宏更强大和复杂。它们操作 Rust 代码的抽象语法树（AST）。有三种类型：
  * **类函数宏：** 看起来像函数调用。
  * **类属性宏：** 与 `#[...]` 语法一起使用。
  * **派生宏：** 与 `#[derive(...)]` 一起使用，用于自动实现 trait。

**XII. 测试**

Rust 内置了编写和运行测试的支持。

* **单元测试：** 测试代码的独立单元（函数、模块）。通常放置在与被测试代码相同的文件中，位于 `#[cfg(test)]` 模块内。

    ```rust
    pub fn add(left: usize, right: usize) -> usize {
        left + right
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn it_works() {
            let result = add(2, 2);
            assert_eq!(result, 4);
        }
    }
    ```

* **集成测试：** 测试库或二进制文件中不同部分如何协同工作。放置在项目顶层的单独 `tests` 目录中。
* **运行测试：** 使用 `cargo test` 命令。

**XIII. 不安全 Rust**

Rust 的安全性保证由编译器强制执行。然而，在某些情况下你可能需要绕过这些保证。这是通过使用 `unsafe` 关键字来完成的。

* **`unsafe` 块：** `unsafe` 块内的代码可以执行编译器无法保证安全的操作，例如：
  * 解引用裸指针 (`*const T`, `*mut T`)。
  * 调用 `unsafe` 函数或方法。
  * 访问 `union` 的字段。
  * 链接到外部（非 Rust）代码。
* **`unsafe` 函数：** 包含 `unsafe` 操作的函数本身被标记为 `unsafe`。调用 `unsafe` 函数需要在 `unsafe` 块内。
* **使用 `unsafe` 的原因：** 与 C 库交互、底层系统编程、在手动维护安全不变量的性能关键代码中。
* **重要提示：** `unsafe` 应谨慎且极少使用。你有责任确保 `unsafe` 块内的内存安全。

**XIV. Rust 生态系统**

* **Crate（包）：** 可在 Rust 项目中使用的库或可执行文件。可在 [https://crates.io/](https://crates.io/) 上找到。
* **流行的 Crate：**
  * `serde`：序列化与反序列化。
  * `tokio`, `async-std`：异步编程。
  * `actix-web`, `rocket`：Web 框架。
  * `diesel`, `sea-orm`：对象关系映射器 (ORM)。
  * `clap`, `structopt`：命令行参数解析。
  * `log`, `env_logger`：日志记录。
  * `rand`：随机数生成。
* **Rust 标准库 (`std`)：** 提供基本功能。

**XV. 学习资源**

* **《Rust 程序设计语言》书籍：** 官方且全面的指南 ([https://doc.rust-lang.org/book/](https://doc.rust-lang.org/book/))。
* **Rust by Example：** 一系列可运行的示例，说明各种 Rust 特性 ([https://doc.rust-lang.org/rust-by-example/](https://doc.rust-lang.org/rust-by-example/))。
* **Rustlings 课程：** 一套小练习，帮助你习惯阅读和编写 Rust 代码 ([https://github.com/rust-lang/rustlings](https://github.com/rust-lang/rustlings))。
* **Rust 文档：** 官方 API 文档 ([https://doc.rust-lang.org/std/](https://doc.rust-lang.org/std/))。
* **Rust 博客：** 官方公告和更新 ([https://blog.rust-lang.org/](https://blog.rust-lang.org/))。
* **Reddit (r/rust)、Discord 和其他社区平台。**

本指南为学习 Rust 提供了坚实的基础。要熟练掌握 Rust，最好的方法是练习编写 Rust 代码、探索生态系统并与社区互动。祝你在 Rust 之旅中好运！
