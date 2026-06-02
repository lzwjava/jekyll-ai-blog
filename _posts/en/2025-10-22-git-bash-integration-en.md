---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Integrating Git Bash with Windows Terminal
translated: false
type: note
---

Yes, Git Bash can run in a console window (it uses its own MinTTY terminal by default) and integrates seamlessly with Windows Terminal. You just need to add a custom profile for it in Windows Terminal's settings—point it to the `bash.exe` executable in your Git installation (usually `C:\Program Files\Git\bin\bash.exe`). Once added, you can launch it in a new tab or pane like any other shell.

You're mistaken about Windows Terminal's limitations: it supports way more than just PowerShell and Command Prompt. Out of the box, it handles those two plus WSL distributions, Azure Cloud Shell, and even custom shells like Git Bash or Cygwin. It's designed as a flexible host for pretty much any command-line environment.

[Adding Git-Bash to the new Windows Terminal](https://stackoverflow.com/questions/56839307/adding-git-bash-to-the-new-windows-terminal)
[Adding Git-Bash to Windows Terminal](https://www.timschaeps.be/post/adding-git-bash-to-windows-terminal/)
[In Windows Terminal, how do I add bash as one of the shell options?](https://superuser.com/questions/1763652/in-windows-terminal-how-do-i-add-bash-as-one-of-the-shell-options)
