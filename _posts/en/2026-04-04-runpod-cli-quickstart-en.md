---
audio: false
generated: true
image: false
lang: en
layout: post
title: Getting Started with RunPod CLI
translated: false
type: note
---

**Question:** What is a comprehensive introduction to the RunPod CLI (`runpodctl`) — the command-line interface for the RunPod GPU platform?

**Answer:**

---

## Introduction to RunPod CLI (`runpodctl`)

### What is RunPod CLI?

`runpodctl` is an open-source command-line interface tool for managing your RunPod resources remotely from your local machine. You can transfer files and data between your local system and RunPod, execute code on remote Pods, and automate Pod deployment workflows.

The CLI offers several key capabilities: managing Pods (create, list, start, stop, terminate), transferring files between your local machine and Pods, and developing and deploying Serverless endpoints using RunPod projects.

Every Pod you deploy comes preinstalled with the `runpodctl` command and a Pod-scoped API key. You can also install it on your local machine to manage your Pods remotely from your own system.

---

### Installation

#### macOS

```bash
# Homebrew (recommended)
brew install runpod/runpodctl/runpodctl

# Apple Silicon (ARM)
wget --quiet --show-progress https://github.com/runpod/runpodctl/releases/download/v1.14.3/runpodctl-darwin-arm64 \
  -O runpodctl && chmod +x runpodctl && sudo mv runpodctl /usr/local/bin/runpodctl

# Intel (AMD)
wget --quiet --show-progress https://github.com/runpod/runpodctl/releases/download/v1.14.3/runpodctl-darwin-amd64 \
  -O runpodctl && chmod +x runpodctl && sudo mv runpodctl /usr/local/bin/runpodctl
```

#### Linux

```bash
wget --quiet --show-progress https://github.com/Run-Pod/runpodctl/releases/download/v1.14.3/runpodctl-linux-amd64 \
  -O runpodctl && chmod +x runpodctl && sudo cp runpodctl /usr/bin/runpodctl
```

#### Windows

```bash
wget https://github.com/runpod/runpodctl/releases/download/v1.14.3/runpodctl-windows-amd64.exe -O runpodctl.exe
```

#### One-liner Universal Installer

```bash
wget -qO- cli.runpod.net | bash
```

---

### Configuration — API Key Setup

Before using `runpodctl` locally, you must authenticate with your RunPod API key:

```bash
runpodctl config --apiKey YOUR_API_KEY
```

This saves the key into `~/.runpod/config.toml`. To verify the installation:

```bash
runpodctl version
```

---

### Command Structure

Commands follow a noun-verb pattern: `runpodctl <resource> <action>`. For example:

```bash
runpodctl pod list
runpodctl pod get <id>
runpodctl pod create --image=<img>
```

---

### Core Command Categories

#### 1. Pod Management

The main pod commands are:

```bash
runpodctl pod list              # list all pods
runpodctl pod get <id>          # get pod details
runpodctl pod create --image=runpod/pytorch:latest --gpu-id=NVIDIA_A100   # create a pod
runpodctl pod update <id>       # update a pod
runpodctl pod start <id>        # start a stopped pod
runpodctl pod stop <id>         # stop a running pod
runpodctl pod delete <id>       # delete a pod
```


You can also start a spot pod with a bid price:

```bash
runpodctl start pod {podId} --bid=0.3
```

The bid price you set is the price you will pay if not outbid.

#### 2. Serverless Endpoint Management



```bash
runpodctl serverless list          # list endpoints (alias: sls)
runpodctl serverless get <id>      # get endpoint details
runpodctl serverless create        # create endpoint
runpodctl serverless update <id>   # update endpoint
runpodctl serverless delete <id>   # delete endpoint
```


#### 3. File Transfer (`send` / `receive`)

`runpodctl` can be used to send files back and forth between the Pod and your local computer, or to send files back and forth between Pods.

To send a file, run the send command and you will receive a unique, one-time transfer code like `8338-galileo-collect-fidel`. On the destination machine, use that code with the receive command.

```bash
# On the sender machine
runpodctl send data.txt
# Output: Code is: 8338-galileo-collect-fidel

# On the receiver machine
runpodctl receive 8338-galileo-collect-fidel
```

Note that you do not need to open any HTTP or TCP ports to use runpodctl — terminal access is enough.

#### 4. Other Resource Management

Other resources managed by `runpodctl` include:

- `template` (alias: `tpl`) — manage templates
- `network-volume` (alias: `nv`) — manage network volumes
- `registry` (alias: `reg`) — manage container registry auth
- `model` — manage model repository


