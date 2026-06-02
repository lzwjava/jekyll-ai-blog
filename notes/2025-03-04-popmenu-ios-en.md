---
audio: false
generated: true
lang: en
layout: post
title: Using PopMenu in iOS
translated: false
type: note
---

To use `pod 'PopMenu', '2.4'` in your iOS project, you’re integrating the PopMenu library (version 2.4) via CocoaPods, a popular dependency manager for iOS. This library provides a pop-up animation menu inspired by apps like Sina Weibo or NetEase. Below are the steps to set it up and use it in your project:

---

### Step 1: Install CocoaPods (if not already installed)

If you don’t have CocoaPods installed on your system, install it first:

1. Open your terminal.
2. Run this command:

   ```bash
   sudo gem install cocoapods
   ```

3. Verify installation:

   ```bash
   pod --version
   ```

---

### Step 2: Set Up Your Podfile

1. Navigate to your Xcode project directory in the terminal:

   ```bash
   cd /path/to/your/project
   ```

2. If you don’t already have a Podfile, create one by running:

   ```bash
   pod init
   ```

3. Open the `Podfile` in a text editor (e.g., `nano Podfile` or use Xcode).
4. Add the following lines to specify the PopMenu pod for your target:

   ```ruby
   platform :ios, '8.0'  # Adjust the iOS version if needed
   target 'YourAppName' do
     use_frameworks!
     pod 'PopMenu', '2.4'
   end
   ```

   - Replace `YourAppName` with the name of your Xcode target.
   - The `use_frameworks!` line is required since PopMenu is likely a framework-based library.

5. Save and close the Podfile.

---

### Step 3: Install the Pod

1. In the terminal, run:

   ```bash
   pod install
   ```

2. This downloads and integrates PopMenu version 2.4 into your project. Wait until you see a message like:

   ```
   Pod installation complete! There are X dependencies from the Podfile and X total pods installed.
   ```

3. Close your Xcode project if it’s open, then open the newly generated `.xcworkspace` file (e.g., `YourAppName.xcworkspace`) instead of the `.xcodeproj` file.

---

### Step 4: Basic Usage in Your Code

PopMenu is written in Objective-C, so you’ll need to use it accordingly. Here’s an example of how to implement it in your app:

1. **Import the Library**:
   - In your Objective-C file (e.g., `ViewController.m`):

     ```objective-c
     #import "PopMenu.h"
     ```

   - If you’re using Swift, create a bridging header:
     - Go to `File > New > File > Header File` (e.g., `YourAppName-Bridging-Header.h`).
     - Add:

       ```objective-c
       #import "PopMenu.h"
       ```

     - In Xcode, set the bridging header under `Build Settings > Swift Compiler - General > Objective-C Bridging Header` to the path of your header file (e.g., `YourAppName/YourAppName-Bridging-Header.h`).

2. **Create Menu Items**:
   Define the items you want in the pop-up menu. Each item can have a title, icon, and glow color.

   ```objective-c
   NSMutableArray *items = [[NSMutableArray alloc] init];

   MenuItem *menuItem1 = [[MenuItem alloc] initWithTitle:@"Flickr"
                                               iconName:@"post_type_bubble_flickr"
                                              glowColor:[UIColor grayColor]
                                                  index:0];
   [items addObject:menuItem1];

   MenuItem *menuItem2 = [[MenuItem alloc] initWithTitle:@"Twitter"
                                               iconName:@"post_type_bubble_twitter"
                                              glowColor:[UIColor blueColor]
                                                  index:1];
   [items addObject:menuItem2];
   ```

3. **Initialize and Show the Menu**:
   Create a `PopMenu` instance and display it in your view.

   ```objective-c
   PopMenu *popMenu = [[PopMenu alloc] initWithFrame:self.view.bounds items:items];
   popMenu.menuAnimationType = kPopMenuAnimationTypeNetEase; // Options: kPopMenuAnimationTypeSina or kPopMenuAnimationTypeNetEase
   popMenu.perRowItemCount = 2; // Number of items per row
   [popMenu showMenuAtView:self.view];
   ```

4. **Handle Selection (Optional)**:
   You can subclass or extend functionality to detect taps, though PopMenu’s basic version (circa 2.4) may not natively support a delegate out of the box. Check the library’s documentation on GitHub (`xhzengAIB/PopMenu`) for any updates or customizations.

---

### Step 5: Run Your Project

Build and run your project (`Cmd + R`) in Xcode. If the icons (e.g., `post_type_bubble_flickr`) are part of your asset catalog, ensure they’re added to your project. If not, you’ll need to source or create them.

---

### Notes

- **Version Specificity**: `pod 'PopMenu', '2.4'` locks you to version 2.4. If you want the latest version, use `pod 'PopMenu'` without a version number, but this might introduce breaking changes.
- **Compatibility**: Ensure your project’s deployment target is at least iOS 8.0 (or adjust the `platform` in the Podfile).
- **Customization**: PopMenu allows animation type and layout tweaks (e.g., `perRowItemCount`). Explore the source code for more options.
- **Troubleshooting**: If you encounter errors like “file not found,” ensure your Pods are correctly installed and your workspace is in use.

This should get you started with PopMenu 2.4 in your iOS app! Let me know if you need further clarification.
