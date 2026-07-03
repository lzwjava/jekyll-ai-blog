---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat on Linux Mint and Fedora
translated: false
type: note
---

The short answer is **yes**, you can use WeChat on both Linux Mint and Fedora. 

However, because Tencent does not officially support Linux, **how well it works depends entirely on which method you choose**. 

Here is the breakdown of your options, ranked from best to worst:

### 1. The Official Web Version (Easiest, but limited)
You can use WeChat directly in your browser (Firefox/Chrome) by visiting **https://wx.qq.com**. 

- **Works on:** Both Mint and Fedora instantly.
- **The Catch:** You **cannot log in** with a regular WeChat account anymore. It only works if your account is linked to a foreign (non-Chinese) phone number. For most users in China, this method is blocked.

### 2. The Official Desktop Flatpak (Recommended for Mint)
Tencent recently released an official WeChat desktop client for Linux, but **only as a Flatpak**. 

- **On Linux Mint:** Flatpak is built-in. Just open the Software Manager, search for "WeChat," and install the official one. 
- **On Fedora:** You must enable Flatpak first (`sudo dnf install flatpak`) and add the Flathub repository, then install it via the software store.
- **Pros:** Full desktop app, supports file transfers, screenshots, and voice/video calls.
- **Cons:** It is actually a wrapped version of the Android app running in a container. It takes up about 1.5GB of disk space and can be a bit slow to start.

### 3. The Deepin-Wine Version (Alternative)
The open-source community packages the Windows version of WeChat to run on Linux using a compatibility layer called "Wine."

- **On Fedora:** This is tricky to set up manually.
- **On Linux Mint:** You can install `deepin-wine` and the WeChat package via third-party repositories.
- **Pros:** Feels more like a native Windows app.
- **Cons:** Can crash randomly, text rendering sometimes looks blurry, and screen-sharing usually doesn't work.

### 4. Android Phone Sync (via KDE Connect)
If you just want to *receive and reply* to messages without opening the app, you can install **KDE Connect** on your Linux PC and the app on your Android phone. This mirrors your phone notifications to your desktop, allowing you to reply to WeChat messages directly from your PC without logging into a desktop client.

---

### Important Login Caveats (Read This)
Regardless of which method you pick, **new users face a huge hurdle**:

- **New accounts cannot log in to desktop clients.** If your WeChat account is less than 1 month old, Tencent will block your login to any PC/Linux client and force you to use the phone app only.
- **You must scan a QR code.** There is no "username/password" login for the desktop. You **must** have your phone nearby, open WeChat on your phone, and scan the QR code on your Linux screen every single time you log in.
- **You cannot log into both at the same time.** You can only be logged into the Linux desktop *or* the web version, not both simultaneously.

---

**My recommendation:** 
If you are on **Linux Mint**, just install the official Flatpak from the Software Manager—it is the most stable. 
If you are on **Fedora**, I strongly recommend just using the **web version** (if your number is foreign) or installing the **Flatpak** version, as Fedora's default package manager (DNF) does not have WeChat natively, and compiling Wine manually is a headache.

**One final warning:** Tencent does not officially audit the code of the Linux client. If you are using WeChat for highly sensitive work chats, stick to the web browser version for better security, or use it inside a Firejail sandbox.