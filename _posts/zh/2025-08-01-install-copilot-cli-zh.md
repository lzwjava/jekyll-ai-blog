---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装GitHub Copilot CLI扩展
translated: true
type: note
---

命令 `gh extension install github/gh-copilot` 用于安装 GitHub CLI 的 GitHub Copilot 扩展，从而启用命令行建议和解释等 Copilot 功能。对于企业用户，该命令是否适用取决于特定条件：

- **企业配置**：如果企业或组织的管理员已启用 CLI 功能，且该组织或企业拥有 GitHub Copilot Business 或 Copilot Enterprise 订阅，则企业用户可使用 Copilot CLI 扩展。若组织所有者或企业管理员在 CLI 中禁用了 Copilot，即使已安装扩展也无法使用。[](https://docs.github.com/fr/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)
- **身份验证**：企业用户必须使用已分配 Copilot 席位的 GitHub 账户向 GitHub CLI 进行身份验证。对于 GitHub Enterprise Cloud (GHE.com) 上的托管用户账户，可能需要进行额外设置，例如在登录前更新设置。[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-extension)
- **安装要求**：运行该命令前必须已安装 GitHub CLI。安装过程对企业用户和个人用户相同，但企业策略可能会限制使用。[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)

**企业用户操作步骤**：

1. 确保已安装 GitHub CLI（参阅 [GitHub CLI 仓库](https://github.com/cli/cli)获取指南）。
2. 向企业管理员确认已为组织启用 Copilot CLI。
3. 在终端中运行 `gh extension install github/gh-copilot`。
4. 使用企业分配的 GitHub 账户通过 `gh auth login` 完成身份验证。
5. 若使用 GHE.com 的托管用户账户，请按照[在 GHE.com 账户上使用 GitHub Copilot](https://docs.github.com/en/enterprise-cloud@latest/copilot/configuring-github-copilot-in-your-environment/using-github-copilot-with-an-account-on-ghecom) 中所述的额外设置步骤操作。[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-extension)

若企业限制 CLI 访问或未启用 Copilot，扩展可能安装但无法运行。请向管理员核实策略详情。

[在 CLI 中安装 GitHub Copilot](https://docs.github.com/en/enterprise-cloud@latest/copilot/installing-github-copilot-in-the-cli)[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/install-copilot-in-the-cli)
[为企业设置 GitHub Copilot](https://docs.github.com/en/enterprise-cloud@latest/copilot/setting-up-github-copilot-for-your-enterprise)[](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/set-up/set-up-for-enterprise)
