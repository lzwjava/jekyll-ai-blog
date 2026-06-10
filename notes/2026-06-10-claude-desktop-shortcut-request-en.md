---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Desktop Shortcut Request
translated: false
type: note
---

**Question:** Is Cmd+1 / Cmd+2 / Cmd+3 to switch between Chat, Cowork, and Code in the Claude desktop app a good design — and does it exist?

**Answer:**

Good idea — but it doesn't appear to exist yet. There's an open feature request asking for exactly this: users want shortcuts (or at least menu items so macOS keyboard shortcuts can be assigned) to move between Chat, Cowork, Code, and conversations, because right now you have to click each mode in the sidebar — and the requester even suggested Cmd+1/2/3 as the binding. A related issue confirms why macOS-level remapping won't save you: the app has no menu items for navigation to bind shortcuts to (verified by checking the Electron menu definitions in app.asar), so System Settings keyboard shortcuts can't help.

So your instinct matches what power users are asking for — Cmd+1/2/3 is the standard tabbed-interface convention (browsers, iTerm, Slack all do it), and mode-switching via mouse is friction for keyboard-first workflows like yours. If a recent version of the desktop app added it, great, but as of the latest reports it's still an open request.

Shortcuts that *do* exist in the desktop app: double-tap Option to pull up Claude quick entry over whatever you're working on, and Caps Lock for voice dictation (disabled by default). Inside Claude Code itself (terminal), keybindings are fully customizable via a keybindings.json with context-scoped bindings like `chat:submit`, applied without restart — but that's the CLI, not the desktop app's mode switcher.

**Workaround until it ships:** since there are no menu items to bind, you'd need a UI-scripting hack — Hammerspoon or Karabiner clicking the sidebar elements via accessibility APIs:

```lua
-- Hammerspoon: crude mode-switch by clicking sidebar positions in Claude.app
local function clickClaudeSidebar(y_offset)
  local app = hs.application.find("Claude")
  if not app then return end
  app:activate()
  local win = app:mainWindow():frame()
  hs.eventtap.leftClick({x = win.x + 40, y = win.y + y_offset})
end

hs.hotkey.bind({"cmd"}, "1", function() clickClaudeSidebar(80)  end) -- Chat
hs.hotkey.bind({"cmd"}, "2", function() clickClaudeSidebar(120) end) -- Cowork
hs.hotkey.bind({"cmd"}, "3", function() clickClaudeSidebar(160) end) -- Code
```

Fragile (coordinates break on UI updates), but functional. Better: thumbs-up the GitHub issue (#18818) to push it up the priority list.

**References:**

- [Issue #18818: Add keyboard shortcuts to move between Chat, Cowork, Code](https://github.com/anthropics/claude-code/issues/18818)
- [Issue #38447: Keyboard shortcut to switch between conversations](https://github.com/anthropics/claude-code/issues/38447)
- [Navigating the Claude desktop app — claude.com](https://claude.com/resources/tutorials/navigating-the-claude-desktop-app)
- [Claude Code keybindings docs](https://code.claude.com/docs/en/keybindings)
