---
audio: false
generated: true
lang: en
layout: post
title: Using iVersion in iOS
translated: false
type: note
---

To use the `iVersion` pod in your iOS project, you need to follow these steps:

1. **Open Your Project in Xcode**: Make sure you have your Xcode project open where you want to add the `iVersion` pod.

2. **Initialize CocoaPods**: If you haven't already initialized CocoaPods in your project, open the Terminal, navigate to your project directory, and run:

   ```bash
   pod init
   ```

   This will create a `Podfile` in your project directory.

3. **Edit the Podfile**: Open the `Podfile` in a text editor or Xcode. Add the `iVersion` pod to your `Podfile` by including the following line within the target section:

   ```ruby
   pod 'iVersion', '1.11.4'
   ```

4. **Install the Pod**: Save the `Podfile` and go back to the Terminal. Run the following command to install the `iVersion` pod:

   ```bash
   pod install
   ```

5. **Open the `.xcworkspace` File**: After the installation is complete, close your Xcode project if it's open, and then open the newly created `.xcworkspace` file. This file is usually located in the same directory as your original `.xcodeproj` file.

6. **Import iVersion**: In your Swift or Objective-C files, import the `iVersion` module to start using it:

   ```swift
   import iVersion
   ```

7. **Use iVersion in Your Code**: Now you can use the `iVersion` library in your project. For example, you can check the app version or build number using the methods provided by `iVersion`.

By following these steps, you should be able to successfully integrate and use the `iVersion` pod in your iOS project.
