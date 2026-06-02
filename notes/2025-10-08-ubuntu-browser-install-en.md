---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Ubuntu 24.04 Browser Installation Guide
translated: false
type: note
---

Besides **Firefox** and **Chromium**, there are quite a few good browsers you can install on **Ubuntu 24.04** — depending on your priorities (speed, privacy, compatibility, resource usage, etc.). Here’s a categorized list with notes:

---

### 🧠 Mainstream Browsers

**1. Google Chrome**

* Based on Chromium but includes Google’s sync, codecs, and proprietary features.
* Great compatibility with web apps (like Google Docs, Meet, etc.).
* Install via `.deb` from Google’s official site.

**2. Microsoft Edge (Linux version)**

* Chromium-based, polished UI, integrates with Microsoft services.
* Often faster than Chrome in memory handling.
* `.deb` package from Microsoft’s site.

---

### 🔒 Privacy-Focused Browsers

**3. Brave**

* Built on Chromium but with built-in ad blocker, tracker blocking, and Tor window mode.
* Maintains Chrome extension compatibility.
* Install:

  ```bash
  sudo apt install apt-transport-https curl
  sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
  sudo apt update
  sudo apt install brave-browser
  ```

**4. Vivaldi**

* Also Chromium-based, but highly customizable (tab tiling, keyboard shortcuts, sidebar tools).
* More feature-rich than Chrome or Edge.
* Download `.deb` from [vivaldi.com](https://vivaldi.com).

**5. Tor Browser**

* Focused on anonymity and censorship circumvention.
* Based on Firefox ESR, routes traffic through Tor network.
* Install via:

  ```bash
  sudo apt install torbrowser-launcher
  ```

---

### 🪶 Lightweight Browsers

**6. Falkon (Qt WebEngine)**

* Lightweight, minimal interface, integrates well with KDE/Qt systems.
* Install:

  ```bash
  sudo apt install falkon
  ```

**7. Midori**

* Older project revived for simplicity and low resource use.
* Decent for simple browsing, not ideal for heavy web apps.
* Install:

  ```bash
  sudo apt install midori
  ```

**8. Epiphany (GNOME Web)**

* Default GNOME browser, WebKit-based (not Chromium).
* Simple, lightweight, fits GNOME environment perfectly.
* Install:

  ```bash
  sudo apt install epiphany-browser
  ```

---

### 🧪 Developer / Niche Browsers

**9. Ungoogled Chromium**

* Chromium stripped of all Google tracking and API dependencies.
* Manual setup but good for strict privacy.
* Often found via community `.deb` or Flatpak.

**10. Floorp**

* A modern fork of Firefox with enhanced privacy and customization.
* Made by Japanese developers; becoming quite popular.
* Flatpak available from Flathub.

---

Would you like me to recommend a combination (e.g., *one privacy-focused, one lightweight, one full-featured*) that suits your workflow on this Ubuntu setup?
