---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 花卉识别应用
translated: true
type: post
---

这是来自 GitHub 项目 [https://github.com/lzwjava/flower-recognition](https://github.com/lzwjava/flower-recognition) 的 README.md。

---

### 花朵识别应用

这是一个花朵识别 Android 应用程序，旨在帮助用户通过拍摄照片并绘制圆圈来识别花朵。

#### 特性：
- **拍摄照片**：用户可以直接在应用内拍摄花朵照片。
- **绘图功能**：能够在花朵图像上绘制圆圈和注解，以辅助识别。
- **认证**：通过登录屏幕进行安全用户认证。
- **结果显示**：在用户友好的界面中显示识别结果。
- **材料设计**：实现材料设计原理，提供现代和直观的用户体验。

#### 文件结构：
```
└── com
    └── lzw
        └── flower
            ├── activity
            │   ├── LoginActivity.java
            │   └── PhotoActivity.java
            ├── adapter
            │   └── PhotoAdapter.java
            ├── avobject
            │   └── Photo.java
            ├── base
            │   ├── App.java
            │   ├── ImageLoader.java
            │   └── SplashActivity.java
            ├── deprecated
            │   ├── CameraActivity.java
            │   └── Deprecated.java
            ├── draw
            │   ├── Draw.java
            │   ├── DrawActivity.java
            │   ├── DrawFragment.java
            │   ├── DrawView.java
            │   ├── HelpBtn.java
            │   ├── History.java
            │   ├── Tooltip.java
            │   └── ZoomImageView.java
            ├── fragment
            │   ├── RecogFragment.java
            │   └── WaitFragment.java
            ├── material
            │   └── MaterialActivity.java
            ├── result
            │   ├── FlowerAdapter.java
            │   ├── FlowerData.java
            │   ├── Image.java
            │   ├── ResultActivity.java
            │   └── ResultFragment.java
            ├── service
            │   └── PhotoService.java
            ├── utils
            │   ├── BitmapUtils.java
            │   ├── Crop.java
            │   ├── ImageListDialogBuilder.java
            │   ├── Logger.java
            │   ├── PathUtils.java
            │   └── Utils.java
            └── web
                ├── Upload.java
                ├── UploadImage.java
                └── Web.java
```

#### 组件：
- **Activities**：包含处理不同应用活动（如登录、拍照和欢迎屏幕）的类。
- **Adapters**：处理照片和识别结果的显示。
- **AVObject**：表示带有相关元数据的照片对象。
- **Drawing**：与在花朵图像上绘制圆圈和注解相关的类。
- **Fragments**：提供用于显示识别结果和等待指示器的 UI 组件。
- **Material**：可能与实现材料设计指南相关。
- **Services**：处理与照片相关的后台任务和数据操作。
- **Utils**：包含各种任务的实用程序类，如图像操作和日志记录。

#### 使用方法：
1. 克隆仓库。
2. 在 Android Studio 中打开项目。
3. 在 Android 设备或模拟器上构建并运行应用程序。

#### 许可证：
本项目采用 [MIT 许可证](LICENSE) 发布。
