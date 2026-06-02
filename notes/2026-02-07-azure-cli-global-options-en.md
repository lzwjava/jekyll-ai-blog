---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Azure CLI Global Options Guide
translated: false
type: note
---

Question: Provide a comprehensive introduction to Azure CLI command line options.

Answer:

The **Azure CLI** (`az`) is a cross-platform command-line tool for managing Azure resources. Almost every command supports a set of **global arguments** (also called global parameters or global options) that work across nearly all commands.

These global options are the most frequently used "command line options" when people talk about Azure CLI usage patterns.

### Most Important Global Arguments (2026)

These arguments can be appended to almost any `az` command:

| Argument              | Short | Common values / Description                                                                 | Typical use case                              |
|-----------------------|-------|---------------------------------------------------------------------------------------------|-----------------------------------------------|
| `--help`              | `-h`  | Show help for the command / group                                                           | Learn any command: `az vm create -h`          |
| `--output`            | `-o`  | `json` (default), `jsonc`, `table`, `tsv`, `yaml`, `yamlc`, `none`                          | Human-readable: `--output table`<br>Machine: `--output json` |
| `--query`             |       | JMESPath expression                                                                         | Filter output: `--query "[].{name:name, id:id}"` |
| `--subscription`      |       | Subscription name or ID                                                                     | Override default: `--subscription "Prod Sub"` |
| `--verbose`           |       | Increase logging verbosity                                                                  | See more details during execution             |
| `--debug`             |       | Show all debug logs + low-level REST API calls                                              | Troubleshooting / deep debugging              |
| `--only-show-errors`  |       | Suppress warnings, show only errors                                                         | Clean CI/CD output                            |

**Quick examples**:

```bash
# Human-friendly table output
az resource list --output table

# Filter to only names and locations
az vm list --query "[].{Name:name, Location:location}" --output table

# Run command in a specific subscription
az group list --subscription "My-Dev-Sub" -o table

# Debug a failing command
az storage account create ... --debug
```

### Other Useful Global / Frequently Encountered Options

- `--resource-group` / `-g`
  Very common positional-style argument (not strictly global, but appears in hundreds of commands)

- `--name` / `-n`
  Resource name (very common)

- `--ids`
  Accepts one or more Azure Resource IDs instead of requiring `--resource-group --name ...`

- `--yes` / `-y`
  Auto-answer "yes" to confirmation prompts (great for automation)

- `--no-wait`
  Do not wait for long-running operations to complete (fire-and-forget)

- `--wait` (some commands)
  Wait until operation finishes and show final status

### Configuration that Affects Command-line Behavior

Many behaviors can be set once (instead of repeating flags every time) using:

```bash
# Interactive wizard (recommended for beginners)
az init

# Or set individual values
az config set core.output=table
az config set core.default_subscription="My-Sub-Name"
az config set logging.enable_log_file=true
```

Common config keys that influence command-line feel:

- `core.output` → default output format
- `core.only_show_errors` → like permanent `--only-show-errors`
- `core.no_color` → disable ANSI colors
- `core.collect_telemetry` → opt out of telemetry
- `core.default_subscription` / `core.default_resource_group` / `core.default_location`

### Positional vs Named Arguments

Azure CLI uses two styles:

- **Named** (most common): `--resource-group myRg --name myVm`
- **Positional** (less common, but exists): some very old commands or extensions

Always prefer named arguments for clarity and script robustness.

### Best Practices Summary (2026 style)

- Use `--output table` interactively
- Use `--output json` + `--query` in scripts / CI/CD
- Prefer `--ids` when scripting with resource IDs
- Chain `--only-show-errors` in pipelines
- Use `az config` or `az init` to reduce typing
- Always check help: `az <group> <command> -h`

The full list of global parameters is shown when you run `az --help` or any command with `--help`.

References:

- [Get started with Azure CLI - Global arguments](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest)
- [Azure CLI global parameters](https://learn.microsoft.com/en-us/cli/azure/azure-cli-global-parameters?view=azure-cli-latest)
- [Azure CLI configuration options](https://learn.microsoft.com/en-us/cli/azure/azure-cli-configuration?view=azure-cli-latest)
- [Azure CLI reference index](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest)
