---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows上的Warp及从源码构建
translated: true
type: note
---

**问题：** Warp 终端是否支持 Windows？由于它使用 Rust 编写，能否通过 Rust + Visual Studio Build Tools 从源码编译？

**答案：**

## 是的，Warp 可以在 Windows 上运行——而且现在也可以从源码构建

### Windows 支持

Warp 于 2025 年 2 月登陆 Windows，支持 PowerShell、WSL 和 Git Bash，兼容 x64 和 ARM64 架构。核心体验在各平台几乎一致——完全用 Rust 编写并直接在 GPU 上渲染。

因此直接下载运行即可，无需特殊设置。

---

### 从源码构建

这是更有趣的部分。Warp 于 2026 年 4 月 30 日开源其客户端，在 GitHub 上以 AGPL 许可证发布源码。现在你真的可以自己构建了。

Warp UI 框架的 crate 使用 MIT 许可证，其余代码使用 AGPL v3。

仓库地址：**<https://github.com/warpdotdev/warp>**

---

### 能否用 Rust + Visual Studio Build Tools 编译？

**原则上可以**——这正是标准的 Windows Rust 工具链配置。

在 Windows 上，Rust 默认使用 MSVC 作为链接后端。标准配置如下：

```powershell
# 安装 Rust（Windows 上默认使用 MSVC 工具链）
winget install Rustlang.Rustup

# 如果缺少 VS Build Tools，Rustup 会提示安装
# 或手动安装：https://visualstudio.microsoft.com/visual-cpp-build-tools/
# 选择“使用 C++ 的桌面开发”工作负载

# 验证工具链
rustup show
# 应显示：stable-x86_64-pc-windows-msvc

# 克隆并构建
git clone https://github.com/warpdotdev/warp
cd warp
cargo build --release
```

**但是**——Warp 是一个 GPU 渲染的终端（使用自己的渲染栈，基于 `wgpu` 等）。在 Windows 上，它直接与 DirectX/图形驱动集成。Warp 自行处理所有图形调用，并需要与 Windows 图形驱动集成以及处理事件。因此构建可能依赖于 Rust + MSVC 之外的其他依赖项——比如 Windows SDK 头文件、可能还需要 `cmake` 以及图形 API 绑定。

**尝试前的实用建议：**

1. 查看仓库的 `CONTRIBUTING.md` 和 `WARP.md`——Warp 在 CONTRIBUTING.md 指南中记录了轻量级的贡献工作流。
2. 查看仓库中的 `.cargo/config.toml`，了解特定平台的链接器标志或目标覆盖。
3. 检查 `Cargo.toml` 中可能依赖本地库的依赖项（例如 `wgpu`、`winit`、`windows-rs`）。

`windows-rs` crate（微软官方的 Windows API Rust 绑定）可以很好地与 MSVC 工具链编译。`wgpu` 在 Windows 上默认使用 DirectX 12，也能用 VS Build Tools 干净地编译。因此整个栈是兼容的——问题只在于 Warp 文档中具体说明了哪些开发依赖项。

---

### 总结

| 问题 | 答案 |
|---|---|
| Warp 是否支持 Windows？ | 是的，自 2025 年 2 月起 |
| 源码是否可用？ | 是的，2026 年 4 月开源（AGPL） |
| 能否用 Rust + VS Build Tools 构建？ | 可以，这是正确的 Windows 工具链 |
| 有什么注意事项？ | GPU 渲染依赖项——请先查看 CONTRIBUTING.md |

**参考资料：**

- [Warp 登陆 Windows（2025 年 2 月）](https://www.warp.dev/blog/launching-warp-on-windows)
- [Warp 现已开源（2026 年 4 月）](https://www.warp.dev/blog/warp-is-now-open-source)
- [warpdotdev/warp 在 GitHub 上](https://github.com/warpdotdev/warp)
