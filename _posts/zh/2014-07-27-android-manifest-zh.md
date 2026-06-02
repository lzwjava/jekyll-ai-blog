---
audio: false
generated: false
image: false
lang: zh
layout: post
title: AndroidManifest.xml 文件的理解
translated: true
type: post
---

如果你正在深入Android开发，你会遇到的第一个文件之一就是`AndroidManifest.xml`。它就像你的应用的蓝图——它在应用运行之前告诉Android系统关于你的应用的一切。今天，我们将分解一个名为“Flower”的应用（包名：`com.lzw.flower`）的示例清单文件，并探索其关键组件、概念和模式。

---

#### 什么是AndroidManifest.xml？

`AndroidManifest.xml`文件是每个Android应用所需的配置文件。它位于项目的根目录，声明了应用的包名、权限、组件（例如活动）以及它所需的硬件/软件功能。可以将其视为应用的身份卡，Android操作系统会读取它。

让我们逐步走过示例。

---

### 清单的结构

这是我们要处理的清单（稍微简化以便阅读）：

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.lzw.flower"
    android:versionCode="8"
    android:versionName="1.5.2">

    <uses-sdk android:minSdkVersion="14" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-feature android:name="android.hardware.camera" />
    <uses-feature android:name="android.hardware.camera.autofocus" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.READ_PHONE_STATE" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />

    <application
        android:label="@string/app_name"
        android:icon="@drawable/icon128"
        android:name=".base.App"
        android:theme="@style/AppTheme">

        <activity android:name=".deprecated.CameraActivity" android:screenOrientation="landscape" />
        <activity android:name=".base.SplashActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".draw.DrawActivity" android:screenOrientation="landscape" />
        <activity android:name=".result.ResultActivity" android:screenOrientation="landscape" />
        <activity android:name=".material.MaterialActivity" android:screenOrientation="landscape" />
        <activity android:name=".activity.PhotoActivity" android:screenOrientation="landscape" />
        <activity android:name=".activity.LoginActivity" android:screenOrientation="portrait" />
    </application>
</manifest>
```

现在，让我们将其分解为其核心部分，并解释其背后的概念。

---

### 1. 根`<manifest>`元素

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.lzw.flower"
    android:versionCode="8"
    android:versionName="1.5.2">
```

- **`xmlns:android`**：这是为Android特定属性定义的XML命名空间。这是你在每个清单中都会看到的标准样板。
- **`package`**：这是你的应用的唯一标识符（例如，`com.lzw.flower`）。它也是你的Java/Kotlin类的默认命名空间。
- **`android:versionCode`**：这是一个内部整数（这里是`8`），用于跟踪版本。每次更新时都会递增。
- **`android:versionName`**：这是一个人类可读的版本字符串（这里是`1.5.2`），显示给用户。

**概念**：`<manifest>`标签设置应用的身份和版本控制，确保系统知道它在处理什么应用以及如何处理更新。

---

### 2. 使用`<uses-sdk>`的SDK版本

```xml
<uses-sdk android:minSdkVersion="14" />
```

- **`android:minSdkVersion`**：指定应用支持的最低Android API级别。API 14对应Android 4.0（冰淇淋三明治）。

**概念**：这确保了兼容性。运行Android版本低于4.0的设备无法安装此应用。这里没有`targetSdkVersion`或`maxSdkVersion`，但可以添加它们以进一步细化兼容性。

---

