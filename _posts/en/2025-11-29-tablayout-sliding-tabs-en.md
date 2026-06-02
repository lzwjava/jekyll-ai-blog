---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Android TabLayout for Sliding Tabs
translated: false
type: note
---

The correct answer is **A. TabLayout**.

**Explanation**:
In Android development (especially with the AndroidX libraries), **TabLayout** is the class specifically designed to create sliding tab interfaces that work seamlessly with **ViewPager** or **ViewPager2**.

Typical setup:

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
tabLayout.setupWithViewPager(viewPager);  // This links them for sliding behavior
```

The other options:

- **Toolbar** → App bar, not for tabs
- **DrawerLayout** → For navigation drawers (slide-in menu)
- **CoordinatorLayout** → Advanced layout for coordinating behaviors (often used as root with AppBarLayout + TabLayout), but not the tab creator itself

So, definitively: **A. TabLayout**
