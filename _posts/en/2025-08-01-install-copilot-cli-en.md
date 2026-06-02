---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install GitHub Copilot CLI Extension
translated: false
type: note
---

The command `gh extension install github/gh-copilot` installs the GitHub Copilot extension for the GitHub CLI, enabling Copilot features like command-line suggestions and explanations. For enterprise users, whether this command applies depends on specific conditions:

- **Enterprise Configuration**: Enterprise users can use the Copilot CLI extension if their organization or enterprise has a GitHub Copilot Business or Copilot Enterprise subscription and the CLI feature is enabled by administrators. If the organization owner or enterprise administrator has disabled Copilot in the CLI, the extension cannot be used, even if installed.[](https://docs.github.com/fr/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)
- **Authentication**: Enterprise users must authenticate to the GitHub CLI with a GitHub account that has an assigned Copilot seat. For managed user accounts on GitHub Enterprise Cloud (GHE.com), additional setup may be required, such as updating settings before signing in.[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-extension)
- **Installation Requirements**: The GitHub CLI must be installed prior to running the command. The installation process itself is the same for enterprise and individual users, but enterprise policies may restrict usage.[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)

**Steps for Enterprise Users**:

1. Ensure GitHub CLI is installed (see [GitHub CLI repository](https://github.com/cli/cli) for instructions).
2. Verify with your enterprise administrator that Copilot CLI is enabled for your organization.
3. Run `gh extension install github/gh-copilot` in your terminal.
4. Authenticate using `gh auth login` with your enterprise-assigned GitHub account.
5. If using a managed user account on GHE.com, follow additional setup steps outlined in [Using GitHub Copilot with an account on GHE.com](https://docs.github.com/en/enterprise-cloud@latest/copilot/configuring-github-copilot-in-your-environment/using-github-copilot-with-an-account-on-ghecom).[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-extension)

If your enterprise restricts CLI access or hasn’t enabled Copilot, the extension may install but won’t function. Check with your admin for policy details.

[Installing GitHub Copilot in the CLI](https://docs.github.com/en/enterprise-cloud@latest/copilot/installing-github-copilot-in-the-cli)[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)
[Setting up GitHub Copilot for your enterprise](https://docs.github.com/en/enterprise-cloud@latest/copilot/setting-up-github-copilot-for-your-enterprise)[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/set-up-for-enterprise)
