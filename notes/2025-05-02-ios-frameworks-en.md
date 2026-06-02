---
audio: false
generated: true
lang: en
layout: post
title: iOS Frameworks
translated: false
type: note
---

Besides UIKit, there are many other essential frameworks provided by the iOS system that developers commonly use to build applications. These frameworks handle various aspects beyond just the user interface elements. Here are some of the most common ones:

1.  **Foundation:** This is a fundamental framework that provides basic data types (like strings, numbers, arrays, dictionaries), collection types, operating system services, and core programming patterns. It's the bedrock for many other frameworks and is almost always imported into an iOS project. It includes essential components like `URLSession` for networking, `FileManager` for file system interactions, and `NotificationCenter` for managing notifications within an application.

2.  **Core Data:** This framework provides a robust and flexible way to manage the model layer objects in your application. It allows you to persist data, manage object graphs, and handle data synchronization. While often described as a database technology, it's more accurately an object graph management framework that can use different persistent stores, such as SQLite, binary files, or in-memory storage.

3.  **Core Animation:** This framework is used to create smooth, high-performance animations and visual effects. It works alongside UIKit (or AppKit on macOS) to render animated content. You can use it to animate views, layers, and other graphical elements, creating complex transitions and effects without directly manipulating pixels.

4.  **Core Graphics:** Also known as Quartz 2D, this is a C-based drawing engine that provides low-level, 2D rendering capabilities. It allows you to draw points, lines, paths, shapes, and images with high fidelity. While UIKit provides higher-level abstractions for drawing, Core Graphics is often used for custom drawing operations, creating gradients, managing contexts, and working directly with graphical primitives.

5.  **AVFoundation:** This framework provides a comprehensive set of tools for working with time-based audiovisual media. You can use it to play, record, and edit audio and video. It gives you control over cameras, microphones, playback engines, and media assets, making it essential for apps that involve multimedia content.

6.  **Core Location:** This framework allows your application to access location services on the device, such as the user's current geographical location, altitude, and heading. It can use GPS, Wi-Fi, and cellular signals to determine location and supports features like region monitoring and geofencing.

7.  **UserNotifications:** This framework is used to schedule and handle local and remote notifications. It allows your app to inform users of important events even when the app is not actively running, displaying alerts, playing sounds, or updating badges on the app icon.

8.  **SwiftUI:** While UIKit is the traditional framework for building user interfaces with an imperative approach, SwiftUI is a newer, declarative framework introduced by Apple for building user interfaces across all Apple platforms. It provides a different paradigm for UI development and is increasingly common in modern iOS development, often used alongside or as an alternative to UIKit, especially for new projects or features.

These frameworks, along with many others like Metal (for graphics acceleration), SpriteKit (for 2D games), SceneKit (for 3D graphics), and Core ML (for machine learning), form the powerful ecosystem that iOS developers leverage to create diverse and feature-rich applications.
