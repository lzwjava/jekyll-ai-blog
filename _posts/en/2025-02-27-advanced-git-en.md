---
audio: false
generated: true
lang: en
layout: post
title: Advanced Git Commands
translated: false
type: note
---

Git is like a Swiss Army knife for developers—versatile, powerful, and occasionally confusing if you don’t know which tool to pull out. Today, we’re diving into some of Git’s niftiest features and workflows: cherry-picking changes, merging with style, rebasing for a cleaner history, deleting those pesky large files you accidentally committed, and undoing a commit when you realize you’ve gone off the rails. Let’s break it down.

#### Cherry-Picking: Grabbing Just What You Need

Imagine you’ve got a feature branch with a dozen commits, but there’s one shiny commit in there that you want to pluck out and apply to your main branch—without bringing the rest along. That’s where `git cherry-pick` comes in.

It’s super straightforward: find the commit hash (you can grab it from `git log`), switch to the branch where you want it, and run:

```
git cherry-pick <commit-hash>
```

Boom, that commit is now part of your current branch. If there’s a conflict, Git will pause and let you resolve it, just like a merge. Once you’re happy, commit the changes, and you’re good.

I use this all the time when a bug fix sneaks into a messy feature branch, and I need it on `main` ASAP. Just be careful—cherry-picking duplicates the commit, so it gets a new hash. Don’t expect it to play nice if you merge the original branch later without some cleanup.

#### Merge Options: More Than Just “Merge”

Merging is Git’s bread and butter, but did you know it comes with flavors? The default `git merge` does a “fast-forward” if possible (straightening the history) or creates a merge commit if branches have diverged. But you’ve got options:

- **`--no-ff` (No Fast-Forward)**: Forces a merge commit even if a fast-forward is possible. I love this for keeping a clear record of when a feature branch landed on `main`. Run it like:

  ```
  git merge --no-ff feature-branch
  ```

- **`--squash`**: Pulls all the changes from the branch into one commit on your current branch. No merge commit, just a single, tidy package. Perfect for squashing a messy branch into something presentable:

  ```
  git merge --squash feature-branch
  ```

  After this, you’ll need to commit manually to seal the deal.

Each has its place. I lean toward `--no-ff` for long-lived branches and `--squash` when I’ve got a branch full of “WIP” commits I’d rather forget.

#### Rebasing: Rewriting History Like a Pro

If merges feel too cluttered, `git rebase` might be your vibe. It takes your commits and replays them onto another branch, giving you a linear history that looks like you planned everything perfectly from the start.

Switch to your feature branch and run:

```
git rebase main
```

Git will lift your commits off, update the branch to match `main`, and slap your changes back on top. If conflicts pop up, resolve them, then `git rebase --continue` until it’s done.

The upside? A pristine timeline. The downside? If you’ve already pushed that branch and others are working on it, rebasing rewrites history—cue the angry emails from teammates. I stick to rebasing for local branches or solo projects. For shared stuff, merge is safer.

#### Deleting Large Files from History: Oops, That 2GB Video

We’ve all been there: you accidentally commit a massive file, push it, and now your repo’s bloated. Git doesn’t forget easily, but you can scrub that file from history with some effort.

The go-to tool here is `git filter-branch` or the newer `git filter-repo` (I recommend the latter—it’s faster and less error-prone). Say you committed `bigfile.zip` and need it gone:

1. Install `git-filter-repo` (check its docs for setup).
2. Run:

   ```
   git filter-repo --path bigfile.zip --invert-paths
   ```

   This removes `bigfile.zip` from every commit in history.
3. Force-push the rewritten history:

   ```
   git push --force
   ```

Heads-up: this rewrites history, so coordinate with your team. And if it’s in a pull request somewhere, you might need to clean up refs too. Once it’s gone, your repo will slim down after a garbage collection (`git gc`).

#### Uncommitting: Rewinding the Clock

Made a commit and instantly regretted it? Git’s got your back. There are a couple ways to undo it, depending on how far you’ve gone:

- **If you haven’t pushed yet**: Use `git reset`. To undo the last commit but keep the changes in your working directory:

  ```
  git reset HEAD^ --soft
  ```

  Want to ditch the changes entirely?

  ```
  git reset HEAD^ --hard
  ```

- **If you’ve already pushed**: You’ll need to rewrite history. Reset locally with `git reset HEAD^`, then force-push:

  ```
  git push --force
  ```

  Again, this messes with shared history, so tread carefully.

I’ve saved myself with `git reset --soft` more times than I can count—perfect for when I commit too soon and need to tweak something.

#### Wrapping Up

Git’s flexibility is what makes it so powerful, but it’s easy to get tangled up if you don’t know your options. Cherry-pick for surgical precision, tweak merges to fit your workflow, rebase for a polished history, and don’t panic when you need to erase a mistake—whether it’s a huge file or a hasty commit. Practice these on a test repo if you’re nervous, and soon they’ll feel like second nature.

What’s your favorite Git trick? Let me know—I’m always up for learning something new!
