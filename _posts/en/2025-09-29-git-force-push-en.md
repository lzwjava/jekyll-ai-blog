---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Git Force Push via Branch Deletion
translated: false
type: note
---

```python
#!/usr/bin/env python3
"""
git_force_push.py

This script performs a "force push" by first deleting the remote branch,
then pushing the local branch. This works if the repository allows branch
deletions but not force pushes.

Usage: python git_force_push.py <remote> <branch>
Example: python git_force_push.py origin main

Note: This assumes you have sufficient permissions and that deletion is allowed.
Be cautious, as deleting a branch can lose commits.
"""

import subprocess
import sys

def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python git_force_push.py <remote> <branch>")
        sys.exit(1)

    remote = sys.argv[1]
    branch = sys.argv[2]

    # Delete the remote branch
    delete_cmd = f"git push {remote} :{branch}"
    print(f"Deleting remote branch: {delete_cmd}")
    run_command(delete_cmd)

    # Push the local branch
    push_cmd = f"git push {remote} {branch}"
    print(f"Pushing local branch: {push_cmd}")
    run_command(push_cmd)

    print("Force push completed successfully.")
```

### How It Works

- **Deletion Step**: Runs `git push origin :main` to delete the remote branch (as allowed in your repo).
- **Push Step**: Runs `git push origin main` to push the local branch, creating it anew on the remote.
- This effectively achieves a force push by discarding the remote history and replacing it with the local history.
- **Safety/Usage Notes**: Test in a non-critical repo first. This requires proper Git setup and permissions. If the repo has additional protections (e.g., via hooks), it might fail. No warranties; Git operations can be destructive.