### 3. 使用`<uses-permission>`的权限

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.READ_PHONE_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
```

这个应用请求了几个权限：
- `CAMERA`：访问设备的摄像头。
- `WRITE_EXTERNAL_STORAGE`：将文件（例如照片）保存到外部存储。
- `INTERNET`：用于网络访问。
- `ACCESS_NETWORK_STATE`：检查网络连接。
- `READ_PHONE_STATE`：访问设备信息（例如IMEI）。
- `ACCESS_WIFI_STATE`：检查Wi-Fi状态。

**概念**：Android使用权限系统来保护用户隐私和安全。这些声明告诉系统（和用户）应用需要哪些敏感功能。在Android 6.0（API 23）之后，危险权限（例如`CAMERA`）还需要在应用代码中进行运行时请求。

---

### 4. 使用`<uses-feature>`的功能

```xml
<uses-feature android:name="android.hardware.camera" />
<uses-feature android:name="android.hardware.camera.autofocus" />
```

- **`android.hardware.camera`**：声明应用需要摄像头。
- **`android.hardware.camera.autofocus`**：指定摄像头必须支持自动对焦。

**概念**：与权限不同，`<uses-feature>`标签在Google Play商店中过滤应用。如果设备没有摄像头或自动对焦，应用将不会显示为可安装，除非这些标记为可选（`android:required="false"`）。

---

### 5. `<application>`元素

```xml
<application
    android:label="@string/app_name"
    android:icon="@drawable/icon128"
    android:name=".base.App"
    android:theme="@style/AppTheme">
```

- **`android:label`**：应用的名称，从字符串资源（`@string/app_name`）中提取。
- **`android:icon`**：应用的图标，引用一个可绘制资源（`@drawable/icon128`）。
- **`android:name`**：一个自定义的Application类（`.base.App`），它扩展了Android的`Application`类以进行应用范围的逻辑。
- **`android:theme`**：应用的默认视觉主题（`@style/AppTheme`）。

**概念**：`<application>`标签定义了应用范围的设置。资源如`@string`和`@drawable`存储在`res/`文件夹中，促进了可重用性和本地化。

---

### 6. 使用`<activity>`的活动

清单列出了几个活动，这些活动是应用的UI屏幕：

#### 示例1：启动屏幕（启动器活动）

```xml
<activity
    android:name=".base.SplashActivity"
    android:theme="@android:style/Theme.Holo.Light.NoActionBar.Fullscreen">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
```

- **`android:name`**：类名（`.base.SplashActivity`）。
- **`intent-filter`**：将其标记为应用的入口点（`MAIN`操作+`LAUNCHER`类别），因此它会出现在设备的应用启动器中。
- **`android:theme`**：一个没有操作栏的全屏主题。

**模式**：启动器活动是一个常见的起点，通常是启动屏幕或主屏幕。

#### 示例2：摄像头活动

```xml
<activity
    android:name=".deprecated.CameraActivity"
    android:screenOrientation="landscape">
```

- **`android:screenOrientation`**：强制横向模式。
- **`.deprecated`**：表明此活动可能已过时，但仍然包含在内。

**模式**：活动通常为特定用例强制方向（例如，摄像头应用在横向模式下工作更好）。

#### 其他活动

清单中列出了更多活动，如`DrawActivity`、`ResultActivity`、`PhotoActivity`等，具有类似的模式：
- 大多数是横向模式，表明这是一个视觉或媒体为中心的应用。
- 一些覆盖了应用的默认主题（例如，`Theme.Holo.Light`）。

**概念**：活动是Android应用的UI的构建块。每个`<activity>`标签都在系统中注册了一个屏幕。

---

### 此清单中的关键模式

1. **媒体为中心的设计**：摄像头、存储和自动对焦的权限和功能表明这是一个照片或绘图应用（可能是识别花朵，鉴于包名`com.lzw.flower`）。
2. **方向控制**：大量使用`android:screenOrientation="landscape"`表明重点放在视觉任务上。
3. **模块化活动**：多个活动（`CameraActivity`、`DrawActivity`、`ResultActivity`）表明一个多步骤的工作流程。
4. **资源使用**：对`@string`、`@drawable`和`@style`的引用显示了一个干净、可维护的结构。

---

### 结论

`AndroidManifest.xml`不仅仅是一个配置文件——它是应用目的和行为的窗口。在这种情况下，“Flower”似乎是一个具有摄像头功能、绘图功能和网络功能的媒体应用，可能用于上传或处理图像。通过理解其组件——权限、功能和活动——你可以看到Android应用是如何构建的以及如何设计你自己的应用。

想要构建类似的东西吗？从一个明确的目的（例如花卉识别）开始，定义你的权限和功能，并规划你的活动。清单将把它们全部联系起来！
