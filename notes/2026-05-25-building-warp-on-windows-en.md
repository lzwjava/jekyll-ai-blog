---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Warp on Windows
translated: false
type: note
---

Yes, Warp **can be compiled on Windows** with Visual Studio Build Tools. Here's the analysis:

== Windows Support Status ==

FULLY SUPPORTED. Warp has:

- Windows platform code in `crates/warpui/src/platform/windows/`
- Windows-specific dependencies (windows crate, DirectX, Win32 APIs)
- CI pipeline running on `windows-latest-large`
- Bootstrap script for Windows (`script/windows/bootstrap.ps1`)
- Inno Setup installer script

== Required Dependencies ==

1. Visual Studio Build Tools 2022
   - MSVC compiler + linker
   - Windows SDK (22621 or later)
   - Install via:
     winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override '--passive --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows11SDK.22621 --includeRecommended'

2. Rust (via rustup)
   - Target: x86_64-pc-windows-msvc
   - Install: <https://rustup.rs>

3. CMake
   - Needed for building sentry-contrib-native
   - winget install -e --id Kitware.CMake

4. Git for Windows
   - winget install -e --id Git.Git

5. Additional tools (optional)
   - jq: winget install jqlang.jq
   - Inno Setup: winget install -e --id JRSoftware.InnoSetup

== Build Commands ==

# Bootstrap (installs all deps)

.\script\windows\bootstrap.ps1

# Build

cargo build --bin warp-oss --features gui

# Run

.\target\debug\warp-oss.exe

== GPU Backend ==

Windows uses:

- DX12 (DirectX 12) via wgpu
- Vulkan as alternative
- DXC shader compiler for DirectX shaders

wgpu = { version = "29.0.1", features = ["dx12", "metal", "vulkan"] }

== Windows-Specific Code ==

- DirectX shader compilation (DXCPath)
- Win32 API calls (SetCurrentProcessExplicitAppUserModelID)
- Windows registry access
- Crash handler / minidumper

== Potential Issues ==

1. Some crates excluded from Windows CI tests:
   --exclude command-signatures-v2 --exclude warp_js

2. Git LFS required (bootstrap checks for it)

3. Some tests may need real GPU (WARPUI_USE_REAL_DISPLAY_IN_INTEGRATION_TESTS)

== Summary ==

Yes, you can build on Windows with Visual Studio Build Tools. The project has official Windows support with CI, platform-specific code, and installer scripts. Run the bootstrap script first to set up everything.
