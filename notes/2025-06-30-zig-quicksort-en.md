---
audio: false
generated: true
lang: en
layout: post
title: Zig Quick Sort Implementation
translated: false
type: note
---

Here's the equivalent Quick Sort implementation in Zig.

```zig
const std = @import("std");

// Quick Sort function
fn quickSort(arr: []i32) void {
    if (arr.len <= 1) {
        return;
    }

    const pivot_index = partition(arr);

    // Split the array into left and right partitions
    // Note: Zig's slice splitting is slightly different from Rust's
    // We need to carefully handle the pivot element
    var left_slice = arr[0..pivot_index];
    var right_slice = arr[pivot_index + 1 .. arr.len]; // Exclude the pivot from the right slice

    quickSort(left_slice);
    quickSort(right_slice);
}

// Partition function
fn partition(arr: []i32) usize {
    const len = arr.len;
    // For simplicity, we'll use the last element as the pivot, similar to the Rust example.
    // In a production quicksort, you might choose a random pivot or median-of-three for better average case performance.
    const pivot = arr[len - 1];
    var i: usize = 0; // Index of the smaller element

    for (0..(len - 1)) |j| {
        if (arr[j] <= pivot) {
            std.mem.swap(i32, &arr[i], &arr[j]);
            i += 1;
        }
    }

    // Place the pivot at its correct position
    std.mem.swap(i32, &arr[i], &arr[len - 1]);

    return i;
}

pub fn main() !void {
    var arr = [_]i32{ 3, 6, 8, 10, 1, 2, 1 };

    // Create a mutable slice from the array for the quicksort function
    var slice: []i32 = &arr;

    std.debug.print("Before: {any}\n", .{slice});

    quickSort(slice);

    std.debug.print("After: {any}\n", .{slice});
}

```

### Explanation of Changes and Zig Concepts:

1.  **`const std = @import("std");`**: This line imports the Zig standard library, which provides useful utilities like `std.debug.print` for printing and `std.mem.swap` for swapping elements.
2.  **`fn quickSort(arr: []i32) void`**:
      * `fn` declares a function.
      * `arr: []i32` declares `arr` as a slice of `i32` (32-bit integers). In Zig, `[]T` denotes a mutable slice of type `T`. There's no separate `&mut` like in Rust; mutability is implied by whether the variable holding the slice is mutable.
      * `void` indicates that the function does not return a value.
3.  **`if (arr.len <= 1)`**: Conditional statements use parentheses around the condition.
4.  **`const pivot_index = partition(arr);`**: `const` is used for immutable variables.
5.  **Slice Splitting in Zig**:
      * `var left_slice = arr[0..pivot_index];`
      * `var right_slice = arr[pivot_index + 1 .. arr.len];`
      * Unlike Rust's `split_at_mut` which creates two mutable slices that don't overlap, Zig's slicing `arr[start..end]` creates new slices (views) into the original array.
      * Crucially, in the recursive calls, we *must* exclude the pivot from both the left and right sub-arrays, as the pivot is already in its final sorted position after `partition`. In the Rust code, `right[1..]` achieves this by effectively skipping the first element of the `right` slice, which is the pivot. We replicate this by using `pivot_index + 1` for the start of the `right_slice`.
6.  **`std.mem.swap(i32, &arr[i], &arr[j]);`**:
      * `std.mem.swap` is used for swapping elements.
      * The first argument (`i32`) is the type of the elements being swapped.
      * The subsequent arguments are pointers to the memory locations to be swapped (`&arr[i]` and `&arr[j]`).
7.  **`for (0..(len - 1)) |j| { ... }`**: This is a `for` loop that iterates from `0` up to (but not including) `len - 1`. The loop variable is captured as `j`.
8.  **`pub fn main() !void { ... }`**:
      * `pub` makes the `main` function publicly accessible.
      * `!void` indicates that the function can return an error, but in this case, we're not explicitly handling any. For simple programs, `void` is fine, but `!void` is often seen in Zig as it encourages robust error handling.
9.  **`var arr = [_]i32{ 3, 6, 8, 10, 1, 2, 1 };`**:
      * `[_]i32` declares a fixed-size array of `i32`. The `_` tells the compiler to infer the size from the initializer list.
10. **`var slice: []i32 = &arr;`**: We create a mutable slice (`[]i32`) from the fixed-size array `arr` because `quickSort` expects a slice.
11. **`std.debug.print("Before: {any}\n", .{slice});`**:
      * `std.debug.print` is Zig's equivalent of `println!` for debugging output.
      * `{any}` is a format specifier that tells Zig to print the value in a human-readable, debug-friendly format.
      * `.{slice}` is a "struct literal" (anonymous struct) used to pass the arguments to the format string.

To compile and run this Zig code:

1.  Save it as `quick_sort.zig`.
2.  Open your terminal in the same directory.
3.  Run: `zig run quick_sort.zig`
