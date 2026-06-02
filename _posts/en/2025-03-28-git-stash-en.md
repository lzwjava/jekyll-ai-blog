---
audio: false
generated: true
lang: en
layout: post
title: Git Stash
translated: false
type: note
---

Here's how to effectively use `git stash` and switch branches/tags frequently with uncommitted changes:

## Using `git stash`

`git stash` is a powerful command that allows you to temporarily save your uncommitted changes (both staged and unstaged) and revert your working directory to the last commit. This is useful when you need to switch branches or work on something else without committing your current, unfinished work.

Here's a breakdown of common `git stash` operations:

**1. Stashing your current changes:**

```bash
git stash
```

This command takes your uncommitted changes, saves them as a new stash, and cleans your working directory. You'll see a message like:

```
Saved working directory and index state WIP on <your_branch>: <commit_hash> <commit_message>
```

**2. Stashing with a message:**

It's helpful to add a descriptive message to your stashes, especially if you have multiple ones:

```bash
git stash save "your descriptive message"
# or
git stash push -m "your descriptive message"
```

**3. Listing your stashes:**

To see a list of all your saved stashes, use:

```bash
git stash list
```

This will display a list of stashes, usually in the format:

```
stash@{0}: On <branch_name>: <commit_hash> <stash_message>
stash@{1}: WIP on <another_branch>: ...
```

`stash@{0}` is the most recent stash.

**4. Applying a stash:**

To bring back the changes from a stash, you can use `git stash apply`. This applies the changes but keeps the stash in the list. By default, it applies the latest stash (`stash@{0}`).

```bash
git stash apply
# or to apply a specific stash:
git stash apply stash@{1}
```

**5. Applying and removing a stash:**

If you want to apply the changes and immediately remove the stash from the list, use `git stash pop`. This also defaults to the latest stash.

```bash
git stash pop
# or to pop a specific stash:
git stash pop stash@{1}
```

**6. Viewing stash details:**

You can see a summary of the changes in a stash using:

```bash
git stash show
# or for a specific stash:
git stash show stash@{2}
```

To see the full diff of a stash, add the `-p` or `--patch` flag:

```bash
git stash show -p stash@{0}
```

**7. Stashing untracked files:**

By default, `git stash` only stashes changes to tracked files. To include untracked files, use the `-u` or `--include-untracked` option:

```bash
git stash -u
git stash save -u "stash with untracked"
```

**8. Stashing ignored files as well:**

To include both untracked and ignored files, use the `-a` or `--all` option:

```bash
git stash -a
git stash save -a "stash with all"
```

**9. Creating a branch from a stash:**

If you stashed some changes and now want to work on them in a new branch, you can create a branch directly from the stash:

```bash
git stash branch <new_branch_name> stash@{0}
# or for the latest stash:
git stash branch <new_branch_name>
```

This command creates a new branch based on the commit where the stash was created, applies the stashed changes to the new branch, and then drops the stash.

**10. Removing stashes:**

* To remove a specific stash:

    ```bash
    git stash drop stash@{1}
    ```

* To remove all stashes:

    ```bash
    git stash clear
    ```

## Switching Branches or Tags Frequently with Uncommitted Changes

Here's how to use `git stash` to facilitate frequent switching between branches or tags when you have uncommitted changes:

**Scenario 1: Switching to another branch**

1. **Stash your current changes:**

    ```bash
    git stash save "WIP on current branch"
    ```

2. **Switch to the target branch:**

    ```bash
    git checkout <target_branch_name>
    # or using the newer `git switch` command:
    git switch <target_branch_name>
    ```

3. **Do your work on the target branch.**
4. **When you need to go back to your original branch:**

    ```bash
    git checkout <original_branch_name>
    # or
    git switch <original_branch_name>
    ```

5. **Reapply your stashed changes:**

    ```bash
    git stash pop  # If you want to apply and remove the stash
    # or
    git stash apply # If you want to apply and keep the stash
    ```

6. **Resolve any potential merge conflicts** that might arise if the original branch has diverged significantly since you stashed.

**Scenario 2: Switching to a tag**

Switching directly to a tag puts you in a "detached HEAD" state, which is generally not recommended for making commits. If you just want to inspect the code at a specific tag:

1. **Stash your current changes:**

    ```bash
    git stash save "WIP before tag inspection"
    ```

2. **Switch to the tag:**

    ```bash
    git checkout <tag_name>
    ```

3. **Inspect the code.**
4. **To go back to your branch:**

    ```bash
    git checkout <your_branch_name>
    # or
    git switch <your_branch_name>
    ```

5. **Reapply your stashed changes:**

    ```bash
    git stash pop
    # or
    git stash apply
    ```

**Scenario 3: Creating a new branch from a tag with your stashed changes**

If you want to start working on a new feature or fix based on a specific tag, and you have stashed changes from a previous context:

1. **Stash your current changes (if you haven't already):**

    ```bash
    git stash save "WIP"
    ```

2. **Create a new branch from the tag:**

    ```bash
    git checkout -b <new_branch_name> <tag_name>
    # or
    git switch -c <new_branch_name> <tag_name>
    ```

3. **Apply your stashed changes to the new branch:**

    ```bash
    git stash pop # or git stash apply
    ```

4. **Resolve any potential merge conflicts.**

**Important Considerations:**

* **Keep your stashes organized:** Use descriptive messages to easily identify your stashes.
* **Stash is local:** Stashes are stored locally in your repository and are not pushed to remote repositories.
* **Potential for conflicts:** When you reapply a stash, there's a possibility of merge conflicts if the branch you're applying to has changed significantly since you created the stash. You'll need to resolve these conflicts manually.
* **Consider creating temporary branches:** For longer-term work that you're not ready to commit, creating a temporary branch might be a better approach than relying heavily on stashes. You can easily switch between branches and commit your progress.

By using `git stash` effectively, you can seamlessly switch between branches and tags even when you have uncommitted changes, allowing for a more flexible and efficient workflow. Remember to manage your stashes and be prepared to handle potential merge conflicts.
