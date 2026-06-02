---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Creating Ubuntu User Accounts
translated: false
type: note
---

### Creating a New User in Ubuntu Linux

Ubuntu provides both command-line and graphical methods to create a user. The command-line approach is straightforward and works on all editions (including servers), while the GUI is available on desktop versions.

#### Command-Line Method (Recommended)
1. Open a terminal (Ctrl+Alt+T).
2. Run the following command, replacing `username` with your desired username:
   ```
   sudo adduser username
   ```
   - This will prompt you to set a strong password for the new user.
   - You'll also be asked for optional details like full name, room number, work phone, etc. Press Enter to skip these or provide info as needed.
3. (Optional) To grant the new user administrative (sudo) privileges:
   ```
   sudo usermod -aG sudo username
   ```
   - This adds the user to the `sudo` group, allowing them to run commands with elevated permissions.

The new user will have a home directory at `/home/username` and can log in immediately.

#### Graphical Method (Desktop Only)
1. Open the **Settings** app (search for it in the Activities overview).
2. Navigate to **Users** in the sidebar.
3. Click **Unlock** in the top-right corner and enter your admin password.
4. Click **Add User**.
5. Fill in the account type (Standard or Administrator), full name, username, and password.
6. Click **Add**.

#### Verification
- Switch to the new user with `su - username` or log out and log in.
- Check users with `cat /etc/passwd | grep username`.

This process works on Ubuntu 24.04 LTS and later versions.

[User management - Ubuntu Server documentation](https://documentation.ubuntu.com/server/how-to/security/user-management/)
[Add a new user account - Ubuntu Documentation](https://help.ubuntu.com/stable/ubuntu-help/user-add.html.en)