#### 5. Info and Utility Commands



```bash
runpodctl user         # show account info and balance (alias: me)
runpodctl gpu          # list available GPU types
runpodctl datacenter   # list datacenters and availability (alias: dc)
runpodctl billing      # view billing history
runpodctl doctor       # diagnose and fix CLI issues
runpodctl ssh          # manage SSH keys and connections
```


#### 6. SSH Key Management

```bash
runpodctl ssh add-key      # add an SSH public key to your account
runpodctl ssh list-keys    # list all added SSH keys
```

---

### Output Formats

Default output is JSON (optimized for agents). Use the `--output` flag for alternatives:

```bash
runpodctl pod list                   # JSON (default)
runpodctl pod list --output=table    # human-readable table
runpodctl pod list --output=yaml     # YAML format
```


---

### RunPod Projects — Dockerless Serverless Workflow

RunPod introduced a "Dockerless" feature in `runpodctl` version 1.11.0+, which simplifies the AI development process by allowing you to deploy custom endpoints on the serverless platform without the complexities of Docker.

The process involves:
1. Configuring `runpodctl` with your API key
2. Creating a new project (prompts for settings and creates a project folder)
3. Starting a development session
4. Deploying your serverless endpoint

Project files generated include:
- `.runpodignore` — specifies files to exclude during deployment
- `builder/requirements.txt` — pip dependencies
- `runpod.toml` — project config and deployment settings


```bash
# Create a new project
runpodctl project create -n my-project && cd my-project

# Start a development session (auto-syncs code changes)
runpodctl project dev

# Deploy as a serverless endpoint
runpodctl project deploy
```

This establishes a connection between your local environment and a RunPod Pod. Changes to your code are automatically synced to the Pod, allowing for real-time testing without rebuilding Docker images.

---

### Pod Configuration via JSON (Advanced)

You can create pods using a JSON configuration file. Three example types exist: minimal, full, and spot/interruptible. All pod configuration fields are optional with sensible defaults.

Example JSON config:

```json
{
  "name": "Dev Pod",
  "imageName": "runpod/pytorch:2.0.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
  "cloudType": "SECURE",
  "gpuTypeIds": ["NVIDIA GeForce RTX 4090"],
  "gpuCount": 1,
  "containerDiskInGb": 50,
  "volumeInGb": 100,
  "ports": ["8888/http", "22/tcp"]
}
```

```bash
runpod-cli pods create --config my-pod.json
```

---

### CI/CD Integration

RunPod's MLOps integration centers around comprehensive API and CLI support for CI/CD pipeline integration. The platform works with GitHub Actions, GitLab CI, Jenkins, and CircleCI through RESTful API calls and command-line interfaces.

You can automate deployment by storing your API key as a secret in your CI/CD system and invoking `runpodctl` commands in pipeline steps — for example, launching a pod after tests pass, or deploying a new serverless endpoint version.

---

### Getting Help

```bash
runpodctl help                # general help
runpodctl [command] help      # help for a specific command
runpodctl doctor              # diagnose and fix issues
```

---

### Summary Table

| Category | Commands |
|---|---|
| Pod lifecycle | `pod list`, `pod get`, `pod create`, `pod start`, `pod stop`, `pod delete` |
| Serverless | `serverless list/get/create/update/delete` |
| File transfer | `send`, `receive` |
| Projects | `project create`, `project dev`, `project deploy` |
| Storage | `network-volume` (alias `nv`) |
| SSH | `ssh add-key`, `ssh list-keys` |
| Info | `user`, `gpu`, `datacenter`, `billing` |
| Utilities | `doctor`, `update`, `version` |

---

**References:**

- [RunPod CLI Official Docs (Overview)](https://docs.runpod.io/runpodctl/overview)
- [runpodctl GitHub Repository](https://github.com/runpod/runpodctl)
- [RunPod CLI — DeepWiki](https://deepwiki.com/runpod/docs/5.1-runpod-cli-(runpodctl))
- [RunPod Dockerless CLI Blog Post](https://www.runpod.io/blog/dockerless-cli-runpod)
- [RunPod File Transfer Docs](https://docs.runpod.io/pods/storage/transfer-files)
- [runpodctl Go Packages Reference](https://pkg.go.dev/github.com/runpod/runpodctl)
- [Pod Config Examples (MomentFactory)](https://github.com/MomentFactory/runpod-cli/blob/main/examples/POD_CONFIG.md)