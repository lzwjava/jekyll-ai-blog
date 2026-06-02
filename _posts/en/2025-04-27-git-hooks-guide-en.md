---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Git Hooks Guide Pre Commit Pre Push
translated: false
type: note
---

### Git Hooks Overview
Git hooks are customizable scripts that automate tasks at specific points in the Git workflow. They can be client-side (run on your local machine) or server-side (run on the remote repository). Hooks are stored in the `.git/hooks/` directory of a repository. Below, I'll break down pre-commit, pre-push, and server-side hooks related to pushing, explaining how they execute.

### Client-Side Hooks: Pre-Commit and Pre-Push
These hooks run locally on your machine before actions are finalized, allowing you to enforce rules or run checks.

- **Pre-Commit Hook**:
  - **When it runs**: Automatically triggered just before you commit changes (e.g., via `git commit`).
  - **Purpose**: Useful for code quality checks, such as running linters, tests, or formatting tools. If the hook fails (exits with a non-zero status), the commit is aborted.
  - **Example**: A sample pre-commit hook might run `eslint` on JavaScript files. If there are errors, the commit stops.
  - **How it works**: The script is in `.git/hooks/pre-commit`. Make it executable with `chmod +x .git/hooks/pre-commit`. If you use tools like Husky (a popular library for managing Git hooks), it simplifies setup.

- **Pre-Push Hook**:
  - **When it runs**: Automatically triggered just before you push to a remote (e.g., via `git push`).
  - **Purpose**: Checks things like running tests, verifying code coverage, or ensuring compatibility before sending changes to the remote. If it fails, the push is blocked.
  - **Note on "some prepush"**: There isn't a standard "prepush" hook in Git—I'm assuming you mean the "pre-push" hook (with a hyphen). You can create custom pre-push scripts, often via tools like Husky, to enforce rules like "only push if all tests pass."
  - **Example**: A pre-push hook could run `npm test` and abort the push if tests fail. If skipped (e.g., with `git push --no-verify`), the hook won't run.
  - **How it works**: Located at `.git/hooks/pre-push`. Executable permissions are needed. It receives arguments like the remote name and ref being pushed.

Client-side hooks ensure issues are caught early, preventing bad commits or pushes from leaving your machine.

### Server-Side Hooks During Push
When you run `git push`, the push is sent to the remote repository (e.g., GitHub, GitLab, or a custom server). The remote can have its own hooks that execute during or after the push process. These are stored in the remote Git repository's `.git/hooks/` directory and are managed by the server admin.

- **Process During Push**:
  1. **Local checks**: Pre-push hook runs first (if present).
  2. **Data transfer**: Changes are sent to the remote.
  3. **Remote execution**: Server-side hooks run on the remote server, not on your machine.

- **Pre-Receive Hook**:
  - **When it runs**: On the remote server, immediately upon receiving the push but before updating any refs (branches or tags).
  - **Purpose**: Validates the incoming changes. It can reject the entire push if checks fail, such as enforcing commit messages, code reviews, or security scans.
  - **How it works**: If the hook exits with a non-zero status, the push is denied, and you'll see an error message. Example: Reject pushes that introduce files over a certain size.

- **Update Hook** (Similar to Pre-Receive but per-ref):
  - **When it runs**: For each branch/tag being updated, after pre-receive.
  - **Purpose**: Allows fine-grained control, like checking if the push is from an authorized user or if the branch follows naming conventions.
  - **How it works**: Receives details about the ref being updated.

- **Post-Receive Hook**:
  - **When it runs**: On the remote server, after the push is fully accepted and refs are updated.
  - **Purpose**: Triggers downstream actions, such as deploying code, sending notifications (e.g., Slack alerts), or running post-deployment scripts like "rebuild the application."
  - **How it works**: Runs reliably after a successful push. Example: Automatically trigger a CI/CD pipeline or update a web server.

Server-side hooks provide centralized enforcement, so even if your local hooks are bypassed, the remote can still validate or react to the push. Platforms like GitHub use webhooks (API-based equivalents) for similar purposes, but for bare Git servers or self-hosted repos, the hooks above are key.

### Key Differences and Best Practices
- **Client vs. Server**: Client hooks (like pre-commit/pre-push) give you quick feedback locally. Server hooks enforce repository-wide rules.
- **Customization**: Hooks are shell scripts (e.g., Bash) but can invoke Python, Node.js, etc. Use tools like pre-commit (a framework) for managing them.
- **Bypassing**: Commit with `--no-verify`, push with `--no-verify`, but server hooks can't be bypassed unless you have admin access.
- **Setup Tips**: Hooks aren't copied between repos, so add them to a repo's template or use a tool to install them.

If you're setting this up, check Git's documentation or tools like Husky for node projects. If you have a specific scenario (e.g., code example), provide more details for tailored advice!
