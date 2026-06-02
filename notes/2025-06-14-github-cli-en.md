---
audio: false
generated: true
lang: en
layout: post
title: Install GitHub CLI
translated: false
type: note
---

To install the GitHub CLI (`gh`) on Ubuntu and use it to trigger GitHub Actions workflows with the `gh workflow run` command, follow these steps:

### Installation Steps for GitHub CLI (`gh`) on Ubuntu

1. **Add the GitHub CLI repository and GPG key**:
   Run the following commands in your terminal to set up the official GitHub CLI package repository:

   ```bash
   (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
   && sudo mkdir -p -m 755 /etc/apt/keyrings \
   && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
   && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
   && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   ```

   This script:
   - Installs `wget` if not already present.
   - Creates a directory for APT keyrings.
   - Downloads and adds the GitHub CLI GPG key.
   - Configures the GitHub CLI repository for your system.

2. **Update the package index and install `gh`**:
   Update your package list and install the `gh` command-line tool:

   ```bash
   sudo apt update
   sudo apt install gh -y
   ```

3. **Verify the installation**:
   Check that `gh` is installed correctly by running:

   ```bash
   gh --version
   ```

   You should see output like `gh version X.Y.Z (YYYY-MM-DD)`, confirming the installation.

4. **Authenticate with GitHub**:
   Before using `gh`, authenticate with your GitHub account:

   ```bash
   gh auth login
   ```

   Follow the prompts:
   - Choose `GitHub.com` (or your enterprise server if applicable).
   - Select your preferred protocol (`HTTPS` or `SSH`; `SSH` is recommended if you have an SSH key set up).
   - Choose the authentication method (browser is easiest; it opens a webpage to log in).
   - Copy the one-time code provided, paste it into the browser, and authorize `gh`.
   - Confirm the default settings or adjust as needed.

   After successful authentication, you’ll see a confirmation message.

### Using `gh workflow run` for GitHub Actions

The `gh workflow run` command triggers a GitHub Actions workflow. Here’s how to use it:

1. **Navigate to your repository** (optional):
   If you’re in a local Git repository linked to GitHub, `gh` will automatically detect it. Otherwise, specify the repository with the `--repo` flag.

2. **List available workflows** (optional):
   To find the workflow ID or filename, run:

   ```bash
   gh workflow list
   ```

   This displays all workflows in the repository, showing their names, IDs, and statuses (e.g., `active`).

3. **Run a workflow**:
   Use the `gh workflow run` command with the workflow’s filename or ID. For example:

   ```bash
   gh workflow run workflow.yml
   ```

   Or, using the workflow ID (e.g., `123456`):

   ```bash
   gh workflow run 123456
   ```

   If the workflow accepts inputs, provide them with the `--field` flag:

   ```bash
   gh workflow run workflow.yml --field key=value
   ```

   To specify a branch or ref, use the `--ref` flag:

   ```bash
   gh workflow run workflow.yml --ref branch-name
   ```

4. **Monitor the workflow**:
   After triggering, check the status of the run:

   ```bash
   gh run list
   ```

   To watch a specific run in real-time, use:

   ```bash
   gh run watch <run-id>
   ```

   Replace `<run-id>` with the run ID from `gh run list`.

### Troubleshooting Tips

- **GPG signature errors**: If you encounter GPG-related issues during `apt update`, refer to GitHub’s issue tracker for fixes (e.g., `cli/cli#9569`) or retry the key import step.[](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- **Firewall issues**: If `keyserver.ubuntu.com` fails, try:

   ```bash
   sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C99B11DEB97541F0
   ```

   Or install `dirmngr` if needed:

   ```bash
   sudo apt-get install dirmngr
   ```

  [](https://gist.github.com/Manoj-Paramsetti/dc957bdd6a4430275d0fc28a0dc43ae9)
- **Snap installation warning**: GitHub discourages using the Snap package for `gh` due to runtime issues. Stick to the APT method above.[](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- **Authentication scopes**: If `gh workflow run` fails due to permissions, ensure your token has the `workflow` scope. Re-authenticate with:

   ```bash
   gh auth refresh -s workflow
   ```

### Additional Notes

- **GitHub CLI manual**: For more details on `gh` commands, run `gh help` or visit the official manual at [cli.github.com](https://cli.github.com).[](https://cli.github.com/manual/)
- **Workflow requirements**: Ensure the workflow file (e.g., `workflow.yml`) exists in the `.github/workflows/` directory of your repository and is configured for manual triggers (e.g., `workflow_dispatch` event).
- **Alternative installation methods**: You can also install `gh` via Homebrew (`brew install gh`) or by downloading binaries from the [releases page](https://github.com/cli/cli/releases), but the APT method is recommended for Ubuntu.[](https://github.com/cli/cli)

This setup allows you to efficiently manage GitHub Actions workflows from the command line on Ubuntu. Let me know if you need help with specific `gh` commands or workflow configurations!
