---
audio: false
generated: true
lang: en
layout: post
title: TortoiseGit
translated: false
type: note
---

TortoiseGit is a Windows shell extension that provides a user-friendly interface for Git, the popular version control system. It integrates directly into Windows Explorer, allowing you to perform Git operations via context menus. This guide covers installing, configuring, and using TortoiseGit on Windows, along with common tasks and best practices.

### Overview of TortoiseGit
TortoiseGit is built on top of msysGit (Git for Windows) and provides a graphical interface for Git commands. It’s ideal for users who prefer a GUI over command-line Git operations. Key features include:
- Context menu integration in Windows Explorer.
- Visual diff and merge tools.
- Support for common Git workflows (commit, push, pull, branch, merge, etc.).
- Integration with popular issue trackers and external tools.

### Prerequisites
Before installing TortoiseGit, ensure you have:
- A Windows operating system (Windows 10 or later recommended).
- Git for Windows installed (TortoiseGit relies on it).
- Basic understanding of Git concepts (repositories, commits, branches, etc.).

### Installation
1. **Install Git for Windows**:
   - Download the latest version from [Git for Windows](https://gitforwindows.org/) or [Git SCM](https://git-scm.com/downloads).
   - Run the installer and follow the prompts. Recommended settings:
     - Use the default editor (e.g., Notepad) or choose one like VS Code.
     - Select “Use Git from the Windows Command Prompt” for accessibility.
     - Choose “OpenSSL” for HTTPS transport.
     - Select “Checkout as-is, commit as-is” for line endings (unless working with cross-platform teams).
   - Complete the installation.

2. **Install TortoiseGit**:
   - Download the latest version from [TortoiseGit’s official website](https://tortoisegit.org/download/).
   - Run the installer:
     - Choose the default language and components.
     - Ensure Git for Windows is detected (TortoiseGit will prompt if it’s missing).
     - Install TortoiseGitPlink (recommended for SSH) if needed.
   - Restart your computer if prompted.

3. **Verify Installation**:
   - Right-click in any folder in Windows Explorer. You should see TortoiseGit options like “Git Clone,” “Git Create Repository here,” etc.

### Initial Configuration
After installation, configure TortoiseGit for your user details and preferences:
1. **Set User Information**:
   - Right-click in a folder, select **TortoiseGit > Settings**.
   - In the settings window, navigate to **Git > Config**.
   - Enter your name and email (same as used in GitHub, GitLab, etc.):
     ```
     Name: Your Name
     Email: your.email@example.com
     ```
   - Click **Apply** and **OK**.

2. **Configure SSH (Optional)**:
   - If using SSH for remote repositories, set up an SSH key:
     - Open **PuTTYgen** (installed with TortoiseGit).
     - Generate a new SSH key pair, save the private key, and copy the public key.
     - Add the public key to your Git hosting service (e.g., GitHub, GitLab).
     - In TortoiseGit settings, under **Git > Remote**, select TortoiseGitPlink as the SSH client.

3. **Set Diff and Merge Tools**:
   - In **TortoiseGit > Settings > Diff Viewer**, choose a tool like TortoiseGitMerge (default) or an external tool like Beyond Compare.
   - For merging, configure under **Merge Tool** (TortoiseGitMerge is recommended for beginners).

### Basic Usage
Below are common TortoiseGit operations, accessible via right-click context menus in Windows Explorer.

#### 1. **Cloning a Repository**
   - Right-click in a folder and select **Git Clone**.
   - In the dialog:
     - Enter the repository URL (e.g., `https://github.com/username/repo.git`).
     - Specify the local directory for the repository.
     - Optionally, select a branch or load SSH keys.
   - Click **OK** to clone the repository.

#### 2. **Creating a New Repository**
   - Navigate to a folder, right-click, and select **Git Create Repository here**.
   - Check “Make it Bare” if creating a server-side repository (rare for local use).
   - Click **OK**. A `.git` folder is created, initializing the repository.

#### 3. **Committing Changes**
   - Add files to your repository folder.
   - Right-click the folder or selected files, then choose **Git Commit -> "main"** (or current branch).
   - In the commit dialog:
     - Enter a commit message describing changes.
     - Select files to stage (check boxes).
     - Click **OK** or **Commit & Push** to push changes to the remote repository.

#### 4. **Pushing Changes**
   - After committing, right-click and select **TortoiseGit > Push**.
   - Choose the remote repository and branch.
   - Authenticate if prompted (username/password for HTTPS or SSH key).
   - Click **OK** to push.

#### 5. **Pulling Changes**
   - To update your local repository with remote changes, right-click and select **TortoiseGit > Pull**.
   - Select the remote branch and click **OK**.
   - Resolve conflicts if prompted (use the merge tool).

#### 6. **Creating and Switching Branches**
   - Right-click and select **TortoiseGit > Create Branch**.
   - Enter a branch name and click **OK**.
   - To switch branches, right-click and select **TortoiseGit > Switch/Checkout**, then choose the branch.

#### 7. **Viewing History**
   - Right-click and select **TortoiseGit > Show Log**.
   - View commit history, including author, date, and messages.
   - Right-click a commit to view changes, revert, or cherry-pick.

#### 8. **Resolving Merge Conflicts**
   - During a pull or merge, if conflicts occur, TortoiseGit will notify you.
   - Right-click conflicting files and select **TortoiseGit > Resolve**.
   - Use the merge tool to edit conflicts manually, then mark as resolved.
   - Commit the resolved changes.

### Advanced Features
1. **Stashing Changes**:
   - To save uncommitted changes temporarily, right-click and select **TortoiseGit > Stash Save**.
   - To retrieve stashed changes, select **TortoiseGit > Stash Pop**.

2. **Rebasing**:
   - Right-click and select **TortoiseGit > Rebase**.
   - Choose the branch to rebase onto and follow the prompts to reorder or squash commits.

3. **Submodules**:
   - To manage submodules, right-click and select **TortoiseGit > Submodule Update** or **Add**.
   - Configure submodule settings in the TortoiseGit settings.

4. **Bisecting**:
   - To find a bug-introducing commit, use **TortoiseGit > Bisect Start**.
   - Mark commits as “good” or “bad” to narrow down the problematic commit.

### Best Practices
- **Commit Often**: Make small, frequent commits with clear messages.
- **Pull Regularly**: Keep your local repository updated to avoid conflicts.
- **Use Branches**: Create feature branches for new work to keep the main branch stable.
- **Backup SSH Keys**: Store SSH keys securely and back them up.
- **Review Changes**: Use the diff viewer to review changes before committing.

### Troubleshooting
- **Authentication Issues**: Ensure SSH keys or credentials are correctly configured in your Git hosting service.
- **Merge Conflicts**: Use TortoiseGitMerge to resolve conflicts visually. Back up files before merging.
- **Missing Context Menu**: Check if TortoiseGit is installed correctly and Explorer integration is enabled in settings.
- **Slow Performance**: Disable unnecessary overlays in **TortoiseGit > Settings > Icon Overlays**.

### Example Workflow
Below is a sample workflow for contributing to a project:

# Sample TortoiseGit Workflow

## 1. Clone the Repository
- Right-click in a folder, select **Git Clone**.
- Enter the repository URL and local directory.
- Click **OK**.

## 2. Create a Feature Branch
- Right-click, select **TortoiseGit > Create Branch**.
- Name the branch (e.g., `feature/add-login`).
- Click **OK** and switch to the new branch.

## 3. Make Changes
- Edit files in the repository folder.
- Right-click, select **Git Commit -> "feature/add-login"**.
- Write a commit message and stage files.
- Click **Commit**.

## 4. Push Changes
- Right-click, select **TortoiseGit > Push**.
- Choose the remote branch (e.g., `origin/feature/add-login`).
- Click **OK**.

## 5. Create a Pull Request
- On your Git hosting service (e.g., GitHub), create a pull request from your branch to the main branch.
- Await review and merge.

## 6. Update Local Repository
- Switch to the main branch (**TortoiseGit > Switch/Checkout**).
- Pull updates (**TortoiseGit > Pull**).


### Resources
- **Official Documentation**: [TortoiseGit Documentation](https://tortoisegit.org/docs/)
- **Git for Windows**: [Git SCM](https://git-scm.com/)
- **Tutorials**: Search for “TortoiseGit tutorial” on YouTube or tech blogs for visual guides.

TortoiseGit simplifies Git operations with its intuitive interface, making version control accessible for Windows users. If you need help with specific tasks or advanced configurations, let me know!
