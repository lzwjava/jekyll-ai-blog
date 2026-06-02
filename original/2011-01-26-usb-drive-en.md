---
audio: false
generated: false
image: false
lang: en
layout: post
title: Customize Your USB Drive with a Background and Icon
translated: false
type: post
---

This post was originally written in Chinese and published on Qzone.

---

**I. Customizing the USB Drive Icon:**

1. First, choose an icon you like. The icon file extension should be `.ico`.
2. Copy the icon file to your USB drive and create a new text document on the USB drive.
3. In the text document, write the following:
   ```
   [autorun]
   ICON=\xxx.ico,0
   ```
   Where `xxx.ico` is the name of your icon file (including the extension).
4. Save the text file as `autorun.inf`.
   **Note:** It's crucial to change the extension to `.inf`, not `.txt`. If the file icon changes to one with a yellow gear, you've done it correctly.
   Unplug the USB drive and plug it back in. You'll see that the USB drive icon has changed to the one you selected.
   This method can also be used for external hard drives or CD/DVD burning.

**II. Customizing the Background:**

1. First, choose a background image you like and copy it to your USB drive.
2. Create a new text file and copy the following into it:
   ```
   [ExtShellFolderViews]
   {BE098140-A513-11D0-A3A4-00C04FD706EC}={BE098140-A513-11D0-A3A4-00C04FD706EC}
   [{BE098140-A513-11D0-A3A4-00C04FD706EC}]
   Attributes=1
   IconArea_Image=aaa.jpg
   IconArea_Text=0x00FFFFFF
   [.ShellClassInfo]
   ConfirmFileOp=0
   ```
   This code means:

   Where `aaa.jpg` is the name of your chosen image file (including the extension).

   `IconArea_Text= 0x00FFFFFF`  This line changes the text color on the USB drive.

   Color codes are:

   *   Red: `0x000000FF`
   *   Yellow: `0x0000FFFF`
   *   Blue: `0x00FF0000`
   *   Gray: `0x00808080`
   *   Lime Green: `0x006BDEC7`
   *   Black: `0x00000000`
   *   Excel Background Color: `0x00848284`
   *   White: `0x00FFFFFF`
   *   Green: `0x00008000`
   *   Purple: `0x00C000C0`

   Choose a color you like (that complements your background) and replace the existing color code.

   You can change the color after `IconArea_Text=` to your preferred color.

3. Save the text file as `Desktop.ini`. The modification is complete.
   Refresh the USB drive, and you should see the changes.
   All four files mentioned above can be hidden to prevent accidental deletion.
   After changing the icon, you need to unplug and replug the USB drive to see the effect.
   After changing the background, refresh the USB drive to see the changes.
