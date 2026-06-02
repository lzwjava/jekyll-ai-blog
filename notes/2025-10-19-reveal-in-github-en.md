---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Reveal In GitHub Xcode Plugin
translated: false
type: note
---

### What is Reveal-In-GitHub?

Reveal-In-GitHub is an Xcode plugin that lets you quickly navigate from your Xcode workspace to key GitHub features for your current repository. It's designed for developers working on GitHub-hosted Git projects, allowing one-click (or keyboard shortcut) access to things like commit history, blame views, pull requests, issues, and notifications—without leaving Xcode or manually typing URLs.

### Prerequisites

- Xcode installed (tested on recent versions; no specific minimum mentioned).
- Your project must be a Git repository hosted on GitHub (the plugin detects the repo URL and file paths automatically).
- If your project has multiple Git remotes, you'll be prompted to select a default on first use.

### Installation

There are two main ways to install it:

#### Option 1: Using Alcatraz (Recommended)

1. Install Alcatraz if you haven't already (a package manager for Xcode plugins). You can find setup guides online, such as [this one](http://blog.devtang.com/blog/2014/03/05/use-alcatraz-to-manage-xcode-plugins/) if you prefer Chinese instructions.
2. Open Alcatraz in Xcode (via the menu: `Window > Package Manager`).
3. Search for "Reveal In GitHub".
4. Click **Install**.
5. Restart Xcode.

#### Option 2: Manual Installation

1. Clone the repository:

   ```
   git clone https://github.com/lzwjava/Reveal-In-GitHub.git
   ```

2. Open the `Reveal-In-GitHub.xcodeproj` file in Xcode.
3. Build the project (Product > Build or ⌘B). This generates the `Reveal-In-GitHub.xcplugin` file.
4. Move the plugin to:
   `~/Library/Application Support/Developer/Shared/Xcode/Plug-ins/`
5. Restart Xcode.

After installation, the plugin should appear in Xcode's menu bar under **Editor > Reveal In GitHub**.

### How to Use It

Once installed and Xcode restarted:

1. Open a GitHub-hosted project in Xcode and edit a source file (e.g., navigate to a specific line).
2. Use one of the keyboard shortcuts or menu items under **Editor > Reveal In GitHub** to jump to GitHub. The plugin auto-detects your repo, current file, line number, and latest commit hash.

Here's a quick reference for the built-in menu items and shortcuts (shortcuts follow the pattern ⌃⇧⌘ + first letter of the title):

| Menu Item      | Shortcut    | What It Does | Example GitHub URL (for file LZAlbumManager.m at line 40 in repo lzwjava/LZAlbum at commit fd7224) |
|----------------|-------------|--------------|-----------------------------------------------------------------------------------------------|
| **Setting**    | ⌃⇧⌘S      | Opens customization panel | N/A |
| **Repo**       | ⌃⇧⌘R      | Opens main repo page | <https://github.com/lzwjava/LZAlbum> |
| **Issues**     | ⌃⇧⌘I      | Opens issues list | <https://github.com/lzwjava/LZAlbum/issues> |
| **PRs**        | ⌃⇧⌘P      | Opens pull requests list | <https://github.com/lzwjava/LZAlbum/pulls> |
| **Quick File** | ⌃⇧⌘Q      | Opens file view at current line | <https://github.com/lzwjava/LZAlbum/blob/fd7224/LZAlbum/manager/LZAlbumManager.m#L40> |
| **List History**| ⌃⇧⌘L     | Opens commit history for the file | <https://github.com/lzwjava/LZAlbum/commits/fd7224/LZAlbum/manager/LZAlbumManager.m> |
| **Blame**      | ⌃⇧⌘B      | Opens blame view for current line | <https://github.com/lzwjava/LZAlbum/blame/fd7224/LZAlbum/manager/LZAlbumManager.m#L40> |
| **Notifications**| ⌃⇧⌘N   | Opens repo notifications | <https://github.com/lzwjava/LZAlbum/notifications?all=1> |

- **Tips**:
  - Shortcuts don't conflict with Xcode's defaults.
  - If you're on a selected text range, some actions (like Blame) will anchor to that range (e.g., #L40-L43).
  - Test it: Open a project, go to a line, and hit ⌃⇧⌘B—it should open the blame page in your browser.

### Customization

To tweak or add menu items:

1. Hit ⌃⇧⌘S or go to **Editor > Reveal In GitHub > Setting**.
2. In the panel:
   - Add new items by clicking the "+" button: Enter a title (e.g., "Wiki"), shortcut, and URL pattern.
   - URL patterns use placeholders like:
     - `{git_remote_url}`: Full repo URL (e.g., <https://github.com/user/repo>).
     - `{commit}`: Latest commit hash of current branch.
     - `{file_path}`: Relative path to the file.
     - `#{selection}`: Current line or selection (e.g., #L40).
   - Example: For a wiki link, set pattern to `{git_remote_url}/wiki`.
3. If you have multiple remotes, use the "Clear Default Repos" button to reset selections.

The plugin is inspired by [ShowInGitHub](https://github.com/larsxschneider/ShowInGitHub) and licensed under MIT.

[Reveal-In-GitHub GitHub Repository](https://github.com/lzwjava/Reveal-In-GitHub)
