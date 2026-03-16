---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zig Comptime Essentials Guide
translated: false
type: note
---

**Question:** Comprehensive introduction to comptime in Zig?

**Answer:**

Here is a structured, comprehensive introduction to `comptime` in Zig (as of 2025–2026 language state)

### What does `comptime` actually mean?

`comptime` means **"guaranteed to run at compile time"**.

Code that is forced to be `comptime` must be fully evaluable when the compiler is running — no runtime values are allowed.

### Main places where `comptime` appears

| Keyword / Context        | Meaning                                                                 | Most common use case                                 |
|--------------------------|-------------------------------------------------------------------------|------------------------------------------------------|
| `comptime var` / `const` | Variable is known & computed at compile time                            | Compile-time constants, loop unrolling counters     |
| `comptime T`             | Type parameter is known at compile time                                 | Generic programming (very common)                    |
| `comptime expr`          | Expression must be compile-time evaluable                               | Metaprogramming, type-dependent logic                |
| `comptime { … }` block   | Entire block runs at compile time                                       | Complex compile-time computation / code generation   |
| `comptime_callable()`    | Function is forced to be compile-time callable                          | Helper functions used in comptime contexts           |
| `if (comptime cond)`     | Condition decided at compile time → dead code elimination              | Static if / conditional compilation                  |
| `@This()`, `@TypeOf()` etc | Many builtins are only allowed in comptime contexts                    | Reflection, building advanced data structures        |

### Most important mental model (2025–2026)

Zig has **two execution contexts**:

1. **comptime world** — runs during compilation, has access to types, can create new types, can run almost arbitrary code
2. **runtime world** — what ends up in the binary, only values, no types

You can move information **from runtime → comptime** very easily (implicitly or with `comptime` keyword).

You **cannot** move information **from comptime → runtime** unless you explicitly produce runtime instructions (arrays, structs, functions, inline assembly, etc.).

### Core examples — from simple to powerful

#### 1. Basic compile-time constant

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

#### 2. Most common pattern — comptime type parameter

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

#### 3. Static if — the replacement for C `#ifdef`

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

#### 4. Compile-time known size → better codegen

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

#### 5. Very powerful: type-dependent code generation

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

#### 6. Comptime-known lookup tables / perfect hashing

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

### Quick reference — most useful comptime builtins

- `@typeInfo(T)`
- `@typeName(T)`
- `@This()`
- `@TypeOf(expr)`
- `@embedFile("path")`
- `@shuffle(...)`, `@reduce(...)`, `@bitCast(...)`
- `@field(parent, field_name)`
- `@hasDecl(T, "name")`, `@hasField(T, "name")`
- `inline for`, `inline while`
- `comptime_int`, `comptime_float`

### Common pitfalls (2025 edition)

- Forgetting `comptime` on a function parameter that should be known → runtime function call instead of comptime type
- Using runtime-known value where comptime is required
- Creating very large comptime arrays → huge compile time & memory usage
- Recursive comptime functions without base case → compiler hangs
- `inline for` on runtime-known length → error

### Summary — how to think about comptime

- `comptime` = "do this now, while compiling"
- Use it to:
  - eliminate branches
  - generate specialised code
  - do reflection / introspection
  - create types on demand
  - build perfect lookup tables
  - move computation from runtime to compile time

Zig's `comptime` is one of the strongest compile-time metaprogramming systems in mainstream languages in 2025–2026 — more ergonomic than C++ templates, more powerful than Rust const generics (at least until generic associated types become very mature).

Happy hacking with comptime!

**References:**

- None (explanation based on Zig language semantics up to 0.13–0.14 era + common patterns in 2025/2026)