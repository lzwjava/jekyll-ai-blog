---
audio: false
generated: true
lang: en
layout: post
title: GNOME Terminal Custom Directory Title
translated: false
type: note
---

To customize the GNOME Terminal tab title to show only the current directory (e.g., `blog-server`) instead of the default format (e.g., `lzw@lzw-MS:~/Projects/blog-server`), you can modify the terminal's prompt or title settings. Here’s how to achieve this:

### Steps to Set GNOME Terminal Tab Title to Show Only the Current Directory

1. **Edit the Bash Configuration File**:
   GNOME Terminal uses the Bash shell by default, and the tab title is often derived from the `PS1` (prompt) or a specific title-setting command. To customize the title, you can modify the `~/.bashrc` file.

2. **Modify the Terminal Title**:
   Add a command to set the terminal title to the current directory in your `~/.bashrc`. Open the file in a text editor:

   ```bash
   nano ~/.bashrc
   ```

   Add the following lines at the end of the file:

   ```bash
   # Set terminal tab title to current directory
   case "$TERM" in
   xterm*|rxvt*)
       PS1="\[\e]0;\W\a\]$PS1"
       ;;
   *)
       ;;
   esac
   ```

   **Explanation**:
   - `\e]0;...` sets the terminal title.
   - `\W` represents the basename of the current directory (e.g., `blog-server` instead of the full path `~/Projects/blog-server`).
   - `\a` is a bell character to terminate the title string.
   - This code checks if the terminal is `xterm`-compatible (which GNOME Terminal is) before applying the change.

3. **Apply the Changes**:
   Save the file and reload the Bash configuration:

   ```bash
   source ~/.bashrc
   ```

   Alternatively, close and reopen the terminal to apply the changes.

4. **Verify the Result**:
   Navigate to a directory (e.g., `cd ~/Projects/blog-server`), and the terminal tab title should now display only `blog-server`.

### Alternative: Modify GNOME Terminal Profile Settings

If you want to customize the title further or avoid editing `~/.bashrc`, you can use GNOME Terminal’s profile settings:

1. Open GNOME Terminal.
2. Go to **Edit** > **Preferences** (or **Terminal** > **Preferences**, depending on your version).
3. Select the profile you’re using (e.g., “Unnamed” or a custom profile).
4. Go to the **Command** tab.
5. Under **Title and Command**, set:
   - **Initial title**: Leave blank or set to something generic.
   - **When command exits**: Choose **Keep initial title** or **Replace with command output**.
6. In the **Command** section, enable **Run a custom command instead of my shell** and set the command to:

   ```bash
   bash --rcfile <(echo '. ~/.bashrc; PS1="\[\e]0;\W\a\]$PS1"')
   ```

   This ensures the terminal uses a custom prompt that sets the title to the current directory.

7. Close the dialog and test by opening a new tab or navigating to a directory.

### Notes

- If you use a shell other than Bash (e.g., Zsh), you’ll need to modify the equivalent configuration file (e.g., `~/.zshrc`) and adjust the syntax accordingly. For Zsh, you can add:

  ```zsh
  precmd() { echo -ne "\e]0;${PWD##*/}\a" }
  ```

- If the title doesn’t update as expected, ensure your terminal emulator is `xterm`-compatible and that no other scripts (e.g., custom `PS1` settings in `~/.bashrc`) are overriding the title.
- For persistent changes across all terminals, ensure the configuration is in the user’s shell profile or GNOME Terminal settings.

This should give you a tab title showing only the current directory name, like `blog-server`. Let me know if you need further clarification!
