---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Android按钮点击事件处理
translated: true
type: note
---

**正确答案：B. OnClickListener**

在 Android 开发中，处理 `Button`（或任何 `View`）点击事件最常用且推荐的方式是实现或设置 **`View.OnClickListener`**。

### 为什么 B 是正确的

- `View.OnClickListener` 仅包含一个方法：`onClick(View v)`
- 该方法专门用于处理标准点击事件
- 使用示例：

  ```java
  button.setOnClickListener(new View.OnClickListener() {
      @Override
      public void onClick(View v) {
          // 处理点击事件
      }
  });
  ```

  或使用 lambda 表达式（Kotlin/Java 8+）：

  ```java
  button.setOnClickListener(v -> { /* 处理点击事件 */ });
  ```

### 为什么其他选项不是最佳选择

- **A. OnTouchListener** – 处理底层触摸事件（ACTION_DOWN、ACTION_UP 等）。对于简单点击而言过于复杂，且可能干扰手势检测
- **C. OnLongClickListener** – 仅适用于长按事件，不适用于常规点击
- **D. OnKeyListener** – 用于处理物理/软键盘按键事件，不适用于视图点击

**最佳实践**：对于标准按钮点击始终使用 `OnClickListener`（也可通过 XML 中的 `android:onClick="方法名"` 直接定义点击处理程序）。

因此，**B** 无疑是正确答案。
