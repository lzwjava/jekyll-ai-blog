---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于摄像头的环境光模式切换
translated: true
type: note
---

问题：使用 macOS 摄像头检测实时环境光亮度，自动切换深色/浅色模式，而不是依赖固定的日出/日落时间——对吗？

回答：

是的，完全正确。这比基于时间的切换更智能，因为：

1. **基于时间的方式在阴天会失效** — 冬季或阴天时，下午3点可能比早上6点更暗
2. **上下文感知** — 如果你移动到不同的房间或办公室，摄像头会立即适配
3. **无需手动调整即可应对季节变化**
4. **物理传感器数据 > 启发式时间算法**

## 实现方法

macOS 没有直接暴露摄像头供此用途（受隐私限制），但你有两条路径：

### 选项 1：使用 AVCaptureSession（Swift，原生）

获取摄像头帧，计算亮度，发送通知以更改系统外观：

```swift
import AVFoundation
import AppKit

class AmbientLightMonitor: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate {
    let captureSession = AVCaptureSession()
    var luxThreshold: Double = 50 // 勒克斯 — 根据偏好调整

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

        // 每第 N 个像素采样（不要处理全部 200 万像素）
        let stride = 16
        for y in stride(from: 0, to: height, by: stride) {
            for x in stride(from: 0, to: width, by: stride) {
                let idx = (y * width + x) * 4 // BGRA
                let r = Double(ptr[idx + 2])
                let g = Double(ptr[idx + 1])
                let b = Double(ptr[idx + 0])

                // 相对亮度（ITU-R BT.709）
                sum += 0.2126 * r + 0.7152 * g + 0.0722 * b
            }
        }
        return sum / Double((width / stride) * (height / stride))
    }
}

// 使用方法
let monitor = AmbientLightMonitor()
monitor.luxThreshold = 40 // 调整此值
monitor.start()
```

### 选项 2：Python + PIL + subprocess（快速迭代）

```python
import cv2
import numpy as np
import subprocess
from threading import Thread
import time

def get_luminance(frame):
    """将 BGR 帧转换为 HSV，提取 V（亮度）通道"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]
    return np.mean(v_channel)

def set_macos_theme(is_dark):
    """通过 AppleScript 切换 macOS 主题"""
    theme = "Dark" if is_dark else "Light"
    script = f'tell app "System Events" to tell appearance preferences to set dark mode to {str(is_dark).lower()}'
    subprocess.run(['osascript', '-e', script])

def monitor_light(lux_threshold=100):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 5)  # 5 FPS 足够用于主题切换

    prev_is_dark = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        lum = get_luminance(frame)
        is_dark = lum < lux_threshold

        # 消抖：仅在稳定超过 2 个采样时才切换
        if is_dark != prev_is_dark:
            set_macos_theme(is_dark)
            prev_is_dark = is_dark
            print(f"亮度: {lum:.1f} → {'深色' if is_dark else '浅色'}模式")

        time.sleep(0.2)

if __name__ == "__main__":
    monitor_light(lux_threshold=100)  # 调整此值
```

## 关键调参参数

- **`luxThreshold`** — 随房间变化。从 80–120 开始，根据偏好调整
- **帧率** — 2–5 FPS 足够；不要浪费 CPU 在 30 FPS 上
- **消抖** — 要求连续 2–3 帧低于阈值才切换（防止边界闪烁）
- **摄像头位置** — 前置摄像头视野略有遮挡；最好朝向环境光源

## 注意事项

1. **隐私/电池** — 摄像头保持打开状态；长时间运行可能耗电
2. **AppleScript 延迟** — 主题切换约需 500ms，可察觉但可接受
3. **深色模式 API** — AppleScript 方法较脆弱；最好直接使用 `NSAppearance`（Swift 方式更干净）
4. **无原生 API** — Apple 未通过公共 API 暴露光传感器；环境光传感器存在但应用无法访问

## 更好的替代方案（如果你想要最大控制权）

构建一个**后台守护进程**（LaunchAgent），运行上述 Swift 代码。编译为 Release 二进制文件，用 `.plist` 包装，并设置为登录时启动：

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

复制到 `~/Library/LaunchAgents/com.lzwjava.ambientlight.plist`，然后：
```bash
launchctl load ~/Library/LaunchAgents/com.lzwjava.ambientlight.plist
```

---

**先从 Python 版本开始** — 快速迭代阈值，测试消抖逻辑。调优后，如果需要零启动开销，再移植到 Swift 作为守护进程模式。

这比基于日落时间的切换好得多。开始实施吧。