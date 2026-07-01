---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 包管理器：dnf、apt、brew
translated: true
type: note
---

问题：比较 dnf、apt 和 brew 三种包管理器。

答案：

| | dnf | apt | brew |
| --- | --- | --- | --- |
| 发行版/操作系统 | Fedora/RHEL | Debian/Ubuntu | macOS/Linux |
| 格式 | `.rpm` | `.deb` | formula/cask（源码 + bottles） |
| 作用范围 | 系统级，root | 系统级，root | 用户级，无 root |
| 后端引擎 | libsolv（SAT 求解器） | APT 解析器（libapt） | Ruby DSL |
| 仓库元数据 | XML（repodata） | 扁平 `Packages` 文件 | git 仓库（taps） |

**依赖解析。** 这是最深层的实际差异。dnf 使用 libsolv，一个真正的 SAT 求解器——依赖解析本质上是一个布尔可满足性问题，libsolv 将包约束编码为 CNF 子句，然后进行求解。这使得 dnf 的解析更加严谨，冲突诊断也更出色。apt 使用较旧的启发式解析器（可插拔 EDSP，但默认是贪婪/回溯，并非完整的 SAT 求解器）。实际使用中，apt 偶尔会出现状态更差的"损坏包"问题，需要运行 `apt --fix-broken` 解决。brew 则几乎不做解析——formulae 大多是扁平的，带有显式依赖，没有真正的求解器，因为 Homebrew 通常每个 formula 只提供单一版本，从而避免版本锁定冲突。

**命令映射：**

```bash
# 安装
dnf install pkg        | apt install pkg        | brew install pkg
# 卸载
dnf remove pkg         | apt remove pkg         | brew uninstall pkg
# 更新元数据
dnf check-update       | apt update             | brew update
# 升级全部
dnf upgrade            | apt upgrade            | brew upgrade
# 搜索
dnf search foo         | apt search foo         | brew search foo
# 查看信息
dnf info pkg           | apt show pkg           | brew info pkg
# 查找文件归属
dnf provides /path     | dpkg -S /path          | brew --prefix pkg
# 列出已安装
dnf list installed     | apt list --installed   | brew list
```

**关键行为注意事项：**

- apt 将 `update`（刷新元数据）和 `upgrade`（执行升级）分开。dnf 在大多数操作中隐式刷新元数据（有缓存，可通过 `metadata_expire` 配置）。`apt install` 之前忘记 `apt update` 是经典的缓存过期问题；dnf 很少遇到这种情况。
- brew 以普通用户身份运行，安装到 `/opt/homebrew`（Apple Silicon）或 `/usr/local`（Intel）。无需 sudo。Casks 用于处理图形界面的 `.app` 应用包。这就是 brew 无法管理底层操作系统的原因——它是用户级叠加层，而非系统级包管理器。
- dnf 基于 Python（启动较慢，约几百毫秒）。dnf5（Fedora 41+）是 C++ 重写版——速度快得多。apt 基于 C++，速度快。brew 基于 Ruby，速度偏慢，且由于依赖 git 而网络开销较大。
- 事务回滚：dnf 提供 `dnf history undo <id>`——非常实用，可撤销整个事务。apt 没有原生等效功能（需从 `/var/log/dpkg.log` 手动重建）。brew 也没有。

**针对你的环境：** Ubuntu 工作站（192.168.x.x）和 AMD 云实例上使用的是 apt——请记得 `apt update && apt install`。ROCm/MI300X 工具链通过 AMD 的 apt 仓库以 `.deb` 形式分发，因此在那些机器上 apt 是必不可少的。M2 Air 上使用 brew。你的技术栈中没有 dnf，除非你启动一个 Fedora 实例，但你并没有这样做。

一个面向 AI 场景的提示：对于可重现的机器学习环境，这些工具都不是最合适的层级——应当使用 `uv`/`pip` 锁定版本，配合容器（在 Dockerfile 中使用 `apt` 安装系统库，如 `libnuma`、ROCm）。将 apt 视为系统库的提供者，而不是环境管理器。
