---
audio: false
generated: true
lang: zh
layout: post
title: Zig快速排序实现
translated: true
type: note
---

以下是 Zig 中的等效快速排序实现。

```zig
const std = @import("std");

// 快速排序函数
fn quickSort(arr: []i32) void {
    if (arr.len <= 1) {
        return;
    }

    const pivot_index = partition(arr);

    // 将数组分割为左右分区
    // 注意：Zig 的切片分割方式与 Rust 略有不同
    // 我们需要小心处理基准元素
    var left_slice = arr[0..pivot_index];
    var right_slice = arr[pivot_index + 1 .. arr.len]; // 从右切片中排除基准元素

    quickSort(left_slice);
    quickSort(right_slice);
}

// 分区函数
fn partition(arr: []i32) usize {
    const len = arr.len;
    // 为简化起见，我们将使用最后一个元素作为基准，类似于 Rust 示例。
    // 在生产环境的快速排序中，您可能会选择随机基准或三数取中以获得更好的平均性能。
    const pivot = arr[len - 1];
    var i: usize = 0; // 较小元素的索引

    for (0..(len - 1)) |j| {
        if (arr[j] <= pivot) {
            std.mem.swap(i32, &arr[i], &arr[j]);
            i += 1;
        }
    }

    // 将基准放置到正确位置
    std.mem.swap(i32, &arr[i], &arr[len - 1]);

    return i;
}

pub fn main() !void {
    var arr = [_]i32{ 3, 6, 8, 10, 1, 2, 1 };

    // 从数组创建可变切片以供快速排序函数使用
    var slice: []i32 = &arr;

    std.debug.print("排序前: {any}\n", .{slice});

    quickSort(slice);

    std.debug.print("排序后: {any}\n", .{slice});
}

```

### 变更说明与 Zig 概念解析

1. **`const std = @import("std");`**：此行导入 Zig 标准库，提供诸如 `std.debug.print`（用于打印）和 `std.mem.swap`（用于交换元素）等实用工具。
2. **`fn quickSort(arr: []i32) void`**：
      * `fn` 声明一个函数。
      * `arr: []i32` 将 `arr` 声明为 `i32`（32 位整数）的可变切片。在 Zig 中，`[]T` 表示类型 `T` 的可变切片。没有像 Rust 中那样的单独 `&mut`；可变性由持有切片的变量是否为可变来隐含表示。
      * `void` 表示该函数不返回值。
3. **`if (arr.len <= 1)`**：条件语句在条件周围使用括号。
4. **`const pivot_index = partition(arr);`**：`const` 用于不可变变量。
5. **Zig 中的切片分割**：
      * `var left_slice = arr[0..pivot_index];`
      * `var right_slice = arr[pivot_index + 1 .. arr.len];`
      * 与 Rust 的 `split_at_mut`（创建两个不重叠的可变切片）不同，Zig 的切片操作 `arr[start..end]` 会创建指向原始数组的新切片（视图）。
      * 关键之处在于，在递归调用中，我们*必须*将基准元素从左右子数组中排除，因为在 `partition` 之后，基准元素已经处于其最终的排序位置。在 Rust 代码中，`right[1..]` 通过有效跳过 `right` 切片的第一个元素（即基准元素）来实现这一点。我们通过使用 `pivot_index + 1` 作为 `right_slice` 的起始索引来复现此行为。
6. **`std.mem.swap(i32, &arr[i], &arr[j]);`**：
      * `std.mem.swap` 用于交换元素。
      * 第一个参数（`i32`）是要交换元素的类型。
      * 后续参数是指向要交换的内存位置的指针（`&arr[i]` 和 `&arr[j]`）。
7. **`for (0..(len - 1)) |j| { ... }`**：这是一个 `for` 循环，从 `0` 迭代到（但不包括）`len - 1`。循环变量被捕获为 `j`。
8. **`pub fn main() !void { ... }`**：
      * `pub` 使 `main` 函数可公开访问。
      * `!void` 表示该函数可以返回错误，但在本例中，我们并未显式处理任何错误。对于简单程序，`void` 即可，但在 Zig 中经常看到 `!void`，因为它鼓励健壮的错误处理。
9. **`var arr = [_]i32{ 3, 6, 8, 10, 1, 2, 1 };`**：
      * `[_]i32` 声明一个固定大小的 `i32` 数组。`_` 告诉编译器根据初始化列表推断大小。
10. **`var slice: []i32 = &arr;`**：我们从固定大小数组 `arr` 创建一个可变切片（`[]i32`），因为 `quickSort` 期望一个切片。
11. **`std.debug.print("排序前: {any}\n", .{slice});`**：
      * `std.debug.print` 是 Zig 中用于调试输出的、相当于 `println!` 的函数。
      * `{any}` 是一个格式说明符，告诉 Zig 以人类可读的、调试友好的格式打印值。
      * `.{slice}` 是一个"结构体字面量"（匿名结构体），用于将参数传递给格式字符串。

要编译并运行此 Zig 代码：

1. 将其保存为 `quick_sort.zig`。
2. 在相同目录下打开终端。
3. 运行：`zig run quick_sort.zig`
