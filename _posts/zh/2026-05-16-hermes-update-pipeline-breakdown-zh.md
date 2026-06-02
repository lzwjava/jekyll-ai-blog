---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯更新管道故障
translated: true
type: note
---

**`hermes update` 的工作原理——它比看起来要复杂得多。**

整个流程位于 `hermes_cli/main.py` 中，主要是 `_cmd_update_impl()`（第 7737 行）。以下是逐步的管道：

**1. 挂断保护**（`_install_hangup_protection`，第 7317 行）

在开始任何操作之前，它会设置 SIGHUP=SIG_IGN，并将 stdout/stderr 包装后镜像到 `~/.hermes/logs/update.log`。这可以防止 SSH 断开连接在更新过程中杀死 pip install，从而避免虚拟环境半损坏。SIGINT（Ctrl-C）和 SIGTERM 被故意保留——它们是合法的取消信号。

**2. 更新前备份**（`_run_pre_update_backup`，第 7590 行）

由 `updates.pre_update_backup` 配置控制（默认关闭）。可以通过 `--backup` 标志强制启用。创建 HERMES_HOME 的完整 zip 快照。默认关闭，因为大型安装会使 zip 花费数分钟。

**3. 安装方法检测**（第 7760 行）

三种路径：
- **没有 .git 目录** -> 在 Windows 上，回退到 ZIP 下载；在 Linux/macOS 上，检查 `detect_install_method()` —— 如果是 `pip`，则路由到 `_cmd_update_pip()`，后者执行 `uv pip install --upgrade hermes-agent`（如果 uv 不可用，则使用普通 pip）
- **存在 .git** -> 继续执行基于 git 的更新

**4. 分支检测**（`_is_fork`，第 6604 行）

将 `origin` 远程 URL 与 `OFFICIAL_REPO_URLS`（NousResearch/hermes-agent 仓库）进行比较。如果不匹配，则你处于分支上——它会打印一条警告，并稍后启用上游同步逻辑。

**5. Git 更新**（第 7811 行）

- `git fetch origin`
- 检测当前分支；如果不是 `main`，则自动贮藏本地更改并切换到 main
- `git rev-list HEAD..origin/main --count` 统计新提交数量
- 如果新提交数为 0：恢复贮藏，切回原分支，打印"Already up to date"
- **更新前快照**：调用 `create_quick_snapshot(label="pre-update")` —— 这是一个轻量级状态快照（state.db、配置、配对 JSON 文件），存储在 HERMES_HOME 中，可通过 `/snapshot list` / `/snapshot restore <id>` 恢复。这就是你输出中产生 `20260516-010419-pre-update` 这一行的原因。

**6. Git 拉取**（第 7927 行）

- `git pull --ff-only origin main` —— 干净的快进合并
- 如果 ff-only 失败（历史分歧）：`git reset --hard origin/main` —— 清除本地分歧，因为贮藏已经保存了未提交的工作
- 拉取后恢复贮藏的更改，如果是交互模式则提示用户

**7. 字节码缓存清理**（`_clear_bytecode_cache`，第 5647 行）

递归删除 `__pycache__/` 目录。防止更新后的源代码引用旧编译 .pyc 文件中不存在的内容时导致 ImportError。这就是你看到的"Cleared 63 stale __pycache__ directories"。

**8. 分支上游同步**（`_sync_with_upstream_if_needed`，第 6699 行）

仅针对分支。巧妙之处：
- 如果没有 `upstream` 远程，则询问用户添加（一次性，记住拒绝）
- 获取上游，比较 `origin/main` 与 `upstream/main`
- 如果 origin 有 upstream 上没有的提交：**跳过**——不会覆盖分支的自定义提交
- 如果 origin 严格落后：从上游合并并使用 force-push-with-lease 推送到 origin
- 这就是你看到"Fork is up to date with upstream"的原因

**9. Python 依赖**（第 7994 行）

- 优先使用 `uv pip install -e .[all]`（如果 uv 可用）
- 回退到 `python -m pip install -e .[all]`
- 有一个特殊的 `_install_python_dependencies_with_optional_fallback`，它首先尝试 `.[all]`；如果某个可选扩展包失败（例如无法编译的 C 依赖），则安装 `.`（基础版），然后逐个重新添加其余扩展包——这样单个失败的可选包不会剥离所有可选能力
- Termux/Android 会获得一个精心策划的 `termux-all` 配置，包含预构建的 psutil 兼容性

**10. 懒加载后端刷新**（`_refresh_active_lazy_features`，第 7006 行）

大多数可选后端（provider、platform 等）都是"懒依赖"——首次使用时安装，不在 pyproject.toml 的 `[all]` 中。问题是：`uv pip install -e .[all]` 不会触及已安装的懒依赖，因此如果懒依赖的版本引脚被提升（CVE、错误修复），用户会永远保留过时的版本。这一步骤找出用户之前激活过的懒功能，并在当前引脚下重新安装它们。这就是你看到的"Refreshing 22 active lazy backend(s)... 14 refreshed"。

**11. Node.js 依赖**（`_update_node_dependencies`，第 7212 行）

如果 `package.json` 存在，则在 TUI 目录（`ui-tui/`）中运行 `npm install`。

**12. 技能同步**（第 8059 行）

将新的捆绑技能复制到 `~/.hermes/skills/`，更新已更改的技能，但尊重用户修改（不会覆盖用户编辑过的技能）。然后同步到所有配置文件。

**13. 配置迁移**（第 8131 行）

检查缺失的环境变量、新的配置字段和配置版本升级。提供交互式迁移（或在非交互/网关模式下自动迁移）。这确保需要配置键的新功能能够获得它们。

**14. 网关自动重启**（第 8275 行）

如果以网关模式运行（`--gateway`），在代码更新后：
- 在尝试重启 *之前* 将退出码 0 写入 `.update_exit_code`（这样即使进程在重启期间被杀死，新网关也能看到成功）
- 尝试优雅的 SIGUSR1 重启（让正在传输的消息最多耗尽 60 秒）
- 对于 systemd 管理的网关，回退到 `systemctl restart`
- 处理多配置文件设置，重启所有正在运行的网关进程

**其创新之处在于：**

- **自我修复的 git**：ff-only 搭配 hard-reset 回退 + 贮藏/恢复，意味着它永远不会让你处于损坏状态
- **分支感知**：自动检测分支，添加上游远程，同步时不覆盖自定义提交
- **懒依赖刷新**：跟踪用户实际使用哪些可选后端，仅升级它们——既避免"永远使用过时的 CVE 版本"又避免"每次更新重新安装 100 个未使用的包"
- **防挂断**：SIGHUP 保护 + 输出镜像意味着 SSH 断开不会破坏更新
- **快照双保险**：拉取前轻量级快照（快速、几乎瞬间）+ 全部操作前可选的完整 zip 备份——两条恢复路径
- **优雅的网关重启**：重启前耗尽正在传输的消息，并带有监视器检测新网关启动
- **可选回退的 pip 安装**：如果某个可选扩展包失败，其余包仍能安装，而不是全有或全无
