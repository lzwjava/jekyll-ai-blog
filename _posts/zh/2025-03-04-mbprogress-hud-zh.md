---
audio: false
generated: true
lang: zh
layout: post
title: 在iOS中使用MBProgressHUD
translated: true
type: note
---

看起来您是在询问如何在 iOS 项目中使用 CocoaPods 的 Podfile 集成 `MBProgressHUD` 库（特指 0.9.1 版本）。让我为您逐步说明具体操作流程。

### 什么是 MBProgressHUD？

`MBProgressHUD` 是一款广受欢迎的 iOS 第三方库，它能便捷地显示包含活动指示器、进度条或自定义视图的 HUD（平视显示器），常用于展示加载状态或简短消息。

### 使用 `pod 'MBProgressHUD', '0.9.1'` 的步骤

#### 1. **安装 CocoaPods（如未安装）**

CocoaPods 是 iOS 项目的依赖管理工具。若尚未安装，请在终端运行：

```bash
sudo gem install cocoapods
```

#### 2. **配置 Podfile**

- 在终端中进入您的 Xcode 项目目录：

  ```bash
  cd /path/to/your/project
  ```

- 如果尚未创建 Podfile，请执行：

  ```bash
  pod init
  ```

- 用文本编辑器打开 `Podfile`（如 `nano Podfile` 或 `open Podfile`）

#### 3. **在 Podfile 中添加 MBProgressHUD**

在应用对应的 target 块内添加 `MBProgressHUD` 0.9.1 版本声明，示例格式如下：

```ruby
platform :ios, '9.0'  # 指定部署目标版本

target 'YourAppName' do
  use_frameworks!
  pod 'MBProgressHUD', '0.9.1'
end
```

- 将 `'YourAppName'` 替换为实际 Xcode 目标名称
- `platform :ios, '9.0'` 用于设置最低 iOS 版本，请根据项目需求调整

#### 4. **安装 Pod**

- 保存 Podfile 后在终端运行：

  ```bash
  pod install
  ```

- 该命令将下载并集成指定版本的 `MBProgressHUD`，成功后会显示确认信息

#### 5. **打开工作空间**

- 安装完成后请关闭当前 Xcode 项目（如果已打开），转而打开新生成的 `.xcworkspace` 文件（如 `YourAppName.xcworkspace`）。CocoaPods 通过此工作空间管理依赖项

#### 6. **在代码中使用 MBProgressHUD**

- **Swift 版本**：导入模块后即可调用

  ```swift
  import MBProgressHUD

  class ViewController: UIViewController {
      override func viewDidLoad() {
          super.viewDidLoad()

          // 显示带加载指示器的简易 HUD
          let hud = MBProgressHUD.showAdded(to: self.view, animated: true)
          hud.label.text = "加载中..."

          // 延时隐藏（示例为2秒后）
          DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
              hud.hide(animated: true)
          }
      }
  }
  ```

- **Objective-C 版本**：引入头文件后使用

  ```objc
  #import <MBProgressHUD/MBProgressHUD.h>

  @interface ViewController ()
  @end

  @implementation ViewController
  - (void)viewDidLoad {
      [super viewDidLoad];

      // 显示带加载指示器的简易 HUD
      MBProgressHUD *hud = [MBProgressHUD showHUDAddedTo:self.view animated:YES];
      hud.label.text = @"加载中...";

      // 延时隐藏（示例为2秒后）
      dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 2 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
          [hud hideAnimated:YES];
      });
  }
  @end
  ```

#### 7. **常用 MBProgressHUD 功能**

- **基础 HUD**：如上文所示，可显示旋转指示器与可选文本
- **纯文本模式**：

  ```swift
  let hud = MBProgressHUD.showAdded(to: view, animated: true)
  hud.mode = .text
  hud.label.text = "操作完成！"
  hud.hide(animated: true, afterDelay: 1.5)
  ```

- **进度条模式**：

  ```swift
  let hud = MBProgressHUD.showAdded(to: view, animated: true)
  hud.mode = .determinate
  hud.progress = 0.5 // 50% 进度
  ```

#### 注意事项

- **版本说明**：0.9.1 是较旧的版本（约2015年发布）。截至2025年3月，最新版本已迭代至 1.2.0 或更高。如需使用最新版，只需声明 `pod 'MBProgressHUD'` 不指定版本号。除非有兼容性需求，建议考虑更新版本
- **文档参考**：可访问 [MBProgressHUD GitHub 页面](https://github.com/jdg/MBProgressHUD) 获取更多配置选项和示例。需注意 0.9.1 版本的功能可能较新版本有所欠缺

如需进一步 troubleshooting 或获取更具体的示例，欢迎随时提问！
