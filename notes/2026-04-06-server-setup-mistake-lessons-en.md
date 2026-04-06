---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lessons from a Server Setup Mistake
translated: false
type: note
---

🦞 Here's what went down and what I could've done better:

**What happened:**
1. You said "GPU inference is live at `http://127.0.0.1:11435`" — I assumed it was Ollama and went down a rabbit hole installing it
2. You had to stop me and say "it's llama-server" — I should've asked first instead of assuming
3. Then I got the model path wrong (used `/home/lzw/models/` instead of the actual llama.cpp models dir)
4. Finally got it running, but it died in the background (nohup wasn't enough)
5. Firewall was blocking the port — only caught it because you said it wasn't accessible
6. The process had already crashed by the time I checked the UFW rules — had to restart via systemd anyway

**What I should've done:**
- **Asked what inference server** you were running before touching anything
- **Checked the process and port first** (`ss -tlnp | grep 11435`, `ps aux | grep llama`)
- **Used systemd from the start** instead of nohup — it's a server, processes die
- **Checked UFW immediately** when setting up a new port
- **Not wasted time on Ollama** — you clearly had a working setup already, I just needed to make it persistent + accessible

**Lessons for next time:**
- Don't assume tech stack — ask
- Check existing state before making changes
- Always firewall-check when opening a new port on a server
- systemd > nohup for services

Basically I overcomplicated what should've been a 2-minute job: "find the running process, make it a service, open the firewall port." 🦞🫠