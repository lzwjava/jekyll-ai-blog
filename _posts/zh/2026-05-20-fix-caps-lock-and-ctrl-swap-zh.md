---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复大写锁定键与控制键交换
translated: true
type: note
---

问题
    
    Caps Lock 和 Left Control 都被映射为 Ctrl（键码 37 = Control_L，键码 66 = Control_L）。你原有的 ~/.Xmodmap 使用了基于 keysym 的交换（keysym Caps_Lock = Control_L），这会在多个键共享同一 keysym 时产生混淆，实际上并未交换任何东西——它几乎没有效果。
    
    已应用修复 — 三种方法，均一致
    
    1. 即时方法：setxkbmap -option ctrl:swapcaps
    
    这是现代、X 服务器原生方式。它告诉 X 键盘扩展（XKB）在硬件映射层面交换两个键。这种方式干净、可组合，不会与其他键盘选项冲突。
    
    修复后的键码：
    
    | 键码 | 物理键       | Keysym             | 作用               |
    |------|--------------|--------------------|--------------------|
    | 37   | Left Ctrl    | Caps_Lock (0xffe5) | 大写锁定切换       |
    | 66   | Caps Lock    | Control_L (0xffe3) | Ctrl（修饰键）     |
    | 105  | Right Ctrl   | Control_R (0xffe4) | Ctrl（未改变）     |
    
    clear Lock / clear Control / add Lock / add Control 步骤确保了修饰键映射的一致性——这是常见的陷阱，xmodmap 修改了 keysym 但修饰键掩码没有同步更新。
    
    2. 通过 ~/.Xmodmap 持久化（重写）
    
    旧文件使用了 keysym 命令——当多个键共享同一个 keysym 时不可靠。已重写为基于键码的命令：
    
    
    keycode 66 = Control_L
    keycode 37 = Caps_Lock
    clear Lock
    clear Control
    add Lock = Caps_Lock
    add Control = Control_L
    
    
    在登录时由 ~/.config/autostart/xmodmap.desktop 加载（XDG Autostart 规范——支持 GNOME、KDE、XFCE、i3、Sway 等）。
    
    3. 通过 ~/.xprofile 回退
    
    创建了 ~/.xprofile，内容为 setxkbmap -option ctrl:swapcaps。该文件在 X11 登录时由显示管理器运行，在桌面环境的自动启动之前执行。并非所有桌面环境都会读取 .xprofile（LightDM 会，GDM 有时会），因此这是尽力而为的冗余方案。
    
    持久化链条
    
    
    X11 登录（显示管理器）
      → ~/.xprofile（setxkbmap）           ← 捕获早期桌面环境初始化
      → 桌面环境启动
      → ~/.config/autostart/*.desktop      ← 捕获支持 XDG 的桌面环境
        → xmodmap ~/.Xmodmap               ← 最终覆盖，基于键码
    
    
    如果桌面环境自身的键盘设置面板覆盖了 XKB 选项（GNOME 设置有时会这样做），你可能还需要在那里锁定该选项——但 setxkbmap -option ctrl:swapcaps 一旦设置通常会保持生效。
    
    如何撤销
    
    如果你想恢复默认：
    
    sh
    setxkbmap -option            # 清除所有自定义选项 → 恢复默认
    或仅针对 Ctrl 交换：
    setxkbmap -option ctrl:nocaps    # Caps Lock 无作用
    setxkbmap -option                   # 默认设置
    
    
    然后删除或注释掉 ~/.xprofile 和 ~/.Xmodmap，以防止重启后恢复。