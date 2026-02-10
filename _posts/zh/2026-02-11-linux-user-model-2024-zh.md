---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Linux 用户模型依然适用
translated: true
type: note
---

Question: 对于只有一个人使用的个人笔记本电脑，传统的 Linux user 和 group 设计是否已经过时了？对于单用户设置，仅拥有一个普通用户、一个 group 和 root 是否足够？像 nginx 这样的服务应该以普通用户还是 root 身份运行？

Answer: 

Linux 经典的 multi-user/group 模型并没有真正**过时**——即使在 2026 年，它仍然是安全性的基石。但你说的没错，在只有一名人类用户的**个人笔记本电脑**上，拥有许多独立用户和组的实际收益会变得非常小。

### 典型的现代单用户笔记本现状 (2025–2026)

大多数人最终的配置大致如下：

- `root` —— 存在，但几乎从不直接登录。
- 一个主要的人类用户（例如 `yourname`） —— 属于多个 **supplementary groups**（用于 sudo 的 wheel/admins，以及 audio, video, render, docker, libvirt, scanner, lpadmin 等）。
- 一个主组，通常与用户名 **同名**（例如 group `yourname`，其中只有你一个人）。

对于交互式/人类用户来说，这就足够了。

许多 distribution 会自动将创建的第一个用户添加到常用组中，以便在不频繁使用 sudo 的情况下使各项功能“正常工作”（例如挂载 USB 驱动器、访问声卡、使用网络摄像头等）。

在单用户笔记本上，你**几乎不需要**创建额外的普通用户，除非你想要实现强隔离（例如，一个用户用于日常工作，另一个用户用于高风险的浏览/游戏）。

### 服务 (nginx, databases, containers, etc.)

这里的情况有所不同 —— 即使在个人机器上，你也应该倾向于**不**以日常用户或 root 身份运行服务。

**最佳实践总结（即使是个人使用）：**

| Service type          | Recommended user/group in 2026                  | Why (even on laptop)                                 | Common on distros          |
|-----------------------|--------------------------------------------------|------------------------------------------------------|----------------------------|
| nginx / apache        | Dedicated system user (`nginx` / `www-data`)     | Principle of least privilege, limits damage if exploited | 几乎所有 distros           |
| mariadb / postgresql  | `mysql` / `postgres`                             | 如果被攻破，是非常高价值的目标                      | Standard                   |
| redis / memcached     | `redis` / `memcached`                            | In-memory databases 对攻击者很有吸引力              | Standard                   |
| docker daemon         | `root`（目前无法避免）                           | 本身就需要很多权限                                   | —                          |
| podman / rootless containers | Your user                                   | 比 rootful docker 具有更好的安全性                   | 越来越流行                 |
| Custom / self-hosted app (e.g. Nextcloud, Jellyfin) | Dedicated system user or your user | 取决于威胁模型                                       | 各异                       |
| Very low-risk background script | Your own user (or systemd --user)     | 更简单，依然能保持合理的隔离                         | 个人使用中很常见           |

**针对 nginx：**

- **master process** 通常以 root 身份启动（需要绑定到 80/443 端口）。
- **worker processes** 会丢弃权限并以 `nginx` / `www-data` 身份运行（这非常重要）。
- 即使机器只有你一个人在使用，在 2026 年这仍然被视为最佳实践。
- 你**可以**在大于等于 1024 的端口上以非 root 身份运行整个 nginx（例如 8080端口 + reverse proxy / iptables 重定向），但大多数人仍保持标准设置。

**在真正的单用户笔记本上，风险较低**，因此许多人确实简化了操作：

- 以自己的用户身份运行小型个人服务（更容易管理文件权限，无需管理额外用户）。
- 使用 `systemd --user` 服务（完全作为你的用户运行，在登录时启动）。
- 使用 podman rootless 容器（在 2025–2026 年处理个人服务时非常流行）。

但是，**以 root 或你的日常用户身份运行重要的面向网络的服务（nginx, databases 等）** 仍被视为不良做法 —— 即使绝对风险感觉很低。

### 2026 年对大多数个人笔记本用户的简要建议

- 只保留一个人类用户 + root。
- 在安装服务时，让 distro 创建标准的系统用户/组（`apt install nginx` → 创建 `nginx` 用户）。
- 对面向网络的 daemons 使用这些专用用户。
- 对于你自己的小型脚本/工具 → 以你的用户身份或通过 `systemd --user` 运行。
- 如果你追求极致的极简主义或安全性 → 考虑为几乎所有内容使用 rootless podman / distrobox。

旧的 multi-user 模型并未消亡 —— 只是在个人机器上，大多数**人类**用户消失了，而**系统/服务**用户变得更加重要。

References:  

- [How to Run NGINX for Root & Non-Root Users](https://support.tools/nginx-root-non-root)
- [Is it a security risk to run master process of nginx as root?](https://security.stackexchange.com/questions/202861/is-it-a-security-risk-to-run-master-process-of-nginx-as-root)
- [Linux User and Group Management Security Best Practices](https://www.itprotoday.com/linux-os/linux-user-and-group-management-security-best-practices)
- [Using systemd features to secure services](https://www.redhat.com/en/blog/systemd-secure-services)