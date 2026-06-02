---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Automated Git Sync via Cron
translated: false
type: note
---

To automatically sync updates from one laptop's Git pushes to another laptop's clone of the same repo (without manual `git pull`), you can't rely on Git alone for real-time "automatic" updates across machines—Git is pull-based by design. However, you can set up a scheduled task on the second laptop to periodically fetch and merge changes from the remote (GitHub in your case). This is the simplest, reliable way for a personal setup like yours.

Here's how to do it on your Mac (since you're using a MacBook Air). We'll use `cron` for scheduling, as it's built-in and lightweight. Assume both laptops have clones of `github.com:lzwjava/blog-source`, and you're on the `main` branch.

### Step 1: Ensure the Second Laptop's Repo is Set Up Correctly

On the second laptop:

1. Navigate to your repo: `cd /path/to/blog-source`
2. Make sure it tracks the remote: `git remote -v` (should show `origin` as your GitHub repo).
3. If not, add it: `git remote add origin git@github.com:lzwjava/blog-source.git`
4. Fetch current state: `git fetch origin`
5. Switch to main: `git checkout main`
6. Set upstream: `git branch --set-upstream-to=origin/main main`

Test a manual pull: `git pull origin main`. It should work like your output.

### Step 2: Create a Script for Automated Pull

Create a simple shell script to handle the pull safely (it fetches, checks for conflicts, and pulls if clean).

1. In your repo root, create `auto-pull.sh`:

   ```bash:disable-run
   #!/bin/bash
   cd "$(dirname "$0")"  # Change to repo directory
   git fetch origin
   if git diff HEAD origin/main --quiet; then
       git pull origin main
       echo "Auto-pull completed: $(date)"
   else
       echo "Warning: Local changes detected. Skipping pull. Resolve manually: $(date)"
       # Optional: Send email or notification (see below)
   fi
   ```

2. Make it executable: `chmod +x auto-pull.sh`

This script:

- Fetches updates without merging.
- Checks if your local branch is clean (no uncommitted changes).
- Pulls only if safe; otherwise, warns you.

### Step 3: Schedule It with Cron

Cron runs jobs periodically. We'll run it every 5 minutes (adjust as needed; e.g., hourly).

1. Open crontab editor: `crontab -e` (use nano if prompted: `nano ~/.crontab`).

2. Add this line at the end (for every 5 minutes):

   ```
   */5 * * * * /path/to/blog-source/auto-pull.sh >> /path/to/blog-source/pull-log.txt 2>&1
   ```

   - Replace `/path/to/blog-source` with your actual repo path (e.g., `~/blog-source`).
   - The `>> pull-log.txt` logs output to a file for debugging.

3. Save and exit (Ctrl+O, Enter, Ctrl+X in nano).
4. Verify: `crontab -l` (should show your line).
5. Test: Wait 5 minutes or run `crontab -e` again to add `* * * * *` temporarily (every minute), then revert.

Cron runs as your user, so it respects your SSH key for GitHub auth (like in your pull output).

### Optional Enhancements

- **Handle Conflicts/Notifications**: If the script detects issues, add a notification. Edit `auto-pull.sh` to append:

  ```bash
  # If warning, send macOS notification
  osascript -e 'display notification "Git pull skipped due to local changes" with title "Blog Repo Sync"'
  ```

- **Run on Push (from First Laptop)**: For more "push-like" sync, use GitHub Actions on the first laptop. Create `.github/workflows/sync.yml`:

  ```yaml
  name: Auto Sync
  on: [push]
  jobs:
    sync:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Notify (e.g., via webhook to second laptop)
          run: curl -X POST https://your-second-laptop-webhook-endpoint  # Set up a simple server on second laptop
  ```

  But this requires a listener on the second machine (e.g., via ngrok + a tiny Flask app), which is overkill for most cases.
- **Frequency Trade-offs**: Every 5 mins is fine for a blog repo. For real-time, consider tools like `watch` in a terminal (`watch -n 300 git pull`), but cron is hands-off.
- **Proxy Note**: Your output shows HTTP/HTTPS proxies—cron will inherit them, so pulls should work as-is.

Now, when you push from the first laptop (`git push origin main`), the second will sync automatically every 5 mins. Check `pull-log.txt` for history.

If you run into auth/proxy issues in cron, add `export HTTP_PROXY=http://127.0.0.1:7890` etc. to the script. For Windows on the other laptop, use Task Scheduler instead.

```
