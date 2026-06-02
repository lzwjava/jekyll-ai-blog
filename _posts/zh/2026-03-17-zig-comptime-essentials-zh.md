---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zig Comptime 基础指南
translated: true
type: note
---

**问题：** Zig 中 comptime 的全面介绍？

**回答：**

以下是 Zig 中 `comptime` 的结构化、全面介绍（基于 2025–2026 语言状态）

### `comptime` 究竟是什么意思？

`comptime` 表示 **“保证在编译时运行”**。

被强制为 `comptime` 的代码必须在编译器运行时完全可求值 — 不允许使用运行时值。

### `comptime` 出现的主要位置

| Keyword / Context        | Meaning                                                                 | Most common use case                                 |
|--------------------------|-------------------------------------------------------------------------|------------------------------------------------------|
| `comptime var` / `const` | 变量在编译时已知并计算                                                  | 编译时常量、循环展开计数器                           |
| `comptime T`             | 类型参数在编译时已知                                                    | 泛型编程（非常常见）                                 |
| `comptime expr`          | 表达式必须在编译时可求值                                                | 元编程、类型相关逻辑                                 |
| `comptime { … }` block   | 整个块在编译时运行                                                      | 复杂的编译时计算 / 代码生成                          |
| `comptime_callable()`    | 函数被强制为编译时可调用                                                | 在 comptime 上下文中使用的辅助函数                   |
| `if (comptime cond)`     | 条件在编译时决定 → 死代码消除                                           | 静态 if / 条件编译                                   |
| `@This()`、`@TypeOf()` 等 | 许多内置函数仅允许在 comptime 上下文中使用                              | 反射、构建高级数据结构                               |

### 最重要的心智模型（2025–2026）

Zig 有 **两个执行上下文**：

1. **comptime 世界** — 在编译期间运行，可访问类型、可创建新类型、几乎可运行任意代码
2. **运行时世界** — 最终进入二进制文件，仅有值、无类型

您可以很容易地将信息 **从运行时 → comptime** 移动（隐式或使用 `comptime` 关键字）。

您 **不能** 将信息 **从 comptime → 运行时** 移动，除非明确生成运行时指令（数组、结构体、函数、内联汇编等）。

### 核心示例 — 从简单到强大

#### 1. 基本的编译时常量

```zig
const fibonacci_40 = comptime fib(40);

fn fib(n: u32) u64 {
    if (n <= 1) return n;
    var a: u64 = 0;
    var b: u64 = 1;
    var i: u32 = 2;
    while (i <= n) : (i += 1) {
        const next = a + b;
        a = b;
        b = next;
    }
    return b;
}
```

#### 2. 最常见模式 — comptime 类型参数

```zig
fn ArrayList(comptime T: type) type {
    return struct {
        items: []T,
        capacity: usize,
        allocator: std.mem.Allocator,

        pub fn init(allocator: std.mem.Allocator) @This() { ... }
        pub fn append(self: *@This(), item: T) !void { ... }
    };
}

// usage
var list_u32   = ArrayList(u32).init(allocator);
var list_f32   = ArrayList(f32).init(allocator);
var list_Mat4  = ArrayList(Mat4).init(allocator);
```

#### 3. 静态 if — C `#ifdef` 的替代品

```zig
pub fn writeBytes(writer: anytype, data: []const u8) !void {
    if (comptime @TypeOf(writer) == std.fs.File.Writer) {
        // fast path: use writev / write_all directly
        try writer.writeAll(data);
    } else {
        // slow path: byte-by-byte fallback
        for (data) |b| try writer.writeByte(b);
    }
}
```

#### 4. 编译时已知大小 → 更好的代码生成

```zig
fn matMul(comptime n: comptime_int, a: [n][n]f32, b: [n][n]f32) [n][n]f32 {
    var result: [n][n]f32 = undefined;

    comptime var i = 0;
    inline while (i < n) : (i += 1) {
        comptime var j = 0;
        inline while (j < n) : (j += 1) {
            var sum: f32 = 0;
            comptime var k = 0;
            inline while (k < n) : (k += 1) {
                sum += a[i][k] * b[k][j];
            }
            result[i][j] = sum;
        }
    }
    return result;
}

// compiler sees fully unrolled 4×4, 8×8, etc. loops when n is known
```

#### 5. 非常强大：类型相关的代码生成

```zig
fn printFields(comptime T: type) void {
    inline for (@typeInfo(T).Struct.fields) |field| {
        std.debug.print("{s}: {s}\n", .{ field.name, @typeName(field.type) });
    }
}

const Person = struct {
    name: []const u8,
    age: u32,
    height_cm: f32,
};

test "print fields" {
    comptime printFields(Person);
    // prints (at compile time):
    // name: []const u8
    // age: u32
    // height_cm: f32
}
```

#### 6. 编译时已知的查找表 / 完美哈希

```zig
fn opcodeToMnemonic(comptime opcode: u8) []const u8 {
    const table = comptime buildOpcodeTable();

    return table[opcode];
}

fn buildOpcodeTable() [256][]const u8 {
    var t: [256][]const u8 = undefined;
    inline for (0..256) |i| {
        t[i] = comptime getMnemonicForOpcode(@intCast(i));
    }
    return t;
}
```

### 快速参考 — 最有用的 comptime 内置函数

- `@typeInfo(T)`
- `@typeName(T)`
- `@This()`
- `@TypeOf(expr)`
- `@embedFile("path")`
- `@shuffle(...)`、`@reduce(...)`、`@bitCast(...)`
- `@field(parent, field_name)`
- `@hasDecl(T, "name")`、`@hasField(T, "name")`
- `inline for`、`inline while`
- `comptime_int`、`comptime_float`

### 常见陷阱（2025 版）

- 忘记在应该已知的函数参数上使用 `comptime` → 变成运行时函数调用而不是 comptime 类型
- 在需要 comptime 的地方使用运行时已知值
- 创建非常大的 comptime 数组 → 巨大的编译时间和内存使用
- 没有基例的递归 comptime 函数 → 编译器挂起
- 在运行时已知长度上使用 `inline for` → 错误

### 总结 — 如何思考 comptime

- `comptime` = “现在就做，在编译时”
- 使用它来：
  - 消除分支
  - 生成专用代码
  - 进行反射 / 自省
  - 按需创建类型
  - 构建完美查找表
  - 将计算从运行时移到编译时

Zig 的 `comptime` 是 2025–2026 年主流语言中最强的编译时元编程系统之一 — 比 C++ 模板更易用，比 Rust const generics 更强大（至少在泛型关联类型非常成熟之前）。

使用 comptime 愉快编程！

**参考文献：**

- 无（解释基于 Zig 语言语义，直至 0.13–0.14 时代 + 2025/2026 常见模式）
