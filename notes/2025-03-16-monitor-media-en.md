---
audio: false
generated: true
lang: en
layout: post
title: Monitor Media Playback on Ubuntu via VLC
translated: false
type: note
---

To watch movies on your monitor using your second laptop (running Ubuntu with an Nginx server) without much hassle, here’s the best approach based on what you already have. You want to avoid buying extra devices like a Fire TV Stick or Apple TV, and while a long HDMI cable works, you’d prefer not to keep interacting with the laptop to select and play videos. Let’s set up a solution that’s simple and convenient using your existing setup.

Since your movies are stored on your Ubuntu laptop and it’s already running an Nginx server, the easiest way is to connect that laptop directly to your monitor via HDMI and make playback control effortless. Here’s how you can do it:

### Solution: Connect Laptop to Monitor and Use VLC with Remote Control

#### What You’ll Need
- **HDMI cable**: To connect your Ubuntu laptop to the monitor.
- **VLC media player**: Likely already installed on Ubuntu, or easy to install.
- **Smartphone or another device**: To control playback remotely over your home network.

#### Steps to Set Up
1. **Connect the Laptop to the Monitor**
   - Plug one end of an HDMI cable into your Ubuntu laptop’s HDMI port and the other into your monitor’s HDMI input.
   - Turn on the monitor and select the correct HDMI input. The laptop’s display should now appear on the monitor, including video and audio (if your monitor has speakers; otherwise, use the laptop’s speakers or connect external ones).

2. **Install VLC (if not already installed)**
   - Open a terminal on your Ubuntu laptop and run:
     ```
     sudo apt update
     sudo apt install vlc
     ```
   - This ensures VLC, a versatile media player, is ready to use.

3. **Enable VLC’s Web Interface for Remote Control**
   - Open VLC on your Ubuntu laptop.
   - Go to **Tools > Preferences**.
   - In the bottom left, click **"All"** to show advanced settings.
   - Navigate to **Interface > Main interfaces**, and check the **"Web"** box to enable the HTTP interface.
   - Go to **Interface > Main interfaces > Lua**, and set a password (e.g., "mypassword") in the **Lua HTTP Password** field.
   - Click **Save**, then restart VLC.

4. **Load Your Movies in VLC**
   - In VLC, go to **Playback > Playlist**.
   - Drag and drop your movie files from their folder (where they’re stored on the laptop) into the VLC playlist, or use **Media > Open File** to add them one by one.
   - Save the playlist (e.g., "My Movies") via **Ctrl+Y** for quick access later.

5. **Find Your Laptop’s IP Address**
   - In the terminal, type:
     ```
     ip addr show
     ```
   - Look for the IP address under your network connection (e.g., `192.168.1.100` under `wlan0` for Wi-Fi). This is how your phone will connect to the laptop.

6. **Control Playback from Your Phone**
   - Ensure your phone and laptop are on the same Wi-Fi network.
   - Open a web browser on your phone and enter: `http://<laptop-ip>:8080` (e.g., `http://192.168.1.100:8080`).
   - When prompted, leave the username blank and enter the password you set (e.g., "mypassword").
   - You’ll see VLC’s web interface. Use it to play, pause, stop, or select the next movie from your playlist.

7. **Start Watching**
   - On the laptop, start playing a movie in VLC (double-click an item in the playlist).
   - Switch VLC to full-screen mode (**View > Fullscreen** or press `F`).
   - Sit back, and use your phone to control playback without touching the laptop.

#### Why This Works for You
- **No Extra Cost**: Uses your existing laptop, monitor, and phone—no need to buy anything new.
- **Minimal Hassle**: After the initial setup, you just turn on the laptop and monitor, open VLC, and control everything from your phone.
- **Local Playback**: Since the movies are on the laptop connected to the monitor, you don’t need to stream over the network (though Nginx is set up, it’s not necessary here). VLC plays the files directly, ensuring smooth performance.

#### Optional Improvements
- **Wireless Control**: If you have a wireless mouse or keyboard, you could use that instead of your phone, but the phone is more convenient from a distance.
- **Auto-Start**: To make it even easier, set VLC to launch your playlist automatically when the laptop boots:
  - Add VLC with your playlist to Ubuntu’s **Startup Applications** (search "Startup Applications" in Ubuntu, click "Add," and enter: `vlc /path/to/your/playlist.m3u`).
- **Audio Check**: If your monitor lacks speakers, ensure audio comes through the laptop or connect external speakers via the laptop’s audio jack.

### Alternative: Use Nginx and a Browser (if Preferred)
If you’d rather use the Nginx server:
- Set up a simple HTML page in your Nginx directory (e.g., `/var/www/html/movies`) with links to your movie files (e.g., `<a href="movie1.mp4">Movie 1</a>`).
- Connect the laptop to the monitor, open a browser, and go to `http://localhost/movies`.
- Click a link to play a movie in the browser, and use full-screen mode.
- However, this doesn’t easily allow phone control unless you access the same page from your phone and cast, which might require extra setup or hardware.

### Final Recommendation
The VLC method is the best fit. It’s straightforward, leverages your current setup, and lets you "open monitor, and then watch without much hassle" by controlling everything from your phone. After setting it up once, you’ll just need to start VLC and use your phone to pick movies—simple and effective!
