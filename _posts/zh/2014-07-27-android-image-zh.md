---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 安卓图像处理简化
translated: true
type: post
---

在 Android 中处理图像可能会很棘手——位图会占用大量内存，旋转会影响方向，裁剪需要精确度。这就是 `BitmapUtils` 和 `Crop` 等实用工具类派上用场的地方。在这篇文章中，我将带你了解 `com.lzw.flower.utils` 包中的一对强大的类。我们将探讨它们的代码，分解每个方法的作用，并展示如何在项目中使用它们。让我们开始吧！

---

#### BitmapUtils：您的图像操作工具包

`BitmapUtils` 类是一组用于操作 `Bitmap` 对象的静态方法。以下是完整的代码，后面是详细的分析：

```java
package com.lzw.flower.utils;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;
import android.provider.MediaStore;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class BitmapUtils {
  public static Bitmap convertGreyImg(Bitmap img) {
    int width = img.getWidth();
    int height = img.getHeight();
    int[] pixels = new int[width * height];
    img.getPixels(pixels, 0, width, 0, 0, width, height);
    int alpha = 0xFF << 24;
    for (int i = 0; i < height; i++) {
      for (int j = 0; j < width; j++) {
        int grey = pixels[width * i + j];
        int red = ((grey & 0x00FF0000) >> 16);
        int green = ((grey & 0x0000FF00) >> 8);
        int blue = (grey & 0x000000FF);
        grey = (int) ((float) red * 0.3 + (float) green * 0.59 + (float) blue * 0.11);
        grey = alpha | (grey << 16) | (grey << 8) | grey;
        pixels[width * i + j] = grey;
      }
    }
    Bitmap result = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
    result.setPixels(pixels, 0, width, 0, 0, width, height);
    return result;
  }

  public static Bitmap toGreyImg(Bitmap bitmapOrg) {
    Bitmap bitmapNew = bitmapOrg.copy(Bitmap.Config.ARGB_8888, true);
    if (bitmapNew == null) {
      return null;
    }
    for (int i = 0; i < bitmapNew.getWidth(); i++) {
      for (int j = 0; j < bitmapNew.getHeight(); j++) {
        int col = bitmapNew.getPixel(i, j);
        int alpha = col & 0xFF000000;
        int red = (col & 0x00FF0000) >> 16;
        int green = (col & 0x0000FF00) >> 8;
        int blue = (col & 0x000000FF);
        int gray = (int) ((float) red * 0.3 + (float) green * 0.59 + (float) blue * 0.11);
        int newColor = alpha | (gray << 16) | (gray << 8) | gray;
        bitmapNew.setPixel(i, j, newColor);
      }
    }
    return bitmapNew;
  }

  public static void saveBitmapToPath(Bitmap bitmap, String imagePath) {
    FileOutputStream out = null;
    File file = new File(imagePath);
    if (file.getParentFile().exists() == false) {
      file.getParentFile().mkdirs();
    }
    try {
      out = new FileOutputStream(imagePath);
      bitmap.compress(Bitmap.CompressFormat.PNG, 100, out);
      out.flush();
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      try {
        if (out != null) out.close();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }
  }

  public static Bitmap rotateBitmap(Bitmap source, float angle) {
    Matrix matrix = new Matrix();
    matrix.postRotate(angle);
    return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(), matrix, true);
  }

  public static Uri getResourceUri(int resId) {
    return Uri.parse("android.resource://com.lzw.flower/" + resId);
  }

  public static Bitmap getBitmapByUri(Context cxt, Uri uri) throws IOException {
    return MediaStore.Images.Media.getBitmap(cxt.getContentResolver(), uri);
  }

  public static int calInSampleSize(BitmapFactory.Options options, int reqWidth) {
    int w = options.outWidth;
    int h = options.outHeight;
    int inSampleSize = 1;
    if (w > reqWidth && reqWidth > 0) {
      inSampleSize = Math.round(w / reqWidth);
    }
    return inSampleSize;
  }

  public static Bitmap decodeSampledBitmapFromPath(String path, int reqWidth) {
    BitmapFactory.Options options = new BitmapFactory.Options();
    options.inJustDecodeBounds = true;
    BitmapFactory.decodeFile(path, options);
    int inSampleSize = calInSampleSize(options, reqWidth);
    options.inJustDecodeBounds = false;
    options.inSampleSize = inSampleSize;
    return BitmapFactory.decodeFile(path, options);
  }

  public static Bitmap decodeFileByHeight(String path, int reqH) {
    BitmapFactory.Options opt = new BitmapFactory.Options();
    opt.inJustDecodeBounds = true;
    BitmapFactory.decodeFile(path, opt);
    int scale = calInSampleSizeByHeight(opt, reqH);
    opt.inSampleSize = scale;
    opt.inJustDecodeBounds = false;
    Bitmap bm = BitmapFactory.decodeFile(path, opt);
    return bm;
  }

  public static int calInSampleSizeByHeight(BitmapFactory.Options options, int reqHeight) {
    int h = options.outHeight;
    int inSampleSize = 1;
    if (h > reqHeight) {
      inSampleSize = Math.round(h * 1.0f / reqHeight);
    }
    return inSampleSize;
  }
}
```

