---
audio: false
generated: true
image: false
lang: en
layout: post
title: Live Streaming to WeChat via OBS
translated: false
type: note
---

Question: How do I live-stream to WeChat Channels (视频号) using OBS?

Answer:

Yes. The basic architecture is:

```text
Camera / Screen / Mic
        ↓
       OBS
        ↓
  RTMP/stream push
        ↓
   微信视频号
        ↓
     Viewers
```

### 1. Install OBS

Install [OBS Studio](https://obsproject.com/?utm_source=chatgpt.com).

### 2. Get the 视频号 live-streaming credentials

In WeChat, go to **视频号 → 直播** and enter the live setup/management page.

You need a **streaming URL + stream key** (推流地址 / 推流密钥), if your account has been granted OBS/external streaming capability.

It will look conceptually like:

```text
Server:
rtmps://...

Stream Key:
<PLACEHOLDER>
```

**Do not share the stream key.**

If you don't see a stream URL/key, your 视频号 account may not currently have the external/OBS streaming capability enabled. WeChat changes this eligibility/UI fairly often.

### 3. Configure OBS

In OBS:

```text
Settings
  → Stream
```

Choose:

```text
Service: Custom
Server: <WeChat RTMP server>
Stream Key: <PLACEHOLDER>
```

Then:

```text
Apply
→ OK
→ Start Streaming
```

### 4. Build your OBS scene

For example, if you want to stream your GPU-repair work:

```text
Scene: GPU Repair

Sources:
├── Video Capture Device     # microscope/camera
├── Display Capture          # Linux/Windows desktop
├── Audio Input Capture      # microphone
└── Text                     # title / status
```

A particularly useful setup for you would be:

```text
Microscope camera
       │
       ├──────────────┐
       ↓              ↓
      OBS ←──── Desktop capture
       │
       ↓
   视频号直播
```

You could show the **PCB/microscope feed as the main video** and keep your terminal / `nvidia-smi` / oscilloscope readings in a smaller window.

### 5. Important distinction

There are two very different workflows:

**Phone live**

```text
Phone camera → WeChat → 视频号
```

**OBS live**

```text
Camera/desktop → OBS → RTMP → 视频号
```

OBS gives you much more control over **multiple cameras, screen capture, overlays, audio mixing, scenes, bitrate, recording, and switching sources**.

For your use case, I'd use **OBS + USB microscope/camera + desktop capture** rather than trying to broadcast directly from the phone.

### Recommended initial OBS settings

Start conservatively:

```text
Resolution: 1920×1080
FPS:        30
Encoder:    NVENC
Bitrate:    ~4,500–6,000 Kbps
Audio:      AAC, 128–160 Kbps
```

Since you have an NVIDIA GPU, NVENC is preferable because encoding doesn't consume much CPU.

If your goal is specifically **"I want to stream my Ubuntu desktop + microscope to 视频号 from my 4070 machine"**, I can give you the exact OBS scene/source/encoder configuration and the WeChat-side steps.
