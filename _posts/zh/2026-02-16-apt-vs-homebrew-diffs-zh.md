---
audio: false
generated: true
image: false
lang: zh
layout: post
title: APT 与 Homebrew 的主要区别
translated: true
type: note
---

Question: Compare APT and Homebrew

Answer:

**APT** 和 **Homebrew**（通常被称为 "brew"）都是流行的 package managers，但它们针对不同的 operating systems 和哲学。

### Key Comparison Table

| Aspect                     | APT (Advanced Package Tool)                          | Homebrew ("brew")                                    |
|----------------------------|------------------------------------------------------|------------------------------------------------------|
| Primary platform           | Linux (Debian, Ubuntu, Mint, Pop!_OS, etc.)          | macOS (native); 同时也支持 Linux (自 2019 年起提供良好支持) |
| Package format             | `.deb`                                               | Source 或 pre-built bottles (binary archives)        |
| Installation scope         | System-wide (大多数操作需要 `sudo`)                   | 默认 User-local (`~/homebrew` 或 `/opt/homebrew`)；安装后不需要 `sudo` |
| Native / Official status   | Built-in / OS 的核心部分                             | 在 macOS 和 Linux 上均为 Third-party                  |
| Typical use case           | 从 distro repos 安装/更新 system tools, servers, desktop apps | Developer tools, CLI utilities, 更新的版本, cross-platform 一致性 (特别是 macOS → Linux 切换者) |
| Package availability       | 庞大的 official repos + PPAs (非常大的 ecosystem)    | 大量的 formula 集合 (~8,000+ formulae + casks)；通常提供较新版本 |
| Binary vs source           | 几乎总是 pre-compiled binaries                  | 优先使用 pre-built "bottles"；如果没有则回退到从 source 编译 |
| Dependency conflicts       | 由 distro 严格管理；如果误用可能会损坏系统              | 隔离在 prefix 中；损坏 OS 的风险非常低               |
| GUI app support            | 通过 `.deb` packages 或 Flatpak/Snap                  | 通过 **Homebrew Cask** (安装 macOS .app bundles)  |
| Update behavior            | `apt update && apt upgrade` (system-wide)            | `brew update && brew upgrade` (user-local)           |
| Speed & UX                 | 稳健但可能感觉冗长                                   | 非常简洁、彩色的输出；被认为更加 user-friendly         |
| Root requirement            | 安装/升级时需要                                     | 不需要 (初始设置之后)                                |
| Cross-platform consistency | 与 distro 绑定                                      | 在 macOS + Linux 上使用相同的 commands 和许多相同的 packages |
| Security model             | Distro-signed packages; 严格                           | 来自 GitHub 的 Formulae；bottles 通常经过签名；casks 越来越多地需要 notarization (2026+) |
| Best for                   | 通用的 Linux system administration & stability      | Developers, macOS users, 希望在没有 PPAs/Flatpaks 的情况下使用最新工具的用户 |

### Common Commands Side-by-Side

| Task                        | APT command                              | Homebrew command                  |
|-----------------------------|------------------------------------------|-----------------------------------|
| Refresh package index       | `sudo apt update`                        | `brew update`                     |
| Upgrade all packages        | `sudo apt upgrade`                       | `brew upgrade`                    |
| Install package             | `sudo apt install git`                   | `brew install git`                |
| Search for package          | `apt search keyword`                     | `brew search keyword`             |
| Show package info           | `apt show git`                           | `brew info git`                   |
| Remove package              | `sudo apt remove git`                    | `brew uninstall git`              |
| Autoremove unused deps      | `sudo apt autoremove`                    | `brew autoremove`                 |
| List installed packages     | `apt list --installed`                   | `brew list`                       |
| Cleanup old versions/cache  | `sudo apt clean` / `autoclean`           | `brew cleanup`                    |
| Install GUI app (if applicable) | 通常通过 `.deb` 或 Snap/Flatpak    | `brew install --cask firefox`     |

### When to Use Which (2026 Perspective)

- **在 Ubuntu/Debian-based Linux 上使用 APT** → 它是原生的、经过实战检验且深度集成的选择。最适合 stability、security updates 和 system packages。
- **在 macOS 上使用 Homebrew** → 它是那里事实上的标准 package manager (在 2026 年没有真正的竞争对手)。
- **在 Linux 上同时使用两者** → 许多 developers 都会这样做：
  - APT/DNF/Pacman 用于 core OS packages (glibc, kernel modules, security-critical 内容)
  - Homebrew 用于 developer tools, bleeding-edge 版本，或在 macOS 和 Linux 之间切换时保持工具链一致
- Linux 上的 Homebrew 在 2026 年已经非常成熟、快速且可靠 (特别是在 ARM64/aarch64 系统上)，但它**不是**你 distro package manager 的替代品 —— 它是一个补充。

简而言之：APT = Linux 上的深度系统集成。Homebrew = 友好、user-local、跨平台且以 developer 为中心的 package management (在 macOS 上尤为强大)。

References:

- [https://brew.sh/](https://brew.sh/)
- [https://www.xda-developers.com/homebrew-good-linux-mac](https://www.xda-developers.com/homebrew-good-linux-mac)
- [https://www.howtogeek.com/most-linux-users-overlook-homebrew-but-heres-why-its-worth-trying](https://www.howtogeek.com/most-linux-users-overlook-homebrew-but-heres-why-its-worth-trying)
- [https://askubuntu.com/questions/1158920/does-it-makes-sense-to-use-brew-on-ubuntu](https://askubuntu.com/questions/1158920/does-it-makes-sense-to-use-brew-on-ubuntu)
- [https://brew.sh/2025/11/12/homebrew-5.0.0](https://brew.sh/2025/11/12/homebrew-5.0.0)