##### 内容概述：
- **灰度转换**：
  - `convertGreyImg`：使用像素数组批量处理位图以转换为灰度。
  - `toGreyImg`：逐像素处理可变副本，提供一种替代方法。
  两者都使用亮度公式（`0.3R + 0.59G + 0.11B`）进行自然灰度转换。

- **文件操作**：
  - `saveBitmapToPath`：将位图保存为 PNG，根据需要创建目录。

- **转换**：
  - `rotateBitmap`：使用 `Matrix` 旋转图像——简单有效。

- **加载和采样**：
  - `getBitmapByUri` 和 `getResourceUri`：从 URI 或资源加载图像。
  - `decodeSampledBitmapFromPath` 和 `decodeFileByHeight`：按宽度或高度高效缩放大图像，避免内存问题。

---

#### Crop：使用 Android 原生工具进行精确裁剪

`Crop` 类利用 Android 内置的裁剪意图。以下是代码：

```java
package com.lzw.flower.utils;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.provider.MediaStore;
import com.lzw.flower.base.App;

import java.io.File;

public class Crop {
  public static void startPhotoCrop(Activity cxt, Uri uri, String outputPath, int resultCode) {
    Intent intent = new Intent("com.android.camera.action.CROP");
    intent.setDataAndType(uri, "image/*");
    int w = App.drawWidth;
    int h = App.drawHeight;
    int factor = gcd(w, h);
    int w1 = w / factor;
    int h1 = h / factor;
    intent.putExtra("crop", "true")
        .putExtra("aspectX", w1)
        .putExtra("aspectY", h1)
        .putExtra("scale", true)
        .putExtra("outputX", w)
        .putExtra("outputY", h)
        .putExtra("outputFormat", Bitmap.CompressFormat.PNG.toString());
    intent.putExtra("noFaceDetection", true);
    intent.putExtra("return-data", false);
    Uri uri1 = Uri.fromFile(new File(outputPath));
    intent.putExtra(MediaStore.EXTRA_OUTPUT, uri1);
    cxt.startActivityForResult(intent, resultCode);
  }

  static int gcd(int a, int b) {
    if (b == 0) {
      return a;
    } else {
      return gcd(b, a % b);
    }
  }
}
```

##### 这里发生了什么？
- `startPhotoCrop`：启动系统裁剪活动，指定 `Uri`、纵横比（使用 GCD 简化）和输出路径。假设 `App.drawWidth` 和 `App.drawHeight` 在其他地方定义（例如在基础 `App` 类中）。
- `gcd`：递归方法计算最大公约数，确保纵横比是最简形式。

---

#### 将它们结合起来：使用示例

以下是如何在 Android 应用中使用这些实用工具：

```java
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import com.lzw.flower.utils.BitmapUtils;
import com.lzw.flower.utils.Crop;

public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_CROP = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 将图像转换为灰度并保存
        Bitmap original = BitmapFactory.decodeResource(getResources(), R.drawable.sample);
        Bitmap grey = BitmapUtils.convertGreyImg(original);
        BitmapUtils.saveBitmapToPath(grey, "/sdcard/DCIM/grey_image.png");

        // 高效加载和缩放图像
        Bitmap scaled = BitmapUtils.decodeSampledBitmapFromPath("/sdcard/DCIM/photo.jpg", 200);

        // 启动裁剪
        Uri imageUri = Uri.fromFile(new File("/sdcard/DCIM/photo.jpg"));
        Crop.startPhotoCrop(this, imageUri, "/sdcard/DCIM/cropped.png", REQUEST_CROP);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CROP && resultCode == RESULT_OK) {
            // 裁剪后的图像保存在 "/sdcard/DCIM/cropped.png"
        }
    }
}
```

**注意**：
- 确保在 `AndroidManifest.xml` 中正确设置存储权限，并在运行时检查文件操作。
- `App` 类（在 `Crop` 中引用）应定义 `drawWidth` 和 `drawHeight`。

---

#### 为什么这些实用工具很棒

1. **高效**：采样方法防止处理大图像时出现 `OutOfMemoryError`。
2. **灵活性**：灰度、旋转和裁剪涵盖了广泛的用例。
3. **简洁**：静态方法使集成变得轻松——无需实例化。

---

#### 最后的想法

`BitmapUtils` 和 `Crop` 类是任何需要图像操作的 Android 应用的绝佳起点。无论您是构建照片编辑器、优化相册缩略图，还是添加用户驱动的裁剪，这段代码都能满足您的需求。试试看，根据需要进行调整，告诉我效果如何！

您在 Android 中遇到过哪些图像处理挑战？请在下面分享您的想法！
