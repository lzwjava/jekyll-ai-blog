---
audio: false
generated: true
lang: en
layout: post
title: Universal Image Loader in Android
translated: false
type: note
---

Universal Image Loader (UIL) version 1.9.3 is a powerful and flexible library for loading, caching, and displaying images in Android applications. Below is a step-by-step guide on how to use it in your Android project. Note that this library is older and has been discontinued (last updated around 2015), so for modern projects, you might consider alternatives like Glide or Picasso. However, if you specifically need to use UIL 1.9.3, here’s how to do it:

---

### Step 1: Add the Library to Your Project

Since UIL 1.9.3 is available via Maven, you can add it to your project using Gradle. If you're working with an older setup (e.g., Eclipse), you can manually download the JAR file.

#### Using Gradle (Android Studio)

1. Open your app’s `build.gradle` file (Module: app).
2. Add the following dependency in the `dependencies` block:

   ```gradle
   implementation 'com.nostra13.universalimageloader:universal-image-loader:1.9.3'
   ```

3. Sync your project with Gradle by clicking "Sync Now" in Android Studio.

#### Manual JAR Setup (e.g., Eclipse)

1. Download the `universal-image-loader-1.9.3.jar` from the Maven Repository or GitHub.
2. Place the JAR file in the `libs` folder of your project.
3. Right-click the JAR in your IDE, then select "Add to Build Path" (Eclipse) or configure it manually in your project settings.

---

### Step 2: Add Permissions

To load images from the internet or save them to storage, add the following permissions to your `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

- `INTERNET`: Required for downloading images from URLs.
- `WRITE_EXTERNAL_STORAGE`: Required for disk caching (optional, but recommended for offline use). For Android 6.0+ (API 23+), you’ll also need to request this permission at runtime.

---

### Step 3: Initialize the ImageLoader

Before using UIL, you must initialize it with a configuration. This is typically done once in your `Application` class or main `Activity`.

#### Create a Custom Application Class (Recommended)

1. Create a new class (e.g., `MyApplication.java`):

   ```java
   import android.app.Application;
   import com.nostra13.universalimageloader.core.ImageLoader;
   import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;

   public class MyApplication extends Application {
       @Override
       public void onCreate() {
           super.onCreate();

           // Create global configuration and initialize ImageLoader
           ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(this)
               .threadPriority(Thread.NORM_PRIORITY - 2) // Lower priority for image loading threads
               .denyCacheImageMultipleSizesInMemory()    // Prevent caching multiple sizes
               .diskCacheSize(50 * 1024 * 1024)          // 50 MB disk cache
               .diskCacheFileCount(100)                  // Max 100 files in cache
               .build();

           ImageLoader.getInstance().init(config);
       }
   }
   ```

2. Register this class in your `AndroidManifest.xml`:

   ```xml
   <application
       android:name=".MyApplication"
       ... >
   ```

#### Or Initialize in an Activity

If you don’t want to use an `Application` class, initialize it in your `Activity`’s `onCreate()` method (but ensure it’s only initialized once):

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

### Step 4: Load and Display an Image

Once initialized, you can use `ImageLoader` to load images into an `ImageView`.

#### Basic Usage

```java
import com.nostra13.universalimageloader.core.ImageLoader;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ImageView imageView = findViewById(R.id.imageView);
        String imageUrl = "https://example.com/image.jpg";

        // Load image into ImageView
        ImageLoader.getInstance().displayImage(imageUrl, imageView);
    }
}
```

#### Advanced Usage with Display Options

You can customize how images are loaded and displayed using `DisplayImageOptions`:

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

        // Define display options
        DisplayImageOptions options = new DisplayImageOptions.Builder()
            .showImageOnLoading(R.drawable.placeholder) // Image shown while loading
            .showImageForEmptyUri(R.drawable.error)     // Image shown if URL is empty
            .showImageOnFail(R.drawable.error)          // Image shown if loading fails
            .cacheInMemory(true)                        // Cache in RAM
            .cacheOnDisk(true)                          // Cache on disk
            .build();

        // Load image with options
        ImageLoader.getInstance().displayImage(imageUrl, imageView, options);
    }
}
```

---

### Step 5: Using UIL in a ListView or GridView

For lists or grids, use UIL in your adapter to efficiently load images.

#### Example Custom Adapter

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
    private String[] imageUrls; // Array of image URLs

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

#### Set the Adapter

```java
String[] imageUrls = {"https://example.com/image1.jpg", "https://example.com/image2.jpg"};
GridView gridView = findViewById(R.id.gridView);
gridView.setAdapter(new ImageAdapter(this, imageUrls));
```

---

### Key Features of UIL 1.9.3

- **Supported URI Types**:
  - Web: `"http://example.com/image.jpg"`
  - SD Card: `"file:///mnt/sdcard/image.png"`
  - Content Provider: `"content://media/external/images/media/13"`
  - Assets: `"assets://image.png"`
  - Drawables: `"drawable://" + R.drawable.image`
- **Caching**: Supports memory and disk caching.
- **Customization**: Thread pool size, cache size, and image decoding options can be adjusted in the configuration.

---

### Troubleshooting

- **Crash: "ImageLoader must be init with configuration"**
  Ensure `ImageLoader.getInstance().init(config)` is called before any `displayImage` calls.
- **Images Not Loading**
  - Check internet permissions and URL validity.
  - Enable logging in the configuration (`.writeDebugLogs()`) to debug issues.
- **Out of Memory Errors**
  - Reduce `diskCacheSize` or `memoryCacheSize` in the configuration.
  - Use smaller images or enable downscaling in `DisplayImageOptions`.

---

### Notes

- **Deprecation**: UIL 1.9.3 is outdated (last release ~2014). For modern Android development, consider Glide (`implementation 'com.github.bumptech.glide:glide:4.16.0'`) or Coil (`implementation 'io.coil-kt:coil:2.6.0'`).
- **Date Context**: As of March 3, 2025, this guide assumes you’re working with legacy code requiring UIL 1.9.3.

Let me know if you need help with a specific use case!
