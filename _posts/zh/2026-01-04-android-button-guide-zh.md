---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Android Button setOnClickListener 方法指南
translated: true
type: note
---

Question: 要在代码中为 Button 设置 onClick listener，通常使用哪个方法？

A) button.setOnClickListener()  
B) button.addClickListener()  
C) button.onClick()  
D) button.setClickEvent()

Answer: 

正确答案是 **A) button.setOnClickListener()**。

在 Android 开发（使用 Java 或 Kotlin）中，以编程方式为 `Button`（或任何 `View`）设置 onClick listener 的标准且最常用的方法是 `setOnClickListener()`。该方法接受 `View.OnClickListener` 接口的实现，通常通过匿名内部类、lambda（在 Kotlin 中）或单独的 listener 对象提供。

### Java 示例：

```java
button.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        // Handle click event
    }
});
```

### Kotlin 示例：

```kotlin
button.setOnClickListener {
    // Handle click event
}
```

### 为什么不选择其他选项？

- **B) addClickListener()**：Android SDK 中不存在此方法。
- **C) onClick()**：这是 listener 内部在发生点击时被调用的方法，而不是用于设置 listener 的方法。
- **D) setClickEvent()**：Android SDK 中不存在此方法。

注意：用户选择的 "C" 是错误的。正确选项是 A。

References:  
- [https://developer.android.com/reference/android/view/View#setOnClickListener(android.view.View.OnClickListener)](https://developer.android.com/reference/android/view/View#setOnClickListener(android.view.View.OnClickListener))  
- [https://developer.android.com/develop/ui/views/components/button](https://developer.android.com/develop/ui/views/components/button)