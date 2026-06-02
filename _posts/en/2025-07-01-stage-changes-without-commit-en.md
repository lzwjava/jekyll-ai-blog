---
audio: false
generated: true
lang: en
layout: post
title: Stage Changes in Pre-Commit Hook
translated: false
type: note
---

To integrate the changes from the `update_notes_link.py` script into the current commit (instead of creating a separate commit) during a pre-commit hook, you’ll need to modify the hook to stage the updated files without committing them separately. This way, the changes from the Python script will be included in the user’s commit. Below, I’ll provide a revised pre-commit hook script that achieves this.

### Key Changes
- **No Separate Commit**: Instead of running `git commit` in the hook, the script will only stage the updated files (`git add`) so they’re included in the user’s commit.
- **Preserve User’s Commit Message**: The hook won’t create a new commit, ensuring the user’s original commit message is used.
- **Error Handling**: If the Python script fails, the hook will exit with a non-zero status to prevent the commit.

### Pre-Commit Hook Script

Here’s the updated pre-commit hook script that stages changes without creating a separate commit:

```x-shellscript
#!/bin/bash

# Run the update_notes_link.py script and capture its output
OUTPUT=$(python scripts/generate/update_notes_link.py 2>&1)
EXIT_CODE=$?

# Check if the Python script executed successfully
if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: update_notes_link.py failed with exit code $EXIT_CODE"
    echo "$OUTPUT"
    exit 1
fi

# Check if the specific file was updated
if echo "$OUTPUT" | grep -q "Updated original/2025-01-11-notes-en.md"; then
    echo "Notes links updated, staging changes for the current commit."

    # Stage the relevant files
    git add original/2025-01-11-notes-en.md
    git add _posts/en/*.md

    # Verify that files were staged
    if ! git diff --cached --quiet; then
        echo "Changes staged successfully."
    else
        echo "No changes to stage."
    fi
else
    echo "No updates to original/2025-01-11-notes-en.md, no additional files staged."
fi

# Exit with success to allow the commit to proceed
exit 0
```

### Explanation of the Script

- **Shebang (`#!/bin/bash`)**: Ensures the script runs in a Bash shell.
- **Run Python Script**: Executes `python scripts/generate/update_notes_link.py` and captures its output and exit code.
- **Error Handling**: Checks the exit code (`$EXIT_CODE`) of the Python script. If it’s non-zero, the hook fails, prints the error, and stops the commit.
- **Check Output**: Uses `grep` to check if the output indicates `original/2025-01-11-notes-en.md` was updated.
- **Stage Files**: Runs `git add` on the specified files (`original/2025-01-11-notes-en.md` and `_posts/en/*.md`) to include them in the user’s commit.
- **No Commit**: Skips `git commit`, allowing the user’s `git commit` command to include the staged changes with their original commit message.
- **Feedback**: Prints messages to inform the user whether changes were staged.
- **Exit Code**: Exits with `0` to allow the commit to proceed, unless the Python script fails.

### Setting Up the Hook

1. **Create the Hook**:
   - Place the script in `.git/hooks/pre-commit` in your repository.

2. **Make It Executable**:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

3. **Test the Hook**:
   - Modify a file or ensure the Python script will update `original/2025-01-11-notes-en.md`.
   - Run `git commit -m "Your commit message"`.
   - Verify that the updated files are included in the commit by checking `git diff --cached` before committing or `git show` after committing.

### Using the `pre-commit` Framework (Optional)

If you prefer using the `pre-commit` framework, you can define the same logic in a `.pre-commit-config.yaml` file. This approach is more portable and allows you to specify which files trigger the hook.

1. **Install pre-commit**:
   ```bash
   pip install pre-commit
   ```

2. **Create `.pre-commit-config.yaml`**:

```yaml
repos:
- repo: local
  hooks:
  - id: update-notes-links
    name: Update Notes Links
    entry: bash -c '
      OUTPUT=$(python scripts/generate/update_notes_link.py 2>&1);
      EXIT_CODE=$?;
      if [ $EXIT_CODE -ne 0 ]; then
        echo "Error: update_notes_link.py failed with exit code $EXIT_CODE";
        echo "$OUTPUT";
        exit 1;
      fi;
      if echo "$OUTPUT" | grep -q "Updated original/2025-01-11-notes-en.md"; then
        echo "Notes links updated, staging changes for the current commit.";
        git add original/2025-01-11-notes-en.md;
        git add _posts/en/*.md;
        if ! git diff --cached --quiet; then
          echo "Changes staged successfully.";
        else
          echo "No changes to stage.";
        fi;
      else
        echo "No updates to original/2025-01-11-notes-en.md, no additional files staged.";
      fi'
    language: script
    files: ^(original/2025-01-11-notes-en\.md|_posts/en/.*\.md)$
    stages: [commit]
```

3. **Install the Hook**:
   ```bash
   pre-commit install
   ```

4. **Test the Hook**:
   - Commit changes to files matching the `files` regex (e.g., `original/2025-01-11-notes-en.md` or `_posts/en/*.md`).
   - Verify that the hook runs, stages changes if applicable, and includes them in your commit.

### Key Differences from Original GitHub Actions

- **No Separate Commit**: Unlike the GitHub Actions workflow, which created a new commit, this hook stages changes for the user’s current commit.
- **No Push**: The hook doesn’t push changes, as pre-commit hooks run locally before the commit is finalized. The user must run `git push` manually.
- **Error Handling**: The hook checks the Python script’s exit code to ensure it doesn’t silently fail.
- **No Git User Config**: The script omits `git config user.name` and `user.email` since the user’s Git configuration will be used for the commit.

### Notes

- **Python Script**: Ensure `scripts/generate/update_notes_link.py` exists and is executable locally. If it relies on environment variables or dependencies, make sure they’re available.
- **File Paths**: Verify that the paths `original/2025-01-11-notes-en.md` and `_posts/en/*.md` match your repository structure.
- **Hook Failure**: If the Python script fails, the hook will prevent the commit, ensuring no partial updates are staged.
- **Testing**: Test with `git commit` to confirm that changes are staged and included in the commit without creating an extra commit. Use `git show` to inspect the commit contents.

### Verification

To verify:
1. Modify a file or ensure the Python script updates `original/2025-01-11-notes-en.md`.
2. Run `git commit -m "Test commit"`.
3. Check `git show` to confirm that the updated files are included in the commit with your original message.
4. Ensure no additional commits are created (e.g., no `chore(notes): Update notes links` commit).

If you need further tweaks, such as handling specific error cases or adding more files to stage, let me know!
