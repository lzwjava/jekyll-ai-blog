---
audio: false
generated: true
lang: en
layout: post
title: Install qBittorrent on Ubuntu
translated: false
type: note
---

Installing qBittorrent on Ubuntu is straightforward. Here are the steps:

### **Method 1: Install qBittorrent via APT (Recommended)**
1. **Update your package list**:
   ```bash
   sudo apt update
   ```

2. **Install qBittorrent**:
   ```bash
   sudo apt install qbittorrent
   ```

3. **Launch qBittorrent**:
   - From the terminal:
     ```bash
     qbittorrent
     ```
   - Or search for "qBittorrent" in the Ubuntu application menu.

---

### **Method 2: Install the Latest Version via PPA (Optional)**
If you want a newer version than Ubuntu's default repository provides, you can use the official PPA:

1. **Add the qBittorrent PPA**:
   ```bash
   sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable
   ```

2. **Update package lists**:
   ```bash
   sudo apt update
   ```

3. **Install qBittorrent**:
   ```bash
   sudo apt install qbittorrent
   ```

4. **Run qBittorrent**:
   ```bash
   qbittorrent
   ```

---

### **Method 3: Install qBittorrent via Flatpak (Alternative)**
If you prefer Flatpak:

1. **Install Flatpak (if not already installed)**:
   ```bash
   sudo apt install flatpak
   ```

2. **Add the Flathub repository**:
   ```bash
   flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
   ```

3. **Install qBittorrent**:
   ```bash
   flatpak install flathub org.qbittorrent.qBittorrent
   ```

4. **Run qBittorrent**:
   ```bash
   flatpak run org.qbittorrent.qBittorrent
   ```

---

### **Uninstalling qBittorrent (if needed)**
- **If installed via APT or PPA**:
  ```bash
  sudo apt remove qbittorrent
  ```
- **If installed via Flatpak**:
  ```bash
  flatpak uninstall org.qbittorrent.qBittorrent
  ```

That’s it! You now have qBittorrent installed on Ubuntu. 🚀 Let me know if you need any help!
