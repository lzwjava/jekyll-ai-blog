---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: ConstraintLayout API 概述
translated: true
type: note
---

**ConstraintLayout** 提供的典型 API 主要由应用于其**子视图**（控件）的专用**布局属性**构成。这些属性定义了**约束**——即视图相对于其他元素的定位和尺寸规则。

该 API 通常分为三个主要领域：**约束属性**、**尺寸属性**和**辅助对象**。

---

## 1. 📏 约束属性（定位）

这些是核心属性，用于定义视图的锚点（边）相对于目标元素的**位置**。`ConstraintLayout` 内的每个视图至少需要一个水平约束和一个垂直约束才能正确定位。

### 相对定位

约束遵循格式：`app:layout_constraint[源侧]_to[目标侧]Of="[目标ID|parent]"`。

| 源侧 | 目标侧 | 描述 | 示例 |
| :--- | :--- | :--- | :--- |
| `Top` | `TopOf` / `BottomOf` | 约束顶部边缘。 | `app:layout_constraintTop_toTopOf="@id/button1"` |
| `Bottom` | `TopOf` / `BottomOf` | 约束底部边缘。 | `app:layout_constraintBottom_toBottomOf="parent"` |
| `Start` / `Left` | `StartOf` / `EndOf` / `LeftOf` / `RightOf` | 约束起始边缘（Start）或左侧边缘。 | `app:layout_constraintStart_toEndOf="@id/imageView"` |
| `End` / `Right` | `StartOf` / `EndOf` / `LeftOf` / `RightOf` | 约束结束边缘（End）或右侧边缘。 | `app:layout_constraintEnd_toStartOf="parent"` |
| `Baseline` | `BaselineOf` | 将一个视图的文本基线与另一个视图对齐。 | `app:layout_constraintBaseline_toBaselineOf="@id/textView2"` |

### 居中和偏斜

当视图的起始/结束边或顶部/底部边都被约束时，视图会在这些目标之间居中。**偏斜**允许您移动此居中位置。

* `app:layout_constraintHorizontal_bias="[浮点数, 0.0 到 1.0]"`：移动水平位置（0.0 是左/起始，1.0 是右/结束）。
* `app:layout_constraintVertical_bias="[浮点数, 0.0 到 1.0]"`：移动垂直位置（0.0 是顶部，1.0 是底部）。

---

## 2. 📐 尺寸属性（大小调整）

虽然使用了标准的 `android:layout_width` 和 `android:layout_height`，但 `ConstraintLayout` 引入了一个特定值，使其约束能够用于尺寸调整。

| 值 | 行为 |
| :--- | :--- |
| **`wrap_content`** | 视图根据其内容调整自身大小（标准 Android 行为）。 |
| **`match_parent`** | **不应使用。** 根据上下文，它实际上被视为 `wrap_content` 或 `0dp`。 |
| **`0dp`（匹配约束）** | 告诉系统根据为该轴设置的**约束**和**边距**计算视图的尺寸。这对于响应式设计至关重要。 |

### 高级尺寸调整

* **比率：** 将视图的宽度/高度定义为另一尺寸的比率。
    * `app:layout_constraintDimensionRatio="[宽度:高度]"`（例如，正方形用 `"1:1"`，或 `"16:9"`）。
* **最小/最大值：** 当使用 `0dp`（匹配约束）时，可以定义尺寸限制。
    * `app:layout_constraintWidth_min`, `app:layout_constraintWidth_max`
    * `app:layout_constraintHeight_min`, `app:layout_constraintHeight_max`

---

## 3. 🛠️ 辅助对象（高级功能）

这些是特殊的、不可见的视图，您可以将其添加到布局中，以管理视图组或创建可重用的约束。

| 辅助对象 | 功能 | 关键属性 |
| :--- | :--- | :--- |
| **`Guideline`** | 一条不可见的固定线，用于约束其他视图。通过百分比或距边缘的绝对距离定位。 | `android:orientation`, `app:layout_constraintGuide_percent`, `app:layout_constraintGuide_begin`, `app:layout_constraintGuide_end` |
| **`Barrier`** | 一条不可见的、灵活的线，根据引用的视图组的大小调整其位置。用于防止文本重叠。 | `app:barrierDirection` (`start`, `end`, `top`, `bottom`), `app:constraint_referenced_ids` |
| **`Chain`** | 一种管理沿单个轴（水平或垂直）的视图组的定位和分布的方式。需要在视图之间设置首尾相接的约束。 | `app:layout_constraintHorizontal_chainStyle`, `app:layout_constraintVertical_chainStyle` (`spread`, `spread_inside`, `packed`) |
| **`Group`** | 一个简单的辅助工具，用于同时控制一组引用视图的**可见性**。它不影响定位。 | `app:constraint_referenced_ids`, `android:visibility` |

下面的视频演示了如何使用各种 ConstraintLayout 功能，包括 Chains 和 Barriers。[在 Jetpack Compose 中掌握 ConstraintLayout：Guidelines、Barriers & Chains 变得简单！](https://www.youtube.com/watch?v=ntCGoQDbrVI)


http://googleusercontent.com/youtube_content/0
