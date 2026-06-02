---
audio: false
generated: true
lang: en
layout: post
title: VS Code Source Control Guide
translated: false
type: note
---

Visual Studio Code (VS Code) has robust built-in support for source control, allowing developers to manage version control systems (VCS) like Git, Mercurial, and others directly within the editor. This guide provides a comprehensive overview of using source control in VS Code, focusing on Git, as it’s the most commonly used VCS, and covers setup, key features, workflows, and advanced usage.

### Overview of Source Control in VS Code
VS Code’s Source Control view provides an intuitive interface to interact with version control systems. It integrates with Git by default and supports extensions for other VCS. The Source Control view displays changes, allows staging, committing, branching, merging, and more, all without leaving the editor. Below is a step-by-step guide to leveraging source control effectively.

### 1. **Setting Up Source Control in VS Code**
To use source control, you need Git installed and a repository initialized. Here’s how to set it up:

#### Prerequisites
- **Install Git**: Download and install Git from [git-scm.com](https://git-scm.com/). Verify installation by running `git --version` in a terminal.
- **Configure Git**:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```
- **Install VS Code**: Ensure you have the latest version of VS Code installed from [code.visualstudio.com](https://code.visualstudio.com/).

#### Initialize a Git Repository
1. Open a project folder in VS Code.
2. Open the Terminal (Ctrl+` or Cmd+` on macOS) and run:
   ```bash
   git init
   ```
   This creates a `.git` folder in your project, initializing it as a Git repository.
3. Alternatively, clone an existing repository:
   ```bash
   git clone <repository-url>
   ```
   Then open the cloned folder in VS Code.

#### Enable Source Control View
- Open the Source Control view by clicking the Source Control icon in the Activity Bar (third icon from the top, resembling a branch) or pressing `Ctrl+Shift+G` (Windows/Linux) or `Cmd+Shift+G` (macOS).
- If a Git repository is detected, VS Code displays the Source Control view with options to manage changes.

### 2. **Using the Source Control View**
The Source Control view is the central hub for version control tasks. It shows:
- **Changes**: Files modified, added, or deleted since the last commit.
- **Staged Changes**: Files ready to be committed.
- **Commit Message Box**: Where you enter commit messages.
- **Actions**: Buttons for committing, refreshing, and more.

#### Common Workflow
1. **Make Changes**: Edit files in your project. VS Code automatically detects changes and lists them under “Changes” in the Source Control view.
2. **Stage Changes**:
   - Click the `+` icon next to a file to stage it, or use the `Stage All Changes` option (three dots menu > Stage All Changes).
   - Staging prepares changes for the next commit.
3. **Write a Commit Message**:
   - Enter a descriptive message in the text box at the top of the Source Control view.
   - Example: `Add user authentication feature`.
4. **Commit Changes**:
   - Click the checkmark icon or press `Ctrl+Enter` (Windows/Linux) or `Cmd+Enter` (macOS) to commit staged changes.
   - Use the three dots menu to choose between `Commit All`, `Commit Staged`, or `Commit All and Push`.
5. **Push to Remote**:
   - If connected to a remote repository (e.g., GitHub), push changes using the `Push` option in the three dots menu or run `git push` in the terminal.

### 3. **Key Features of Source Control in VS Code**
VS Code provides several features to streamline version control:

#### Diff View
- Click a file under “Changes” to open a side-by-side diff view, showing modifications compared to the last commit.
- Use inline actions to stage or discard specific lines.

#### Branch Management
- Switch branches: Click the branch name at the bottom-left status bar or use the Source Control view’s branch menu (three dots > Branch > Checkout to...).
- Create a new branch: Select `Create Branch` from the branch menu, enter a name, and confirm.
- Merge branches: Use `Branch > Merge Branch` and select the branch to merge into the current one.

#### Pull and Fetch
- **Pull**: Sync changes from the remote repository using the `Pull` option in the three dots menu.
- **Fetch**: Retrieve remote changes without merging using `Fetch`.

#### Resolve Conflicts
- When merging or pulling, conflicts may arise. VS Code highlights conflicts in files and provides an inline conflict resolution interface:
  - Choose `Accept Current Change`, `Accept Incoming Change`, `Accept Both Changes`, or manually edit the file.
  - Stage and commit the resolved file.

#### Git Lens Extension
For advanced Git features, install the **GitLens** extension:
- View commit history, blame annotations, and file changes.
- Access repository insights like recent commits and stashes.
- Install via the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`).

