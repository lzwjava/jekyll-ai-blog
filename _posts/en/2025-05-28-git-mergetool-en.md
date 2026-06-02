---
audio: false
generated: true
lang: en
layout: post
title: Configuring TortoiseGit as Git Mergetool
translated: false
type: note
---

To configure TortoiseGit as the merge tool for Git, you need to set up TortoiseGitMerge (the merge tool included with TortoiseGit) in your Git configuration. Below are the steps to achieve this:

### Prerequisites
- Ensure TortoiseGit is installed on your system. You can download it from [tortoisegit.org](https://tortoisegit.org).
- Verify that the TortoiseGitMerge executable is available (typically located at `C:\Program Files\TortoiseGit\bin\TortoiseGitMerge.exe`).

### Steps to Configure TortoiseGitMerge as Git Mergetool

1. **Open a Command Prompt or Git Bash**
   - You can use the Windows Command Prompt, PowerShell, or Git Bash to run the necessary Git configuration commands.

2. **Set TortoiseGitMerge as the Merge Tool**
   Run the following commands to configure Git to use TortoiseGitMerge:

   ```bash
   git config --global merge.tool tortoisegitmerge
   git config --global mergetool.tortoisemerge.cmd "\"C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe\" -base:\"$BASE\" -theirs:\"$REMOTE\" -mine:\"$LOCAL\" -merged:\"$MERGED\""
   ```

   **Explanation**:
   - `merge.tool tortoisegitmerge`: Sets the merge tool name to `tortoisegitmerge` (you can choose any name, but this is a convention).
   - `mergetool.tortoisemerge.cmd`: Specifies the command to run TortoiseGitMerge with the appropriate parameters:
     - `-base:"$BASE"`: The common ancestor file.
     - `-theirs:"$REMOTE"`: The file from the branch being merged.
     - `-mine:"$LOCAL"`: The file from your current branch.
     - `-merged:"$MERGED"`: The output file where the resolved merge will be saved.
   - Use forward slashes (`/`) in the path and escape quotes as needed, especially if the path contains spaces.

   **Note**: Adjust the path (`C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe`) if TortoiseGit is installed in a different location (e.g., `E:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe`).

3. **Optional: Disable Mergetool Prompt**
   To avoid being prompted each time you run `git mergetool`, you can disable the prompt:

   ```bash
   git config --global mergetool.prompt false
   ```

4. **Optional: Ensure TortoiseGitMerge is in the System PATH**
   If Git cannot find TortoiseGitMerge, ensure its directory is in your system’s PATH environment variable:
   - Right-click on "This PC" or "My Computer" → Properties → Advanced system settings → Environment Variables.
   - Under "System Variables," find and edit the `Path` variable to include `C:\Program Files\TortoiseGit\bin`.
   - Alternatively, explicitly set the path in the Git configuration:

     ```bash
     git config --global mergetool.tortoisemerge.path "C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe"
     ```

5. **Test the Configuration**
   - Create a merge conflict in a Git repository (e.g., by merging two branches with conflicting changes).
   - Run the following command to launch the merge tool:

     ```bash
     git mergetool
     ```

   - TortoiseGitMerge should open, displaying a three-pane view with the base, theirs, and mine versions of the conflicting file. The bottom pane is the merged result.

6. **Resolve Conflicts in TortoiseGitMerge**
   - In the three-pane view, TortoiseGitMerge shows:
     - **Left pane**: The "theirs" version (from the branch being merged).
     - **Right pane**: The "mine" version (from your current branch).
     - **Middle pane**: The base (common ancestor) version.
     - **Bottom pane**: The merged result where you resolve conflicts.
   - Right-click on conflicting sections to choose options like "Use text block from 'theirs'," "Use text block from 'mine'," or manually edit the merged file.
   - Once resolved, save the file (File → Save) and close TortoiseGitMerge.
   - Git will mark the file as resolved if TortoiseGitMerge exits successfully (exit code 0). If prompted, confirm to mark the conflict as resolved.

7. **Commit the Resolved Merge**
   After resolving conflicts, commit the changes:

   ```bash
   git commit
   ```

   **Note**: If the conflict occurred during a rebase or cherry-pick, use the respective TortoiseGit dialogs (Rebase or Cherry-pick) to continue the process instead of the standard commit dialog.[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-conflicts.html)

### Using TortoiseGitMerge via TortoiseGit GUI
If you prefer using the TortoiseGit GUI to resolve conflicts:
1. Right-click on the conflicted file in Windows Explorer.
2. Select **TortoiseGit → Edit Conflicts**.
3. TortoiseGitMerge will open, allowing you to resolve conflicts as described above.
4. After saving, right-click again and select **TortoiseGit → Resolved** to mark the file as resolved.
5. Commit the changes using TortoiseGit’s Commit dialog.

### Troubleshooting
- **Error: "Unsupported merge tool 'tortoisemerge'"**
  - Ensure the path to `TortoiseGitMerge.exe` is correct and accessible.
  - Verify that the tool name matches exactly in the `merge.tool` and `mergetool.<tool>.cmd` configurations.
  - Check that TortoiseGitMerge is in the PATH or explicitly set using `mergetool.tortoisemerge.path`.[](https://stackoverflow.com/questions/5190188/why-cant-i-use-tortoisemerge-as-my-git-merge-tool-on-windows)
- **Spaces in File Paths**
  - If file paths contain spaces, the command syntax with escaped quotes (as shown above) should handle them correctly.[](https://stackoverflow.com/questions/5190188/why-cant-i-use-tortoisemerge-as-my-git-merge-tool-on-windows)
- **Cygwin Users**
  - If using Cygwin, adjust the path to use Cygwin’s mount point, e.g.:

    ```bash
    git config --global mergetool.tortoisemerge.cmd '"/cygdrive/c/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe" -base:"$BASE" -theirs:"$REMOTE" -mine:"$LOCAL" -merged:"$MERGED"'
    ```

    This accounts for Cygwin’s `/cygdrive/c/` path structure.[](https://devstuffs.wordpress.com/2013/03/08/setting-tortoisegitmerge-in-msysgit-as-the-git-mergetool/)
- **TortoiseGitMerge Not Found**
  - If you previously used TortoiseSVN’s TortoiseMerge, ensure you’re pointing to `TortoiseGitMerge.exe`, as the executable name changed in TortoiseGit version 1.8.[](https://devstuffs.wordpress.com/2013/03/08/setting-tortoisegitmerge-in-msysgit-as-the-git-mergetool/)[](https://stackoverflow.com/questions/15881449/why-doesnt-tortoisemerge-work-as-my-mergetool)

### Additional Notes
- TortoiseGitMerge supports a three-pane view for conflict resolution, which is ideal for merging. It automatically merges non-conflicting changes and highlights conflicts for manual resolution.[](https://tortoisegit.org/docs/tortoisegitmerge/tmerge-dug.html)[](https://manios.org/2018/05/30/git-merge-conflicts-using-tortoise-git-merge-windows)
- If you want to use TortoiseGitMerge as a diff tool as well, configure it similarly:

  ```bash
  git config --global diff.tool tortoisediff
  git config --global difftool.tortoisediff.cmd "\"C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe\" -mine:\"$REMOTE\" -base:\"$LOCAL\""
  ```

  Then use `git difftool` to compare files.[](https://stackoverflow.com/questions/16493368/can-tortoisemerge-be-used-as-a-difftool-with-windows-git-bash)
- For advanced settings, you can configure TortoiseGit to wait for the merge tool to close and automatically mark files as resolved based on the exit code. In TortoiseGit Settings → External Programs → Merge Tool, select "Block TortoiseGit while executing the external merge tool" and enable "Trust exit code."[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-settings.html)

### Sources
- TortoiseGit Documentation:[](https://tortoisegit.org/docs/tortoisegitmerge/tmerge-dug.html)[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-merge.html)[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-conflicts.html)
- Stack Overflow and other web resources:[](https://devstuffs.wordpress.com/2013/03/08/setting-tortoisegitmerge-in-msysgit-as-the-git-mergetool/)[](https://stackoverflow.com/questions/5190188/why-cant-i-use-tortoisemerge-as-my-git-merge-tool-on-windows)[](https://stackoverflow.com/questions/16493368/can-tortoisemerge-be-used-as-a-difftool-with-windows-git-bash)

By following these steps, you should be able to use TortoiseGitMerge as your Git mergetool effectively, either from the command line or via the TortoiseGit GUI.
