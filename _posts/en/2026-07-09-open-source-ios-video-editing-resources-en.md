---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source iOS Video Editing Resources
translated: false
type: note
---

Question: You're looking for an iOS video editor (preferably open source) that has an editing workflow similar to InShot: extract audio from a video, add/remove audio tracks, insert videos, and a timeline where the "Add" button is on the left. You also want open-source editing software you can study.

Answer:

The UI you're describing is the standard mobile NLE (non-linear editor) workflow:

```
Timeline

+ Add Video   + Audio
----------------------------
Video Track
Audio Track
Text Track
Sticker Track
```

InShot, CapCut, and VN Video Editor all follow roughly this design.

### Open-source iOS video editors

Unfortunately, there are **very few mature open-source iOS video editors** on the App Store. Most commercial apps (InShot, CapCut, VN, LumaFusion) are closed source.

The best open-source projects to study are:

| Project          | iOS | Timeline | Audio editing | Notes                           |
| ---------------- | --- | -------- | ------------- | ------------------------------- |
| Kdenlive         | No  | ✅        | ✅             | Excellent architecture (Qt/C++) |
| OpenShot Studios | No  | ✅        | ✅             | Python/C++, easy to understand  |
| Olive Team       | No  | ✅        | ✅             | Modern timeline implementation  |
| Shotcut          | No  | ✅        | ✅             | Uses MLT framework              |

These aren't iOS apps, but they contain solid timeline and editing logic that can be ported.

---

### Open-source iOS frameworks

If you're building your own editor, these are more useful than finding a full app.

#### 1. GPUImage 2

Created by Brad Larson.

Features:

* filters
* camera
* video processing
* Metal/OpenGL

Great for effects.

---

#### 2. NextLevel

A Swift framework for:

* recording
* trimming
* exporting
* AVFoundation wrapper

Very clean codebase.

---

#### 3. VideoLab

Swift timeline editing.

Supports:

* multiple clips
* overlays
* audio
* transitions
* export

Probably one of the closest open-source libraries to an editor.

---

#### 4. PryntTrimmerView

Very popular trimming UI.

Provides the familiar:

```
|------video------|
^                 ^
left handle   right handle
```

---

#### 5. BBMetalImage

Modern Metal replacement for GPUImage.

---

### Commercial apps worth studying

These have excellent UX even though they're closed source.

![Image](https://images.openai.com/static-rsc-4/Gzw1Sj74z21BJ1Mw7g54f4bgo9b-5fsRZQ-fdm3-B2hp15b-R2mWRM7XTTXnH0J7zExYmtpRxd21vb0hsvdeisqAN7YtpLOudBUJ97X8OC56mJkCV5e-O2dbgetuhjudHkbfBNEWmCzoWxeCWrmlrHXHNCsGdsIRJKNukH8e5oQZ5HXSqJNCsqlVz5-ZOgBY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qry3qYJzMXhd3pnqYQFMMzV7-zZMtj1skB5kWMU1qUF51lCGKjzttMgtMN2W5CFPGAe0DYXYkQ8DMGznKUxUU3MtMjhib5sW6igKHl3N9n-h4WTCMselVYGauQXwDaHS88dMG8w0HWer1Z1J_-5LdmN4C4qowRb3srFLd_kWNkeymxYVdjoubnVb_0g9VQXF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/z5mTPOP26stDrl2HdQLEEmgrgHnG6sJv2gGDgh7giuMt0r5WnG0Xr3Oz3Q5EFOrKxo6Co6CM_IJR-XZapn2uwzcn7DthS-jHB4UE6ANAHcLIDE8bnIAKpzb_BaUJVu_yDqSzswMAmKzsbqhCqqTAXi78alk53HVg23r0haWY8Ns2QFPsNxTzNAzIKmFZaKfk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tuQbToZFFXByZ8mJP48JOnczRCrPiR8mqRrbhxpxhsLawSyRJs1HObfG6UfAKLPc2_XHTmyrKvO-t7vjQ7gw367jFwsSd_k5MtWvgOrydcpdJGw5tXxbdxi3_c8mX7zkaE4DGoMBnStisIWC-XHxMarMVPifHQHgQyNfq9UZP1L5xJJ2IoG99rGIldEjdyKr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yylzP0lvoK-bH2PkvHwqGOAVNZsTr0WfnXya4EPKnQGxaTDFVoeF0rpcI5JuUGIg7RK8tP2qsnitQMFTsQtzyQJ0m5vOMl-c6nxuqnA9ynD1oQ9VtkTRqVZt3S4-ZHsYQi7Es8qMERxHVMsuwxjR6SX0Y8A9EpWzqFLBRd-vDsnEmzUkMYNIgeo6OSVuQI0C?purpose=fullsize)

* InShot

  * Extract Audio
  * Voiceover
  * Music
  * Stickers
  * Very simple timeline

* CapCut

  * multi-track
  * keyframes
  * audio extraction
  * AI features

* VN Video Editor

  * closest to desktop editors
  * free
  * multi-track

* LumaTouch's LumaFusion

  * arguably the best professional iOS editor
  * excellent timeline architecture

---

### If you're implementing it yourself

Apple already provides nearly everything through **AVFoundation**.

Typical architecture:

```
Project
├── VideoTrack
│     clip1
│     clip2
│
├── AudioTrack
│     extracted audio
│     music.mp3
│
├── TextTrack
│
└── StickerTrack
```

Operations become:

```
Insert Clip

Extract Audio

Delete Audio

Move Clip

Split Clip

Trim Clip

Export
```

Export is typically done with:

```
AVMutableComposition

AVMutableVideoComposition

AVAssetExportSession
```

This is also how many commercial editors are built internally.

### If your goal is to build an InShot-like editor

I'd recommend studying, in this order:

1. **VideoLab** (Swift timeline composition)
2. **NextLevel** (recording and capture)
3. **PryntTrimmerView** (trim UI)
4. Apple's AVFoundation sample code
5. Kdenlive/OpenShot for larger-scale timeline architecture

This combination gets you much closer to a production-quality iOS editor than searching for a fully open-source InShot clone, because there currently isn't a mature open-source iOS app that matches InShot's feature set.

References:

* [https://github.com/ruanjx/VideoLab](https://github.com/ruanjx/VideoLab)
* [https://github.com/NextLevel/NextLevel](https://github.com/NextLevel/NextLevel)
* [https://github.com/HHK1/PryntTrimmerView](https://github.com/HHK1/PryntTrimmerView)
* [https://github.com/BradLarson/GPUImage2](https://github.com/BradLarson/GPUImage2)
* [https://github.com/MetalPetal/BBMetalImage](https://github.com/MetalPetal/BBMetalImage)
* [https://developer.apple.com/documentation/avfoundation](https://developer.apple.com/documentation/avfoundation)