---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal Web Browsing Tools Guide
translated: false
type: note
---

I'll search for information about tools that allow browsing web pages through a terminal interface.Question: Are there any tools that allow people to treat the terminal as a browser, enabling them to browse web pages and follow redirects?

Answer:

Yes, there are several excellent tools that allow you to browse the web directly from your terminal. These are text-based web browsers that can render HTML, follow links, and navigate redirects just like a traditional graphical browser.

## Popular Terminal-Based Web Browsers

### 1. **Lynx**

Lynx is a text-based web browser that allows users to browse the web in a terminal environment, developed in 1992, and supports HTML, HTTPS, and FTP protocols. It's one of the oldest and most established command-line browsers. To use it:

- Install: `sudo apt install lynx`
- Usage: `lynx [URL]`
- Navigation: Arrow keys to move, Enter to follow links, left arrow to go back

### 2. **w3m**

w3m is a popular open-source text-based web browser for the terminal that supports SSL connections, colors, and inline images. It's actively maintained and very capable:

- Install: `sudo apt install w3m`
- Usage: `w3m [URL]`
- Navigation: Arrow keys to navigate, Shift+B to go back, Shift+T for new tab, Shift+U to open new URL

### 3. **Links/ELinks**

ELinks stands out with its menu system accessible by pressing ESC, letting you enter and save URLs, add bookmarks, and set up the browser. This browser offers a more interactive experience:

- Install: `sudo apt install links` or `sudo apt install elinks`
- Usage: `links [URL]` or `elinks [URL]`
- Navigation: Right arrow to follow links, left arrow to go back, ESC for menus

### 4. **Browsh**

Browsh is a modern text-based browser that shows HTML5, CSS3, JS, video, and even WebGL, designed to be run on a remote server via SSH or Mosh and browse web pages as text from the terminal by significantly reducing bandwidth and increasing browsing speed.

- Usage: `ssh brow.sh` (use SSH connection)
- Press Ctrl+L to focus on URL bar

## Key Features

These tools support:

- Following hyperlinks and redirects
- Multiple tabs (in some browsers)
- Cookie handling
- Mouse support (in some implementations)
- Image viewing through external programs
- Search functionality
- Keyboard navigation

## Use Cases

Terminal browsers are useful in remote server scenarios without a graphical interface, for checking status pages, reading documentation, or troubleshooting by browsing relevant web resources directly from the command line. They're also beneficial for low-bandwidth environments and distraction-free browsing.

References:

- <https://itsfoss.com/terminal-web-browsers/>
- <https://opensource.com/article/16/12/web-browsers-linux-command-line>
- <https://www.tecmint.com/command-line-web-browser-download-file-in-linux/>
- <https://www.tutorialspoint.com/a-command-line-web-browsing-with-lynx-and-links-tools>
- <https://www.fosslinux.com/18554/how-to-access-website-using-command-line-from-the-terminal.htm>
