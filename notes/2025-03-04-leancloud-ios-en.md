---
audio: false
generated: true
lang: en
layout: post
title: LeanCloud iOS SDK
translated: false
type: note
---

To use the `pod 'AVOSCloud', '3.1.6.2'` in an iOS project, you're referring to integrating the AVOSCloud SDK (likely LeanCloud's SDK for cloud services) via CocoaPods, a dependency manager for iOS projects. Here's a step-by-step guide to set it up:

---

### Prerequisites

1. **Install CocoaPods**: If you don’t have CocoaPods installed, install it first by running this in your terminal:

   ```bash
   sudo gem install cocoapods
   ```

2. **Xcode Project**: Ensure you have an existing iOS project in Xcode.

---

### Steps to Use `pod 'AVOSCloud', '3.1.6.2'`

1. **Navigate to Your Project Directory**:
   Open your terminal and go to the directory containing your `.xcodeproj` file:

   ```bash
   cd /path/to/your/project
   ```

2. **Initialize a Podfile** (if you don’t already have one):
   Run the following command to create a `Podfile`:

   ```bash
   pod init
   ```

3. **Edit the Podfile**:
   Open the `Podfile` in a text editor (e.g., `nano Podfile` or `open Podfile`) and add the `AVOSCloud` pod with the specific version `3.1.6.2`. Your `Podfile` should look something like this:

   ```ruby
   platform :ios, '9.0'  # Specify the minimum iOS version (adjust as needed)

   target 'YourAppName' do
     use_frameworks!
     pod 'AVOSCloud', '3.1.6.2'  # Add this line for AVOSCloud SDK
   end
   ```

   - Replace `'YourAppName'` with the actual name of your Xcode target.
   - `use_frameworks!` is required if you're using Swift or dynamic frameworks.

4. **Install the Pod**:
   Save the `Podfile`, then run this command in the terminal to install the specified version of AVOSCloud:

   ```bash
   pod install
   ```

   - This will download version `3.1.6.2` of the AVOSCloud SDK and set up your project with a `.xcworkspace` file.

5. **Open the Workspace**:
   After installation, close your `.xcodeproj` if it’s open, and open the newly created `.xcworkspace` file:

   ```bash
   open YourAppName.xcworkspace
   ```

6. **Import and Use AVOSCloud in Your Code**:
   - In Objective-C:

     ```objc
     #import <AVOSCloud/AVOSCloud.h>

     - (void)example {
         [AVOSCloud setApplicationId:@"your_app_id" clientKey:@"your_client_key"];
         AVObject *testObject = [AVObject objectWithClassName:@"TestObject"];
         [testObject setObject:@"Hello" forKey:@"message"];
         [testObject save];
     }
     ```

   - In Swift:

     ```swift
     import AVOSCloud

     func example() {
         AVOSCloud.setApplicationId("your_app_id", clientKey: "your_client_key")
         let testObject = AVObject(className: "TestObject")
         testObject["message"] = "Hello"
         try? testObject.save()
     }
     ```

   - Replace `"your_app_id"` and `"your_client_key"` with your LeanCloud app credentials from their dashboard.

7. **Configure App Credentials**:
   - Sign up at [LeanCloud](https://leancloud.app) (or the relevant AVOSCloud service provider).
   - Get your `App ID` and `Client Key` from your app’s settings and set them in your code (as shown above).

8. **Build and Run**:
   Build your project in Xcode (`Cmd + B`) to ensure everything is set up correctly. If there are errors, check your Podfile syntax or network connection.

---

### Notes

- **Version Specific**: By specifying `'3.1.6.2'`, you’re locking the SDK to that exact version. This might be outdated as of March 03, 2025. To use the latest version, simply write `pod 'AVOSCloud'` without a version number.
- **Compatibility**: Ensure version `3.1.6.2` supports your iOS deployment target (e.g., iOS 9.0 or higher). Check the [LeanCloud documentation](https://leancloud.app/docs) for details.
- **Pod Update**: If you need to update CocoaPods or troubleshoot, run:

  ```bash
  pod update
  ```

- **Troubleshooting**: If `pod install` fails, try:

  ```bash
  pod repo update
  pod install --verbose
  ```

---

Let me know if you need help with a specific part, like integrating a feature (e.g., push notifications, real-time messaging) from AVOSCloud!
