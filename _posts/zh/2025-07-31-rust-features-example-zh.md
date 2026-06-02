---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust核心特性示例
translated: true
type: note
---

以下是一个简单的 Rust 代码示例，展示了包括借用、可变性、所有权、结构体、枚举、模式匹配等关键特性。我将保持简洁但具有说明性，并通过注释解释每个特性。

```rust
// 定义表示点的结构体
struct Point {
    x: i32,
    y: i32,
}

// 为不同形状定义枚举
enum Shape {
    Circle(Point, f32), // 中心点和半径
    Rectangle(Point, i32, i32), // 左上角点、宽度、高度
}

// 为 Point 实现方法
impl Point {
    // 不可变借用计算到原点的距离
    fn distance_from_origin(&self) -> f32 {
        ((self.x.pow(2) + self.y.pow(2)) as f32).sqrt()
    }

    // 可变借用来平移点
    fn translate(&mut self, dx: i32, dy: i32) {
        self.x += dx;
        self.y += dy;
    }
}

// 演示所有权和借用的函数
fn describe_shape(shape: &Shape) -> String {
    match shape {
        Shape::Circle(center, radius) => {
            // 对 center 的不可变借用
            format!(
                "位于 ({}, {}) 半径为 {} 的圆形",
                center.x, center.y, radius
            )
        }
        Shape::Rectangle(top_left, width, height) => {
            // 对 top_left 的不可变借用
            format!(
                "位于 ({}, {}) 宽度为 {} 高度为 {} 的矩形",
                top_left.x, top_left.y, width, height
            )
        }
    }
}

fn main() {
    // 可变变量绑定
    let mut point = Point { x: 3, y: 4 };

    // 不可变借用来调用方法
    println!("到原点的距离: {}", point.distance_from_origin());

    // 可变借用来修改点
    point.translate(2, 1);
    println!("平移后坐标: ({}, {})", point.x, point.y);

    // 创建形状（所有权转移给变量）
    let circle = Shape::Circle(point, 5.0);

    // 对形状的不可变借用来描述它
    println!("形状: {}", describe_shape(&circle));

    // 拥有元素所有权的向量
    let mut shapes: Vec<Shape> = Vec::new();
    shapes.push(circle);
    shapes.push(Shape::Rectangle(Point { x: 0, y: 0 }, 10, 20));

    // 使用不可变借用迭代
    for shape in &shapes {
        println!("向量中的形状: {}", describe_shape(shape));
    }

    // Option 和模式匹配
    let maybe_number: Option<i32> = Some(42);
    match maybe_number {
        Some(num) => println!("获得数字: {}", num),
        None => println!("没有数字"),
    }

    // 用于错误处理的 Result
    let result: Result<i32, &str> = Ok(100);
    if let Ok(value) = result {
        println!("Result 值: {}", value);
    }
}
```

### 演示的关键特性：
1. **结构体**：表示二维点的 `Point` 结构体
2. **枚举**：表示不同形状的 `Shape` 枚举（圆形、矩形）
3. **所有权**：创建 `circle` 变量时获取了 `point` 的所有权
4. **借用**：
   - `distance_from_origin` 中的不可变借用（`&self`）
   - `translate` 中的可变借用（`&mut self`）
   - `describe_shape` 中对 `Shape` 的不可变借用
5. **可变性**：用于可变变量的 `mut` 关键字（`point`、`shapes`）
6. **模式匹配**：在 `describe_shape` 和 `Option` 处理中使用 `match`
7. **方法**：在 `impl Point` 块中定义的方法
8. **向量**：用于存储形状集合的 `Vec<Shape>`
9. **Option**：使用 `Some` 和 `None` 处理可选值
10. **Result**：使用 `Ok` 和 `Err` 的基本错误处理
11. **字符串格式化**：使用 `format!` 创建动态字符串

### 输出（运行时）：
```
到原点的距离: 5
平移后坐标: (5, 5)
形状: 位于 (5, 5) 半径为 5 的圆形
向量中的形状: 位于 (5, 5) 半径为 5 的圆形
向量中的形状: 位于 (0, 0) 宽度为 10 高度为 20 的矩形
获得数字: 42
Result 值: 100
```

这段代码简洁但展示了 Rust 的核心概念，如所有权、借用和可变性，以及其类型系统和错误处理。您可以使用 `rustc` 或带有 `cargo run` 的 Rust 项目来运行它。如果您想深入了解任何特定功能，请告诉我！
