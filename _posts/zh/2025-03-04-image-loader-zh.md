---
audio: false
generated: true
lang: zh
layout: post
title: Android通用图像加载器
translated: true
type: note
---

Universal Image Loader (UIL) 1.9.3 版本是一个强大灵活的 Android 图像加载、缓存和显示库。以下是逐步指南，说明如何在 Android 项目中使用它。请注意，该库较旧且已停止维护（最后更新于 2015 年左右），因此对于现代项目，建议考虑使用 Glide 或 Picasso 等替代方案。但如果您确实需要使用 UIL 1.9.3，以下是具体方法：

---

### 步骤 1：将库添加到项目
由于 UIL 1.9.3 可通过 Maven 获取，您可以使用 Gradle 将其添加到项目中。如果使用旧版开发环境（如 Eclipse），可手动下载 JAR 文件。

#### 使用 Gradle (Android Studio)：
1. 打开应用的 `build.gradle` 文件（Module: app）。
2. 在 `dependencies` 块中添加以下依赖：
   ```gradle
   implementation 'com.nostra13.universalimageloader:universal-image-loader:1.9.3'
   ```
3. 点击 Android Studio 中的 "Sync Now" 同步 Gradle 项目。

#### 手动 JAR 配置（如 Eclipse）：
1. 从 Maven 仓库或 GitHub 下载 `universal-image-loader-1.9.3.jar`。
2. 将 JAR 文件放入项目的 `libs` 文件夹。
3. 在 IDE 中右键单击 JAR，选择 "Add to Build Path"（Eclipse）或在项目设置中手动配置。

---

### 步骤 2：添加权限
要从网络加载图像或保存到存储设备，请在 `AndroidManifest.xml` 中添加以下权限：
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```
- `INTERNET`：用于从 URL 下载图像。
- `WRITE_EXTERNAL_STORAGE`：用于磁盘缓存（可选，但推荐用于离线使用）。对于 Android 6.0+ (API 23+)，还需在运行时请求此权限。

---

### 步骤 3：初始化 ImageLoader
在使用 UIL 前，必须通过配置进行初始化。通常建议在 `Application` 类或主 `Activity` 中完成一次初始化。

#### 创建自定义 Application 类（推荐）：
1. 创建新类（如 `MyApplication.java`）：
   ```java
   import android.app.Application;
   import com.nostra13.universalimageloader.core.ImageLoader;
   import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;

   public class MyApplication extends Application {
       @Override
       public void onCreate() {
           super.onCreate();

           // 创建全局配置并初始化 ImageLoader
           ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(this)
               .threadPriority(Thread.NORM_PRIORITY - 2) // 降低图像加载线程优先级
               .denyCacheImageMultipleSizesInMemory()    // 防止缓存多尺寸图像
               .diskCacheSize(50 * 1024 * 1024)          // 50 MB 磁盘缓存
               .diskCacheFileCount(100)                  // 缓存最多 100 个文件
               .build();

           ImageLoader.getInstance().init(config);
       }
   }
   ```
2. 在 `AndroidManifest.xml` 中注册此类：
   ```xml
   <application
       android:name=".MyApplication"
       ... >
   ```

#### 或在 Activity 中初始化：
如果不想使用 `Application` 类，可在 `Activity` 的 `onCreate()` 方法中初始化（确保仅初始化一次）：
```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(this)
        .build();
    ImageLoader.getInstance().init(config);
}
```

---

### 步骤 4：加载并显示图像
初始化后，即可使用 `ImageLoader` 将图像加载到 `ImageView` 中。

#### 基础用法：
```java
import com.nostra13.universalimageloader.core.ImageLoader;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ImageView imageView = findViewById(R.id.imageView);
        String imageUrl = "https://example.com/image.jpg";

        // 将图像加载到 ImageView
        ImageLoader.getInstance().displayImage(imageUrl, imageView);
    }
}
```

#### 使用 DisplayImageOptions 的高级用法：
可通过 `DisplayImageOptions` 自定义图像加载和显示方式：
```java
import com.nostra13.universalimageloader.core.DisplayImageOptions;
import com.nostra13.universalimageloader.core.ImageLoader;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ImageView imageView = findViewById(R.id.imageView);
        String imageUrl = "https://example.com/image.jpg";

        // 定义显示选项
        DisplayImageOptions options = new DisplayImageOptions.Builder()
            .showImageOnLoading(R.drawable.placeholder) // 加载时显示的图像
            .showImageForEmptyUri(R.drawable.error)     // URL 为空时显示的图像
            .showImageOnFail(R.drawable.error)          // 加载失败时显示的图像
            .cacheInMemory(true)                        // 在内存中缓存
            .cacheOnDisk(true)                          // 在磁盘中缓存
            .build();

        // 使用选项加载图像
        ImageLoader.getInstance().displayImage(imageUrl, imageView, options);
    }
}
```

---

### 步骤 5：在 ListView 或 GridView 中使用 UIL
对于列表或网格，可在适配器中使用 UIL 高效加载图像。

#### 示例自定义适配器：
```java
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import com.nostra13.universalimageloader.core.ImageLoader;

public class ImageAdapter extends BaseAdapter {
    private Context context;
    private String[] imageUrls; // 图像 URL 数组

    public ImageAdapter(Context context, String[] imageUrls) {
        this.context = context;
        this.imageUrls = imageUrls;
    }

    @Override
    public int getCount() {
        return imageUrls.length;
    }

    @Override
    public Object getItem(int position) {
        return imageUrls[position];
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.list_item, parent, false);
        }

        ImageView imageView = convertView.findViewById(R.id.imageView);
        ImageLoader.getInstance().displayImage(imageUrls[position], imageView);

        return convertView;
    }
}
```

#### 设置适配器：
```java
String[] imageUrls = {"https://example.com/image1.jpg", "https://example.com/image2.jpg"};
GridView gridView = findViewById(R.id.gridView);
gridView.setAdapter(new ImageAdapter(this, imageUrls));
```

---

### UIL 1.9.3 主要特性
- **支持的 URI 类型**：
  - 网络：`"http://example.com/image.jpg"`
  - SD 卡：`"file:///mnt/sdcard/image.png"`
  - 内容提供器：`"content://media/external/images/media/13"`
  - Assets：`"assets://image.png"`
  - Drawables：`"drawable://" + R.drawable.image`
- **缓存**：支持内存和磁盘缓存。
- **自定义**：可在配置中调整线程池大小、缓存大小和图像解码选项。

---

### 故障排除
- **崩溃："ImageLoader must be init with configuration"**
  确保在调用任何 `displayImage` 前执行 `ImageLoader.getInstance().init(config)`。
- **图像无法加载**
  - 检查网络权限和 URL 有效性。
  - 在配置中启用日志记录（`.writeDebugLogs()`）以调试问题。
- **内存不足错误**
  - 在配置中减小 `diskCacheSize` 或 `memoryCacheSize`。
  - 使用较小图像或在 `DisplayImageOptions` 中启用降采样。

---

### 注意事项
- **过时性**：UIL 1.9.3 已过时（最后发布版本约 2014 年）。对于现代 Android 开发，建议考虑 Glide（`implementation 'com.github.bumptech.glide:glide:4.16.0'`）或 Coil（`implementation 'io.coil-kt:coil:2.6.0'`）。
- **时间背景**：截至 2025 年 3 月 3 日，本指南假设您正在处理需要 UIL 1.9.3 的遗留代码。

如有具体使用场景需要帮助，请随时告知！
