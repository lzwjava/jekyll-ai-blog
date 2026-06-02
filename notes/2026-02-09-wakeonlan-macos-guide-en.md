---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Install WakeOnLan on macOS Guide
translated: false
type: note
---

Question: How to install wakeonlan on macOS?

Answer:

You can install the `wakeonlan` command-line tool on macOS using one of these main methods (the Homebrew approach is the most common and recommended).

### Recommended Method: Using Homebrew (package manager)

1. If you don't have Homebrew installed yet, open **Terminal** and run:

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   (Follow any on-screen instructions; it may ask for your password.)

2. Once Homebrew is installed, run this command to install wakeonlan:

   ```
   brew install wakeonlan
   ```

3. After installation, you can use it directly:

   ```
   wakeonlan AA:BB:CC:DD:EE:FF
   ```

   (Replace with your target MAC address. You can add options like `-i 192.168.1.255` for broadcast IP if needed.)

Homebrew installs it to `/opt/homebrew/bin/wakeonlan` (Apple Silicon) or `/usr/local/bin/wakeonlan` (Intel), which is automatically added to your PATH.

### Alternative: Manual Installation (no Homebrew needed)

If you prefer not to install Homebrew:

1. Open **Terminal** and create a bin directory (if you don't have one):

   ```
   mkdir -p ~/bin
   ```

2. Download the wakeonlan Perl script:

   ```
   curl https://raw.githubusercontent.com/jpoliv/wakeonlan/master/wakeonlan -o ~/bin/wakeonlan
   ```

3. Make it executable:

   ```
   chmod +x ~/bin/wakeonlan
   ```

4. Add `~/bin` to your PATH (if not already). Edit `~/.zshrc` (or `~/.bash_profile` on older macOS):

   ```
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

5. Now use it the same way:

   ```
   wakeonlan AA:BB:CC:DD:EE:FF
   ```

### Other Options

- Using **MacPorts** (alternative package manager): `sudo port install wakeonlan` (less common than Homebrew).
- GUI alternatives exist (e.g., miniWOL or Wolow), but for command-line testing like in your original steps, the above methods match the Linux `wakeonlan` behavior best.

Note: On very recent macOS versions (e.g., Sequoia), if you see a Perl-related error after `brew install`, try `brew reinstall wakeonlan` to fix the shebang/path.

References:

- [https://formulae.brew.sh/formula/wakeonlan](https://formulae.brew.sh/formula/wakeonlan)
- [https://www.cyberciti.biz/faq/apple-os-x-wake-on-lancommand-line-utility](https://www.cyberciti.biz/faq/apple-os-x-wake-on-lancommand-line-utility)
- [https://superuser.com/questions/411213/how-to-send-a-magic-packet-from-os-x-in-order-to-wake-a-pc-on-the-lan-wol](https://superuser.com/questions/411213/how-to-send-a-magic-packet-from-os-x-in-order-to-wake-a-pc-on-the-lan-wol)
- [https://github.com/jpoliv/wakeonlan](https://github.com/jpoliv/wakeonlan)
