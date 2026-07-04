---
audio: false
generated: true
image: false
lang: en
layout: post
title: The tmux Adoption Reality
translated: false
type: note
---

**Question:** Do a lot of people actually use tmux to switch between projects like that, or is it a niche practice?

Let me check what data exists on actual adoption.**Answer:**

Honest answer: it's a large, loud minority — not the majority. Let me break down who actually uses it and why, so you can decide if you're in that group (you are, mostly).

**Who actually uses tmux heavily:**

1. **Anyone SSHing into remote machines** — this is the killer use case, and it's *your* use case. When you SSH into your RTX 4070 box or the MI300X droplet, tmux is close to mandatory: losing terminal sessions due to SSH disconnects is the pain that converts most people. Your training run survives your Air going to sleep. Without tmux (or `nohup`/`systemd`), a dropped WiFi connection kills your job.

2. **Terminal-first developers** — vim/neovim users, backend/infra people, SREs. tmux has over 37k stars on GitHub, and it keeps getting written about in 2026, so it's not dying. But it correlates strongly with the neovim crowd — it's a subculture.

3. **The new wave: CLI agent users.** This is the interesting 2025–2026 shift. People running Claude Code, aider, or custom agents (like your `ww`/`iclaw`/`zz`) increasingly use tmux to run multiple long-lived agent sessions in parallel — one agent per project, detached, checked on periodically. If you're building CLI agents, tmux sessions are basically your process supervisor.

**Who doesn't:**

- **Most developers, honestly.** The majority live in VS Code / JetBrains integrated terminals + IDE workspace switching. One search result captures this perfectly: a tmux user pairs with teammates and they ask "what is this, you can't even paste properly here". That's the median developer reaction.
- **Modern terminal users without remote needs.** Kitty, Ghostty, and Alacritty have tabs, split screens, and other functionality built-in — and you use Warp, which has tabs, split panes, and saved sessions natively. For *local* work, Warp already gives you 70% of tmux.

**So the practical answer for you specifically:**

- **Local on the Air**: you don't strictly need tmux — Warp tabs per project are fine. One Warp tab = one project is the lightweight version of what I described.
- **Remote (4070 box, MI300X droplet)**: yes, use tmux, non-negotiable. This is where "a lot of people" is actually "nearly everyone serious." The pattern:

```bash
# on the remote box
tmux new -s train      # start training run here, then Ctrl-b d to detach
tmux new -s agent      # long-running CLI agent

# from your Air, days later
ssh lzw@192.168.x.x -t "tmux attach -t train"
```

- **Alternative worth knowing**: `zellij` (Rust, discoverable keybindings) is the modern tmux competitor — friendlier defaults, same session model. Given your Rust interest, worth 20 minutes.

The meta-point from your previous question stands either way: the mechanism doesn't matter (tmux sessions, Warp tabs, virtual desktops) — what matters is *one named context per project* instead of 30 anonymous terminals. tmux is just the mechanism that also survives disconnects, which is why the remote-heavy crowd — the crowd you're in — converges on it.

**References:**

- [Why I love tmux — DEV Community](https://dev.to/antjanus/why-i-love-tmux-12ak)
- [How Tmux Supercharged My Development Workflow — Medium](https://devprogramming.medium.com/how-tmux-supercharged-my-development-workflow-5b9dcf004789)
- [Why You Should Finally Learn Tmux (Yes, Even in 2026) — Medium](https://medium.com/quick-programming/why-you-should-finally-learn-tmux-yes-even-in-2026-4dc9478bde30)
- [Tmux Tutorial: The Complete Developer Workflow Guide (2026) — DEV Community](https://dev.to/_d7eb1c1703182e3ce1782/tmux-tutorial-the-complete-developer-workflow-guide-2026-33b3)