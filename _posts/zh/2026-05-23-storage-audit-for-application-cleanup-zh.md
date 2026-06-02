---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 应用清理的存储审计
translated: true
type: note
---

以下是完整的审计报告。共74个应用，总计33GB。按操作建议分类：

**安全删除 — 明显未使用/过时（可节省约10.5GB）**

```
应用                           最后使用时间    大小    删除原因
─────────────────────────────────────────────────────────────
iTerm.app                     2023-01      --      已被 Ghostty 替代
OBS.app                       2023-02      351MB   屏幕录制，非直播需求
FileZilla.app                 2023-03      46MB    FTP 客户端，可使用终端
HP Easy Scan.app              2023-03      201MB   HP 扫描仪驱动
VirtualBox.app                2023-03      253MB   你已有工作站 + 云环境
Anaconda-Navigator.app        2023-05      --      改用终端 conda
Color Widgets.app             2023-07      32MB    桌面小组件
TencentMeeting.app            2023-12      442MB   已2.5年未使用
Safe Connect.app              2024-08      4MB     VPN 客户端
Nutstore.app                  2024-10      220MB   云存储（坚果云）
Screen Mirror to TV           2024-12      7MB     流氓软件
Tailwind.app                  2024-12      6MB     CSS 工具，可使用终端
calibre.app                   2023-03      762MB   电子书管理器
Electrum.app                  2024-10      104MB   比特币钱包
qbittorrent.app               2024-12      --      BT 下载客户端
SQuirreLSQL.app               2025-02      48MB    SQL 图形界面，可使用终端
Scratch 3.app                 2025-05      538MB   儿童编程，不相关
balenaEtcher.app              2025-07      376MB   U盘刷写，一次性使用
Amazon Kindle.app             2025-09      130MB   电子书阅读器
V2RayXS.app                   2023-04      42MB    旧代理，现用 ClashX Pro
OneDrive.app                  2025-03      177MB   微软云，改用 Google Drive
CapCut.app                    2025-09      1.6GB   视频编辑，一次性使用
Sketch.app                    2025-12      115MB   设计工具，非设计师
Microsoft To Do.app           2025-12      32MB    任务管理器
Outline.app                   2025-12      48MB    维基/笔记
sogou_mac_616b.app            2025-01      --      搜狗输入法（若已改用苹果输入法）
Sniffnet.app                  2025-06      35MB    网络监控
```

**考虑删除 — 重复/冗余（可节省约3.3GB）**

```
应用                           大小    替代品
──────────────────────────────────────────────────
Vivaldi.app                   656MB   你已有 Chrome + Safari + Firefox
Firefox.app                   474MB   你已有 Chrome + Safari
GitHub Desktop.app            423MB   你使用终端 git
Anaconda-Navigator.app        --      终端 conda 即可
superwhisper.app              132MB   AI 语音，Claude 可完成
IntelliJ IDEA.app             3.9GB   若不做 Java/Kotlin
```

**保留 — 活跃使用（最近一个月内使用过）**

```
核心工作：  Ghostty, Zed, VSCode, Claude, Chrome, Safari
通讯：      WeChat, 企业微信, Lark, Teams, Zoom, QQ, Telegram, WhatsApp, Discord
AI/开发：   Docker, Xcode, OpenClacky
系统：      Google Drive, VLC, Pages, Swift Playground, TestFlight
代理：      ClashX Pro
```

**待定 — 需你确认**

```
应用               大小    问题
──────────────────────────────────────────────────
Xcode.app          4.7GB   你还做 iOS 开发吗？体积最大的单个应用
Docker.app         1.7GB   你本地使用 Docker 还是仅远程？
IntelliJ IDEA      3.9GB   做 Java/Kotlin 工作？还是仅 Python/TS？
Android Studio     2.5GB   还在进行 Android 开发？
Multipass.app      --      Ubuntu 虚拟机？你已有工作站
```

**若删除安全列表+考虑列表，潜在节省空间：约14GB**

需要我删除其中哪些？告诉我类别或具体应用，或者直接说“删除安全列表”，我会执行。
