---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DNF 与 APT 的主要区别
translated: true
type: note
---

Question: Compare DNF and APT

Answer:

**DNF** 和 **APT** 是 Linux 中使用最广泛的两个命令行 package manager，但它们属于不同的生态系统。

### Key Comparison Table

| Aspect                  | APT                                      | DNF                                          |
|-------------------------|------------------------------------------|----------------------------------------------|
| Primary distributions   | Debian, Ubuntu, Linux Mint, Pop!_OS, etc. | Fedora, RHEL ≥8, CentOS Stream, Rocky Linux, AlmaLinux, etc. |
| Package format          | `.deb`                                   | `.rpm`                                       |
| Underlying low-level tool | `dpkg`                                 | `rpm`                                        |
| Predecessor             | `apt-get` / `apt-cache`                  | `yum` (DNF = Dandified YUM)                  |
| Introduced              | 2000 年代早期 (非常成熟)                | 2015 (在 Fedora 中取代了 yum)                |
| Speed (2025–2026 perception) | 通常感觉更快、更轻快     | 大幅改进 (尤其是新版 Fedora 中的 DNF5)，接近或有时等同于 APT |
| Dependency resolution   | 非常好                                | 极佳 (历史上比 yum 更强，支持 modular streams) |
| Cache handling          | 需要显式的 `apt update`              | 需要时自动刷新 metadata |
| Command structure       | 历史上曾有多个工具 (`apt`, `apt-get`, `apt-cache`) | 单个现代命令 `dnf`                  |
| Output style            | 紧凑的逗号分隔列表           | 格式更美观的表格 (version, size, repo 等) |
| Remove behavior         | `remove` 保留配置文件<br>`purge` 删除配置文件 | `remove` 通常也会删除配置文件    |
| Module / Streams support| 无原生支持 (通常使用 PPAs)            | 是 – 非常强大 (例如 nginx, python 等的多个版本) |
| Enterprise / Signing focus | Metadata signing                       | Per-package PGP signing (更适合严格的企业审计) |
| Typical repo size       | 非常庞大 (尤其是包含 PPAs)        | 庞大 + 不断增长的 Flatpak/AppImage 集成 |

### Common Commands Side-by-Side

| Task                        | APT command                              | DNF command                       |
|-----------------------------|------------------------------------------|-----------------------------------|
| Refresh package index       | `sudo apt update`                        | 通常是自动的或使用 `sudo dnf check-update` |
| Upgrade all packages        | `sudo apt upgrade`                       | `sudo dnf upgrade`                |
| Install package             | `sudo apt install firefox`               | `sudo dnf install firefox`        |
| Search package              | `apt search keyword`                     | `dnf search keyword`              |
| Show package info           | `apt show package`                       | `dnf info package`                |
| Remove package              | `sudo apt remove package`                | `sudo dnf remove package`         |
| Remove + config files       | `sudo apt purge package`                 | 通常已包含在 `remove` 中      |
| Autoremove unused deps      | `sudo apt autoremove`                    | `sudo dnf autoremove`             |
| List installed packages     | `apt list --installed`                   | `dnf list installed`              |
| History / undo              | 受限                                  | `dnf history`, `dnf history undo` |

### Which one is better in 2026?

**没有客观上更好**的 package manager —— 这取决于你使用的 distribution：

- 如果你使用 **Ubuntu / Debian 家族**，请选择 **APT** → 最大的生态系统，对许多用户来说速度最快，拥有海量的 packages 和 PPAs。
- 如果你使用 **Fedora / RHEL 家族**，请选择 **DNF** → 更好的 modular streams，更清晰的企业级 signing 方案，非常出色的 dependency solver，以及精美的输出格式。

多年前存在的性能差距 (DNF 明显较慢) 随着 DNF 的改进 (以及 Fedora 中 DNF5 的工作) 已基本消失。

在 2026 年，两者都是成熟、安全且可靠的工具。

References:  

- [https://docs.fedoraproject.org/en-US/quick-docs/dnf-vs-apt](https://docs.fedoraproject.org/en-US/quick-docs/dnf-vs-apt)
- [https://opensource.com/article/21/7/dnf-vs-apt](https://opensource.com/article/21/7/dnf-vs-apt)
- [https://www.ssdnodes.com/blog/package-management-in-linux-use-apt-and-dnf](https://www.ssdnodes.com/blog/package-management-in-linux-use-apt-and-dnf)
- [https://linuxcommunity.io/t/linux-package-managers-compared-apt-dnf-pacman-and-zypper/5760](https://linuxcommunity.io/t/linux-package-managers-compared-apt-dnf-pacman-and-zypper/5760)