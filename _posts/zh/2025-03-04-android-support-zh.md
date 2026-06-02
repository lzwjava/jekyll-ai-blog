---
audio: false
generated: true
lang: zh
layout: post
title: Android 支持库
translated: true
type: note
---

Android Support Library 版本 `support-v4:19.1.0` 是 Android 支持库的旧版本（特别是 v4 兼容库），它为运行低于其发布时（约 2014 年）最新 API 级别的 Android 设备提供向后兼容的 API。该库允许您在旧设备上使用新版 Android 中引入的功能，例如 Fragments、Loaders 和其他实用程序。

由于 `support-v4:19.1.0` 属于旧版 Android 支持库，现已被 AndroidX 库取代。但如果您需要使用此特定版本（例如维护旧项目），以下是在 Android 项目中设置和使用它的方法：

---

### 步骤 1：添加依赖项
要使用 `support-v4:19.1.0`，您需要将其作为依赖项包含在项目中。这通常在您的 `build.gradle` 文件（模块：app）中完成。

#### 对于基于 Gradle 的项目
1. 打开您的 `app/build.gradle` 文件。
2. 在 `dependencies` 块中添加以下行：

```gradle
dependencies {
    implementation 'com.android.support:support-v4:19.1.0'
}
```

3. 在 Android Studio 中点击“立即同步”以同步项目与 Gradle。

#### 注意：
- 确保您的 `compileSdkVersion` 设置为至少 19（Android 4.4 KitKat）或更高，因为此库与 API 19 功能对齐。
- `support-v4:19.1.0` 支持的最低 SDK 版本为 API 4（Android 1.6），但您应根据应用需求设置 `minSdkVersion`。

示例 `build.gradle`：
```gradle
android {
    compileSdkVersion 19
    defaultConfig {
        minSdkVersion 14  // 根据需要调整
        targetSdkVersion 19
    }
}

dependencies {
    implementation 'com.android.support:support-v4:19.1.0'
}
```

---

### 步骤 2：验证可用性
Android 支持库托管在 Google 的 Maven 仓库中。从 Android Studio 3.0+ 开始，默认包含此仓库。如果您使用旧版 Android Studio，请确保在您的 `build.gradle`（项目级）中包含以下内容：

```gradle
allprojects {
    repositories {
        google()
        jcenter()  // 注意：JCenter 已弃用，但旧版库曾使用
    }
}
```

如果下载库时遇到问题，您可能需要通过 SDK 管理器安装 Android Support Repository：
1. 转到 `Tools > SDK Manager`。
2. 在“SDK Tools”选项卡下，勾选“Android Support Repository”并安装。

---

### 步骤 3：在代码中使用库
`support-v4` 库提供了多种类，例如 `Fragment`、`Loader`、`AsyncTaskLoader` 以及 `ActivityCompat` 等实用程序。以下是使用一些常见组件的示例：

#### 示例 1：使用 Fragments
`support-v4` 库包含一个可在旧版 Android 上使用的向后移植的 `Fragment` 类。

```java
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class MyFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_layout, container, false);
    }
}
```

在 Activity 中使用此 Fragment：
```java
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.os.Bundle;

public class MainActivity extends FragmentActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        FragmentManager fm = getSupportFragmentManager();
        fm.beginTransaction()
            .add(R.id.fragment_container, new MyFragment())
            .commit();
    }
}
```

#### 示例 2：使用 ActivityCompat
`ActivityCompat` 类提供了向后兼容功能的辅助方法，例如请求权限（在 API 23 中引入，但可通过支持库在早期版本中使用）。

```java
import android.support.v4.app.ActivityCompat;
import android.Manifest;
import android.content.pm.PackageManager;

public class MainActivity extends FragmentActivity {
    private static final int REQUEST_CODE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.CAMERA},
                    REQUEST_CODE);
        }
    }
}
```

---

### 步骤 4：注意事项
- **已弃用的库**：Android 支持库（包括 `support-v4:19.1.0`）已弃用。对于现代开发，请迁移到 AndroidX（例如 `androidx.legacy:legacy-support-v4:1.0.0`）。AndroidX 是后续版本，提供持续更新和支持。
- **版本匹配**：如果您使用其他支持库（例如 `appcompat-v7`），请确保它们版本相同（19.1.0），以避免版本不匹配错误。
- **最低 SDK**：虽然 `support-v4:19.1.0` 支持 API 4+，但某些功能可能需要更高的 `minSdkVersion`（例如，后期引入的某些组件需要 API 14）。

---

### 步骤 5：迁移到 AndroidX（可选但推荐）
如果您正在维护旧项目，请考虑迁移到 AndroidX：
1. 在 Android Studio 中，转到 `Refactor > Migrate to AndroidX`。
2. 更新您的依赖项，例如将 `com.android.support:support-v4:19.1.0` 替换为 `androidx.legacy:legacy-support-v4:1.0.0`。
3. 遵循 Android Studio 提供的迁移指南。

---

### 故障排除
- **“找不到库”**：确保您的互联网连接正常，并且可以访问 Google Maven 仓库。
- **版本不匹配**：如果看到有关支持库版本不匹配的错误，请将所有 `com.android.support` 依赖项对齐到 19.1.0。
- **过时功能**：`support-v4:19.1.0` 中的某些 API（例如 `AsyncTask`）已过时。请查阅文档以了解替代方案。

如果您需要特定用例或设置的帮助，请告诉我！
