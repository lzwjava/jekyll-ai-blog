---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows上构建Warp
translated: true
type: note
---

是的，Warp **可以在 Windows 上编译**，使用 Visual Studio Build Tools。以下是分析：

== Windows 支持状态 ==

完全支持。Warp 具备：
- `crates/warpui/src/platform/windows/` 中的 Windows 平台代码
- Windows 特定依赖（windows crate、DirectX、Win32 API）
- 运行在 `windows-latest-large` 上的 CI 流水线
- Windows 引导脚本（`script/windows/bootstrap.ps1`）
- Inno Setup 安装程序脚本

== 必需依赖 ==

1. Visual Studio Build Tools 2022
   - MSVC 编译器和链接器
   - Windows SDK（22621 或更新版本）
   - 安装方式：
     winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override '--passive --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows11SDK.22621 --includeRecommended'

2. Rust（通过 rustup）
   - 目标：x86_64-pc-windows-msvc
   - 安装：https://rustup.rs

3. CMake
   - 用于构建 sentry-contrib-native
   - winget install -e --id Kitware.CMake

4. Git for Windows
   - winget install -e --id Git.Git

5. 其他工具（可选）
   - jq: winget install jqlang.jq
   - Inno Setup: winget install -e --id JRSoftware.InnoSetup

== 构建命令 ==

# 引导（安装所有依赖）
.\script\windows\bootstrap.ps1

# 构建
cargo build --bin warp-oss --features gui

# 运行
.\target\debug\warp-oss.exe

== GPU 后端 ==

Windows 使用：
- 通过 wgpu 使用 DX12（DirectX 12）
- Vulkan 作为替代
- 用于 DirectX 着色器的 DXC 着色器编译器

wgpu = { version = "29.0.1", features = ["dx12", "metal", "vulkan"] }

== Windows 特定代码 ==

- DirectX 着色器编译（DXCPath）
- Win32 API 调用（SetCurrentProcessExplicitAppUserModelID）
- Windows 注册表访问
- 崩溃处理 / 迷你转储程序

== 潜在问题 ==

1. 某些 crate 已从 Windows CI 测试中排除：
   --exclude command-signatures-v2 --exclude warp_js

2. 需要 Git LFS（引导脚本会检查）

3. 某些测试可能需要真实 GPU（WARPUI_USE_REAL_DISPLAY_IN_INTEGRATION_TESTS）

== 总结 ==

是的，你可以使用 Visual Studio Build Tools 在 Windows 上构建。该项目具有官方 Windows 支持，包括 CI、平台特定代码和安装脚本。首先运行引导脚本以完成所有设置。
