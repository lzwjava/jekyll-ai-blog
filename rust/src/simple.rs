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

pub fn run_simple() {
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
