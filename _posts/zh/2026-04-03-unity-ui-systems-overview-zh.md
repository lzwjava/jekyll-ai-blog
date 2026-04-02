---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Unity UI 系统概述
translated: true
type: note
---

Question:
游戏开发中，如何找到 Unity Studio 的 XML/HTML 或 UI 代码，以及 Unity 使用什么 UI 语言？

Answer:

简短回答：
Unity **不**使用像 web UI 那样的 HTML/XML。它使用 **C# + Unity UI systems**。根据 UI 框架的不同，你可能会看到 **UXML (XML-like)**、**USS (CSS-like)** 或 **C# code**。

有 **三种主要的 Unity UI 系统**：

---

# 1. uGUI (现有 Unity 项目中最常见)

这是经典的 Unity UI 系统。

UI 存储为：

* Scene (.unity)
* Prefab (.prefab)
* Serialized YAML (非 XML / HTML)

示例结构：

```
Canvas
 ├── Panel
 │    ├── Button
 │    └── Text
```

UI 在 Unity Editor 中视觉化创建，然后通过 C# 控制：

```csharp
public Button startButton;

void Start()
{
    startButton.onClick.AddListener(OnStart);
}
```

所以不是 HTML：

HTML 思维：

```
<button id="start">Start</button>
```

Unity 思维：

```
Button component + GameObject + C#
```

---

# 2. UI Toolkit (现代 Unity UI — 最接近 HTML/XML)

这是类似于 **HTML + CSS** 的系统。

Unity 使用：

* **UXML** → 类似 HTML
* **USS** → 类似 CSS
* **C#** → 类似 JavaScript 逻辑

示例 UXML：

```xml
<ui:VisualElement>
    <ui:Button text="Start Game" name="startBtn"/>
</ui:VisualElement>
```

USS：

```css
#startBtn {
    width: 200px;
    height: 40px;
}
```

C#：

```csharp
var btn = root.Q<Button>("startBtn");
btn.clicked += OnStart;
```

这是 Unity 中 **最接近 HTML 的东西**。

---

# 3. IMGUI (仅用于编辑器工具)

用于 Unity Editor 窗口。

纯代码 UI：

```csharp
void OnGUI()
{
    if (GUILayout.Button("Start"))
    {
        StartGame();
    }
}
```

通常不用于游戏 UI。

---

# 如何“找到 Unity UI 源代码”（类似于 HTML 检查）

你有 4 种方法：

### 方法 1 — 检查 prefab（最常见）

在 Unity 中：

```
Hierarchy → select UI → Right click → Open Prefab
```

你会看到：

```
Button
 ├── Image
 └── Text
```

这是你的“DOM 树”

---

### 方法 2 — 调试 UI Toolkit（类似于浏览器开发者工具）

Unity 有 **UI Toolkit Debugger**

打开：

```
Window
 → UI Toolkit
 → Debugger
```

这显示：

* visual tree
* styles
* hierarchy
* attributes

这基本上是 **Unity DevTools**

---

### 方法 3 — 查看序列化 YAML

Unity 场景是 YAML 文件：

```
MyScene.unity
```

内部：

```
--- !u!224 &123456
RectTransform:
  m_AnchoredPosition: {x: 0, y: 0}
```

这是 Unity 的“XML”

但通常不手动编辑。

---

### 方法 4 — 运行时 UI 检查（类似于浏览器检查）

你可以使用：

* Unity UI Toolkit debugger
* Runtime Inspector plugin
* Debug.Log tree

示例：

```csharp
Debug.Log(button.gameObject.name);
```

---

# Unity UI 与 Web UI 的映射

| Web             | Unity               |
| --------------- | ------------------- |
| HTML            | UXML / Prefab       |
| CSS             | USS                 |
| DOM             | GameObject tree     |
| JS              | C#                  |
| inspect element | UI Toolkit debugger |
| div             | VisualElement       |
| button          | Button              |
| id              | name                |
| class           | USS class           |

---

# 你的想法是正确的

你说：

* 找到 UI 结构
* 转换为代码
* 发送给 AI
* 让 Copilot 修复

这是 **完全正确的流程**。

因为 Unity UI 是：

```
Visual layout → hierarchy → components → C#
```

一旦 AI 看到：

```
Canvas
 ├── Panel
 │    ├── Button Start
 │    └── Button Exit
```

它就能生成：

* UI 逻辑
* 导航
* 动画
* 状态机

---

# 你提到的游戏引擎

### cocos2d

UI：

* Cocos Creator → scene JSON
* cocos2d-x → C++ layout
* 有时 XML

示例：

```
Button
 ├── Sprite
 └── Label
```

---

### Unity

UI：

* Prefab
* UXML
* C#

---

### OpenGL

无 UI 系统

你需要手动构建：

```
draw rect
draw text
handle click
```

一切手动。

---

### Skynet (Lua server framework)

无 UI

仅后端：

* networking
* message passing
* services

UI 仍为 Unity / cocos / web

---

# 使用 AI 的最佳流程（你的想法）

步骤 1

在 Unity 中视觉化设计 UI

步骤 2

复制 hierarchy

```
Canvas
 MainMenu
  StartBtn
  ExitBtn
```

步骤 3

告诉 AI：

“生成 Unity C# 代码来连接按钮”

步骤 4

AI 编写逻辑

步骤 5

迭代小块

这与你在 Angular 中做的 **完全一样**。

这对 **Unity 开发非常强大**。

---

# 最现代推荐的 Unity UI

使用：

* UI Toolkit
* UXML
* USS

因为：

* 基于文本
* AI 友好
* diff 友好
* git 友好

就像 HTML。

---

# 最终总结

Unity UI 语言：

* 旧版：Prefab + C#
* 现代：**UXML + USS + C#**
* 编辑器：IMGUI

Unity **不**使用：

* HTML
* XML（仅 UXML-like）
* DOM

但概念上：

```
Unity UI ≈ HTML DOM
```

所以你的流程：

“检查 → 提取结构 → 喂给 AI”

是 **完全正确的**。

References:

* [https://docs.unity3d.com/Manual/UIElements.html](https://docs.unity3d.com/Manual/UIElements.html)
* [https://docs.unity3d.com/Manual/UIE-UXML.html](https://docs.unity3d.com/Manual/UIE-UXML.html)
* [https://docs.unity3d.com/Manual/com.unity.ui.html](https://docs.unity3d.com/Manual/com.unity.ui.html)