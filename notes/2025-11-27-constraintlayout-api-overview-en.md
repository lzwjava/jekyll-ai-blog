---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: ConstraintLayout API Overview
translated: false
type: note
---

The typical API provided by **ConstraintLayout** primarily consists of specialized **layout attributes** that are applied to its **child views** (widgets). These attributes define the **constraints**—the rules for how a view is positioned and sized relative to other elements.

The API is usually categorized into three main areas: **Constraint Attributes**, **Dimension Attributes**, and **Helper Objects**.

---

## 1. 📏 Constraint Attributes (Positioning)

These are the core attributes used to define the **position** of a view's anchor points (sides) relative to a target element. Every view inside a `ConstraintLayout` needs at least one horizontal and one vertical constraint to be positioned correctly.

### Relative Positioning

Constraints follow the format: `app:layout_constraint[SourceSide]_to[TargetSide]Of="[TargetID|parent]"`.

| Source Side | Target Side | Description | Example |
| :--- | :--- | :--- | :--- |
| `Top` | `TopOf` / `BottomOf` | Constrains the top edge. | `app:layout_constraintTop_toTopOf="@id/button1"` |
| `Bottom` | `TopOf` / `BottomOf` | Constrains the bottom edge. | `app:layout_constraintBottom_toBottomOf="parent"` |
| `Start` / `Left` | `StartOf` / `EndOf` / `LeftOf` / `RightOf` | Constrains the leading edge (Start) or Left edge. | `app:layout_constraintStart_toEndOf="@id/imageView"` |
| `End` / `Right` | `StartOf` / `EndOf` / `LeftOf` / `RightOf` | Constrains the trailing edge (End) or Right edge. | `app:layout_constraintEnd_toStartOf="parent"` |
| `Baseline` | `BaselineOf` | Aligns the text baseline of one view to another. | `app:layout_constraintBaseline_toBaselineOf="@id/textView2"` |

### Centering and Bias

When both the start/end or top/bottom sides are constrained, the view is centered between those targets. **Bias** allows you to shift this centering.

* `app:layout_constraintHorizontal_bias="[float, 0.0 to 1.0]"`: Shifts the horizontal position (0.0 is left/start, 1.0 is right/end).
* `app:layout_constraintVertical_bias="[float, 0.0 to 1.0]"`: Shifts the vertical position (0.0 is top, 1.0 is bottom).

---

## 2. 📐 Dimension Attributes (Sizing)

While standard `android:layout_width` and `android:layout_height` are used, `ConstraintLayout` introduces a specific value to make its constraints work for sizing.

| Value | Behavior |
| :--- | :--- |
| **`wrap_content`** | The view sizes itself based on its content (standard Android behavior). |
| **`match_parent`** | **Should not be used.** It's effectively treated as `wrap_content` or `0dp` depending on context. |
| **`0dp` (Match Constraints)** | Tells the system to calculate the view's size based on the **constraints** and **margins** set for that axis. This is crucial for responsive design. |

### Advanced Sizing

* **Ratio:** Defines a view's width/height as a ratio of the other dimension.
    * `app:layout_constraintDimensionRatio="[width:height]"` (e.g., `"1:1"` for a square, or `"16:9"`).
* **Min/Max:** When using `0dp` (Match Constraints), you can define size limits.
    * `app:layout_constraintWidth_min`, `app:layout_constraintWidth_max`
    * `app:layout_constraintHeight_min`, `app:layout_constraintHeight_max`

---

## 3. 🛠️ Helper Objects (Advanced Features)

These are special, non-visible views that you can add to the layout to manage groups of views or create reusable constraints.

| Helper Object | Function | Key Attributes |
| :--- | :--- | :--- |
| **`Guideline`** | An invisible, fixed line used to constrain other views. Positioned by percentage or absolute distance from an edge. | `android:orientation`, `app:layout_constraintGuide_percent`, `app:layout_constraintGuide_begin`, `app:layout_constraintGuide_end` |
| **`Barrier`** | An invisible, flexible line that adapts its position based on the size of a referenced group of views. Useful for preventing overlapping text. | `app:barrierDirection` (`start`, `end`, `top`, `bottom`), `app:constraint_referenced_ids` |
| **`Chain`** | A way to manage the positioning and distribution of a group of views along a single axis (horizontal or vertical). Requires back-to-back constraints between the views. | `app:layout_constraintHorizontal_chainStyle`, `app:layout_constraintVertical_chainStyle` (`spread`, `spread_inside`, `packed`) |
| **`Group`** | A simple helper used to control the **visibility** of a set of referenced views simultaneously. It doesn't affect positioning. | `app:constraint_referenced_ids`, `android:visibility` |

The video below demonstrates using various ConstraintLayout features, including Chains and Barriers. [Master ConstraintLayout in Jetpack Compose: Guidelines, Barriers & Chains Made Easy!](https://www.youtube.com/watch?v=ntCGoQDbrVI)


http://googleusercontent.com/youtube_content/0
