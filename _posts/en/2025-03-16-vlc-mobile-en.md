---
audio: false
generated: true
lang: en
layout: post
title: Streaming MKV Files on iPad with VLC Mobile and Other Apps
translated: false
type: note
---

To stream your `.mkv` files from your Nginx server (e.g., `http://192.168.1.27/movies/`) on your iPad without downloading them entirely, you’ll need an app that supports HTTP streaming and `.mkv` playback. iPadOS doesn’t natively handle `.mkv` files well in Safari or the Files app, so a third-party media player is the way to go. Here’s how to achieve that "magic" on your iPad:

### Recommended Apps for Streaming `.mkv` on iPad

#### 1. VLC for Mobile (Free, Best Option)

VLC is available on iPadOS and works similarly to the Mac version, supporting HTTP streaming with range requests.

- **Install**:
  1. Open the **App Store** on your iPad.
  2. Search for **VLC for Mobile**.
  3. Tap **Get** (or the cloud icon if you’ve installed it before), then authenticate with your Apple ID if prompted.
- **Stream**:
  1. Open the **VLC** app.
  2. Tap the **Network** tab (cone icon) at the bottom.
  3. Select **Open Network Stream**.
  4. Enter `http://192.168.1.27/movies/yourfile.mkv`.
  5. Tap **Open Network Stream** (or the play button).
- **Why It Works**: VLC buffers the stream, letting you play and seek without downloading the full file.

#### 2. nPlayer (Paid, Premium Option)

nPlayer is a powerful media player with excellent `.mkv` support and streaming capabilities.

- **Install**:
  1. Open the **App Store**.
  2. Search for **nPlayer** (costs around $8.99, but there’s a free lite version with ads).
  3. Tap **Get** or **Buy**, then install.
- **Stream**:
  1. Open **nPlayer**.
  2. Tap the **+** icon or **Network** option.
  3. Select **Add URL** or **HTTP/HTTPS**.
  4. Enter `http://192.168.1.27/movies/yourfile.mkv`.
  5. Tap **Play**.
- **Why It Works**: Supports advanced codecs and smooth streaming; great UI for iPad.

#### 3. Infuse (Free with In-App Purchases)

Infuse is another popular choice for streaming and playing `.mkv` files, with a sleek interface.

- **Install**:
  1. Open the **App Store**.
  2. Search for **Infuse**.
  3. Tap **Get** (free tier works for basic streaming; Pro upgrade is optional).
- **Stream**:
  1. Open **Infuse**.
  2. Tap **Add Files** > **Via URL**.
  3. Enter `http://192.168.1.27/movies/yourfile.mkv`.
  4. Tap **Add** or **Play**.
- **Why It Works**: Streams over HTTP and handles `.mkv` well; Pro features (like AirPlay) are optional.

### Steps to Get Started

1. **Connect to the Same Network**:
   - Ensure your iPad is on the same Wi-Fi network as your Nginx server (e.g., `192.168.1.x`).
   - Test connectivity: Open Safari on your iPad and go to `http://192.168.1.27/movies/`. You should see the file list (even if Safari can’t play `.mkv`).

2. **Pick an App**:
   - **VLC** is free and reliable—start here.
   - Install it from the App Store as described.

3. **Enter the URL**:
   - Use the exact URL of your `.mkv` file (e.g., `http://192.168.1.27/movies/yourfile.mkv`).
   - You can copy the link from Safari’s file listing and paste it into the app.

4. **Play and Enjoy**:
   - The app will stream the video. You can pause, seek, or adjust playback without downloading the whole file.

### Troubleshooting

- **Connection Fails**: If the iPad can’t reach `192.168.1.27`, ensure the server’s firewall allows port 80 (`sudo ufw allow 80`) and the iPad is on the same LAN.
- **Buffering**: Slow Wi-Fi might cause delays—move closer to the router or check your network speed.
- **Codec Issues**: If the `.mkv` won’t play, it might use an unsupported codec (e.g., VP9). VLC handles most, but you could re-encode with HandBrake to H.264/AAC for broader compatibility.
- **URL Typo**: Double-check the IP and path—`http://192.168.1.27/movies/yourfile.mkv` must match your setup.

### Bonus: Browse and Select

Since `autoindex on;` gives you a directory listing:

- Open Safari on your iPad, go to `http://192.168.1.27/movies/`, tap a file link, then copy the URL.
- Paste it into VLC/nPlayer/Infuse for streaming.

With **VLC for Mobile**, you’ll have that "magic" on your iPad in no time—streaming your `.mkv` files effortlessly! Let me know if you need help setting it up.
