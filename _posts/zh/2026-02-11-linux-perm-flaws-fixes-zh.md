---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Linux 权限缺陷与修复
translated: true
type: note
---

**Question:** 关于 Linux user/group/permission 设计，有哪些冷门的观点？

**Answer:**

以下是一些关于经典 Unix/Linux 用户/组/其他（user/group/other）权限模型相对**冷门**或具有争议的看法（经常出现在 sysadmin 圈子、安全讨论或旧式 Unix 与现代系统之争中）：

- **在现代多用户系统中，owner 权限字段大多是多余的** —— group 权限 + ACLs 几乎可以更好地处理所有事情。
  owner bit位 的存在主要是历史原因（它早于 groups 出现）。在实践中，许多人认为如果你总是将用户放入合适的 groups 中，owner 字段很少能提供有意义的额外安全性 —— 它只会增加认知负担。

- 强制每个用户拥有一个 **primary group**（特别是默认的 username==group 惯例）是不必要的，且略有危害。
  许多人认为 primary groups 应该是可选的，或者默认指向像 `users`/`nogroup` 这样中立的组。目前的设计创建了大量无用的 per-user groups，既让 `/etc/group` 变得臃肿，又导致了关于 secondary 与 primary 成员身份的混淆。

- **三层模型 (user/group/other)** 在理论上很优雅，但在 202x 年的环境中实际上是有害的。
  它鼓励了坏习惯（chmod 777、全员可读的 home directories、凡事皆 sudo），因为在没有 ACLs 的情况下，表达哪怕稍微复杂一点的规则都是痛苦的 —— 而大多数人因为 ACLs “复杂”且不可移植而避开它。该模型假装提供了细粒度的控制，实则将人们推向了过度粗放（且不安全）的解决方案。

- 按照现代标准，传统的 Unix 权限 **并不是特别安全** —— 整个系统与其说是真正的 access control，不如说是一个方便的过滤器。
  令人惊讶的是，大量的 privilege escalations（提权）和 container breakouts 仍然是通过权限过于宽松的文件/目录发生的。有人认为 Linux 在权限方面“设计即安全”的声誉是过度营销。

- 目录从一开始就应该拥有 **相互独立的 execute 和 search 权限**（就像其他一些系统尝试过的那样）。
  目录上 'x' bit位 的多重含义（既是 traversal 又是 listing）造成了无尽的困惑，特别是对于初学者以及尝试在不允许列出目录的情况下允许某人访问已知路径时。

- **chmod o=**（移除 other 权限）应该是 desktop/多用户系统中 home directories 真正的默认设置 —— 而不是 755/022 umask。
  目前的设计默认暴露了过多的用户数据（dotfiles, configs, keys, browser data）。许多人认为这是历史残留产物，在 202x 年对隐私保护非常不利。

- 该权限模型积极地 **阻碍了应用程序开发中的 least-privilege（最小权限）思维**。
  因为在没有 ACLs 或 capabilities 的情况下管理权限很麻烦，许多服务最终都在以过高的权限运行（或者人们干脆在任何地方都使用 containers 来逃避问题，而不是修复权限）。

- 在 2025+ 年，特殊位 (**SUID/SGID**) 引起的安全问题比解决的问题更多。
  少数派观点认为，几乎所有剩余的 SUID binaries 都应该被移除，或由 systemd capabilities / ambient capabilities / policykit 风格的机制所取代 —— SUID 的设计从根本上说是脆弱的。

大多数 Linux 用户和管理员将传统模型视为“简单且经受过验证”的，因此这些观点往往比较冷门，或者被斥为过度工程/ACL 狂热主义。

**References:**

- [https://unix.stackexchange.com/questions/55533/is-there-a-reason-why-owner-permissions-exist-arent-group-permissions-enough](https://unix.stackexchange.com/questions/55533/is-there-a-reason-why-owner-permissions-exist-arent-group-permissions-enough)
- [https://www.reddit.com/r/linux/comments/9ptql6/the_problem_with_linux_permissions/](https://www.reddit.com/r/linux/comments/9ptql6/the_problem_with_linux_permissions/)
- [https://www.linuxquestions.org/questions/linux-newbie-8/why-does-linux-require-a-file-user-to-have-a-group-4175515941](https://www.linuxquestions.org/questions/linux-newbie-8/why-does-linux-require-a-file-user-to-have-a-group-4175515941)
