---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ejecting Mac Volumes Safely
translated: false
type: note
---

Question: On a Mac, if Finder is using a volume, can I move the cursor to another folder and then eject the disk?

Answer:

Not exactly. On macOS, if a volume (like an external drive) is “in use,” Finder or another app may prevent it from being ejected. Simply moving the Finder cursor to another folder **does not automatically release the volume**. What matters is whether **any process or app is actively accessing files on that volume**.

Here’s how to safely eject it:

1. **Close any open files or windows** on the volume.
2. **Quit apps** that might be using files from that drive (including Finder windows showing that drive).
3. Once nothing is accessing the volume, you can:

   * Right-click the drive on the Desktop or in Finder → *Eject*.
   * Drag the drive icon to the Trash (it turns into an Eject symbol).
4. If the system still says the disk is in use, you can check which process is using it:

   * Open **Terminal** and run:

     ```bash
     lsof | grep /Volumes/YourDriveName
     ```

     This shows files or processes accessing the drive. You can then quit or force-close those processes.

Moving the cursor or changing folders in Finder alone won’t release the volume if some background process is still using it.

References:

* [Apple Support – Eject an external drive](https://support.apple.com/guide/mac-help/eject-an-external-drive-mchlp2591/mac)
* [Macworld – How to force eject a stuck drive](https://www.macworld.com/article/671749/how-to-force-eject-an-external-drive-mac.html)
