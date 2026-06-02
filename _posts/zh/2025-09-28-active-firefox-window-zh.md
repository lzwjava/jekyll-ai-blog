---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: 活动火狐窗口识别脚本
translated: true
type: note
---

#!/usr/bin/env python3
import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck

def 获取火狐窗口():
    screen = Wnck.Screen.get_default()
    screen.force_update()

    firefox_windows = []
    for window in screen.get_windows():
        if window.get_application():
            app_name = window.get_application().get_name().lower()
            window_name = window.get_name()

            if 'firefox' in app_name or 'firefox' in window_name.lower():
                firefox_windows.append({
                    'title': window_name,
                    'app_name': app_name,
                    'is_active': window.is_active(),
                    'pid': window.get_pid()
                })

    return firefox_windows

# 获取活动火狐窗口
windows = 获取火狐窗口()
active_firefox = [w for w in windows if w['is_active']]
print("活动火狐窗口:", active_firefox)
