---
audio: false
generated: true
lang: en
layout: post
title: Streaming Movies on Local Network
translated: false
type: note
---

To access movies downloaded on your laptop using qBittorrent from your iPad while both devices are on the same local area network (LAN), you have several options. You specifically asked about using NAS software or setting up an Nginx media server, so I’ll address those and provide a recommended approach based on ease of use and functionality.

---

### Option 1: Using NAS Software (Recommended: Plex Media Server)
NAS stands for Network Attached Storage, which typically refers to a device that stores and shares files over a network. However, since you’re using your laptop to download movies, you can install software to turn it into a NAS-like device. A popular and user-friendly choice is **Plex Media Server**, which acts as both a file-sharing solution and a media server with added features like organizing your movies and streaming them seamlessly.

#### Steps to Set Up Plex:
1. **Install Plex Media Server on Your Laptop:**
   - Download Plex Media Server from [plex.tv](https://www.plex.tv) and install it on your laptop (available for Windows, macOS, or Linux).
   - Follow the setup wizard to create an account (optional for local use) and configure the server.

2. **Add Your Movie Folder:**
   - During setup, point Plex to the folder where qBittorrent saves your downloaded movies. This adds the movies to your Plex library, and Plex can fetch metadata (like posters and descriptions) automatically.

3. **Install Plex on Your iPad:**
   - Download the free Plex app from the App Store on your iPad.

4. **Access Your Movies:**
   - Ensure both your laptop and iPad are on the same Wi-Fi network.
   - Open the Plex app on your iPad—it should automatically detect the Plex server running on your laptop.
   - Browse your movie library and tap a movie to play it. The Plex app streams the video directly from your laptop.

#### Benefits:
- **User-Friendly:** Offers a polished interface with movie artwork and details.
- **Transcoding:** If a movie format isn’t natively supported by your iPad, Plex can convert it on the fly (though this may require sufficient laptop resources).
- **No Technical Expertise Needed:** Setup is straightforward with a guided process.

#### Considerations:
- The free version of Plex is sufficient for local streaming within your LAN.
- Your laptop must remain powered on and connected to the network while you watch movies.

---

### Option 2: Simple File Sharing (No Additional Software)
If you prefer a lightweight solution without installing extra software, you can share the movie folder directly from your laptop using your operating system’s built-in file-sharing features. This uses the SMB (Server Message Block) protocol, which is supported by the iPad’s Files app.

#### Steps to Set Up File Sharing:
1. **Share the Folder on Your Laptop:**
   - **Windows:** Right-click the folder where qBittorrent saves movies, select “Properties,” go to the “Sharing” tab, and click “Share.” Choose to share it with “Everyone” or specific users and set permissions.
   - **macOS:** Open System Settings > General > Sharing, enable “File Sharing,” and add the movie folder, setting permissions as needed.
   - **Linux:** Install and configure Samba, then share the folder (requires some command-line setup).

2. **Find Your Laptop’s IP Address:**
   - On your laptop, open a command prompt or terminal and type `ipconfig` (Windows) or `ifconfig`/`ip addr` (Linux/macOS) to find the IP address (e.g., 192.168.1.100).

3. **Connect from Your iPad:**
   - Open the **Files** app on your iPad.
   - Tap the three dots (...) in the top-right corner and select “Connect to Server.”
   - Enter `smb://<laptop-ip>` (e.g., `smb://192.168.1.100`) and tap “Connect.” Provide credentials if prompted (e.g., your laptop’s username and password).
   - Navigate to the shared folder.

4. **Play the Movies:**
   - Tap a movie file to open it in the Files app’s default player, or use a third-party app like **VLC for Mobile** (available on the App Store) for broader format support.

#### Benefits:
- **Simple:** No additional software required beyond what’s already on your laptop.
- **Quick Setup:** Works with your existing system.

#### Considerations:
- Browsing files is less intuitive than with Plex—you’ll see a basic folder structure.
- Playback depends on the iPad supporting the movie format (e.g., MP4 with H.264 works well natively; VLC can handle more formats).
- Your laptop must be on and connected to the LAN.

---

### Option 3: Setting Up an Nginx Media Server
Nginx is a lightweight web server that can serve files over HTTP. You can configure it on your laptop to make your movie folder accessible via a web browser or media player on your iPad.

#### Steps to Set Up Nginx:
1. **Install Nginx on Your Laptop:**
   - Download and install Nginx (available for Windows, macOS, or Linux) from [nginx.org](https://nginx.org) or via a package manager (e.g., `sudo apt install nginx` on Ubuntu).

2. **Configure Nginx:**
   - Edit the Nginx configuration file (e.g., `/etc/nginx/nginx.conf` on Linux or a similar location):
     ```
     server {
         listen 80;
         server_name localhost;
         location /movies {
             root /path/to/your/movie/folder;
             autoindex on; # Enables directory listing
         }
     }
     ```
   - Replace `/path/to/your/movie/folder` with the actual path where qBittorrent saves movies.

3. **Start Nginx:**
   - Run `nginx` (Windows) or `sudo systemctl start nginx` (Linux) to launch the server.

4. **Access from Your iPad:**
   - Open Safari or another browser on your iPad.
   - Enter `http://<laptop-ip>/movies` (e.g., `http://192.168.1.100/movies`).
   - You’ll see a list of movie files. Tap one to play it in the browser, or copy the link and open it in a media player like VLC.

#### Benefits:
- **Lightweight:** Uses fewer resources than Plex.
- **Customizable:** You can tweak Nginx settings as needed.

#### Considerations:
- **Technical Setup:** Requires editing configuration files and some server knowledge.
- **Basic Experience:** No fancy interface—just a file list in the browser.
- **Playback:** Depends on the browser or app supporting the movie format; no transcoding is available.

---

### Recommendation
Given your options, I recommend **using Plex Media Server** as your “NAS software” solution. Here’s why:
- **Ease of Use:** Plex is simpler to set up than Nginx and provides a much better experience than basic file sharing.
- **Features:** It organizes your movies, supports transcoding if needed, and offers a dedicated iPad app for seamless streaming.
- **LAN Focus:** Works perfectly within your local network, as you specified.

If you want to avoid installing software, the **file sharing** method is a solid alternative—just share the folder and use the Files app with VLC on your iPad. However, **Nginx** is overkill for this use case unless you’re comfortable with server configuration and prefer a minimal setup.

#### Final Answer
For the best experience, install Plex Media Server on your laptop, add your qBittorrent download folder to it, and use the Plex app on your iPad to watch your movies over your LAN. Alternatively, for a simpler approach, share the folder via SMB and access it with the Files app and VLC on your iPad.
