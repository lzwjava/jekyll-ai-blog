---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: How to Use Windows 11 Remote Desktop
translated: false
type: note
---

Question: How to use Remote Desktop to connect to a Windows 11 PC?

Answer: 

Microsoft's Remote Desktop feature allows you to connect to and control a Windows 11 PC from another device. Note that the **Windows 11 PC you want to connect to (the host)** must be running the Pro, Enterprise, or Education edition—Windows 11 Home does not support hosting Remote Desktop connections.

### Step 1: Enable Remote Desktop on the Windows 11 Host PC
1. Open **Settings** (press Windows key + I).
2. Go to **System** > **Remote Desktop**.
3. Toggle **Enable Remote Desktop** to **On** and confirm the prompt.
4. Note the **PC name** displayed on this page—you'll need it to connect from another device.
5. (Optional) Under **Remote Desktop users**, add any additional user accounts that should have remote access.

The host PC must be powered on, connected to the network/internet, and not in sleep mode for connections to work.

### Step 2: Connect from Another Windows PC (Client)
1. On the client PC, search for **Remote Desktop Connection** in the Start menu and open it (or run `mstsc.exe`).
2. Enter the **PC name** or **IP address** of the Windows 11 host PC.
3. Click **Connect**.
4. Enter the username and password of an allowed account on the host PC.
5. If prompted about the certificate, click **Yes** to proceed.

You will now have full control of the remote desktop session.

### Step 3: Connect from macOS, iOS, Android, or Other Devices
- Download the **Windows App** (recommended by Microsoft) or the **Microsoft Remote Desktop** app from the App Store, Google Play, or Microsoft Store.
- Add a new PC connection by entering the host PC's name or IP address.
- Save and connect, then provide credentials when prompted.

### Additional Tips
- For connections within the same local network, use the PC name.
- For connections over the internet, use the public IP address or set up port forwarding (port 3389) on your router, or preferably use a VPN for security. Direct exposure of RDP to the internet is risky due to potential attacks—always use strong passwords and consider Network Level Authentication (enabled by default).
- Firewall: Windows usually allows RDP automatically when enabled, but ensure no third-party firewall blocks it.
- Troubleshooting: If connection fails, check that the host is awake, credentials are correct, and both devices can reach each other (try pinging the host).

References:  
- [How to use Remote Desktop - Microsoft Support](https://support.microsoft.com/en-us/windows/how-to-use-remote-desktop-5fe128d5-8fb1-7a23-3b8a-41e636865e8c)  
- [Enable Remote Desktop on your PC | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access)