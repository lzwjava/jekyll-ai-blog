---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Key Features Example
translated: false
type: note
---

Here's a simple Rust code example that demonstrates several key features, including borrowing, mutability, ownership, structs, enums, pattern matching, and more. I'll keep it concise yet illustrative, with comments explaining each feature.

```rust
// Define a struct to represent a Point
struct Point {
    x: i32,
    y: i32,
}

// Define an enum for different shapes
enum Shape {
    Circle(Point, f32), // Center point and radius
    Rectangle(Point, i32, i32), // Top-left point, width, height
}

// Implement methods for Point
impl Point {
    // Immutable borrow to calculate distance from origin
    fn distance_from_origin(&self) -> f32 {
        ((self.x.pow(2) + self.y.pow(2)) as f32).sqrt()
    }

    // Mutable borrow to translate point
    fn translate(&mut self, dx: i32, dy: i32) {
        self.x += dx;
        self.y += dy;
    }
}

// Function demonstrating ownership and borrowing
fn describe_shape(shape: &Shape) -> String {
    match shape {
        Shape::Circle(center, radius) => {
            // Immutable borrow of center
            format!(
                "Circle at ({}, {}) with radius {}",
                center.x, center.y, radius
            )
        }
        Shape::Rectangle(top_left, width, height) => {
            // Immutable borrow of top_left
            format!(
                "Rectangle at ({}, {}) with width {}, height {}",
                top_left.x, top_left.y, width, height
            )
        }
    }
}

fn main() {
    // Mutable variable binding
    let mut point = Point { x: 3, y: 4 };

    // Immutable borrow to call method
    println!("Distance from origin: {}", point.distance_from_origin());

    // Mutable borrow to modify point
    point.translate(2, 1);
    println!("After translation: ({}, {})", point.x, point.y);

    // Create a shape (ownership transferred to variable)
    let circle = Shape::Circle(point, 5.0);

    // Immutable borrow of shape to describe it
    println!("Shape: {}", describe_shape(&circle));

    // Vector with ownership of elements
    let mut shapes: Vec<Shape> = Vec::new();
    shapes.push(circle);
    shapes.push(Shape::Rectangle(Point { x: 0, y: 0 }, 10, 20));

    // Iterate with immutable borrow
    for shape in &shapes {
        println!("Shape in vec: {}", describe_shape(shape));
    }

    // Option and pattern matching
    let maybe_number: Option<i32> = Some(42);
    match maybe_number {
        Some(num) => println!("Got a number: {}", num),
        None => println!("No number"),
    }

    // Result for error handling
    let result: Result<i32, &str> = Ok(100);
    if let Ok(value) = result {
        println!("Result value: {}", value);
    }
}
```

### Key Features Demonstrated

1. **Structs**: `Point` struct to represent a 2D point.
2. **Enums**: `Shape` enum to represent different shapes (Circle, Rectangle).
3. **Ownership**: The `circle` variable takes ownership of `point` when created.
4. **Borrowing**:
   - Immutable borrow (`&self`) in `distance_from_origin`.
   - Mutable borrow (`&mut self`) in `translate`.
   - Immutable borrow (`&Shape`) in `describe_shape`.
5. **Mutability**: `mut` keyword for mutable variables (`point`, `shapes`).
6. **Pattern Matching**: Used with `match` in `describe_shape` and for `Option`.
7. **Methods**: Defined in `impl Point` block.
8. **Vectors**: `Vec<Shape>` to store a collection of shapes.
9. **Option**: Handling optional values with `Some` and `None`.
10. **Result**: Basic error handling with `Ok` and `Err`.
11. **String Formatting**: Using `format!` for dynamic strings.

### Output (when run)

```
Distance from origin: 5
After translation: (5, 5)
Shape: Circle at (5, 5) with radius 5
Shape in vec: Circle at (5, 5) with radius 5
Shape in vec: Rectangle at (0, 0) with width 10, height 20
Got a number: 42
Result value: 100
```

This code is concise but showcases Rust's core concepts like ownership, borrowing, and mutability, along with its type system and error handling. You can run it using `rustc` or a Rust project with `cargo run`. Let me know if you'd like a deeper dive into any specific feature!
