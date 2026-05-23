---
audio: false
generated: true
image: false
lang: en
layout: post
title: Storage Audit for Application Cleanup
translated: false
type: note
---

Here's the full audit. 74 apps, 33GB total. Organized by what to do:

**SAFE DELETE — clearly unused/stale (save ~10.5GB)**

```
App                           Last Touch   Size    Why remove
─────────────────────────────────────────────────────────────
iTerm.app                     2023-01      --      Replaced by Ghostty
OBS.app                       2023-02      351MB   Screen recording, not streaming
FileZilla.app                 2023-03      46MB    FTP client, use terminal
HP Easy Scan.app              2023-03      201MB   HP scanner driver
VirtualBox.app                2023-03      253MB   You have workstation + cloud
Anaconda-Navigator.app        2023-05      --      Use terminal conda instead
Color Widgets.app             2023-07      32MB    Desktop widgets
TencentMeeting.app            2023-12      442MB   Not used in 2.5 years
Safe Connect.app              2024-08      4MB     VPN client
Nutstore.app                  2024-10      220MB   Cloud storage (坚果云)
Screen Mirror to TV           2024-12      7MB     Bloatware
Tailwind.app                  2024-12      6MB     CSS tool, use terminal
calibre.app                   2023-03      762MB   Ebook manager
Electrum.app                  2024-10      104MB   Bitcoin wallet
qbittorrent.app               2024-12      --      Torrent client
SQuirreLSQL.app               2025-02      48MB    SQL GUI, use terminal
Scratch 3.app                 2025-05      538MB   Kids coding, not relevant
balenaEtcher.app              2025-07      376MB   Flash USB, one-time use
Amazon Kindle.app             2025-09      130MB   Ebook reader
V2RayXS.app                   2023-04      42MB    Old proxy, using ClashX Pro
OneDrive.app                  2025-03      177MB   Microsoft cloud, use Google Drive
CapCut.app                    2025-09      1.6GB   Video editor, one-time use
Sketch.app                    2025-12      115MB   Design tool, not a designer
Microsoft To Do.app           2025-12      32MB    Task manager
Outline.app                   2025-12      48MB    Wiki/notes
sogou_mac_616b.app            2025-01      --      Sogou input (if using Apple input)
Sniffnet.app                  2025-06      35MB    Network monitor
```

**CONSIDER DELETING — duplicates/redundant (save ~3.3GB)**

```
App                           Size    Replaces
──────────────────────────────────────────────────
Vivaldi.app                   656MB   You have Chrome + Safari + Firefox
Firefox.app                   474MB   You have Chrome + Safari
GitHub Desktop.app            423MB   You use terminal git
Anaconda-Navigator.app        --      conda CLI works fine
superwhisper.app              132MB   AI voice, Claude can do this
IntelliJ IDEA.app             3.9GB   If not doing Java/Kotlin
```

**KEEP — active use (touched in last month)**

```
Core work:     Ghostty, Zed, VSCode, Claude, Chrome, Safari
Comms:         WeChat, 企业微信, Lark, Teams, Zoom, QQ, Telegram, WhatsApp, Discord
AI/Dev:        Docker, Xcode, OpenClacky
System:        Google Drive, VLC, Pages, Swift Playground, TestFlight
Proxy:         ClashX Pro
```

**HOLD — need your input**

```
App                Size    Question
──────────────────────────────────────────────────
Xcode.app          4.7GB   Do you still do iOS dev? Biggest single app
Docker.app         1.7GB   Do you use Docker locally or just remote?
IntelliJ IDEA      3.9GB   Java/Kotlin work? Or just Python/TS?
Android Studio     2.5GB   Android dev still active?
Multipass.app      --      Ubuntu VMs? You have the workstation
```

**Potential savings if you delete the safe list + consider list: ~14GB**

Want me to trash any of these? Tell me which categories or specific apps to remove, or just say "trash the safe list" and I'll do it.