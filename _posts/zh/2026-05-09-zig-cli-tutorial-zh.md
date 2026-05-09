---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建 Zig CLI 教程
translated: true
type: note
---

我们刚刚完成的简短演示：从零安装 Zig，到实现一个能打印 `Hello, world!` 和系统信息的 CLI，并推送到 GitHub。

## 1. 安装工具链

```sh
brew install zig
zig version   # 0.15.2
```

这会拉取 `llvm@20` 和 `lld@20` 作为依赖，占用约 200 MB 磁盘空间。

## 2. 脚手架项目

```sh
zig init
```

这会创建四个文件：

```
build.zig         # 构建脚本（基于 std.Build 的 DSL）
build.zig.zon     # 包清单（名称、版本、依赖）
src/main.zig      # 入口点
src/root.zig      # 库模块
```

`zig init` 假设你可能同时需要可执行文件和可复用库。对于单文件 CLI 不需要，所以我删除了 `src/root.zig` 并把 `build.zig` 精简到约 20 行——只保留可执行文件 + `run` 步骤。默认脚手架约 150 行，大部分是注释。

## 3. CLI

`src/main.zig` 中有两个值得注意的地方：

**Zig 0.15 的新 writer API。** 旧的 `std.io.getStdOut().writer()` 已移除。新模式更显式：你提供缓冲区，获取 `File.Writer`，然后拿到它的 `interface`：

```zig
var stdout_buffer: [4096]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
const out = &stdout_writer.interface;

try out.print("Hello, world!\n", .{});
// ...
try out.flush();   // 别忘了这个
```

缓冲区分配在栈上，大小由你决定。你还必须自己调用 `flush()`——缓冲 IO 不再隐藏在多态 writer 后面。

**系统信息的来源。** 根据信息类型不同，有三个来源：

| 信息             | 来源                                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| 操作系统、架构、Zig 版本 | `@import("builtin")` —— 编译期常量，嵌入二进制                         |
| 主机名、内核     | `std.posix.uname()` —— POSIX 系统调用                                  |
| CPU 数量         | `std.Thread.getCpuCount()`                                             |
| 用户、Shell      | `std.process.getEnvVarOwned(allocator, "USER")` —— 环境变量，需分配内存 |
| 当前工作目录     | `std.posix.getcwd(&buf)` —— 填充栈缓冲区                               |
| 时间             | `std.time.timestamp()`                                                 |

`builtin` 很有趣：`builtin.os.tag` 和 `builtin.cpu.arch` 是*编译期*枚举，因此 `@tagName()` 能零运行时开销地给出字符串。构建目标就是答案。

`uname` 返回固定长度的以 null 结尾的数组（约 `[65]u8`）。要将其作为 Zig 切片打印，需要用 `std.mem.sliceTo(&uts.nodename, 0)` 找到 null 终止符。

`getEnvVarOwned` 返回的是错误联合而非可选值——`USER` 可能确实未设置。惯用处理方式：

```zig
if (std.process.getEnvVarOwned(allocator, "USER")) |u| {
    defer allocator.free(u);
    try out.print("User: {s}\n", .{u});
} else |_| {
    try out.print("User: (unknown)\n", .{});
}
```

`|u|` / `else |_|` 分支在一个表达式中处理成功和错误。成功分支拥有分配的内存，必须释放。

## 4. 构建和运行

```sh
zig build run        # 构建 + 运行
zig build            # 构建 → ./zig-out/bin/ii
```

输出：

```
Hello, world!

== System Info ==
OS:           macos
Architecture: aarch64
Zig version:  0.15.2
Hostname:     lzw-mac.local
Kernel:       Darwin 25.4.0
CPU cores:    8
Working dir:  /Users/lzwjava/projects/ii
User:         lzwjava
Shell:        /bin/zsh
Unix time:    1778318750
```

## 5. Git

```sh
git init
echo -e ".zig-cache/\nzig-out/" > .gitignore
git add .gitignore build.zig build.zig.zon src/main.zig
git commit -m "Initial commit: Zig CLI printing hello world and system info"
git remote add origin git@github.com:lzwjava/ii.git
git push -u origin main
```

`.zig-cache/` 和 `zig-out/` 是需要忽略的两个目录——分别是增量缓存和安装前缀。

## 要点

- `zig init` 提供了丰富的脚手架，但需要精简。
- 0.15 的 IO 重写更啰嗦但也更诚实——你看到缓冲区，并需要调用 `flush`。
- Unix 上的大部分“系统信息”要么是编译期 `builtin`，要么是 POSIX 系统调用（`uname`、`getcwd`），要么是环境变量。
- 总源码：约 50 行 Zig 代码 + 一个 20 行的构建脚本。

仓库：`git@github.com:lzwjava/ii.git`