---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Ubuntu @all Icon Flash
translated: false
type: note
---

Question: Does WeChat on Ubuntu flash its icon when there is an `@all` notification in a group?

Answer:

Yes, **normally it should**.

On the Linux (Ubuntu) version of WeChat, when you receive an important unread message such as:

* `@you`
* `@all`
* a direct message

the desktop integration typically marks the application as needing attention. Depending on your desktop environment, you'll see one or more of:

* The WeChat dock/taskbar icon **flashing or pulsing**.
* A **red unread badge** on the icon.
* The icon highlighted in the Ubuntu Dock.
* A desktop notification (if notifications are enabled).

Whether the icon actually **flashes repeatedly** depends more on **your desktop environment** than WeChat itself:

* **Ubuntu GNOME**: usually shows a badge/highlight; some versions animate the icon briefly rather than flashing continuously.
* **KDE Plasma**: task manager often flashes the task until you focus the window.
* **Xfce/MATE/Cinnamon**: behavior varies.

If you're **not** seeing any indication, check:

```bash
# Is notification daemon running?
ps aux | grep notification

# GNOME notification setting
gsettings get org.gnome.desktop.notifications show-banners
```

Also verify:

* Notifications are enabled for WeChat.
* "Do Not Disturb" is off.
* You're using the native Linux client rather than running WeChat inside Wine or another compatibility layer, since notification behavior differs.

An `@all` is generally treated the same as an `@you` mention, so it should generate a notification and an unread indicator if notifications are enabled. Continuous flashing, however, is controlled by the desktop shell and isn't guaranteed on every Ubuntu setup.