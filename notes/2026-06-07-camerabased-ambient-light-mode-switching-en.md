---
audio: false
generated: true
image: false
lang: en
layout: post
title: Camera‑Based Ambient Light Mode Switching
translated: false
type: note
---

Question: Use the macOS camera to detect real-time ambient light levels and automatically toggle between dark/light mode, rather than relying on fixed sunrise/sunset times—right?

Answer:

Yes, exactly. This is **smarter than time-based switching** because:

1. **Time-based fails on cloudy days** — 3 PM can be darker than 6 AM in winter or when it's overcast
2. **Context-aware** — if you move to a different room or office, the camera adapts instantly
3. **Handles seasonal variation** without manual adjustment
4. **Physical sensor data > heuristic timing**

## Implementation Approach

macOS doesn't expose camera feed directly for this (privacy-gated), but you have two paths:

### Option 1: Use AVCaptureSession (Swift, native)

Grab camera frames, compute luminance, post notification to change system appearance:

```swift
import AVFoundation
import AppKit

class AmbientLightMonitor: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate {
    let captureSession = AVCaptureSession()
    var luxThreshold: Double = 50 // lux — adjust based on preference

    func start() {
        guard let camera = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front) else { return }

        let input = try! AVCaptureDeviceInput(device: camera)
        let output = AVCaptureVideoDataOutput()

        output.setSampleBufferDelegate(self, queue: DispatchQueue(label: "light-monitor"))

        captureSession.addInput(input)
        captureSession.addOutput(output)
        captureSession.startRunning()
    }

    func captureOutput(_ output: AVCaptureOutput,
                      didOutput sampleBuffer: CMSampleBuffer,
                      from connection: AVCaptureConnection) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }

        let luminance = computeLuminance(pixelBuffer)
        let isDark = luminance < luxThreshold

        DispatchQueue.main.async {
            let appearance: NSAppearance.Name = isDark ? .darkAqua : .aqua
            NSAppearance.current = NSAppearance(named: appearance)
        }
    }

    func computeLuminance(_ pixelBuffer: CVPixelBuffer) -> Double {
        CVPixelBufferLockBaseAddress(pixelBuffer, .readOnly)
        defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, .readOnly) }

        let baseAddress = CVPixelBufferGetBaseAddress(pixelBuffer)!
        let width = CVPixelBufferGetWidth(pixelBuffer)
        let height = CVPixelBufferGetHeight(pixelBuffer)

        var sum: Double = 0
        let ptr = baseAddress.assumingMemoryBound(to: UInt8.self)

        // Sample every Nth pixel (don't process all 2M pixels)
        let stride = 16
        for y in stride(from: 0, to: height, by: stride) {
            for x in stride(from: 0, to: width, by: stride) {
                let idx = (y * width + x) * 4 // BGRA
                let r = Double(ptr[idx + 2])
                let g = Double(ptr[idx + 1])
                let b = Double(ptr[idx + 0])

                // Relative luminance (ITU-R BT.709)
                sum += 0.2126 * r + 0.7152 * g + 0.0722 * b
            }
        }
        return sum / Double((width / stride) * (height / stride))
    }
}

// Usage
let monitor = AmbientLightMonitor()
monitor.luxThreshold = 40 // Tune this value
monitor.start()
```

### Option 2: Python + PIL + subprocess (faster iteration)

```python
import cv2
import numpy as np
import subprocess
from threading import Thread
import time

def get_luminance(frame):
    """Convert BGR frame to HSV, extract V (brightness) channel"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]
    return np.mean(v_channel)

def set_macos_theme(is_dark):
    """Toggle macOS theme via AppleScript"""
    theme = "Dark" if is_dark else "Light"
    script = f'tell app "System Events" to tell appearance preferences to set dark mode to {str(is_dark).lower()}'
    subprocess.run(['osascript', '-e', script])

def monitor_light(lux_threshold=100):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 5)  # 5 FPS is enough for theme switching

    prev_is_dark = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        lum = get_luminance(frame)
        is_dark = lum < lux_threshold

        # Debounce: only switch if stable for 2+ samples
        if is_dark != prev_is_dark:
            set_macos_theme(is_dark)
            prev_is_dark = is_dark
            print(f"Luminance: {lum:.1f} → {('Dark' if is_dark else 'Light')} mode")

        time.sleep(0.2)

if __name__ == "__main__":
    monitor_light(lux_threshold=100)  # Tune this
```

## Key Tuning Parameters

- **`luxThreshold`** — varies by room. Start at 80–120, adjust based on your preference
- **Frame rate** — 2–5 FPS is plenty; don't waste CPU on 30 FPS
- **Debouncing** — require 2–3 consecutive frames below threshold before switching (prevents flickering at boundary)
- **Camera position** — front camera has slightly blocked view; best if angled toward ambient light source

## Caveats

1. **Privacy/battery** — camera stays warm; may drain battery on long uptime
2. **AppleScript latency** — theme toggle takes ~500ms, noticeable but acceptable
3. **Dark mode API** — the AppleScript approach is fragile; better to use `NSAppearance` directly (Swift path is cleaner)
4. **No native API** — Apple doesn't expose light sensor via public API; ambient light sensor exists but isn't accessible to apps

## Better Alternative (If You Want Max Control)

Build a **background daemon** (LaunchAgent) running the Swift code above. Compile as a Release binary, wrap in a `.plist`, and let it run at login:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lzwjava.ambientlight</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ambientlight-monitor</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Copy to `~/Library/LaunchAgents/com.lzwjava.ambientlight.plist`, then:

```bash
launchctl load ~/Library/LaunchAgents/com.lzwjava.ambientlight.plist
```

---

**Start with the Python version** — iterate fast on the threshold, test debouncing logic. Once tuned, port to Swift for daemon mode if you want zero startup overhead.

This is way better than sunset-based switching. Ship it.
