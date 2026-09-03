---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Microscope AMCap and gloptics.net
translated: false
type: note
---

**Question:** For a USB digital industrial microscope like **星微光学 高倍电子显微镜 USB 高清工业维修测量鉴定数码放大镜**, do we use **AMCap**, and is `gloptics.net` the place to get it?

**Answer:** Yes — **if that microscope exposes itself to Windows as a standard USB UVC camera**, AMCap is a very common choice.

The typical chain is:

```text
USB microscope
      │
      ▼
Windows USB/UVC driver
      │
      ▼
"USB2.0 UVC PC Camera"
or
"GL USB2.0 UVC Camera Device"
      │
      ▼
     AMCap
      │
      ├── live microscope image
      ├── snapshot
      ├── video capture
      └── sometimes microscope ZOOM/SNAP buttons
```

And **`gloptics.net` is indeed associated with these generic USB microscopes**. I found an actual microscope manual that explicitly says to go to `www.gloptics.net` and download the **“USB Microscope Driver amcap software”**. ([ncsciencefestival.org][1])

So for the kind of microscope you're talking about, I'd try:

1. Plug USB microscope into Windows.
2. Open **Device Manager → Cameras / Imaging devices**.
3. See whether it appears as something like:

   ```text
   USB2.0 UVC PC Camera
   GL USB2.0 UVC Camera Device
   ```
4. Open **AMCap**.
5. `Devices` → select the microscope.
6. You should get the microscope's live video.

AMCap itself is basically a **USB camera/UVC viewer**, not a special microscope technology. Other UVC software can work too. ([Arducam][2])

### One important distinction

If you're doing **GPU/PCB repair**, there are really two levels:

```text
AMCap
  ↓
just gives you the camera image
```

versus

```text
S-EYE / measurement software
  ↓
image
+ measurement
+ calibration
+ distance/angle/diameter measurement
```

For example, microscope vendors distinguish AMCap from measurement software: AMCap handles the camera feed and capture, while S-EYE provides measurement functions. ([jiusion.com][3])

So **for inspecting GPU solder joints, VRAM, MOSFETs, coils, PCB traces, etc., AMCap is perfectly fine as the basic viewer**. You don't necessarily need the vendor's fancy software.

And yes: **`gloptics.net` → USB Microscope Driver / AMCap** is the exact ecosystem you're remembering. ([the-colliers.net][4])

[AMCap / USB microscope driver information](https://gloptics.net/?utm_source=chatgpt.com)

**References:**

* [Jiusion USB Microscope Driver Guide](https://jiusion.com/pages/driver-microscope?utm_source=chatgpt.com)
* [Digital Microscope Connection Instructions](https://ncsciencefestival.org/sites/default/files/documents/Digital%20Microscope%20Connection%20Instructions.pdf?utm_source=chatgpt.com)
* [USB Microscope User Manual referencing gloptics.net + AMCap](https://www.the-colliers.net/docs/public/guides%20%26%20manuals/WiFi%20Box%20Digital%20Microscope%20User%20Manual.pdf?utm_source=chatgpt.com)

[1]: https://ncsciencefestival.org/sites/default/files/documents/Digital%20Microscope%20Connection%20Instructions.pdf?utm_source=chatgpt.com "Digital Microscope Connection Instructions"
[2]: https://docs.arducam.com/UVC-Camera/USB2-UVC-Camera-Kit/Quick-Start-Guide/Windows/?utm_source=chatgpt.com "UVC Cameras on Windows - Arducam Wiki"
[3]: https://jiusion.com/pages/driver-microscope?utm_source=chatgpt.com "USB Microscope Driver Downloads"
[4]: https://www.the-colliers.net/docs/public/guides%20%26%20manuals/WiFi%20Box%20Digital%20Microscope%20User%20Manual.pdf?utm_source=chatgpt.com "3. How to install the Amcap software in PC / Windows 7/8/10 system (only use this software the ZOOM and SNAP button can work normal, and use this method you needn’t run the CD)"
