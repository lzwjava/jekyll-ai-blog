---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Git Bash Warp Proc锁定错误
translated: true
type: note
---

**问题：** 在 Windows 上使用 Warp 终端时，如何修复 Git Bash 作为终端配置时出现的 Cygwin/MSYS2 `get_proc_lock` / `sync_proc_subproc` 错误？

**回答：**

该错误是经典的 Cygwin fork/proc 锁定问题：

```
[sig] bash 10696! get_proc_lock: Couldn't acquire sync_proc_subproc for(4,0), last 2, Win32 error 0
[sig] bash 10696! proc_subproc: couldn't get proc lock. what 4, val 0
```

这是因为 Warp 注入了自己的 PTY/shell 钩子，与 Cygwin 的进程同步原语冲突。Git Bash 基于 MSYS2/Cygwin，因此对父进程如何设置环境较为敏感。

**修复选项（按效果排序）：**

**1. 在 Warp 配置中使用 `--login -i` 标志启动 Git Bash**

在 Warp → Settings → Features → Terminal Profiles 中，将 shell 命令设置为：

```
C:\Program Files\Git\bin\bash.exe --login -i
```

`--login` 标志可确保正确加载 `.bash_profile`，并在 Warp 的钩子触发前正确初始化 Cygwin 运行时。

**2. 禁用 Warp 对 Git Bash 的 shell 集成**

Warp 的 shell 集成（用于提示检测、命令块等）会注入代码以派生子进程——这恰恰触发了该错误。在 Warp 设置中，专门为 Git Bash 禁用 shell 集成，或在 `~/.bashrc` 中添加：

```bash
unset WARP_IS_LOCAL_SHELL_SESSION
```

**3. 设置 `MSYS` 环境变量以抑制 fork 警告**

在 Git Bash 的 `.bashrc` 中或 Warp 配置文件的环境变量中添加：

```
MSYS=winsymlinks:nativestrict
MSYS2_ARG_CONV_EXCL="*"
```

更直接的方式，fork 错误有时可以通过以下方式抑制：

```
MSYS=disable_pcon
```

**4. 使用 `mintty` 包装器而非直接 `bash.exe` 启动 Git Bash**

```
C:\Program Files\Git\git-bash.exe
```

但这会打开独立窗口——不适合嵌入 Warp。

**5. 改用 WSL2 作为 Warp 配置**

说实话，这是最干净的修复方案。Windows 上的 Git Bash 只是一个兼容层。如果你正在做正经的开发工作（显然是的），Warp 中的 WSL2 Ubuntu 能提供一个真正的 Linux 环境，无需处理 Cygwin 的 proc-lock 问题。Warp 的 shell 集成原生支持 WSL2 的 bash/zsh。

**一句话总结根本原因：** Warp 通过派生子进程实现命令检测，当父进程（Warp）不符合 Cygwin 预期的进程树时，Cygwin 的 `sync_proc_subproc` 互斥量超时或失败——Win32 错误 0 表示未找到锁对象，而非权限错误。