---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyWin32 Window Control Essentials
translated: false
type: note
---

Here’s a guide to working with **PyWin32 windows**—focusing on their properties, activation, and bottom area handling.

---

## 1. What is a Window in PyWin32?

In PyWin32, a “window” refers to any GUI element managed by the Windows API that has a **handle (HWND)**. This can be a top-level application window, a dialog, or even a control inside a form.

You typically interact with windows via:

* `win32gui` – low-level functions for window handles, properties, and messages.
* `win32con` – constants for Windows messages and styles.
* `win32api` – general Windows API functions.

---

## 2. Common Window Properties

A window has a lot of attributes you can query or modify:

* **Handle (HWND)**: Unique identifier of the window.
* **Title (Caption)**: Text shown in the title bar (`win32gui.GetWindowText(hwnd)`).
* **Class name**: Window’s registered class (`win32gui.GetClassName(hwnd)`).
* **Styles**: Defines how the window behaves/looks (`GetWindowLong` with `GWL_STYLE`).
* **Position & size**: Rectangle coordinates via `GetWindowRect(hwnd)` or `MoveWindow`.
* **Visibility**: Whether the window is shown (`IsWindowVisible`).
* **Enabled state**: Whether it accepts input (`IsWindowEnabled`).
* **Parent/Owner**: Hierarchy of windows (`GetParent(hwnd)`).

---

## 3. Window Activation

To bring a window to the front or make it active:

* **SetForegroundWindow(hwnd)** – makes the window the active one.
* **SetActiveWindow(hwnd)** – activates but doesn’t guarantee topmost.
* **BringWindowToTop(hwnd)** – raises it above others.
* **ShowWindow(hwnd, flag)** – shows/hides/minimizes/maximizes depending on `flag` (like `SW_SHOW`, `SW_MINIMIZE`, `SW_RESTORE`).

---

## 4. “Bottom Area” (Z-Order & Placement)

Windows are layered in a Z-order:

* **Topmost** – always above others (`SetWindowPos` with `HWND_TOPMOST`).
* **Bottom** – can push a window behind all others using `SetWindowPos(hwnd, win32con.HWND_BOTTOM, …)`.
* **NoActivate** – you can show or position a window without activating it (using flags like `SWP_NOACTIVATE`).

This is often useful if you want a background utility window to stay open but not steal focus.

---

## 5. Typical Functions You’ll Use

Here are some key PyWin32 functions with examples:

```python
import win32gui
import win32con

# Find window by title
hwnd = win32gui.FindWindow(None, "Untitled - Notepad")

# Get properties
title = win32gui.GetWindowText(hwnd)
rect = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)

# Activate window
win32gui.SetForegroundWindow(hwnd)

# Move to bottom (behind others)
win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# Show/restore
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
```

---

## 6. Event/Message Handling

You can also hook into window events (activation, resizing, closing) using:

* `SetWindowLong` to subclass.
* `SendMessage` / `PostMessage` to simulate actions.
* Messages like `WM_ACTIVATE`, `WM_SIZE`, etc.

---

✅ In summary:

* **Properties**: title, class, size, style, visibility, enabled state.
* **Activation**: use `SetForegroundWindow`, `BringWindowToTop`.
* **Bottom area**: manage Z-order with `SetWindowPos` and `HWND_BOTTOM`.

Would you like me to also include a **practical script** that lists all top-level windows with their properties (title, position, z-order), and allows you to activate or send them to the bottom interactively?
