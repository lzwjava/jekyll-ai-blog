---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apple Vision Pro SDK Stack
translated: false
type: note
---

Question: **What SDK does Apple provide for Vision Pro / VR glasses?**

Answer: Apple Vision Pro is primarily developed through the **visionOS SDK**. It is not just a generic VR SDK; Apple exposes a fairly deep spatial-computing stack:

```text
                    visionOS
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     SwiftUI       RealityKit       ARKit
        │              │              │
   UI / windows     3D rendering    spatial sensing
        │              │              │
        └──────────────┼──────────────┘
                       │
               Apple Vision Pro
```

### The important APIs

| Framework                             | What you use it for                        |
| ------------------------------------- | ------------------------------------------ |
| **visionOS SDK**                      | Platform/application APIs                  |
| **SwiftUI**                           | Windows, spatial UI, gestures              |
| **RealityKit**                        | 3D rendering, entities, physics, animation |
| **ARKit**                             | World/hand/plane/image/scene tracking      |
| **Reality Composer Pro**              | Authoring 3D scenes/assets                 |
| **Metal**                             | Low-level GPU rendering                    |
| **UIKit**                             | Existing iOS-style UI compatibility        |
| **AVFoundation / spatial media APIs** | Audio/video and immersive media            |
| **Unity**                             | Alternative game/3D engine integration     |

Apple's recommended path for native spatial apps is basically:

```swift
import SwiftUI
import RealityKit

struct ContentView: View {
    var body: some View {
        RealityView { content in
            let box = ModelEntity(
                mesh: .generateBox(size: 0.2),
                materials: [SimpleMaterial()]
            )

            content.add(box)
        }
    }
}
```

Then for **actual perception of the physical environment**, you use ARKit:

```text
Vision Pro sensors
      │
      ▼
    ARKit
      │
 ┌────┼───────────┐
 │    │           │
hand world      planes
tracking tracking detection
 │    │           │
 └────┼───────────┘
      ▼
   RealityKit
      │
      ▼
  your 3D app
```

Apple explicitly exposes APIs for **hand tracking, world tracking, plane estimation, image anchoring, scene reconstruction**, etc. ([Apple Developer][1])

One particularly interesting distinction from ordinary ARKit on iPhone: **visionOS handles compositing your app into the user's environment**. You generally don't grab the camera image and render an AR overlay yourself. Your app provides content, while visionOS manages the spatial presentation. ([Apple Developer][2])

And as of the current visionOS documentation, Apple is also adding things like **object tracking** and **Gaussian splat APIs in RealityKit**. ([Apple Developer][3])

So if you're thinking about your **AI-only camera/audio device idea**, Vision Pro is actually a useful reference architecture:

```text
camera / microphones / sensors
            ↓
      spatial perception
            ↓
         AI model
            ↓
   spatial UI / voice / 3D
```

The key difference is that Apple's SDK gives you the **sensor + spatial-computing layer**, while you can put your own AI inference/agent layer on top.

References:

* [Apple visionOS Developer Platform](https://developer.apple.com/visionos/?utm_source=chatgpt.com)
* [Apple visionOS Documentation](https://developer.apple.com/documentation/visionos?utm_source=chatgpt.com)
* [RealityKit Documentation](https://developer.apple.com/documentation/realitykit?utm_source=chatgpt.com)

I can also map **Vision Pro's available sensors → APIs → what raw data an AI agent can actually access**, which is probably the more interesting part if you're evaluating it as an AI hardware platform.

[1]: https://developer.apple.com/visionos/?utm_source=chatgpt.com "visionOS - Apple Developer"
[2]: https://developer.apple.com/documentation/visionos/bringing-your-arkit-app-to-visionos?utm_source=chatgpt.com "Bringing your ARKit app to visionOS | Apple Developer Documentation"
[3]: https://developer.apple.com/documentation/visionos?changes=_2_1__1&utm_source=chatgpt.com "visionOS | Apple Developer Documentation"