### 4. **Advanced Usage**
#### Stashing Changes
- Save uncommitted changes temporarily:
  - Go to the three dots menu > Stash > Stash.
  - Apply or pop stashes later via the same menu.
- Useful for switching branches without committing incomplete work.

#### Git Commands in Terminal
- For tasks not directly supported in the UI, use the integrated terminal:
  ```bash
  git rebase <branch>
  git cherry-pick <commit>
  git log --oneline
  ```

#### Customizing Source Control
- **Settings**: Adjust source control behavior in VS Code settings (`Ctrl+,` or `Cmd+,`):
  - `git.autoRepositoryDetection`: Enable/disable automatic Git repository detection.
  - `git.enableSmartCommit`: Commit all changes when no files are staged.
- **SCM Providers**: Install extensions for other VCS like Mercurial or SVN.

#### GitHub Integration
- Use the **GitHub Pull Requests and Issues** extension to manage PRs and issues directly in VS Code.
- Authenticate with GitHub via the Accounts menu (bottom-left corner) to push/pull from GitHub repositories.

### 5. **Sample Workflow: Creating and Pushing a Feature Branch**
Here’s a practical example of a common Git workflow in VS Code:


# Sample Git Workflow in VS Code

## Steps to Create and Push a Feature Branch

1. **Create a New Branch**:
   - In the Source Control view, click the branch name in the status bar or use the three dots menu > Branch > Create Branch.
   - Name the branch, e.g., `feature/add-login`.
   - VS Code switches to the new branch.

2. **Make and Stage Changes**:
   - Edit files (e.g., add a login component to `src/Login.js`).
   - In the Source Control view, files appear under “Changes.”
   - Click the `+` icon to stage changes or select “Stage All Changes.”

3. **Commit Changes**:
   - Enter a commit message, e.g., `Add login component`.
   - Click the checkmark or press `Ctrl+Enter` (Windows/Linux) or `Cmd+Enter` (macOS) to commit.

4. **Push the Branch**:
   - If no remote exists, add one:
     ```bash
     git remote add origin <repository-url>
     ```
   - Push the branch: Three dots menu > Push, or run:
     ```bash
     git push -u origin feature/add-login
     ```

5. **Create a Pull Request**:
   - If using GitHub, open the repository in a browser or use the GitHub Pull Requests extension to create a PR.
   - Link the PR to the `feature/add-login` branch.

## Tips
- Regularly pull updates from the main branch to avoid conflicts.
- Use descriptive commit messages for better collaboration.
- Install GitLens for enhanced commit history and blame views.


### 6. **Troubleshooting Common Issues**
- **Git Not Detected**: Ensure Git is installed and added to your system PATH. Restart VS Code after installation.
- **Authentication Errors**: Configure SSH keys or use a personal access token for GitHub/GitLab. Authenticate via the Accounts menu.
- **Merge Conflicts**: Use the inline conflict resolution tools or manually edit files, then stage and commit.
- **Slow Performance**: Disable `git.autoRepositoryDetection` for large projects or use GitLens for optimized Git operations.

### 7. **Best Practices**
- **Commit Often**: Make small, logical commits to track progress.
- **Use Descriptive Messages**: Follow a convention like `<type>(<scope>): <description>` (e.g., `feat(auth): add login endpoint`).
- **Pull Regularly**: Stay in sync with the remote repository to minimize conflicts.
- **Backup Stashes**: Before applying stashes, ensure they won’t overwrite important changes.
- **Leverage Extensions**: Use GitLens, Git History, or Git Graph for enhanced functionality.

### 8. **Additional Resources**
- **VS Code Documentation**: [Version Control in VS Code](https://code.visualstudio.com/docs/editor/versioncontrol)
- **Git Documentation**: [git-scm.com/doc](https://git-scm.com/doc)
- **GitLens Extension**: Available in the VS Code Marketplace.
- **GitHub Pull Requests Extension**: For managing PRs and issues.

This guide covers the essentials and advanced features of source control in VS Code, with a focus on Git. By following these steps and best practices, you can efficiently manage version control workflows directly within the editor.
