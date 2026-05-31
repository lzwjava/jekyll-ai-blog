---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codex代码库中的重置详解
translated: true
type: note
---

现在我有了清晰的图景。以下是 Codex 代码库中 "reset" 的含义：

---

在 codex-rs 中，有几个不同的 "reset" 概念：

**1. `/clear` 斜杠命令（UI 重置 + 新聊天）**

`/clear` 命令执行两件事：
- 清除终端 UI（transcript 单元格、覆盖层、延迟历史行、回溯状态）
- 开始一次全新的聊天会话

来自 `event_dispatch.rs:32`：
```rust
AppEvent::ClearUi => {
    self.clear_terminal_ui(tui, /*redraw_header*/ false)?;
    self.reset_app_ui_state_after_clear();
    self.start_fresh_session_with_summary_hint(
        tui, app_server, Some(ThreadStartSource::Clear),
        /*initial_user_message*/ None,
    ).await;
}
```

`reset_app_ui_state_after_clear()` 方法清除：
- transcript 单元格
- 覆盖层
- 延迟历史行
- 回溯状态（primed、overlay_preview_active、pending_rollback）

但关键的是，它保留了聊天 widget 的会话状态（thread_id、model、composer text 等）——正如测试 `clear_only_ui_reset_preserves_chat_session_state` 所确认的那样。

**2. `/new` 斜杠命令（新聊天，不清除 UI）**

更简单——仅启动一个新会话，不清除终端：
```rust
AppEvent::NewSession => {
    self.start_fresh_session_with_summary_hint(
        tui, app_server, /*session_start_source*/ None,
        /*initial_user_message*/ None,
    ).await;
}
```

**3. WebSocket 会话重置（传输层）**

在 `core/src/client.rs:958` 中，`reset_websocket_session()` 丢弃当前的 WebSocket 连接状态：
```rust
fn reset_websocket_session(&mut self) {
    self.websocket_session.connection = None;
    self.websocket_session.last_request = None;
    self.websocket_session.last_response_rx = None;
    ...
}
```
这是一个传输层面的关注点——当需要重新建立 WebSocket 时，它会清除过时的连接状态。

**4. 记忆重置（`memory/reset` API）**

一个实验性 API（`memory/reset`），用于重置记忆工作空间基线。它在记忆根目录上运行 `reset_git_repository()`，从而有效地撤销未提交的记忆变更。这是记忆子系统的一部分（`memories/write/src/workspace.rs`）。

**5. 轮次历史重置**

在 `app-server/src/thread_state.rs` 中，`current_turn_history.reset()` 清除当前轮次累积的工具调用历史——这是一种每轮次的记账重置。

---

**总结：** 大多数人在 Codex 中说 "reset" 时，指的是 `/clear`——清除 UI 并开始一次全新的聊天会话，同时保留会话配置（模型、权限等）。其他的 reset 是内部机制（WebSocket 连接、记忆基线、轮次历史缓冲区）。