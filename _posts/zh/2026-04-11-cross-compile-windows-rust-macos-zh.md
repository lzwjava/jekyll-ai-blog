---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在macOS上交叉编译Windows Rust程序
translated: true
type: note
---

## 在macOS上交叉编译仅限Windows的Rust项目：来自WeFriends的经验

最近我发现了[WeFriends](https://github.com/StrayMeteor3337/WeFriends)——一个用Rust编写的开源微信好友检测工具。它使用`egui`构建GUI，并通过DLL注入Windows版微信桌面客户端来检测哪些好友已删除或拉黑你。这个项目很有趣——但它是专门为Windows构建的。我想看看能否至少让它在macOS上完成编译。

### 首次构建尝试

运行`cargo build`立即遇到了障碍：

```
error[E0433]: failed to resolve: could not find `windows` in `os`
 --> src/wechat_manager.rs:1:14
  |
1 | use std::os::windows::process::CommandExt;
  |              ^^^^^^^ could not find `windows` in `os`
```

这很合理——在macOS上根本不存在`std::os::windows`这个模块。该模块由`rustc`根据条件编译，仅在针对Windows目标时可用。

### 根本问题

代码库中的Windows专用代码分散在多个层面：

1. **无条件Windows导入**——`std::os::windows::process::CommandExt`、`std::process::Command`（仅在Windows代码块中使用）、用于DLL加载的`libloading`类型
2. **构建脚本**——`build.rs`无条件使用了`extern crate winres`，这在非Windows系统上无法解析
3. **Cargo.toml**——`winres`和`winapi`被列为普通的`[build-dependencies]`，导致在所有平台都被下载和编译

有趣的是，原作者*确实*在函数体内使用了`#[cfg(target_os = "windows")]`（例如`kill_wechat`、`start_wechat`），但忘记在文件顶部对**导入语句**和**类型别名**进行条件控制。

### 解决方案

**1. 使用`#[cfg]`控制Windows专用导入**

```rust
// 修改前
use std::os::windows::process::CommandExt;
use std::process::{Command, Stdio};
use libloading::{Library, Symbol};
use rand::Rng;

// 修改后
#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;
#[cfg(target_os = "windows")]
use std::process::{Command, Stdio};
#[cfg(target_os = "windows")]
use libloading::{Library, Symbol};
#[cfg(target_os = "windows")]
use rand::Rng;
```

关键点：仅在`#[cfg(target_os = "windows")]`代码块内使用的导入语句本身也必须受条件控制。Rust的未使用导入警告通常能发现这个问题，但由于代码从未在非Windows平台编译，所以无人察觉。

像`std::time::Duration`和`tokio::time`这样的导入被跨平台代码使用（`install_wechat`使用了`tokio::time::sleep`），因此保持无条件导入。

**2. 为公开函数添加非Windows存根实现**

`login_wechat`和`unhook_wechat`等函数在`main.rs`中被无条件调用。与其在每个调用点包装`#[cfg]`，不如添加存根实现：

```rust
#[cfg(not(target_os = "windows"))]
pub async fn login_wechat() -> Result<u16> {
    Err(anyhow::anyhow!("仅支持Windows系统"))
}

#[cfg(target_os = "windows")]
pub async fn login_wechat() -> Result<u16> {
    // ... 实际实现
}
```

这保持了所有平台上公开API的一致性。GUI可以在任何地方编译运行；只是尝试执行Windows特定功能时会返回错误。

**3. 使构建依赖平台特定化**

```toml
# 修改前
[build-dependencies]
winres = "0.1"
winapi = { version = "0.3", features = ["winnt"] }

# 修改后
[target.'cfg(target_os = "windows")'.build-dependencies]
winres = "0.1"
winapi = { version = "0.3", features = ["winnt"] }
```

并在`build.rs`中包装整个主体：

```rust
fn main() {
    #[cfg(target_os = "windows")]
    {
        let mut res = winres::WindowsResource::new();
        res.set_manifest_file("app.manifest");
        // ...
        res.compile().unwrap();
    }
}
```

### 结果

经过这些修改，`cargo build`在macOS上成功运行，仅有一些警告（已弃用的`rand`方法、注释代码块中未使用的变量）。

### 它真的能在macOS上运行吗？

**不能**——至少在功能上不行。GUI可以启动，但每个核心功能都依赖于：

- **DLL注入**（`wxdriver64.dll`）——仅限Windows的机制
- **进程命令**（`taskkill`、`tasklist`）——Windows命令行工具
- **文件路径**（`%LocalAppData%\Tencent\WeChat`）——Windows目录结构
- **进程创建标志**（`.creation_flags()`）——Windows API

这个应用本质上是一个Windows工具。让它跨平台编译对开发很有用（IDE支持、CI检查、库兼容性测试），但运行时行为从设计上就是仅限Windows的。

### 经验总结

1. **控制导入语句，而不仅仅是函数体。** 如果函数内的代码受`#[cfg]`控制，那么它使用的类型很可能需要在导入层面进行同样的条件控制。

2. **在Cargo.toml中使用平台特定的依赖表。** `[target.'cfg(target_os = "windows")'.dependencies]`可以防止在其他平台拉取和编译Windows专用的crate。

3. **为公开API提供存根实现。** 如果你的库公开了仅在一个平台可用的函数，返回`Err("unsupported")`的存根实现比缺失符号更好。这让下游代码可以在任何地方编译，同时在运行时优雅地失败。

4. **`#[cfg]`具有传染性。** 一旦某个元素被条件控制，所有依赖它的元素也需要被控制——或者你需要提供替代路径。在模块层面规划cfg边界，而不是逐行添加。