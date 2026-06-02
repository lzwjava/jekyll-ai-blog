---
audio: false
generated: true
lang: zh
layout: post
title: 使用ButterKnife进行视图绑定
translated: true
type: note
---

Butter Knife 是一款广受欢迎的 Android 视图绑定库，它能简化将 UI 元素与代码字段绑定的过程。但请注意，Butter Knife 现已弃用，现代 Android 开发推荐使用 Android Jetpack 引入的视图绑定功能。不过，如果您仍需在 Android 项目中使用 2015 年左右发布的旧版本 Butter Knife 6.1.0（通过 `.jar` 文件），以下是在 2025 年 3 月 3 日当前 Android Studio 中的配置方法。

### 前置条件

- 已安装 Android Studio（任何近期版本均可，具体操作可能因版本略有差异）
- 已创建基础 Android 项目
- 已下载 `butterknife-6.1.0.jar` 文件（可通过 Maven Central 等代码库或本地存档获取）

### 在 Android 开发中使用 `butterknife-6.1.0.jar` 的步骤

#### 步骤 1：将 `.jar` 文件添加至项目

1. **定位 libs 文件夹**：
   - 在 Android Studio 项目中进入 `app` 模块
   - 在 `app` 文件夹内找到或创建名为 `libs` 的目录（如不存在可右键点击 `app` 文件夹选择「新建 > 目录」并命名为 `libs`）

2. **复制 `.jar` 文件**：
   - 将 `butterknife-6.1.0.jar` 文件复制到 `libs` 文件夹（可通过拖拽至 Android Studio 的 `libs` 目录或通过文件管理器手动放置）

3. **同步 Gradle 配置**：
   - 打开 `app` 模块的 `build.gradle` 文件（位于 `app/build.gradle`）
   - 在 `dependencies` 代码块中添加以下配置以引入 `libs` 目录下所有 `.jar` 文件：

     ```gradle
     dependencies {
         compile fileTree(dir: 'libs', include: ['*.jar'])
     }
     ```

   - 点击 Android Studio 的「Sync Project with Gradle Files」按钮同步项目

#### 步骤 2：配置项目参数

由于 Butter Knife 6.1.0 采用注解处理机制，该特定版本不需要像 8.x 等后续版本那样添加注解处理器依赖。此 `.jar` 文件包含运行时库，且 6.1.0 版本主要依赖运行时反射而非编译时代码生成。

请确保项目已配置支持 Java 注解：

- 在 `app/build.gradle` 中确认 Java 版本兼容性（Butter Knife 6.1.0 支持 Java 6+）：

  ```gradle
  android {
      compileOptions {
          sourceCompatibility JavaVersion.VERSION_1_6
          targetCompatibility JavaVersion.VERSION_1_6
      }
  }
  ```

#### 步骤 3：在代码中使用 Butter Knife

1. **添加注解声明**：
   - 在 Activity 或 Fragment 中导入 Butter Knife 并使用 `@InjectView` 注解（6.1.0 版本专用）：

     ```java
     import android.os.Bundle;
     import android.widget.Button;
     import android.widget.TextView;
     import butterknife.InjectView;
     import butterknife.ButterKnife;
     import androidx.appcompat.app.AppCompatActivity;

     public class MainActivity extends AppCompatActivity {

         @InjectView(R.id.my_button)
         Button myButton;

         @InjectView(R.id.my_text)
         TextView myText;

         @Override
         protected void onCreate(Bundle savedInstanceState) {
             super.onCreate(savedInstanceState);
             setContentView(R.layout.activity_main);
             ButterKnife.inject(this); // 视图绑定

             // 使用示例
             myButton.setOnClickListener(v -> myText.setText("按钮已点击!"));
         }
     }
     ```

2. **XML 布局配置**：
   - 确保布局文件（如 `res/layout/activity_main.xml`）包含对应 ID 的视图组件：

     ```xml
     <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
         android:layout_width="match_parent"
         android:layout_height="match_parent"
         android:orientation="vertical">

         <TextView
             android:id="@+id/my_text"
             android:layout_width="wrap_content"
             android:layout_height="wrap_content"
             android:text="Hello World" />

         <Button
             android:id="@+id/my_button"
             android:layout_width="wrap_content"
             android:layout_height="wrap_content"
             android:text="点击这里" />
     </LinearLayout>
     ```

3. **执行视图绑定**：
   - 在 `onCreate` 中调用 `ButterKnife.inject(this)` 实现注解字段与布局视图的绑定（注意 6.1.0 版本使用 `inject` 而非后续版本的 `bind` 方法）

#### 步骤 4：运行项目

- 编译并运行项目。若配置正确，Butter Knife 将完成视图绑定，您将看到正常运行的 UI 界面

### 重要说明

- **版本限制**：Butter Knife 6.1.0 版本较旧（2015 年发布），缺少后续版本引入的编译时代码生成等特性，且使用运行时反射机制，性能可能略低于现代替代方案
- **弃用状态**：Butter Knife 已停止维护（2020 年左右终止开发），官方建议新项目使用视图绑定或 Jetpack Compose
- **替代方案配置**：若使用新版（如 10.2.3）需添加注解处理器依赖，但 6.1.0 版本通过 `.jar` 文件使用时无需此配置
- **故障排查**：
  - 如出现「无法解析符号」错误，请检查 `.jar` 文件是否正确添加至 `libs` 目录并包含在 Gradle 依赖中
  - 如应用崩溃并报 `NoClassDefFoundError`，请确认 `.jar` 文件位置及项目同步状态

### 建议

虽然本指南展示了如何使用 `butterknife-6.1.0.jar`，但建议迁移至视图绑定以获得更现代的官方支持方案。以下为简要对比：

- **Butter Knife 6.1.0**：使用 `@InjectView` 注解、运行时反射、手动集成 `.jar` 文件
- **视图绑定**：Android 原生支持、无需外部依赖、编译时生成绑定类、具备空值安全特性

是否需要了解如何迁移至视图绑定的指导？
