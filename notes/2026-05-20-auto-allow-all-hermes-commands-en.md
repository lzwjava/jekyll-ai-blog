---
audio: false
generated: true
image: false
lang: en
layout: post
title: Auto-Allow All Hermes Commands
translated: false
type: note
---

Auto-Allowing All Commands in Hermes

    Hermes has a multi-layered approval system. Here's what controls it and how to bypass each layer:

    1. The Config Setting (persistent, recommended for sandboxed environments)

    bash
    hermes config set approvals.mode off


    This permanently disables all dangerous-command prompts. The modes are:

    | Mode   | Behavior                                                                                |
    |--------|-----------------------------------------------------------------------------------------|
    | manual | Always prompt (default)                                                                 |
    | smart  | Auxiliary LLM auto-approves low-risk, auto-denies dangerous, escalates uncertain to you |
    | off    | Skip all approval prompts — equivalent to --yolo                                        |

    The default lives in hermes_cli/config.py:
    yaml
    approvals:
      mode: manual
      timeout: 60
      cron_mode: deny


    The full flow lives in tools/approval.py (1393 lines). At line 1079, the bypass check is:

    python
    if is_truthy_value(os.getenv("HERMES_YOLO_MODE")) or is_current_session_yolo_enabled() or approval_mode == "off":
        return {"approved": True, "message": None}


    2. Per-Invocation Bypass (no config change)

    bash
    hermes --yolo ...
    or
    export HERMES_YOLO_MODE=1
    hermes ...


    The --yolo flag is defined in hermes_cli/_parser.py:
    python
    "--yolo",
    action="store_true",
    default=False,
    help="Bypass all dangerous command approval prompts (use at your own risk)",


    3. In-Session Toggle (/yolo slash command)

    During an interactive session, type:


    /yolo


    This toggles HERMES_YOLO_MODE on/off for the current session. Implemented in cli.py:_toggle_yolo() at line 9124.

    4. What Is and Isn't Gated

    Approval covers (only in local and ssh terminal backends — not in containers like docker/singularity/modal/daytona):
    - Terminal commands flagged as dangerous by pattern matching in tools/approval.py (47 patterns: rm -rf, git reset --hard, force push, chmod 777, pipe-to-shell, system config writes, DROP TABLE, etc.)
    - Computer Use destructive actions (in tools/computer_use/tool.py)

    Hardline block — these are always blocked, even with --yolo or approvals.mode=off:
    - rm -rf /, mkfs, dd to block devices, shutdown/reboot, fork bombs, kill -1 (all processes)
    - sudo -S without configured SUDO_PASSWORD (prevents password guessing)

    5. Smart Mode (Recommended Middle Ground)

    If you don't want to blindly allow everything but also want fewer interruptions:

    bash
    hermes config set approvals.mode smart


    This uses an auxiliary LLM to assess risk. Check the implementation at tools/approval.py:_smart_approve() (line 866) — it asks a lightweight LLM whether a flagged command is genuinely dangerous or a false positive (e.g., python -c "print('hello')" is flagged as "script execution via -c" but is harmless).

    6. For Cron Jobs

    bash
    hermes config set approvals.cron_mode approve


    Default is deny — cron jobs auto-deny dangerous commands. Flip to approve to let them through since there's no user to ask.

    Summary

    | Method              | Scope           | Command                                |
    |---------------------|-----------------|----------------------------------------|
    | Config (persistent) | All sessions    | hermes config set approvals.mode off   |
    | CLI flag            | One invocation  | hermes --yolo                          |
    | Env var             | Process-wide    | export HERMES_YOLO_MODE=1              |
    | In-session toggle   | Current session | /yolo                                  |
    | Smart approval      | All sessions    | hermes config set approvals.mode smart |
