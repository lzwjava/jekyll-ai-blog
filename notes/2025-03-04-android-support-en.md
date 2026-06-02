---
audio: false
generated: true
lang: en
layout: post
title: Android Support Library
translated: false
type: note
---

The Android Support Library version `support-v4:19.1.0` is an older version of the Android Support Library (specifically the v4 compatibility library), which provides backward-compatible APIs for Android devices running API levels lower than the latest ones at the time of its release (circa 2014). This library allows you to use features introduced in newer Android versions on older devices, such as Fragments, Loaders, and other utilities.

Since `support-v4:19.1.0` is part of the legacy Android Support Library, it has been superseded by AndroidX libraries. However, if you need to use this specific version (e.g., for maintaining an older project), here's how you can set it up and use it in your Android project:

---

### Step 1: Add the Dependency

To use `support-v4:19.1.0`, you need to include it as a dependency in your project. This is typically done in your `build.gradle` file (Module: app).

#### For Gradle-Based Projects

1. Open your `app/build.gradle` file.
2. Add the following line to the `dependencies` block:

```gradle
dependencies {
    implementation 'com.android.support:support-v4:19.1.0'
}
```

3. Sync your project with Gradle by clicking "Sync Now" in Android Studio.

#### Notes

- Ensure your `compileSdkVersion` is set to at least 19 (Android 4.4 KitKat) or higher, as this library is aligned with API 19 features.
- The minimum SDK version supported by `support-v4:19.1.0` is API 4 (Android 1.6), but you should set your `minSdkVersion` based on your app’s requirements.

Example `build.gradle`:

```gradle
android {
    compileSdkVersion 19
    defaultConfig {
        minSdkVersion 14  // Adjust as needed
        targetSdkVersion 19
    }
}

dependencies {
    implementation 'com.android.support:support-v4:19.1.0'
}
```

---

### Step 2: Verify Availability

The Android Support Libraries are hosted in Google's Maven repository. Starting with Android Studio 3.0+, this repository is included by default. If you're using an older version of Android Studio, ensure the following is in your `build.gradle` (Project-level):

```gradle
allprojects {
    repositories {
        google()
        jcenter()  // Note: JCenter is deprecated, but was used for older libraries
    }
}
```

If you encounter issues downloading the library, you may need to install the Android Support Repository via the SDK Manager:

1. Go to `Tools > SDK Manager`.
2. Under the "SDK Tools" tab, check "Android Support Repository" and install it.

---

### Step 3: Using the Library in Your Code

The `support-v4` library provides a variety of classes, such as `Fragment`, `Loader`, `AsyncTaskLoader`, and utilities like `ActivityCompat`. Below are examples of how to use some common components:

#### Example 1: Using Fragments

The `support-v4` library includes a backported `Fragment` class that works on older Android versions.

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

To use this fragment in an activity:

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

#### Example 2: Using ActivityCompat

The `ActivityCompat` class provides helper methods for backward-compatible features, such as requesting permissions (introduced in API 23 but usable earlier with the support library).

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

### Step 4: Considerations

- **Deprecated Library**: The Android Support Library, including `support-v4:19.1.0`, is deprecated. For modern development, migrate to AndroidX (e.g., `androidx.legacy:legacy-support-v4:1.0.0`). AndroidX is the successor and provides ongoing updates and support.
- **Version Matching**: If you use other support libraries (e.g., `appcompat-v7`), ensure they are the same version (19.1.0) to avoid version mismatch errors.
- **Minimum SDK**: While `support-v4:19.1.0` supports API 4+, some features may require a higher `minSdkVersion` (e.g., API 14 for certain components introduced later).

---

### Step 5: Migrating to AndroidX (Optional but Recommended)

If you’re maintaining an old project, consider migrating to AndroidX:

1. In Android Studio, go to `Refactor > Migrate to AndroidX`.
2. Update your dependencies, e.g., replace `com.android.support:support-v4:19.1.0` with `androidx.legacy:legacy-support-v4:1.0.0`.
3. Follow the migration guide provided by Android Studio.

---

### Troubleshooting

- **"Could not find library"**: Ensure your internet connection is active and the Google Maven repository is accessible.
- **Version Mismatch**: If you see errors about mismatched support library versions, align all `com.android.support` dependencies to 19.1.0.
- **Obsolete Features**: Some APIs in `support-v4:19.1.0` (e.g., `AsyncTask`) are outdated. Check the documentation for alternatives.

Let me know if you need help with a specific use case or setup!
