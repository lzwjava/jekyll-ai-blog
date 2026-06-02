---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Installing WezTerm on Ubuntu
translated: false
type: note
---

The error "Unable to locate package wezterm" occurs because WezTerm isn't available in Ubuntu's default repositories. You need to add the official third-party repository first. Here's the step-by-step fix using the native APT method (recommended for seamless integration):

1. Add the GPG key for the repository:

   ```
   curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
   ```

2. Add the repository to your sources:

   ```
   echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
   ```

3. Set the correct permissions on the key file:

   ```
   sudo chmod 644 /usr/share/keyrings/wezterm-fury.gpg
   ```

4. Update your package list:

   ```
   sudo apt update
   ```

5. Now install WezTerm:

   ```
   sudo apt install wezterm
   ```

Once installed, you can run it with `wezterm` from the terminal. If you want the nightly (bleeding-edge) version instead, use `sudo apt install wezterm-nightly` in step 5—but note that it can't coexist with the stable version.

### Alternative: Flatpak (No Repo Needed)

If you prefer a sandboxed install without modifying APT sources:

1. Install Flatpak if not already present: `sudo apt install flatpak`.
2. Add Flathub: `flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`.
3. Install: `flatpak install flathub org.wezfurlong.wezterm`.
4. Run: `flatpak run org.wezfurlong.wezterm` (or add an alias: `alias wezterm='flatpak run org.wezfurlong.wezterm'`).

Flatpak is isolated, so it might limit some advanced features, but it's simpler for testing.

[WezTerm Linux Installation Guide](https://wezterm.org/install/linux.html)
