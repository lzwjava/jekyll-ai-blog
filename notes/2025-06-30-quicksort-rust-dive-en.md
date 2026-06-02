---
audio: false
generated: true
lang: en
layout: post
title: Quicksort in Rust for Experienced Devs
translated: false
type: note
---

Alright, given your strong background in algorithms, full-stack development, and even mobile engineering, you'll find Rust's approach to memory safety and explicit control quite familiar in concept, even if the syntax and strictness are new. Let's break down this Quicksort implementation in Rust.

-----

### Quicksort in Rust: A Dive for Experienced Devs

This Rust code implements the classic **Quicksort algorithm**. The core idea of Quicksort is to pick an element as a pivot and partition the array around it, such that elements smaller than the pivot are on one side, and elements greater are on the other. This process is then recursively applied to the sub-arrays.

Let's go through the functions:

-----

### `fn quick_sort(arr: &mut [i32])`

```rust
fn quick_sort(arr: &mut [i32]) {
    if arr.len() <= 1 {
        return;
    }
    let pivot_index = partition(arr);
    let (left, right) = arr.split_at_mut(pivot_index);
    quick_sort(left);
    quick_sort(&mut right[1..]);
}
```

* **`arr: &mut [i32]`**: This is where Rust's type system immediately shows its colors.
  * `&mut` signifies a **mutable reference**. This means the `quick_sort` function gets a borrowed reference to the array `arr`, and it's allowed to modify the contents of that array *in place*.
  * `[i32]` is a **slice** of `i32` integers. In Rust, `[T]` is the type for a slice, which is a view into a contiguous sequence of elements. It doesn't own the data; it just points to a portion of an array or `Vec`. This is crucial for efficiency, as it avoids copying data around. You're familiar with pointers and array sections from your C/C++/Java background; think of this as Rust's safe and explicit way to manage that.
* **Base Case `if arr.len() <= 1`**: Standard recursive base case for Quicksort. If the slice has 0 or 1 element, it's already sorted, so just return.
* **`let pivot_index = partition(arr);`**: This calls the `partition` function (which we'll look at next) to rearrange the slice. It returns the final position of the pivot element.
* **`let (left, right) = arr.split_at_mut(pivot_index);`**: This is a key Rust feature for safe mutable aliasing.
  * `split_at_mut` is a method on mutable slices. It takes an index and splits the mutable slice into two *disjoint* mutable slices.
  * `left` will be `arr[0..pivot_index]` and `right` will be `arr[pivot_index..len]`.
  * This is fundamental to Rust's **borrow checker**. You cannot have two mutable references to the *same data* at the same time. `split_at_mut` ensures that `left` and `right` refer to completely separate parts of the original array, satisfying the borrow checker and preventing data races in a multi-threaded context (even though this is single-threaded, the principle applies).
* **`quick_sort(left);`**: Recursively sort the `left` sub-slice.
* **`quick_sort(&mut right[1..]);`**: Recursively sort the `right` sub-slice.
  * `right[1..]` is important: The `right` slice starts at `pivot_index`. Since `arr[pivot_index]` is now the correctly positioned pivot element, we exclude it from the recursive call on the right side.
  * `&mut` explicitly re-borrows a mutable slice from `right`.

-----

### `fn partition(arr: &mut [i32]) -> usize`

```rust
fn partition(arr: &mut [i32]) -> usize {
    let len = arr.len();
    let pivot = arr[len - 1];
    let mut i = 0;
    for j in 0..len - 1 {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, len - 1);
    i
}
```

This function implements the Lomuto partition scheme, which is a common way to partition an array for Quicksort.

* **`let len = arr.len();`**: Gets the length of the current slice.
* **`let pivot = arr[len - 1];`**: The **last element** of the slice is chosen as the pivot.
* **`let mut i = 0;`**: `i` acts as a pointer to the "boundary" between elements smaller than or equal to the pivot and elements greater than the pivot. Elements to the left of `i` will be less than or equal to the pivot.
* **`for j in 0..len - 1`**: This loop iterates through all elements *except* the pivot (which is at `len - 1`).
* **`if arr[j] <= pivot { ... }`**: If the current element `arr[j]` is less than or equal to the pivot:
  * **`arr.swap(i, j);`**: Swap `arr[j]` with `arr[i]`. This moves the smaller element into the "less than or equal" section.
  * **`i += 1;`**: Increment `i` to extend the "less than or equal" section.
* **`arr.swap(i, len - 1);`**: After the loop, `i` is the correct position for the pivot. We swap the pivot (which is still at `len - 1`) into its final sorted position. Now, all elements to the left of `i` are less than or equal to `arr[i]` (the pivot), and all elements to the right are greater.
* **`i`**: The function returns `i`, which is the final index of the pivot element.

-----

### `fn main()`

```rust
fn main() {
    let mut arr = [3, 6, 8, 10, 1, 2, 1];
    println!("Before: {:?}", arr);
    quick_sort(&mut arr);
    println!("After: {:?}", arr);
}
```

* **`let mut arr = [3, 6, 8, 10, 1, 2, 1];`**:
  * `let mut` declares a **mutable variable**. This allows you to reassign the variable or modify its contents (if it's a mutable type).
  * `[3, ...]` creates a **fixed-size array** on the stack. Its size is known at compile time.
* **`println!("Before: {:?}", arr);`**: Uses the `println!` macro for output.
  * `{:?}` is the **debug print** format specifier. It uses the `Debug` trait to print a human-readable representation of the array.
* **`quick_sort(&mut arr);`**: Calls the `quick_sort` function, passing a mutable reference to the `arr` array.
* **`println!("After: {:?}", arr);`**: Prints the array again after sorting.

-----

### Rust-Specific Takeaways for You

* **Ownership and Borrowing**: This code is a prime example of Rust's core concepts. You're passing around **references (`&` and `&mut`)** rather than copying data. The `&mut` references are critical for modifying the array in place, and the **borrow checker** (e.g., enforced by `split_at_mut`) ensures you never have multiple mutable references to the same data, eliminating a whole class of concurrency bugs at compile time. This is likely the biggest paradigm shift from languages like Java or Python, but it offers memory safety without a garbage collector.
* **Slices `[T]`**: These are incredibly powerful for working with contiguous data. They provide a safe, efficient view into parts of arrays or vectors without allocating new memory.
* **Macros (`println!`)**: You'll see `!` after many standard library functions (like `println!`, `vec!`, `format!`). These indicate that they are **macros**, not regular functions. Macros expand code at compile time, offering more flexibility and power (like variadic arguments or compile-time code generation) compared to regular functions.

Given your background, you'll likely appreciate the performance characteristics and safety guarantees that Rust offers, even if the "borrow checker dance" takes a bit of getting used to. It's a different way of thinking about memory management, but one that leads to highly robust and efficient code.
