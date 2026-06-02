---
audio: false
generated: true
lang: en
layout: post
title: Install VLC Media Player on Ubuntu
translated: false
type: note
---

To install VLC media player on your Ubuntu system, you can use either the terminal (command line) or the Ubuntu Software Center (graphical interface). Below are detailed instructions for both methods.

---

### **Method 1: Install VLC Using the Terminal**

This method is quick and efficient, especially if you're comfortable with the command line. Follow these steps:

1. **Open the Terminal**
   - Search for "Terminal" in the Ubuntu application menu, or press `Ctrl + Alt + T` to open it.

2. **Update the Package List**
   - Before installing software, it’s a good practice to ensure your package list is up to date. Run this command:

     ```bash
     sudo apt update
     ```

   - Enter your password when prompted. This command refreshes the list of available software packages.

3. **Install VLC**
   - Once the package list is updated, install VLC by running:

     ```bash
     sudo apt install vlc
     ```

   - You’ll need to enter your password again. The system may ask you to confirm the installation by typing `y` and pressing Enter. This will download and install VLC along with its necessary dependencies.

4. **Verify the Installation**
   - After installation, check if VLC is installed by typing:

     ```bash
     vlc
     ```

   - This should launch the VLC media player. If it opens, the installation was successful.
   - Alternatively, you can check the version of VLC by running:

     ```bash
     vlc --version
     ```

   - This will display something like "VLC media player 3.0.11.1 Vetinari" (the version number may vary).

5. **Optional: Test VLC**
   - To ensure VLC works properly, try playing a media file. For example, if you have an MP4 file on your desktop, right-click it and select "Open with VLC media player." If it plays, VLC is fully functional.

---

### **Method 2: Install VLC Using Ubuntu Software Center**

If you prefer a graphical interface over the terminal, use the Ubuntu Software Center:

1. **Open Ubuntu Software Center**
   - Search for "Ubuntu Software" in the application menu and click to open it.

2. **Search for VLC**
   - In the Software Center, click the search icon (usually a magnifying glass) and type "VLC" into the search bar.

3. **Install VLC**
   - Find "VLC media player" in the search results, click on it, and then click the "Install" button. You may need to enter your password to authorize the installation.

4. **Launch VLC**
   - Once installed, you can launch VLC directly from the Software Center by clicking "Open" (if available) or by searching for "VLC" in the application menu.

---

### **Additional Notes**

- **Keeping VLC Updated**
  - If you installed VLC using the terminal, you can keep it updated by periodically running:

     ```bash
     sudo apt update
     sudo apt upgrade
     ```

  - This updates VLC along with other system packages. If you used the Software Center, updates are typically managed through the same interface.

- **Plugins and Codecs**
  - The default VLC installation via `sudo apt install vlc` includes essential plugins (like `vlc-plugin-base`) and codecs, so it should play most common media formats (e.g., MP4, AVI) out of the box. If you encounter issues with specific file types, you can install additional codecs later, such as `ubuntu-restricted-extras`, using:

     ```bash
     sudo apt install ubuntu-restricted-extras
     ```

- **Alternative Installation via Snap**
  - VLC is also available as a Snap package. If you prefer this method, run:

     ```bash
     sudo snap install vlc
     ```

  - However, the `apt` method is recommended for most users as it integrates well with the system.

---

By following either method, you’ll have VLC installed and ready to use on your Ubuntu system. The terminal method is faster for command-line users, while the Software Center is ideal for those who prefer a graphical approach. Enjoy your media playback!

---

To fix the error you're encountering when playing an MKV file in VLC on Ubuntu—specifically the message about missing MPEG-4 AAC and H.265 decoders—follow the steps below. This issue typically occurs because Ubuntu doesn’t include certain proprietary codecs by default due to licensing restrictions. Installing additional codec packages should resolve the problem.

---

### **Solution**

#### **Step 1: Install the `ubuntu-restricted-extras` Package**

This package provides support for a variety of codecs, including MPEG-4 AAC (audio) and H.265 (HEVC) video, which are likely missing from your VLC installation.

1. **Open the Terminal**
   - Search for "Terminal" in the Ubuntu application menu or press `Ctrl + Alt + T`.

2. **Update the Package List**
   - Run this command to ensure your system’s package list is up to date:

     ```bash
     sudo apt update
     ```

3. **Install `ubuntu-restricted-extras`**
   - Run the following command:

     ```bash
     sudo apt install ubuntu-restricted-extras
     ```

   - You may need to enter your password. During installation, you might be prompted to accept the End User License Agreement (EULA) for certain components—follow the on-screen instructions to agree and proceed.

4. **Restart VLC**
   - Close VLC if it’s open, then reopen it and try playing the MKV file again.

---

#### **Step 2: Install Additional Codec Packages (If Needed)**

If the error persists after Step 1, install specific packages that provide additional support for H.265 and other codecs.

1. **Install `libde265-0` and `libavcodec-extra`**
   - Run this command to install libraries for H.265 decoding and extra codec support:

     ```bash
     sudo apt install libde265-0 libavcodec-extra
     ```

2. **Restart VLC**
   - Close and reopen VLC, then attempt to play the MKV file again.

---

#### **Step 3: Additional Troubleshooting (If Necessary)**

If the issue still isn’t resolved, try these extra steps:

- **Check VLC Version**
  - Ensure you’re using the latest VLC version. Check your current version with:

    ```bash
    vlc --version
    ```

  - If it’s outdated, update it by running:

    ```bash
    sudo apt update
    sudo apt upgrade vlc
    ```

- **Test Another MKV File**
  - Play a different MKV file to see if the issue is specific to one file. If other files work, the problematic file might be corrupted or use an unsupported encoding.

- **View VLC Logs for More Details**
  - For advanced troubleshooting, run VLC from the terminal with verbose output:

    ```bash
    vlc --verbose 2
    ```

  - Try playing the file and look for detailed error messages about the missing codecs.

---

### **Additional Notes**

- **Why This Happens**: MKV is a container format that can use various codecs like MPEG-4 AAC for audio and H.265 for video. Ubuntu’s default VLC installation might lack these due to legal restrictions on proprietary software.
- **Hardware Acceleration**: If your system supports H.265 hardware decoding (e.g., via a modern GPU), ensure your graphics drivers are updated. However, this error suggests a missing software decoder, so hardware acceleration is likely not the main issue.
- **Next Steps**: If none of the above works, consider reinstalling VLC or seeking help on Ubuntu or VLC forums with details about your system and the specific MKV file.

---

By following these steps, you should be able to fix the missing decoder errors and play your MKV files in VLC successfully. Start with Step 1, as it’s the most straightforward and likely solution.
