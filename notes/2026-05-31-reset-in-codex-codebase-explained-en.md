---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reset in Codex Codebase Explained
translated: false
type: note
---

Now I have a clear picture. Here's what "reset" means in the Codex codebase:

---

There are several distinct "reset" concepts in codex-rs:

**1. `/clear` slash command (UI reset + new chat)**

The `/clear` command does two things:
- Clears the terminal UI (transcript cells, overlays, deferred history lines, backtrack state)
- Starts a fresh chat session

From `event_dispatch.rs:32`:
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

The `reset_app_ui_state_after_clear()` method clears:
- Transcript cells
- Overlays
- Deferred history lines
- Backtrack state (primed, overlay_preview_active, pending_rollback)

But critically, it preserves the chat widget's session state (thread_id, model, composer text, etc.) — as confirmed by the test `clear_only_ui_reset_preserves_chat_session_state`.

**2. `/new` slash command (new chat, no UI clear)**

Simpler — just starts a new session without clearing the terminal:
```rust
AppEvent::NewSession => {
    self.start_fresh_session_with_summary_hint(
        tui, app_server, /*session_start_source*/ None,
        /*initial_user_message*/ None,
    ).await;
}
```

**3. WebSocket session reset (transport-level)**

In `core/src/client.rs:958`, `reset_websocket_session()` drops the current WebSocket connection state:
```rust
fn reset_websocket_session(&mut self) {
    self.websocket_session.connection = None;
    self.websocket_session.last_request = None;
    self.websocket_session.last_response_rx = None;
    ...
}
```
This is a transport concern — it clears stale connection state when a WebSocket needs to be re-established.

**4. Memory reset (`memory/reset` API)**

An experimental API (`memory/reset`) that resets the memory workspace baseline. It runs `reset_git_repository()` on the memory root, effectively reverting uncommitted memory changes. This is part of the memories subsystem (`memories/write/src/workspace.rs`).

**5. Turn history reset**

In `app-server/src/thread_state.rs`, `current_turn_history.reset()` clears the accumulated tool call history for the current turn — a per-turn bookkeeping reset.

---

**Summary:** When most people say "reset" in Codex, they mean `/clear` — wipe the UI and start a fresh chat session while preserving session config (model, permissions, etc.). The other resets are internal plumbing (WebSocket connections, memory baselines, turn history buffers).
