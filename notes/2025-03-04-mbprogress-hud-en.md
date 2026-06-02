---
audio: false
generated: true
lang: en
layout: post
title: Using MBProgressHUD in iOS
translated: false
type: note
---

It looks like you're asking about how to use the `MBProgressHUD` library in an iOS project, specifically version `0.9.1`, via a Podfile in CocoaPods. Let me guide you through the process step-by-step.

### What is MBProgressHUD?
`MBProgressHUD` is a popular third-party library for iOS that provides an easy way to display a HUD (Heads-Up Display) with activity indicators, progress bars, or custom views, typically used to show loading states or brief messages.

### Steps to Use `pod 'MBProgressHUD', '0.9.1'`

#### 1. **Install CocoaPods (if not already installed)**
CocoaPods is a dependency manager for iOS projects. If you don’t have it installed, run this command in your terminal:
```bash
sudo gem install cocoapods
```

#### 2. **Set Up a Podfile**
- Navigate to your Xcode project directory in the terminal:
  ```bash
  cd /path/to/your/project
  ```
- If you don’t already have a Podfile, create one by running:
  ```bash
  pod init
  ```
- Open the `Podfile` in a text editor (e.g., `nano Podfile` or `open Podfile`).

#### 3. **Add MBProgressHUD to Your Podfile**
In your `Podfile`, add the line for `MBProgressHUD` version `0.9.1` within the target block for your app. It should look something like this:
```ruby
platform :ios, '9.0'  # Specify your deployment target

target 'YourAppName' do
  use_frameworks!
  pod 'MBProgressHUD', '0.9.1'
end
```
- Replace `'YourAppName'` with the actual name of your Xcode target.
- The `platform :ios, '9.0'` line sets the minimum iOS version; adjust it based on your project’s needs.

#### 4. **Install the Pod**
- Save the `Podfile` and run this command in the terminal:
  ```bash
  pod install
  ```
- This downloads and integrates `MBProgressHUD` version `0.9.1` into your project. If successful, you'll see output confirming the installation.

#### 5. **Open the Workspace**
- After installation, close your Xcode project (if open) and open the newly created `.xcworkspace` file (e.g., `YourAppName.xcworkspace`) instead of the `.xcodeproj` file. CocoaPods generates this workspace to manage dependencies.

#### 6. **Using MBProgressHUD in Your Code**
- **Swift**: Import the module and use it in your code:
  ```swift
  import MBProgressHUD

  class ViewController: UIViewController {
      override func viewDidLoad() {
          super.viewDidLoad()

          // Show a simple HUD with a loading indicator
          let hud = MBProgressHUD.showAdded(to: self.view, animated: true)
          hud.label.text = "Loading..."

          // Hide it after some time (e.g., 2 seconds)
          DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
              hud.hide(animated: true)
          }
      }
  }
  ```

- **Objective-C**: Import the header and use it:
  ```objc
  #import <MBProgressHUD/MBProgressHUD.h>

  @interface ViewController ()
  @end

  @implementation ViewController
  - (void)viewDidLoad {
      [super viewDidLoad];

      // Show a simple HUD with a loading indicator
      MBProgressHUD *hud = [MBProgressHUD showHUDAddedTo:self.view animated:YES];
      hud.label.text = @"Loading...";

      // Hide it after some time (e.g., 2 seconds)
      dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 2 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
          [hud hideAnimated:YES];
      });
  }
  @end
  ```

#### 7. **Common MBProgressHUD Features**
- **Basic HUD**: As shown above, display a spinning indicator with optional text.
- **Custom Text Only**:
  ```swift
  let hud = MBProgressHUD.showAdded(to: view, animated: true)
  hud.mode = .text
  hud.label.text = "Done!"
  hud.hide(animated: true, afterDelay: 1.5)
  ```
- **Progress Bar**:
  ```swift
  let hud = MBProgressHUD.showAdded(to: view, animated: true)
  hud.mode = .determinate
  hud.progress = 0.5 // 50% progress
  ```

#### Notes
- **Version 0.9.1**: This is an older version (released around 2015). The latest version as of March 2025 is much newer (e.g., 1.2.0 or higher). To use the latest, simply write `pod 'MBProgressHUD'` without a version number. Consider updating unless you specifically need 0.9.1 for compatibility.
- **Documentation**: Check the [MBProgressHUD GitHub page](https://github.com/jdg/MBProgressHUD) for more options and examples. Version 0.9.1 might have fewer features than modern releases.

Let me know if you need help troubleshooting or more specific examples!
