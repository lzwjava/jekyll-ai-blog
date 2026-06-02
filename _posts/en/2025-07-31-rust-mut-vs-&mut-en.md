---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust's `mut` and `&mut` Explained
translated: false
type: note
---

In Rust, the keywords `mut` and `&mut` serve related but distinct purposes, and they're not directly equivalent to Java's deep/shallow copy concepts or C's pointers—though there are some analogies we can draw for clarity. I'll break this down step by step, explain the differences, and address your questions about value passing vs. reference passing, mutability, and how changes affect the original data. I'll use examples based on your provided code to illustrate.

### 1. **Understanding `mut` in Variable Declarations**

- When you declare a variable with `let mut`, you're making the *binding* (the variable name) mutable. This means you can reassign the variable or modify its contents directly, but only within the scope where it's declared.
- Example from your code:

     ```rust
     let mut arr = [3, 6, 8, 10, 1, 2, 1];
     ```

     Here, `arr` is mutable, so you could do `arr[0] = 99;` or even reassign `arr = [1, 2, 3];` later if you wanted. Without `mut`, Rust would complain about trying to modify an immutable variable (Rust defaults to immutability for safety).
- This `mut` is about the variable itself, not about how it's passed to functions. It doesn't imply copying or referencing—it's just permission to change the variable in place.

### 2. **Understanding `&mut` in Function Parameters and References**

- `&mut` creates a *mutable reference* (also called a mutable borrow). This is like a pointer in C that allows reading *and* writing to the pointed-to data, but with Rust's strict borrow checker ensuring safety (no data races, no dangling pointers).
- In your code:

     ```rust
     fn quick_sort(arr: &mut [i32]) { ... }
     ```

  - The parameter `arr` is a mutable reference to a slice of `i32`s (`&mut [i32]`). Slices in Rust are views into arrays or vectors (like a pointer + length), and they're almost always passed as references because slices are "unsized" types (their size isn't known at compile time).
  - When you call `quick_sort(&mut arr);`, you're passing a mutable reference to the original `arr`. This allows the function to modify the elements of the original array through the reference (e.g., via swaps in `partition`).
  - Inside the function, operations like `arr.swap(i, j);` directly affect the original data because `arr` is a reference pointing back to it.
- Without the `&`, you couldn't pass a slice like `[i32]` directly as a parameter in this way—Rust requires references for unsized types. But more generally, `&mut` enables reference passing with mutation rights.

### 3. **Value Passing vs. Reference Passing in Rust**

- Rust uses *ownership* as its core model, which is different from Java (which is mostly reference-based with garbage collection) or C (manual pointers).
  - **Value passing (ownership transfer)**: When you pass a value without `&` (e.g., `fn foo(x: i32)` or `fn bar(mut v: Vec<i32>)`), ownership of the data moves to the function. The function can modify it locally, but changes don't affect the caller's original (because the caller no longer owns it). If the type implements `Copy` (like primitives such as `i32`), it's automatically copied instead of moved—no deep copy unless you explicitly clone.
    - Example:

         ```rust
         fn foo(mut x: i32) {
             x += 1;  // Modifies local x, but caller's original is unchanged (or moved/copied).
             println!("Inside: {}", x);
         }

         let y = 5;
         foo(y);  // Passes by value (copy, since i32 is Copy).
         println!("After: {}", y);  // Still 5.
         ```

    - This is like "value passing" in other languages: primitives are copied, larger types (like arrays/vectors) are moved (efficient, no copy unless cloned).
  - **Reference passing (borrowing)**: Using `&` (immutable reference) or `&mut` (mutable reference) "borrows" the data without transferring ownership. The function gets a temporary view (like a pointer), and the original owner retains control.
    - `&`: Read-only borrow. Can't modify the original.
    - `&mut`: Read-write borrow. *Can* modify the original, like passing by reference in C++ or a mutable pointer in C.
    - Example:

         ```rust
         fn bar(x: &mut i32) {
             *x += 1;  // Dereference and modify the original.
         }

         let mut y = 5;
         bar(&mut y);  // Pass mutable reference.
         println!("After: {}", y);  // Now 6, original changed.
         ```

    - In your quicksort code, it's reference passing with `&mut`, so swaps change the original array. If it were just `& [i32]`, you couldn't modify it (immutable borrow).

- To your point: Yes, `&mut` allows changing the original values (reference passing with mutation), while passing without `&` (value passing) either copies/moves the data, so modifications are local and don't affect the original. But:
  - Not all types copy automatically—only those implementing `Copy` (e.g., `i32`, not arrays or vectors). For non-`Copy` types like your array, passing by value would *move* ownership, and you'd need to return it to "give back" to the caller.
  - Rust avoids unnecessary copies for efficiency. Your array isn't copied when passed as `&mut [i32]`—it's just a reference (shallow, like a pointer).

### 4. **Comparison to Java and C**

- **Java**: Everything non-primitive is passed by reference (shallow—objects are shared, but reassigning the parameter doesn't affect the caller). Primitives are passed by value (copy). No direct equivalent to `mut` or `&mut`; mutability is controlled by class design (e.g., final fields). Java doesn't have Rust's ownership, so it's more prone to shared mutable state issues. Deep copy requires manual cloning.
- **C**: `&mut` is like passing a pointer (`int*`) where you can dereference and modify (`*ptr = 10;`). Plain `mut` (in declarations) is like non-const variables. But C has no borrow checker, so you manage lifetimes manually (error-prone). Passing by value in C copies the data (shallow for structs unless you deep-copy).
- Key difference: Rust enforces "one mutable reference at a time" (or multiple immutable ones), preventing bugs. No nulls, no wild pointers.

### 5. **Why `mut` Sometimes and `&mut` Sometimes in Your Code?**

- `mut` alone: Used for local variables that need to be changeable, like `let mut arr` (so you can pass `&mut arr` later or modify it directly).
- `&mut`: Used in parameters when the function needs to borrow and modify the caller's data without taking ownership. In `quick_sort` and `partition`, `&mut [i32]` lets them sort the array in place without moving/copying it.
- If you tried `fn quick_sort(mut arr: [i32])`, it wouldn't compile—slices can't be passed by value like that. You'd need a fixed-size array (e.g., `[i32; 7]`) and it would move ownership.
- In `partition`, the loop uses `mut i` internally—that's a local mutable variable, unrelated to passing.

### 6. **Does It Change Original Values?**

- Yes for `&mut`: Changes propagate to the original (reference passing).
- No for value passing (without `&`): Local changes only (unless you return the modified value).
- In your `quick_sort_interact()`, the `println!("After: {:?}", arr);` will show the sorted array because `&mut` was used.

If you run your code, it should output:

```
Before: [3, 6, 8, 10, 1, 2, 1]
After: [1, 1, 2, 3, 6, 8, 10]
```

(The `mod simple;` and `simple::run_simple();` seem unrelated—perhaps a placeholder? If there's an error there, it might be because `simple` isn't defined.)

If this doesn't clarify or you have a specific part of the code to tweak/test, let me know!
