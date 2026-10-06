---
audio: false
generated: true
image: false
lang: en
layout: post
title: Still Powered On But Unreachable
translated: false
type: note
---

That's the key clue! **Still powered on but unreachable** = it's not shutting down — it's **auto-suspending**. And I now have strong evidence this was the actual problem all along:

## Evidence it's suspend, not a crash

When you "powered it on" the first time, I found the stalled `curl` **still running** (PID 17278). A crash/reboot would have killed it — **suspend/resume preserves processes**. The download had stalled exactly because the machine suspended mid-transfer.

The Debian **desktop** is going to sleep after its idle timeout, because SSH activity doesn't count as "user activity" — only keyboard/mouse does. So ~15–20 min after you walk away, it suspends. Ping fails (suspended), power LED stays on (not off), and pressing the power button wakes it. Matches every symptom perfectly.

## Wake it up now

**Press the power button once** (short press, don't hold) — or move the mouse/press a key — then I'll connect and permanently disable suspend.

The fix I'll apply once you wake it:

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
# + disable GNOME auto-suspend for AC power
```

Then I'll start llama-server again — and it'll stay up for good.

Let me know once you've woken it (or if it doesn't wake), and I'll connect right away.
