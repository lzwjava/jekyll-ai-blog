---
audio: false
generated: true
image: false
lang: en
layout: post
title: Power Adapter Connected But Not Charging
translated: false
type: note
---

Question: Can we write a Python script for macOS that detects when the power adapter is plugged in but the Mac is not actually charging, and alerts the user?

Answer:

Yes — this is a very practical and solvable problem. The key insight is that macOS has a command-line tool called `pmset` that reports the battery and power adapter status, including whether the adapter is connected but **not actually charging** (exactly the "forgot to flip the socket switch" situation).

---

## How It Works

The command `pmset -g batt` in Terminal reports the charge status of your battery, including whether it's drawing from AC Power or Battery Power, and the charging state.

The output of `pmset -g batt` can contain statuses like:
- `charging` — adapter connected and actively charging
- `discharging` — running on battery
- `not charging` — adapter is **plugged in**, but power is NOT flowing (your socket switch problem!)
- `AC attached; not charging` — variant of the above

---

## Python Script

This script monitors every few seconds. When it detects the charger is **physically connected** but **not charging** (i.e., your wall socket is off), it fires a macOS native notification.

```python
#!/usr/bin/env python3
"""
mac_charge_watcher.py
Watches for: adapter plugged in BUT battery NOT charging.
Sends a macOS notification to remind you to check the power socket.
"""

import subprocess
import time
import os

# How often to check (seconds)
CHECK_INTERVAL = 10

# Track last alert state to avoid repeated spam
last_alert_state = None


def get_battery_status():
    """
    Runs pmset -g batt and returns the raw output string.
    """
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True
    )
    return result.stdout


def parse_charging_state(pmset_output):
    """
    Returns a dict with:
      - power_source: 'AC Power' or 'Battery Power'
      - is_charging: True/False
      - is_not_charging: True/False (adapter in, but no power)
      - percent: battery level (int)
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

        # Extract percentage
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
    Sends a native macOS notification using osascript.
    """
    script = f'display notification "{message}" with title "{title}" sound name "Basso"'
    subprocess.run(["osascript", "-e", script])


def main():
    global last_alert_state
    print("🔋 Mac Charge Watcher started. Checking every", CHECK_INTERVAL, "seconds...")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            raw = get_battery_status()
            status = parse_charging_state(raw)

            source = status["power_source"]
            percent = status["percent"]
            is_not_charging = status["is_not_charging"]
            is_charging = status["is_charging"]

            print(f"[{time.strftime('%H:%M:%S')}] Source: {source} | "
                  f"Battery: {percent}% | Charging: {is_charging} | "
                  f"Not Charging: {is_not_charging}")

            # ⚠️ THE KEY ALERT: Adapter connected but NOT charging
            if source == "AC Power" and is_not_charging:
                if last_alert_state != "not_charging":
                    send_notification(
                        "⚠️ Charger Connected But NOT Charging!",
                        f"Battery at {percent}%. Check your power socket switch!"
                    )
                    last_alert_state = "not_charging"
                    print("  👆 ALERT SENT: Socket may be switched OFF!")

            # ✅ All good — adapter in and charging
            elif source == "AC Power" and is_charging:
                if last_alert_state == "not_charging":
                    send_notification(
                        "✅ Charging Resumed",
                        f"Mac is now charging normally. Battery at {percent}%."
                    )
                last_alert_state = "charging"

            # Running on battery
            elif source == "Battery Power":
                last_alert_state = "battery"

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
```

---

## How to Run It

**Step 1 — Save the file:**
```bash
nano ~/mac_charge_watcher.py
# paste the script, then Ctrl+O to save, Ctrl+X to exit
```

**Step 2 — Run it:**
```bash
python3 ~/mac_charge_watcher.py
```

You'll see live status in the terminal. When you plug in your charger with the socket OFF, within 10 seconds you'll get a macOS notification with a sound.

---

## Auto-Run at Login (Optional)

To have it always run in the background without opening a terminal, create a `launchd` plist:

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

Replace `YOUR_USERNAME` with your actual macOS username, then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.user.chargewatcher.plist
```

---

## Why macOS Doesn't Do This By Default

macOS does recognize a "Not Charging" state — it occurs when the Mac is connected to a power source that provides enough power to run but not enough to charge the battery. However, Apple doesn't proactively alert you in the case where the adapter is physically plugged in but the wall socket has no power — it just silently runs on battery. This script closes that gap.

References:

- [pmset battery script discussion - Apple Community](https://discussions.apple.com/thread/7049834)
- [If your Mac battery status is "Not Charging" - Apple Support](https://support.apple.com/guide/mac-help/if-your-battery-status-is-not-charging-mh20876/mac)
- [Battery Percentage Boundary Notification Script for macOS - GitHub Gist](https://gist.github.com/brandon1024/74b81564aa0b91aa8287faaa175593e6)
