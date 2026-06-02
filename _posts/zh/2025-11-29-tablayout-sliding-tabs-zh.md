---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 安卓滑动标签页布局
translated: true
type: note
---

正确答案是 **A. TabLayout**。

**说明**：
在 Android 开发（特别是使用 AndroidX 库）中，**TabLayout** 是专门设计用于创建滑动标签界面的类，可与 **ViewPager** 或 **ViewPager2** 无缝协作。

典型配置：
```xml
<com.google.android.material.tabs.TabLayout
    android:id="@+id/tabLayout"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"/>

<androidx.viewpager.widget.ViewPager
    android:id="@+id/viewPager"
    android:layout_width="match_parent"
    android:layout_height="match_parent"/>
```

```java
TabLayout tabLayout = findViewById(R.id.tabLayout);
ViewPager viewPager = findViewById(R.id.viewPager);
viewPager.setAdapter(myAdapter);
tabLayout.setupWithViewPager(viewPager);  // 此方法实现两者滑动联动
```

其他选项说明：
- **Toolbar** → 应用栏，不用于创建标签页
- **DrawerLayout** → 用于导航抽屉（侧滑菜单）
- **CoordinatorLayout** → 用于协调子视图行为的高级布局容器（常作为包含 AppBarLayout + TabLayout 的根布局），但本身不是标签页创建组件

因此正确定义为：**A. TabLayout**
