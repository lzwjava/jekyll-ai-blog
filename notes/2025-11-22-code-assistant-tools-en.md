---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-pro-preview
title: Code Assistant Tool Categories
translated: false
type: note
---

The typical **tool calls** or **actions** in a powerful code assistant like Claude Code are centered around enabling it to interact with a real-world coding environment and perform the tasks a human developer would.

These tool calls fall into a few primary categories:

### 1. File System and Codebase Interaction

These are essential for the assistant to understand the project, read existing code, and make changes.

| Tool/Action | Typical Use Case |
| :--- | :--- |
| **`read_file`** (or file reference like `@filename`) | Retrieving the content of a specific file to understand its logic, dependencies, or context. |
| **`list_directory`** | Getting a file structure or a list of files in a directory to identify relevant modules or find a specific file. |
| **`edit_file` / `write_file`** | The core action for implementing a solution, refactoring, adding a feature, or fixing a bug in the code. |
| **`create_file`** | Writing new files, such as a new test file, configuration file, or a new component. |
| **`search_files`** | Finding all files in the codebase that contain a specific string (e.g., a function name, a class name, or an error message). |

### 2. Execution and Debugging

To verify its work, fix errors, and get real-time feedback, the assistant needs to run commands.

| Tool/Action | Typical Use Case |
| :--- | :--- |
| **`bash` / `run_command`** | Executing shell commands like running a build (`npm build`), running tests (`pytest`, `npm test`), linting the code (`eslint`), or running a script. |
| **`code_interpreter`** | Running a small snippet of code in a sandboxed environment to quickly calculate something, test a library function, or analyze a small dataset. |

### 3. Version Control (Git)

An agentic coding assistant can manage the development workflow by interacting with Git.

| Tool/Action | Typical Use Case |
| :--- | :--- |
| **`git status`** | Checking the current state of the working directory. |
| **`git diff`** | Seeing the changes that have been made to review its own work. |
| **`git commit`** | Saving changes to the repository, often with a generated commit message. |
| **`git checkout`** | Switching branches or discarding uncommitted changes. |
| **`create_pull_request`** | Automating the final step of a feature or fix. |

### 4. External Information

For up-to-date information, documentation, or connecting to external services, specialized tools are used.

| Tool/Action | Typical Use Case |
| :--- | :--- |
| **`web_search`** | Looking up the latest syntax, reading official API documentation, or finding troubleshooting guides for a specific error. |
| **Custom APIs / MCP Servers** | Connecting to external services using the Model Context Protocol (MCP), such as fetching data from a Google Drive, interacting with a database (PostgreSQL), or sending a message to a communication tool (Slack). |

In essence, these "tool calls" allow the Large Language Model (LLM) to transform from a text generator into a full **agent** that can observe its environment (read files, run commands), think (plan the work), and act (edit files, commit code).

Would you like to see a step-by-step example of how a code assistant might use these tools to fix a simple bug?
