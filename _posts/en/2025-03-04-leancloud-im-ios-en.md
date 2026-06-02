---
audio: false
generated: true
lang: en
layout: post
title: LeanCloud Realtime iOS SDK
translated: false
type: note
---

To use the `pod 'AVOSCloudIM', '3.1.6.2'` in your iOS project with CocoaPods, follow these steps. This assumes you have CocoaPods installed and are familiar with basic iOS development using Xcode.

---

### Step 1: Set Up CocoaPods (if not already done)
If you haven’t installed CocoaPods yet, install it via the terminal:
```bash
sudo gem install cocoapods
```
Verify the installation:
```bash
pod --version
```

---

### Step 2: Create or Open Your Xcode Project
1. Open your existing Xcode project or create a new one in Xcode.
2. Close Xcode for now (we’ll reopen it later with the workspace).

---

### Step 3: Initialize a Podfile
1. Open your terminal and navigate to your project’s root directory (where the `.xcodeproj` file is located):
   ```bash
   cd /path/to/your/project
   ```
2. If you don’t already have a Podfile, create one by running:
   ```bash
   pod init
   ```
   This generates a basic `Podfile` in your project directory.

---

### Step 4: Edit the Podfile
1. Open the `Podfile` in a text editor (e.g., `nano`, `vim`, or any code editor like VS Code):
   ```bash
   open Podfile
   ```
2. Modify the `Podfile` to include the `AVOSCloudIM` pod with version `3.1.6.2`. Here’s an example of what your `Podfile` might look like:
   ```ruby
   platform :ios, '9.0'  # Specify the minimum iOS version (adjust as needed)
   use_frameworks!       # Optional: Use this if your project uses Swift or frameworks

   target 'YourAppName' do
     pod 'AVOSCloudIM', '3.1.6.2'  # Add this line to include AVOSCloudIM version 3.1.6.2
   end
   ```
   - Replace `'YourAppName'` with the actual name of your Xcode target (usually the name of your app).
   - The `platform :ios, '9.0'` line specifies the minimum iOS version; adjust it based on your project’s requirements.
   - `use_frameworks!` is needed if your project uses Swift or if the pod requires dynamic frameworks.

3. Save and close the `Podfile`.

---

### Step 5: Install the Pod
1. In the terminal, run the following command from your project’s root directory:
   ```bash
   pod install
   ```
   - This downloads and integrates the `AVOSCloudIM` library (version 3.1.6.2) into your project.
   - If successful, you’ll see output like:
     ```
     Pod installation complete! There are X dependencies from the Podfile and X total pods installed.
     ```

2. If you encounter errors (e.g., pod not found), ensure the version `3.1.6.2` is still available in the CocoaPods repository. Older versions might not be supported anymore. You can check the latest version on [CocoaPods.org](https://cocoapods.org) under `AVOSCloudIM` or update to a newer version (e.g., `pod 'AVOSCloudIM', '~> 12.3'`).

---

### Step 6: Open the Workspace
1. After installation, a `.xcworkspace` file will be created in your project directory (e.g., `YourAppName.xcworkspace`).
2. Open this file in Xcode:
   ```bash
   open YourAppName.xcworkspace
   ```
   - From now on, always use the `.xcworkspace` file instead of the `.xcodeproj` file to work with your project.

---

### Step 7: Import and Use AVOSCloudIM in Your Code
1. In your Swift or Objective-C files, import the `AVOSCloudIM` module:
   - **Swift**:
     ```swift
     import AVOSCloudIM
     ```
   - **Objective-C**:
     ```objc
     #import <AVOSCloudIM/AVOSCloudIM.h>
     ```
2. Start using the library’s features. `AVOSCloudIM` is part of the LeanCloud SDK, typically used for real-time messaging. Refer to the [LeanCloud documentation](https://leancloud.app/docs/) for specific usage examples, such as setting up a chat client:
   - Example (Swift):
     ```swift
     let client = AVIMClient(clientId: "yourClientID")
     client.open { (succeeded, error) in
         if succeeded {
             print("Connected to LeanCloud IM!")
         } else {
             print("Error: \\(error?.localizedDescription ?? "Unknown")")
         }
     }
     ```

---

### Step 8: Configure Your Project (if needed)
- **App Key and Initialization**: LeanCloud SDKs often require an app ID and key. Add this initialization code (e.g., in `AppDelegate`):
  - **Swift**:
    ```swift
    import AVOSCloud
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        AVOSCloud.setApplicationId("yourAppID", clientKey: "yourAppKey")
        return true
    }
    ```
  - Replace `"yourAppID"` and `"yourAppKey"` with credentials from your LeanCloud account.
- **Permissions**: Ensure your app has the necessary permissions (e.g., internet access) in `Info.plist`:
  ```xml
  <key>NSAppTransportSecurity</key>
  <dict>
      <key>NSAllowsArbitraryLoads</key>
      <true/>
  </dict>
  ```

---

### Notes
- **Version Specificity**: Using `pod 'AVOSCloudIM', '3.1.6.2'` locks you to that exact version. If you want flexibility for minor updates, use `~>` (e.g., `pod 'AVOSCloudIM', '~> 3.1.6'` allows updates like 3.1.6.1 but not 3.2).
- **Troubleshooting**: If `pod install` fails, try:
  - Updating CocoaPods: `sudo gem install cocoapods`
  - Clearing the cache: `pod cache clean --all`
  - Running `pod repo update` to refresh the local CocoaPods spec repository.
- **LeanCloud SDK**: Since `AVOSCloudIM` is part of LeanCloud, ensure you follow their setup guide for additional configuration (e.g., registering on their platform).

---

That’s it! You’ve now integrated `AVOSCloudIM` version 3.1.6.2 into your iOS project. Build and run your app in Xcode to test it. Let me know if you need help with specific LeanCloud features!
