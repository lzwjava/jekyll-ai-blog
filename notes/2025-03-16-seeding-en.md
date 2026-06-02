---
audio: false
generated: true
lang: en
layout: post
title: Configuring qBittorrent for Seeding and Automatic File Management
translated: false
type: note
---

It seems like you want to configure qBittorrent to continue seeding your torrents while automatically moving completed `.mkv` files to `/var/www/movies` for serving on a server. Below, I’ll guide you through the steps to achieve this, assuming you’re using qBittorrent on a system where `/var/www/movies` is a valid directory (e.g., a Linux server with a web server like Apache or Nginx). Here's how you can set it up:

---

### Step-by-Step Guide

#### 1. **Understand qBittorrent’s File Management**
   - qBittorrent can move files automatically after download completion while still seeding them, as long as you use its built-in "Set Location" or "Move" features properly. Moving files manually outside of qBittorrent (e.g., via a file explorer) will break seeding unless you re-point qBittorrent to the new location.

#### 2. **Configure qBittorrent Settings**
   - Open qBittorrent.
   - Go to **Tools > Options** (or press `Alt + O`).

   ##### a) **Set Default Download Location**
   - Under the **Downloads** tab:
     - Set **Default Save Path** to a temporary directory where files will download initially (e.g., `/home/user/downloads` or wherever you have space). This is where qBittorrent will store files while downloading and seeding until they’re moved.
     - Ensure **Keep incomplete files in** is set to the same or a different directory if you prefer (optional).

   ##### b) **Enable Automatic File Moving**
   - Scroll down to **When Torrent Finishes**:
     - Check the box for **Automatically move completed downloads to**.
     - Set the path to `/var/www/movies`. This tells qBittorrent to move the `.mkv` files to `/var/www/movies` once the download is complete.
   - Important: qBittorrent will continue seeding from the new location (`/var/www/movies`) after the move, so you don’t need to worry about losing seeding capability.

   ##### c) **Optional: Filter for .mkv Files**
   - If you only want `.mkv` files to move to `/var/www/movies` (and not other file types like `.txt` or `.nfo`), you can use qBittorrent’s **Run External Program** feature (see Step 3 below) instead of the automatic move option.

   ##### d) **Seeding Limits**
   - Under **BitTorrent** tab or **Downloads** tab:
     - Set seeding limits if desired (e.g., seed until a certain ratio or time is reached). For unlimited seeding, set **Ratio** and **Time** to `0` or uncheck the limits.
     - This ensures qBittorrent keeps uploading your seeds indefinitely from `/var/www/movies`.

   - Click **Apply** and **OK** to save settings.

#### 3. **Alternative: Use "Run External Program" for More Control**
   - If you need more customization (e.g., only move `.mkv` files and leave others seeding from the original location), use this:
     - In **Options > Downloads**, scroll to **Run External Program**.
     - Check **Run external program on torrent completion**.
     - Enter a command like:
       ```
       mv "%F"/*.mkv /var/www/movies/
       ```
       - `%F` is a qBittorrent placeholder for the content folder path. This command moves only `.mkv` files to `/var/www/movies`.
     - Note: qBittorrent will still seed the `.mkv` files from `/var/www/movies` after the move, but other files (e.g., `.torrent`, `.nfo`) will remain in the original location and continue seeding from there unless you adjust further.

#### 4. **Verify Permissions**
   - Ensure qBittorrent has write permissions to `/var/www/movies`:
     - On Linux, run:
       ```
       sudo chown -R <qbittorrent-user>:<qbittorrent-group> /var/www/movies
       sudo chmod -R 775 /var/www/movies
       ```
       Replace `<qbittorrent-user>` and `<qbittorrent-group>` with the user and group under which qBittorrent runs (e.g., your username or `qbittorrent` if it’s a service).
   - Without proper permissions, qBittorrent won’t be able to move files to this directory.

#### 5. **Test the Setup**
   - Add a torrent with `.mkv` files to qBittorrent.
   - Wait for it to finish downloading.
   - Check that:
     - The `.mkv` files move to `/var/www/movies`.
     - The torrent status in qBittorrent switches to **Seeding**, and the upload speed indicates it’s still sharing the files.
   - Visit `/var/www/movies` to confirm the files are there and accessible (e.g., via your web server at `http://<server-ip>/movies`).

#### 6. **Manually Move Existing Files (If Needed)**
   - For torrents you’ve already downloaded and want to move to `/var/www/movies` without breaking seeding:
     - In qBittorrent, right-click the torrent.
     - Select **Set Location**.
     - Choose `/var/www/movies` and let qBittorrent move the files.
     - After the move, qBittorrent will resume seeding from the new location.

#### 7. **Optimize Upload Settings**
   - To maximize seeding:
     - Go to **Options > Speed**:
       - Set **Upload** to `0` (unlimited) or a high value (e.g., 80% of your max upload speed).
     - Go to **Options > Connection**:
       - Ensure **Enable UPnP / NAT-PMP port forwarding** is checked (if your router supports it) or manually forward a port for better connectivity.
       - Increase **Global maximum number of upload slots** (e.g., to 50 or 100) to allow more peers to connect.

---

### Key Notes
- **Seeding Continuity**: As long as you let qBittorrent handle the file moving (via automatic move or "Set Location"), it will update its internal tracking and continue seeding from `/var/www/movies`.
- **Web Server Access**: Ensure your web server (e.g., Apache/Nginx) is configured to serve files from `/var/www/movies`. This is outside qBittorrent’s scope but critical for your server goal.
- **Storage**: Make sure `/var/www/movies` has enough space for your files.

If you run into issues (e.g., files not moving or seeding stopping), let me know your setup details (OS, qBittorrent version, etc.), and I’ll refine the solution!
