---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: MinGW-w64 包含的可执行文件
translated: true
type: note
---

### MinGW-w64 包含的可执行文件

MinGW-w64 主要是一个用于交叉编译原生 Windows 应用程序的最小化工具链，使用 GCC 及相关工具。它侧重于开发实用程序，而非完整的类 Unix 命令套件（例如，默认情况下它**不**包含 `gpg` 或 GnuPG——这些在 MSYS2 等环境中可作为独立软件包获取）。核心安装的 `bin` 目录通常包含以下可执行文件（基于标准的独立下载，例如来自官方 SourceForge 版本）。此列表可能因版本和构建略有不同，但以下是常见的可执行文件：

| 可执行文件 | 描述 |
| ------------ | ------------- |
| `gcc.exe` | GNU C 编译器 |
| `g++.exe` | GNU C++ 编译器 |
| `cpp.exe` | C 预处理器 |
| `gfortran.exe` | GNU Fortran 编译器（如果构建中包含） |
| `ld.exe` | GNU 链接器 |
| `as.exe` | GNU 汇编器 |
| `ar.exe` | 用于创建库的归档器 |
| `ranlib.exe` | 为归档库生成索引 |
| `nm.exe` | 列出目标文件中的符号 |
| `objdump.exe` | 显示目标文件信息 |
| `objcopy.exe` | 复制和转换目标文件 |
| `strip.exe` | 从可执行文件中剥离符号 |
| `size.exe` | 列出目标文件的段大小 |
| `strings.exe` | 打印文件中的可打印字符串 |
| `readelf.exe` | 显示 ELF 文件信息（用于交叉工具） |
| `dlltool.exe` | 创建 DLL 导入/导出文件 |
| `windres.exe` | 编译 Windows 资源文件 |
| `gendef.exe` | 从 DLL 生成 .def 文件 |
| `genidl.exe` | 从 DLL 生成 .idl 文件 |
| `widl.exe` | 为 Wine/Winelib 编译 IDL 文件 |
| `gcc-ar.exe` | 用于 ar 的 GCC 包装器 |
| `gcc-nm.exe` | 用于 nm 的 GCC 包装器 |
| `gcc-ranlib.exe` | 用于 ranlib 的 GCC 包装器 |

这些主要是来自 GCC 和 Binutils 的编译器、链接器和二进制操作工具。如需更完整的类 Unix 环境（包含 `gpg`、`make`、`bash` 等工具），请考虑安装 MSYS2（其中包含 MinGW-w64 作为组件）并通过 `pacman` 添加软件包。

[MinGW-w64 官方网站](https://www.mingw-w64.org/)
[MSYS2 软件包（用于 GnuPG 等扩展功能）](https://packages.msys2.org/package/mingw-w64-x86_64-gnupg)
[SourceForge MinGW-w64 下载](https://sourceforge.net/projects/mingw-w64/files/)
