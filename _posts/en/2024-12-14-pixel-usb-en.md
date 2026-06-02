---
audio: false
generated: false
image: true
lang: en
layout: post
title: Pixel USB, iOS Developer Tools, Swipe Typing
translated: false
type: post
---

### Table of Contents

1. [Pixel's USB Options](#pixels-usb-options)
   - Use Pixel as a webcam
   - Enable Developer Mode in settings
   - Activate USB Debugging for connection
   - Verify connection with ADB command

2. [Developer Mode of iOS and ideviceinstaller](#developer-mode-of-ios-and-ideviceinstaller)
   - View installed apps via Xcode
   - Use Xcode for screenshots and logs
   - List apps with xcrun command
   - Install and use ideviceinstaller tool

3. [Quick Swipe Typing](#quick-swipe-typing)
   - Input words by swiping over letters
   - Discovered feature by accident
   - Line appears during fast touch

## Pixel's USB Options

<div style="text-align: center;">
    <img class="responsive" src="/assets/images/pixel/pixel.jpg" alt="Pixel" width="50%" />
</div>

Pixel offers several USB options, and one particularly interesting feature is its ability to function as a webcam. On macOS, QuickTime can access the Android webcam as a video source, providing a simple and effective solution.

To set this up:

1. Navigate to About Phone in the settings and tap Build Number seven times to enable Developer Mode.
2. Open Developer Options and enable USB Debugging.
3. Connect your Pixel to your computer via USB and run the following command in a terminal to verify the connection:

   ```bash
   adb devices
   ```

---

## Developer Mode of iOS and ideviceinstaller

*2024.12.03*

## Developer Mode

I was once an iOS developer for some time. But my career focus has shifted to other technologies. However, it is still very useful to apply iOS development knowledge even though I am not a professional iOS developer now.

Recently, I wanted to share my installed apps. But if I took screenshots of all apps from the home screen or from the app list in settings, it would be a mess. So I needed to find a way to view all installed apps.

Here are the steps to view all installed apps using Xcode:

1. Connect your iPhone to your Mac via USB
2. Open Xcode
3. Go to Window → Devices and Simulators (or press Shift + Cmd + 2)
4. Select your iPhone from the left sidebar
5. In the main panel, scroll down to the "Installed Apps" section

It has other useful functions:

1. Taking screenshots
2. Opening recent logs
3. Opening the console

## xcrun

```bash
(base) lzwjava@192 Downloads % xcrun devicectl device info apps --device 00008120-xxxx --verbose
Using verbose logging.
2024-12-03 16:24:18.579+0800  Enabling developer disk image services.
2024-12-03 16:24:18.637+0800  Acquired usage assertion.
Apps installed:
  - 0 elements

Command Completed, took 0.120 seconds
```

## ideviceinstaller

```bash
brew install ideviceinstaller
ideviceinstaller -l
```

```bash
(base) lzwjava@192 Downloads % ideviceinstaller -l
CFBundleIdentifier, CFBundleVersion, CFBundleDisplayName
com.huawei.smarthome-ios, "14.1.1.325", "HUAWEI AI Life"
com.sf-express.waybillcn, "9.70.0.1", "顺丰速运"
com.roblox.robloxmobile, "2.652.762", "Roblox"
co.alphaexploration.clubhouse, "3273", "Clubhouse"
com.dbs.mbanking.cn, "11", "DBS digibank"
global.longbridge.ios, "59579", "Longbridge"
imgurmobile, "416", "Imgur"
com.creditkarma.mobile, "17316145", "Credit Karma"
...
```

---

## Quick Swipe Typing

*2024.12.01*

If you want to input "threads" in iOS, you just need to quickly draw a line to cover the positions of letters "threads" to get the result. Let's see how it works.

<video width="50%" controls>
  <source src="/assets/images/input/in.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

I accidently found this. When my finger quickly touches the input area, it will show a line. I don't know what that means. After some experiments, I found the above discovery.
