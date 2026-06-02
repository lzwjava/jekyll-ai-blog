---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unity UI Systems Overview
translated: false
type: note
---

Question:
For game development, how can we find Unity Studio’s XML/HTML or UI code, and what UI language does Unity use?

Answer:

Short answer:
Unity does **not** use HTML/XML like web UI. It uses **C# + Unity UI systems**. Depending on the UI framework, you may see **UXML (XML-like)**, **USS (CSS-like)**, or **C# code**.

There are **three main Unity UI systems**:

---

# 1. uGUI (Most common in existing Unity projects)

This is the classic Unity UI system.

UI is stored as:

* Scene (.unity)
* Prefab (.prefab)
* Serialized YAML (not XML / HTML)

Example structure:

```
Canvas
 ├── Panel
 │    ├── Button
 │    └── Text
```

The UI is created visually in Unity Editor, then controlled via C#:

```csharp
public Button startButton;

void Start()
{
    startButton.onClick.AddListener(OnStart);
}
```

So instead of HTML:

HTML thinking:

```
<button id="start">Start</button>
```

Unity thinking:

```
Button component + GameObject + C#
```

---

# 2. UI Toolkit (Modern Unity UI — closest to HTML/XML)

This is the one similar to **HTML + CSS**.

Unity uses:

* **UXML** → like HTML
* **USS** → like CSS
* **C#** → like JavaScript logic

Example UXML:

```xml
<ui:VisualElement>
    <ui:Button text="Start Game" name="startBtn"/>
</ui:VisualElement>
```

USS:

```css
#startBtn {
    width: 200px;
    height: 40px;
}
```

C#:

```csharp
var btn = root.Q<Button>("startBtn");
btn.clicked += OnStart;
```

This is the **closest thing to HTML in Unity**.

---

# 3. IMGUI (Editor tools only)

Used for Unity Editor windows.

Code-only UI:

```csharp
void OnGUI()
{
    if (GUILayout.Button("Start"))
    {
        StartGame();
    }
}
```

Not used for game UI usually.

---

# How to "find Unity UI source" (like HTML inspection)

You have 4 ways:

### Method 1 — Inspect prefab (most common)

In Unity:

```
Hierarchy → select UI → Right click → Open Prefab
```

You’ll see:

```
Button
 ├── Image
 └── Text
```

This is your "DOM tree"

---

### Method 2 — Debug UI Toolkit (like browser devtools)

Unity has **UI Toolkit Debugger**

Open:

```
Window
 → UI Toolkit
 → Debugger
```

This shows:

* visual tree
* styles
* hierarchy
* attributes

This is basically **Unity DevTools**

---

### Method 3 — View serialized YAML

Unity scenes are YAML files:

```
MyScene.unity
```

Inside:

```
--- !u!224 &123456
RectTransform:
  m_AnchoredPosition: {x: 0, y: 0}
```

This is Unity’s "XML"

But usually not edited manually.

---

### Method 4 — Runtime UI inspection (like browser inspect)

You can use:

* Unity UI Toolkit debugger
* Runtime Inspector plugin
* Debug.Log tree

Example:

```csharp
Debug.Log(button.gameObject.name);
```

---

# Unity UI vs Web UI mapping

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

# Your idea is correct

You said:

* find UI structure
* convert to code
* send to AI
* let Copilot fix

This is **exactly the right workflow**.

Because Unity UI is:

```
Visual layout → hierarchy → components → C#
```

Once AI sees:

```
Canvas
 ├── Panel
 │    ├── Button Start
 │    └── Button Exit
```

It can generate:

* UI logic
* navigation
* animation
* state machine

---

# For game engines you mentioned

### cocos2d

UI:

* Cocos Creator → scene JSON
* cocos2d-x → C++ layout
* sometimes XML

Example:

```
Button
 ├── Sprite
 └── Label
```

---

### Unity

UI:

* Prefab
* UXML
* C#

---

### OpenGL

No UI system

You build manually:

```
draw rect
draw text
handle click
```

Everything manual.

---

### Skynet (Lua server framework)

No UI

Only backend:

* networking
* message passing
* services

UI still Unity / cocos / web

---

# Best workflow with AI (your idea)

Step 1

Design UI visually in Unity

Step 2

Copy hierarchy

```
Canvas
 MainMenu
  StartBtn
  ExitBtn
```

Step 3

Tell AI:

"generate Unity C# code to wire buttons"

Step 4

AI writes logic

Step 5

iterate small pieces

Exactly what you're doing with Angular.

This is **very powerful for Unity dev**.

---

# Most modern recommended Unity UI

Use:

* UI Toolkit
* UXML
* USS

Because:

* text based
* AI friendly
* diff friendly
* git friendly

Just like HTML.

---

# Final summary

Unity UI language:

* Old: Prefab + C#
* Modern: **UXML + USS + C#**
* Editor: IMGUI

Unity does NOT use:

* HTML
* XML (only UXML-like)
* DOM

But conceptually:

```
Unity UI ≈ HTML DOM
```

So your workflow:

"inspect → extract structure → feed AI"

is exactly right.

References:

* [https://docs.unity3d.com/Manual/UIElements.html](https://docs.unity3d.com/Manual/UIElements.html)
* [https://docs.unity3d.com/Manual/UIE-UXML.html](https://docs.unity3d.com/Manual/UIE-UXML.html)
* [https://docs.unity3d.com/Manual/com.unity.ui.html](https://docs.unity3d.com/Manual/com.unity.ui.html)
