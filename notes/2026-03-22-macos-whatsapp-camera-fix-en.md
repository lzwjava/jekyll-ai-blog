---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix WhatsApp Camera Permission on macOS
translated: false
type: note
---

This is a common macOS permission issue. When an app doesn't show up in Privacy & Security settings, it means it hasn't requested that permission yet. Here's how to fix it:

## Force WhatsApp to request camera permission:

1. **Fully quit WhatsApp** (Cmd+Q, not just close the window)

2. **Reset the TCC database for WhatsApp** (this clears its permission state):
   ```bash
   tccutil reset Camera com.whatsapp.WhatsApp
   ```

3. **Restart WhatsApp** and try to scan the QR code again. It should now pop up asking for camera permission.

## If that doesn't work:

**Manual TCC database edit** (advanced):
```bash
# Open the TCC database
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT or REPLACE INTO access VALUES('kTCCServiceCamera','com.whatsapp.WhatsApp',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1687910000);"
```

Then restart WhatsApp.

## Alternative: Use WhatsApp Web instead

If the camera permission issue persists, you can bypass it entirely:
1. Open WhatsApp on your phone
2. Go to Settings > Linked Devices > Link a Device
3. On Mac, open https://web.whatsapp.com in a browser
4. Scan the QR code with your phone (not the Mac camera)

This way you're using your phone's camera to scan, avoiding the Mac permission issue entirely.

Try the `tccutil reset` command first - that usually fixes it.