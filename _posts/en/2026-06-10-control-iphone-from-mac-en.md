---
audio: false
generated: true
image: false
lang: en
layout: post
title: Control iPhone from Mac
translated: false
type: note
---

**Question:** Can a Mac connect to an iPhone (e.g., over Bluetooth) to remotely control it — sending swipe up/down gestures to scroll TikTok videos?

**Answer:**

Yes — three viable routes, from zero-code to fully scriptable. Note the one thing that *doesn't* work: macOS can't natively act as a **Bluetooth HID peripheral** (keyboard/mouse server), so "Mac pretends to be a Bluetooth mouse for the iPhone" is the only path that's blocked without extra hardware.

## Option 1 — iPhone Mirroring (zero code, macOS 15+ / iOS 18+)

Apple's official solution. Mac and iPhone pair over Bluetooth/Wi-Fi; the iPhone screen streams to a Mac window and your trackpad gestures (two-finger swipe = screen swipe) pass through. Open TikTok in the mirror window, two-finger swipe up → next video. Works locked-screen, no cables.

Setup: same Apple ID, Bluetooth + Wi-Fi on, then on Mac: `open -a "iPhone Mirroring"`.

Limitation: it's interactive only — you can't script it cleanly (the window accepts synthetic scroll events inconsistently, and Apple actively sandboxes it).

## Option 2 — Programmatic swipes via WebDriverAgent (the builder route)

This is what you want if the goal is *automated* shuffling (e.g., "swipe every N seconds", or an agent deciding when to swipe). WDA runs an XCUITest server on the iPhone; you drive it from Python over USB or Wi-Fi.

One-time setup:

```bash
# 1. Clone & sign WDA with your free Apple ID in Xcode (set your own team)
git clone https://github.com/appium/WebDriverAgent
open WebDriverAgent/WebDriverAgent.xcodeproj
# Product > Test on your iPhone once, trust the dev cert on device

# 2. Python client
pip install facebook-wda tidevice
tidevice wdaproxy -B com.<yourname>.WebDriverAgentRunner.xctrunner --port 8100
```

Then the swipe loop is ~10 lines:

```python
import wda, time, random

c = wda.Client("http://localhost:8100")
c.app_launch("com.zhiliaoapp.musically")  # TikTok bundle ID

while True:
    c.swipe(0.5, 0.8, 0.5, 0.2, duration=0.2)   # swipe up = next video
    time.sleep(random.uniform(5, 12))            # human-ish dwell time
```

`c.swipe(0.5, 0.2, 0.5, 0.8)` goes back (swipe down). Coordinates are screen-relative floats, so it's resolution-independent. You can layer an LLM on top trivially — screenshot via `c.screenshot()`, feed to a vision model, decide swipe/like/skip. That's a TikTok agent in <100 lines.

Caveat: WDA signed with a free Apple ID expires every 7 days; a paid developer account ($99/yr) extends to a year. Appium is the same engine with more ceremony — `facebook-wda` direct is leaner.

## Option 3 — True Bluetooth HID via ESP32 (~$5 hardware)

If you specifically want the Bluetooth-mouse model: flash an ESP32 with [ESP32-BLE-Mouse](https://github.com/T-vK/ESP32-BLE-Mouse), pair it to the iPhone (iOS 13+ supports BLE mice via AssistiveTouch), and have your Mac send commands to the ESP32 over USB serial:

```cpp
// ESP32 sketch: serial byte 'u' -> drag up gesture
#include <BleMouse.h>
BleMouse mouse;
void setup() { Serial.begin(115200); mouse.begin(); }
void loop() {
  if (Serial.read() == 'u') {
    mouse.press();
    for (int i=0; i<30; i++) { mouse.move(0,-10); delay(8); }
    mouse.release();
  }
}
```

```python
# Mac side
import serial, time
s = serial.Serial('/dev/tty.usbserial-XXXX', 115200)
while True:
    s.write(b'u'); time.sleep(8)
```

This is jailbreak-free, app-agnostic, and survives iOS updates — the iPhone just thinks a mouse is dragging. Downside: AssistiveTouch pointer must be enabled, and the drag emulation is slightly less crisp than a finger flick.

**Recommendation:** Option 1 if you just want to lean back and scroll from your Air; Option 2 if you're building automation (it composes naturally with your agent tooling — `wda` + a vision model is a real "AI watches TikTok" project); Option 3 if you want hardware-level robustness.

**References:**

- [facebook-wda (Python WDA client)](https://github.com/openatx/facebook-wda)
- [WebDriverAgent](https://github.com/appium/WebDriverAgent)
- [ESP32-BLE-Mouse](https://github.com/T-vK/ESP32-BLE-Mouse)
- [Apple — iPhone Mirroring](https://support.apple.com/en-us/120421)
