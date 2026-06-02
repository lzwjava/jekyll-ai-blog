---
audio: false
generated: true
lang: en
layout: post
title: An Infuse Issue
translated: false
type: note
---

The "Failed to open input stream in demuxing stream" error in Infuse typically indicates that the app cannot properly access or process the video file you're trying to stream. Since you're streaming `.mkv` files from your Nginx server (e.g., `http://192.168.1.27/movies/yourfile.mkv`) and it works with VLC but not Infuse, the issue might stem from network issues, file compatibility, or Infuse-specific quirks. Here’s how to troubleshoot and fix it:

### 1. Verify Network Connectivity

Infuse often throws this error due to network interruptions or misconfigurations.

- **Test Accessibility**: From your iPad (or wherever Infuse is running), ensure the URL works:
  - Open Safari and go to `http://192.168.1.27/movies/`. You should see the file list.
  - Tap `yourfile.mkv`—it might not play, but confirm the link is reachable.
- **Ping the Server**: On your iPad, use an app like **Network Ping Lite** (free on the App Store) to ping `192.168.1.27`. If it fails, check your Wi-Fi or server firewall.
- **Firewall Check**: On your Ubuntu server:

  ```bash
  sudo ufw status
  ```

  Ensure port 80 is open (`80/tcp ALLOW`). If not:

  ```bash
  sudo ufw allow 80
  sudo systemctl restart nginx
  ```

### 2. Restart Infuse and Device

Temporary glitches can cause this error.

- **Close Infuse**: Double-tap the Home button (or swipe up on newer iPads) and swipe Infuse away.
- **Reopen**: Launch Infuse and retry the stream.
- **Reboot iPad**: Hold the power button, slide to power off, then restart. Test again.

### 3. Check File Compatibility

While Infuse supports `.mkv`, the error might relate to the file’s codecs or structure.

- **Test Another File**: Upload a small, known-working `.mkv` (e.g., encoded with H.264 video and AAC audio) to `/var/www/movies/`:

  ```bash
  sudo mv /path/to/testfile.mkv /var/www/movies/
  sudo chown www-data:www-data /var/www/movies/testfile.mkv
  sudo chmod 644 /var/www/movies/testfile.mkv
  ```

  Try streaming `http://192.168.1.27/movies/testfile.mkv` in Infuse.
- **Codec Check**: Since VLC plays it, the file is likely streamable, but Infuse might struggle with rare codecs (e.g., VP9, Opus). Use VLC on your Mac to inspect:
  - Open the `.mkv`, press `Cmd + I` (Tools > Codec Information), and note the video/audio codecs.
  - If it’s not H.264/AAC, re-encode with HandBrake (free, handbrake.fr):
    - Load the `.mkv`, select "H.264 (x264)" video and "AAC" audio, then convert.

### 4. Adjust Nginx Config

Infuse might need specific headers or settings for smooth streaming.

- **Update Config**: Edit your Nginx file (e.g., `/etc/nginx/sites-enabled/default`):

  ```nginx
  server {
      listen 80;
      server_name 192.168.1.27 localhost;

      location /movies/ {
          alias /var/www/movies/;
          autoindex on;
          add_header Accept-Ranges bytes;  # Ensures range requests work
          add_header Content-Disposition "inline";  # Helps streaming
      }
  }
  ```

- **Reload**:

  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```

- **Why**: `Accept-Ranges` ensures Infuse can request parts of the file (critical for streaming).

### 5. Submit a Diagnostic Report

Infuse’s developers suggest this for persistent issues.

- **Steps**:
  1. In Infuse, go to **Settings > General**.
  2. Tap **Submit Diagnostic Report**.
  3. Note the code it gives you.
  4. Visit [Firecore’s Community Forum](https://community.firecore.com/), post the code, and describe your setup (Nginx, `.mkv`, HTTP streaming).
- **Why**: They can pinpoint if it’s a bug or config issue.

### 6. Alternative Workaround

If Infuse keeps failing:

- **Use VLC**: Stick with VLC for Mobile on your iPad (as it works reliably).
- **Switch Apps**: Try **nPlayer** or **PlayerXtreme** (App Store) with the same URL.

### Likely Cause

Since VLC streams it fine, it’s probably a network hiccup or Infuse’s stricter handling of the HTTP stream. The Nginx tweak (step 4) and a test file (step 3) often resolve this. If not, the diagnostic report will clarify.

Let me know what you see after trying these—especially any log errors or the diagnostic code!
