---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Azure CLI Quick Start Guide
translated: false
type: note
---

Azure CLI (Command-Line Interface) is a cross-platform toolset for managing Azure resources from the command line. It's ideal for automating tasks, scripting deployments, and interacting with Azure services without needing the web portal. It supports Bash, PowerShell, and Command Prompt on Windows, macOS, and Linux.

## Installation

1. **Prerequisites**: Ensure you have Python 3.8 or later installed (check with `python --version`).

2. **Install via Package Manager** (Recommended):
   - **Windows**: Use Winget (`winget install Microsoft.AzureCLI`) or Chocolatey (`choco install azure-cli`).
   - **macOS**: Use Homebrew (`brew install azure-cli`).
   - **Linux (Ubuntu/Debian)**: Run `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`.
   - **Other Linux**: Use RPM or manual download from the official site.

3. **Verify Installation**: Open a terminal and run `az --version`. You should see the CLI version (e.g., 2.64.0 as of late 2025).

For detailed platform-specific steps, refer to the official installation docs.

## Authentication

Before using Azure CLI, sign in to your Azure account:

1. **Interactive Login**: Run `az login`. This opens a browser for Microsoft Entra ID authentication. Follow the prompts to sign in.

2. **Service Principal (for automation)**: Create a service principal with `az ad sp create-for-rbac --name "MyApp" --role contributor --scopes /subscriptions/{subscription-id}`. Then use `az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>`.

3. **Check Login**: Use `az account show` to verify your active subscription.

4. **Logout**: `az logout`.

Multi-factor authentication (MFA) is supported, and you can manage multiple subscriptions with `az account set --subscription <id>`.

## Basic Commands

Azure CLI uses the `az` command followed by a group (e.g., `vm`, `storage`) and subcommands. Use `az --help` for overview, or `az <group> --help` for specifics.

### Common Global Options
- `--help` or `-h`: Show help.
- `--output table/json/yaml`: Format output (default: table).
- `--query`: JMESPath query for filtering JSON output (e.g., `--query "[].name"`).

### Key Examples
- **List Subscriptions**: `az account list --output table`
- **Get Resource Groups**: `az group list --output table`
- **Create a Resource Group**: `az group create --name "MyResourceGroup" --location "eastus"`

## Managing Virtual Machines (VMs)
Azure CLI excels at VM lifecycle management.

1. **Create a VM**:
   ```
   az vm create \
     --resource-group "MyResourceGroup" \
     --name "MyVM" \
     --image Ubuntu2204 \
     --admin-username azureuser \
     --admin-password MyP@ssw0rd123! \
     --location "eastus"
   ```

2. **List VMs**: `az vm list --output table`

3. **Start/Stop VM**: `az vm start --name "MyVM" --resource-group "MyResourceGroup"` or `az vm stop --name "MyVM" --resource-group "MyResourceGroup"`

4. **SSH into VM**: `az vm ssh "MyVM" --resource-group "MyResourceGroup"`

5. **Delete VM**: `az vm delete --name "MyVM" --resource-group "MyResourceGroup" --yes`

## Managing Storage Accounts
1. **Create Storage Account**:
   ```
   az storage account create \
     --name mystorageaccount \
     --resource-group "MyResourceGroup" \
     --location "eastus" \
     --sku Standard_LRS
   ```

2. **Upload Blob**: First, get key with `az storage account keys list --account-name mystorageaccount --resource-group "MyResourceGroup" --query "[0].value -o tsv"`. Then: `az storage blob upload --account-name mystorageaccount --container-name mycontainer --name myfile.txt --file ./myfile.txt --auth-mode key`

## Other Common Scenarios
- **Deploy ARM Templates**: `az deployment group create --resource-group "MyResourceGroup" --template-file template.json`
- **Query Resources**: `az resource list --resource-group "MyResourceGroup" --output table`
- **Update CLI**: `az upgrade`
- **Extensions**: Install extensions like `az extension add --name azure-devops` for additional commands.

For scripting, combine with Bash/PowerShell loops or use Azure CLI in CI/CD pipelines like GitHub Actions.

## Tips and Best Practices
- Use `--dry-run` for previews (where supported).
- Enable auto-completion: On Bash, run `az completion`.
- Handle errors: Check exit codes (0 for success) and use `--debug` for troubleshooting.
- Security: Avoid hardcoding credentials; use environment variables or Azure Key Vault.

## References
[Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
[Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
[Azure CLI Quickstart](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)
