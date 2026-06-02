---
audio: false
generated: true
lang: en
layout: post
title: Streaming MKV Files from Nginx with VLC
translated: false
type: note
---

Since you have an Nginx server serving `.mkv` files (e.g., at `http://192.168.1.27/movies/`), and you want to view them from a Mac without downloading the entire file, you’re looking to **stream** the videos. Nginx can serve files in a way that supports HTTP range requests (which it does by default), allowing media players to stream rather than download fully. Here’s how to do it, along with suitable tools for macOS.

### Prerequisites
- Your Nginx config (e.g., `alias /var/www/movies/; autoindex on;`) is working, and `http://192.168.1.27/movies/` lists files.
- The `.mkv` files are accessible over the network (tested from another machine).

### Tools to Stream `.mkv` Files on macOS
You need a media player that supports streaming via HTTP and handles `.mkv` files well. Here are the best options:

#### 1. VLC Media Player (Free, Recommended)
VLC is a versatile, open-source player that supports streaming `.mkv` files over HTTP without downloading the whole file (it uses range requests).
- **Install**:
  - Download from [videolan.org](https://www.videolan.org/vlc/).
  - Install it on your Mac.
- **Stream**:
  1. Open VLC.
  2. Press `Cmd + N` (or go to `File > Open Network`).
  3. Enter the URL, e.g., `http://192.168.1.27/movies/yourfile.mkv`.
  4. Click `Open`.
- **Why It Works**: VLC buffers only what’s needed, letting you seek and play without downloading the entire file.

#### 2. IINA (Free, macOS-Native)
IINA is a modern, macOS-specific player with excellent `.mkv` support and streaming capabilities.
- **Install**:
  - Download from [iina.io](https://iina.io/) or `brew install iina` (with Homebrew).
- **Stream**:
  1. Open IINA.
  2. Press `Cmd + U` (or `File > Open URL`).
  3. Enter `http://192.168.1.27/movies/yourfile.mkv`.
  4. Click `OK`.
- **Why It Works**: Lightweight, supports HTTP streaming, and integrates nicely with macOS.

#### 3. QuickTime Player (Built-in, Limited)
macOS’s default QuickTime Player can stream some formats, but `.mkv` support is spotty without extra codecs.
- **Try It**:
  1. Open QuickTime Player.
  2. Press `Cmd + U` (or `File > Open Location`).
  3. Enter `http://192.168.1.27/movies/yourfile.mkv`.
  4. Click `Open`.
- **Caveat**: If it doesn’t work, install Perian (an old codec pack) or use VLC/IINA instead.

#### 4. Browser (Safari/Chrome, Simplest)
Modern browsers can stream `.mkv` files directly if they’re encoded with supported codecs (e.g., H.264 video, AAC audio).
- **How**:
  1. Open Safari or Chrome on your Mac.
  2. Go to `http://192.168.1.27/movies/`.
  3. Click `yourfile.mkv`.
- **Why It Works**: Browsers use HTML5 video tags and range requests for streaming.
- **Limitation**: If the `.mkv` uses unsupported codecs (e.g., VP9, Opus), it won’t play—fall back to VLC or IINA.

### Ensure Nginx Supports Streaming
Nginx handles range requests by default, which is what enables streaming. To confirm:
- Check your config doesn’t disable this (e.g., no `limit_rate` or custom headers blocking ranges).
- Test with VLC or IINA—if you can seek (e.g., jump to 5 minutes in), streaming is working.

### Recommended Workflow
1. **Use VLC** (it’s the most reliable):
   - Install VLC.
   - Open `http://192.168.1.27/movies/yourfile.mkv` via `Cmd + N`.
   - Play, pause, or seek as needed.
2. **Directory Browsing**:
   - Visit `http://192.168.1.27/movies/` in Safari/Chrome to see the file list (thanks to `autoindex on;`).
   - Copy the URL of `yourfile.mkv` and paste it into VLC or IINA.

### Troubleshooting
- **Buffering Issues**: Slow network or large `.mkv` files might lag—ensure your LAN is stable (e.g., Wi-Fi isn’t dropping).
- **Codec Errors**: If VLC says "unsupported format," the `.mkv` might use rare codecs—try re-encoding it with HandBrake to H.264/AAC.
- **Connection Refused**: Revisit firewall settings on the server (`sudo ufw allow 80` or equivalent).

With VLC or IINA, you’ll be streaming your `.mkv` files from your Mac in no time without downloading them fully. Let me know if you hit any snags!

---

Installing VLC on a Mac is straightforward. Here’s a quick guide to get it set up so you can stream your `.mkv` files from your Nginx server:

### Method 1: Download from the Official Website
1. **Visit the VLC Website**:
   - Open your browser (e.g., Safari or Chrome).
   - Go to [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/).

2. **Download VLC**:
   - Click the **Download VLC** button. It should automatically detect your macOS and offer the correct version (e.g., VLC 3.0.20 as of now).
   - You’ll get a `.dmg` file (e.g., `vlc-3.0.20.dmg`).

3. **Install VLC**:
   - Open the downloaded `.dmg` file (usually in your `Downloads` folder).
   - Drag the VLC icon to the **Applications** folder as prompted in the window.
   - Close the `.dmg` window and eject it (right-click the disk icon on your desktop or in Finder and select "Eject").

4. **Run VLC**:
   - Go to your **Applications** folder (e.g., via Finder or Spotlight with `Cmd + Space`, then type "Applications").
   - Double-click **VLC**.
   - If macOS blocks it ("unidentified developer"), right-click VLC, select **Open**, then click **Open** in the dialog.

5. **Stream Your File**:
   - Open VLC.
   - Press `Cmd + N` (or `File > Open Network`).
   - Enter `http://192.168.1.27/movies/yourfile.mkv`.
   - Click **Open**.

### Method 2: Install via Homebrew (Terminal)
If you prefer the command line and have Homebrew installed:
1. **Install Homebrew** (if not already):
   - Open Terminal.
   - Run:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Follow the prompts.

2. **Install VLC**:
   - In Terminal:
     ```bash
     brew install vlc
     ```

3. **Run VLC**:
   - Launch it from Terminal with:
     ```bash
     open -a VLC
     ```
   - Or find it in **Applications** as `VLC.app`.

4. **Stream**:
   - Same as above: `Cmd + N`, enter your URL, and play.

### Verify Installation
- Once installed, VLC should appear in your **Applications** folder.
- Test it with a local file first (drag an `.mkv` into VLC) to ensure it works, then try streaming `http://192.168.1.27/movies/yourfile.mkv`.

### Troubleshooting
- **Download Fails**: Use a mirror link from the VLC site if the main download is slow.
- **Security Prompt**: If macOS blocks it, go to `System Settings > Security & Privacy > General` and click **Open Anyway**.
- **Not Playing**: Ensure the URL is correct and your server is reachable (`ping 192.168.1.27` from Terminal).

That’s it! VLC should now be ready on your Mac to stream your `.mkv` files. Let me know if you need help with the next step!
