---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 无源码安装DirB
translated: true
type: note
---

### 不修改 DirB 源代码的替代方案

如果无法编辑源代码（比如 `variables.h`）——可能是因为只读环境限制、策略规定，或是个人偏好——这里有几个无需编译就能运行 DirB 的简单方法。这些方案利用预构建的包或重写实现。我将优先介绍 Linux 解决方案（根据你的构建路径），但也会注明不同操作系统的调整方法。

#### 1. **通过包管理器安装（Debian/Ubuntu/Kali 最简单）**
   DirB 已作为预编译包包含在许多发行版的软件仓库中，因此无需修改源代码或执行构建。
   - **Kali Linux**（推荐用于渗透测试工具）：
     ```
     sudo apt update
     sudo apt install dirb
     ```
     - 该工具在 Kali 仓库中受官方支持维护。[Kali 工具页面](https://www.kali.org/tools/dirb/)
   - **Ubuntu/Debian**：
     ```
     sudo apt update
     sudo apt install dirb
     ```
     - 若提示未找到（旧版本可能未收录），可启用 universe 仓库：`sudo add-apt-repository universe && sudo apt update`
   - **验证**：安装后运行 `dirb --help`。字典文件位于 `/usr/share/dirb/wordlists/`
   - **原理**：软件包会在上游处理所有修复（包括多重定义问题）

   其他发行版：
   - **Fedora/RHEL**：`sudo dnf install dirb`（若在 EPEL 仓库中；需先添加 EPEL：`sudo dnf install epel-release`）
   - **Arch**：`sudo pacman -S dirb`

#### 2. **使用 Python 重写版（跨平台，无需 C 编译）**
   原版 DirB 基于 C 语言且构建过程复杂，但存在功能相同（或更优）的现代 Python 移植版，可通过 pip 安装且无需修改源码。
   - **代码库**：[ct-Open-Source/dirb on GitHub](https://github.com/ct-Open-Source/dirb)
   - **安装**：
     ```
     pip install git+https://github.com/ct-Open-Source/dirb.git
     ```
     - 或克隆安装：`git clone https://github.com/ct-Open-Source/dirb.git && cd dirb && pip install .`
   - **用法**：与原版相同，例如 `dirb https://example.com /usr/share/wordlists/dirb/common.txt`
   - **优势**：持续维护、某些场景速度更快、支持 Mac/Windows/Linux。包含递归扫描等增强功能
   - **不足**：非“官方”二进制版本，但输出结果高度吻合

#### 3. **下载预编译二进制文件（选择有限）**
   - 官方 SourceForge 发布页主要提供需编译的源码包（如 dirb222.tar.gz）
   - 虽无通用二进制文件，但若使用 Kali/Parrot OS，推荐包管理安装
   - 变通方案：通过 Docker 运行 Kali 镜像执行 DirB：
     ```
     docker run -it kalilinux/kali-rolling dirb http://example.com
     ```
     - 无需安装，容器环境已预配置

#### 方案对比

| 方案                | 支持平台            | 部署难度 | 备注 |
|---------------------|---------------------|--------|-------|
| **Apt/DNF/Pacman**  | Linux (Debian/Fedora/Arch) | 低 | 预编译版本，含字典文件 |
| **Python 移植版**   | 全平台 (Python 3+)  | 低 | 现代替代方案，仅需 pip |
| **Docker 运行**     | 全平台 (需 Docker)  | 中 | 环境隔离，无需主机安装 |

如果以上方案均不适用（如受限环境），可考虑 Gobuster 等替代工具（`go install github.com/OJ/gobuster/v3@latest`）——基于 Go 语言构建，编译无依赖问题，且具备相同目录爆破功能。

请告知你使用的操作系统以便精准推荐。若遇到问题，可提供具体错误信息。
