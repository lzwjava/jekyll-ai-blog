---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯 / 目标命令拉尔夫·卢普
translated: true
type: note
---

以下是在 hermes-agent 中使用 `/goal` 指令的方式：

## 概述

`/goal` 实现了一种 **"Ralph 循环"** —— 一个持久、自主的目标，能让 Hermes 在多个轮次中持续工作，直到目标达成、用户停止或轮次预算耗尽。该功能在 `hermes_cli/goals.py` 中描述。

## 核心流程

```
用户设置 /goal <文本>
        |
        v
   目标变为 "激活"（持久化存储于 SessionDB）
        |
        v
   Hermes 将目标作为普通用户消息处理
        |
        v
   每轮结束后，_maybe_continue_goal_after_turn() 被触发
        |
        v
   评判模型评估："目标是否完成？"
        |
      / \
    完成  继续
    |       |
    v       v
  标记完成  将延续提示推回
            _pending_input 队列
            |
            v
         自动开始下一轮
```

## 关键组件

### 1. GoalState（数据类，第 130 行）

存储每个会话的目标状态：`goal` 文本、`status`（激活/暂停/完成/清除）、`turns_used`、`max_turns`（默认 20）、`subgoals` 列表、`consecutive_parse_failures` 等。持久化存储于 SessionDB 的 `state_meta` 表中，键值为 `goal:<session_id>`。

### 2. 评判器（`judge_goal()`，第 334 行）

每轮结束后，调用辅助模型并使用严格提示词询问："基于智能体的最后回复，目标是否已满足？" 评判器必须以 JSON 形式回复：`{"done": true/false, "reason": "..."}`。评判器采用 **容错开放** 机制 —— 任何错误默认视为"继续"，以防评判器故障阻碍进度。轮次预算作为最后保障。

### 3. GoalManager（第 431 行）

协调状态管理。主要方法：

- `set(goal)` —— 创建新的激活目标，持久化到数据库
- `pause(reason)` / `resume()` —— 用户控制
- `clear()` —— 移除目标
- `evaluate_after_turn(last_response)` —— 每轮后调用的主入口点。调用评判器，更新状态，返回包含 `should_continue` 和 `continuation_prompt` 的决策字典
- `next_continuation_prompt()` —— 构建反馈给用户的消息提示

### 4. CLI 处理器（`_handle_goal_command`，cli.py 第 8263 行）

分发子命令：

- `/goal <文本>` —— 设置新目标（同时将目标文本立即加入 `_pending_input` 队列以启动循环）
- `/goal status` —— 显示当前状态
- `/goal pause` / `/goal resume` —— 手动控制
- `/goal clear|stop|done` —— 移除目标

### 5. 循环钩子（`_maybe_continue_goal_after_turn`，cli.py 第 8404 行）

每次 CLI 轮次后调用。它：

1. 如果没有激活目标或已存在用户消息队列则跳过（抢占机制）
2. 如果该轮被 Ctrl+C 中断则自动暂停
3. 从对话历史中提取最后一条助手回复
4. 调用 `mgr.evaluate_after_turn()` 运行评判器
5. 如果 `should_continue` 为真，将延续提示推入 `_pending_input` —— 自动触发下一轮

### 6. 延续提示（第 60-81 行）

两种模板：一种简单版本，一种带子目标版本。示例：

```
[继续朝着您的既定目标前进]
目标：重构 auth 模块

继续朝着此目标努力。执行下一步具体操作。
如果您认为目标已完成，请明确说明并停止。
```

## 停止条件

| 条件 | 结果 |
| ----------- | ------------- |
| 评判器判定"完成" | 目标标记为完成，通知用户 |
| 轮次预算耗尽（默认 20） | 自动暂停，`/goal resume` 重置预算 |
| 用户在循环中发送真实消息 | 抢占延续，该轮暂停目标 |
| 用户按下 Ctrl+C | 自动暂停（可通过 `/goal resume` 恢复） |
| 连续 3 次评判器解析失败 | 自动暂停，并提示配置更好的评判模型 |
| `/goal pause` 或 `/goal clear` | 手动停止 |

## 子目标（`/subgoal`）

用户可在循环中通过 `/subgoal <文本>` 添加额外条件。这些条件会附加到评判提示（判定时需考虑）和延续提示（智能体会看到）中。支持 `remove <n>` 和 `clear` 子命令。

## 设计原则

- **不修改系统提示** —— 延续提示仅为用户消息，因此提示缓存保持不变
- **容错开放的评判器** —— 错误默认视为"继续"；轮次预算是真正的最后保障
- **用户抢占** —— 真实用户消息始终优先于延续提示
- **会话持久化** —— 目标状态在 `/resume` 跨会话时依然保留
