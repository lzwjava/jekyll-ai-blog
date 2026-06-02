---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 电源适配器已连接但未充电
translated: true
type: note
---

question: 能否为macOS编写一个Python脚本，用于检测电源适配器已插入但Mac实际上并未充电的情况，并提醒用户？

answer:

可以——这是一个非常实际且可解决的问题。关键在于macOS有一个名为 `pmset` 的命令行工具，可报告电池和电源适配器的状态，包括适配器已连接但 **实际上并未充电** 的情况（这正是“忘记打开插座开关”的场景）。

---

## 工作原理

在终端中运行命令 `pmset -g batt` 会报告电池的充电状态，包括当前是从交流电源还是电池电源供电，以及充电状态。

`pmset -g batt` 的输出可能包含如下状态：

- `charging` —— 适配器已连接且正在充电
- `discharging` —— 正在使用电池供电
- `not charging` —— 适配器 **已插入**，但电力并未流动（你的插座开关问题！）
- `AC attached; not charging` —— 上述状态的变体

---

## Python脚本

此脚本每隔几秒检查一次。当检测到充电器 **物理上已连接** 但 **并未充电**（即墙上的插座开关未打开）时，它会触发macOS原生通知。

```python
#!/usr/bin/env python3
"""
mac_charge_watcher.py
监视：适配器已插入但电池并未充电的情况。
发送macOS通知以提醒你检查电源插座。
"""

import subprocess
import time
import os

# 检查频率（秒）
CHECK_INTERVAL = 10

# 跟踪上一次警报状态，避免重复发送
last_alert_state = None


def get_battery_status():
    """
    运行 pmset -g batt 并返回原始输出字符串。
    """
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True
    )
    return result.stdout


def parse_charging_state(pmset_output):
    """
    返回一个包含以下信息的字典：
      - power_source: 'AC Power' 或 'Battery Power'
      - is_charging: True/False
      - is_not_charging: True/False (适配器已插入，但无电力)
      - percent: 电池电量百分比（整数）
    """
    lines = pmset_output.strip().splitlines()
    power_source = "Unknown"
    is_charging = False
    is_not_charging = False
    percent = -1

    for line in lines:
        if "AC Power" in line:
            power_source = "AC Power"
        elif "Battery Power" in line:
            power_source = "Battery Power"

        if "charging" in line.lower():
            if "not charging" in line.lower():
                is_not_charging = True
                is_charging = False
            elif "discharging" in line.lower():
                is_charging = False
            else:
                is_charging = True

        # 提取百分比
        import re
        match = re.search(r'(\d+)%', line)
        if match:
            percent = int(match.group(1))

    return {
        "power_source": power_source,
        "is_charging": is_charging,
        "is_not_charging": is_not_charging,
        "percent": percent,
    }


def send_notification(title, message):
    """
    使用 osascript 发送原生macOS通知。
    """
    script = f'display notification "{message}" with title "{title}" sound name "Basso"'
    subprocess.run(["osascript", "-e", script])


def main():
    global last_alert_state
    print("🔋 Mac充电监视器已启动。每隔", CHECK_INTERVAL, "秒检查一次...")
    print("按Ctrl+C停止。\n")

    while True:
        try:
            raw = get_battery_status()
            status = parse_charging_state(raw)

            source = status["power_source"]
            percent = status["percent"]
            is_not_charging = status["is_not_charging"]
            is_charging = status["is_charging"]

            print(f"[{time.strftime('%H:%M:%S')}] 电源: {source} | "
                  f"电池: {percent}% | 充电中: {is_charging} | "
                  f"未充电: {is_not_charging}")

            # ⚠️ 关键警报：适配器已连接但未充电
            if source == "AC Power" and is_not_charging:
                if last_alert_state != "not_charging":
                    send_notification(
                        "⚠️ 充电器已连接但未充电！",
                        f"电池电量 {percent}%。请检查电源插座开关！"
                    )
                    last_alert_state = "not_charging"
                    print("  👆 已发送警报：插座开关可能未打开！")

            # ✅ 一切正常——适配器已插入且正在充电
            elif source == "AC Power" and is_charging:
                if last_alert_state == "not_charging":
                    send_notification(
                        "✅ 充电已恢复",
                        f"Mac正在正常充电。电池电量 {percent}%。"
                    )
                last_alert_state = "charging"

            # 使用电池供电
            elif source == "Battery Power":
                last_alert_state = "battery"

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n已停止。")
            break
        except Exception as e:
            print(f"错误: {e}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
```

---

## 如何运行

**第1步 — 保存文件：**

```bash
nano ~/mac_charge_watcher.py
# 粘贴脚本，然后按Ctrl+O保存，Ctrl+X退出
```

**第2步 — 运行：**

```bash
python3 ~/mac_charge_watcher.py
```

你将在终端中看到实时状态。当你插入充电器但插座开关未打开时，10秒内你将收到带声音的macOS通知。

---

## 登录时自动运行（可选）

要让它始终在后台运行而无需打开终端，请创建一个 `launchd` plist文件：

```bash
cat > ~/Library/LaunchAgents/com.user.chargewatcher.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.chargewatcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/mac_charge_watcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF
```

将 `YOUR_USERNAME` 替换为你的实际macOS用户名，然后加载它：

```bash
launchctl load ~/Library/LaunchAgents/com.user.chargewatcher.plist
```

---

## 为什么macOS默认不这样做

macOS确实能识别“未充电”状态——当Mac连接到电源，该电源提供的电力足以运行但不足以充电时，就会出现此状态。然而，在适配器已物理插入但墙上插座无电力的情况下，苹果并不会主动提醒你——它只会默默地使用电池供电。这个脚本弥补了这一空缺。

参考：

- [pmset battery script discussion - Apple Community](https://discussions.apple.com/thread/7049834)
- [If your Mac battery status is "Not Charging" - Apple Support](https://support.apple.com/guide/mac-help/if-your-battery-status-is-not-charging-mh20876/mac)
- [Battery Percentage Boundary Notification Script for macOS - GitHub Gist](https://gist.github.com/brandon1024/74b81564aa0b91aa8287faaa175593e6)
