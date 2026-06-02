---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自动允许所有Hermes命令
translated: true
type: note
---

在 Hermes 中自动允许所有命令

Hermes 拥有一个多层审批系统。以下是控制它的机制以及如何绕过每一层：

1. 配置设置（持久化，推荐用于沙箱环境）

bash
hermes config set approvals.mode off

这会永久禁用所有危险命令提示。模式如下：

| 模式   | 行为                                                                                |
|--------|-------------------------------------------------------------------------------------|
| manual | 始终提示（默认）                                                                     |
| smart  | 辅助 LLM 自动批准低风险、自动拒绝危险、将不确定的升级给你                             |
| off    | 跳过所有批准提示 — 等效于 --yolo                                                      |

默认配置位于 hermes_cli/config.py：

yaml
approvals:
  mode: manual
  timeout: 60
  cron_mode: deny

完整流程位于 tools/approval.py（1393 行）。在第 1079 行，绕过检查如下：

python
if is_truthy_value(os.getenv("HERMES_YOLO_MODE")) or is_current_session_yolo_enabled() or approval_mode == "off":
    return {"approved": True, "message": None}

2. 每次调用绕过（无需更改配置）

bash
hermes --yolo ...
或
export HERMES_YOLO_MODE=1
hermes ...

--yolo 标志在 hermes_cli/_parser.py 中定义：

python
"--yolo",
action="store_true",
default=False,
help="Bypass all dangerous command approval prompts (use at your own risk)",

3. 会话内切换（/yolo 斜杠命令）

在交互式会话中，输入：

/yolo

这会切换当前会话的 HERMES_YOLO_MODE 开/关。实现在 cli.py:_toggle_yolo() 的第 9124 行。

4. 什么被限制什么不被限制

批准覆盖范围（仅在本地和 SSH 终端后端 — 不在容器如 docker/singularity/modal/daytona 中）：

- 终端命令通过 tools/approval.py 中的模式匹配标记为危险（47 种模式：rm -rf、git reset --hard、强制推送、chmod 777、管道到 shell、系统配置写入、DROP TABLE 等）
- Computer Use 破坏性操作（在 tools/computer_use/tool.py 中）

强硬阻止 — 这些始终被阻止，即使使用 --yolo 或 approvals.mode=off：

- rm -rf /、mkfs、dd 到块设备、shutdown/reboot、fork 炸弹、kill -1（所有进程）
- 未配置 SUDO_PASSWORD 时使用 sudo -S（防止密码猜测）

5. 智能模式（推荐的中庸之道）

bash
hermes config set approvals.mode smart

这使用辅助 LLM 来评估风险。查看 tools/approval.py:_smart_approve() 的实现（第 866 行）——它询问一个轻量级 LLM 被标记的命令是真正危险还是误报（例如，python -c "print('hello')" 被标记为“通过 -c 执行脚本”但无害）。

6. 对于 Cron 作业

bash
hermes config set approvals.cron_mode approve

默认为 deny — cron 作业自动拒绝危险命令。切换到 approve 以允许它们通过，因为没有用户可询问。

总结

| 方法                | 范围           | 命令                                    |
|---------------------|----------------|-----------------------------------------|
| 配置（持久化）      | 所有会话       | hermes config set approvals.mode off    |
| CLI 标志            | 单次调用       | hermes --yolo                           |
| 环境变量            | 进程范围       | export HERMES_YOLO_MODE=1               |
| 会话内切换          | 当前会话       | /yolo                                   |
| 智能批准            | 所有会话       | hermes config set approvals.mode smart  |
