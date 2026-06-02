---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Enforce 30-Minute Build Gap
translated: false
type: note
---

### Modify the Workflow to Enforce a 30-Minute Gap Between Builds

To ensure your Jekyll deployment workflow doesn't run too frequently (i.e., at least a 30-minute gap between consecutive runs), you can add a conditional step early in the `build` job. This step will query the GitHub API for the timestamp of the most recent successful run of this workflow. If the current trigger is within 30 minutes of that run's completion, the job will exit early with a message (skipping the build).

This approach:

- Uses the GitHub REST API (no external tools needed).
- Only checks for **successful** previous runs (status: "completed", conclusion: "success").
- Calculates the time difference in seconds and compares it to 1800 (30 minutes).
- Works with your existing push and `workflow_dispatch` triggers.
- Doesn't interfere with the concurrency setup (which handles overlapping runs).

#### Updated YAML Snippet

Insert this new step right after the "Checkout Repository" step in your `build` job. The rest of the workflow remains unchanged.

{% raw %}

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      TELEGRAM_BOT_API_KEY: ${{ secrets.TELEGRAM_BOT_API_KEY }}
      OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: Enforce 30-Minute Build Gap
        id: cooldown
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Fetch the most recent successful run of this workflow
          RUNS_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/${{ github.repository }}/actions/workflows/${{ github.workflow_ref }}/runs?status=completed&conclusion=success&per_page=1&sort=timestamp&direction=desc")

          # Extract the completed_at timestamp of the latest successful run (ISO 8601 format)
          LAST_COMPLETED_AT=$(echo "$RUNS_RESPONSE" | jq -r '.[0].completed_at // empty')

          if [ -z "$LAST_COMPLETED_AT" ] || [ "$LAST_COMPLETED_AT" = "null" ]; then
            echo "No previous successful run found. Proceeding with build."
            echo "skip_build=false" >> $GITHUB_OUTPUT
            exit 0
          fi

          # Convert timestamps to Unix seconds for comparison
          CURRENT_TIME=$(date -u +%s)
          LAST_TIME=$(date -d "$LAST_COMPLETED_AT" +%s)
          TIME_DIFF=$((CURRENT_TIME - LAST_TIME))

          echo "Last successful run completed at: $LAST_COMPLETED_AT (diff: ${TIME_DIFF}s)"

          if [ $TIME_DIFF -lt 1800 ]; then  # 1800 seconds = 30 minutes
            echo "Build skipped: Less than 30 minutes since last successful run."
            echo "skip_build=true" >> $GITHUB_OUTPUT
            exit 0
          else
            echo "Sufficient time gap. Proceeding with build."
            echo "skip_build=false" >> $GITHUB_OUTPUT
            exit 0
          fi

      # Skip the entire build if cooldown check fails (add this condition to subsequent steps or wrap the build in an if)
      - name: Set up Python 3.13.2
        if: steps.cooldown.outputs.skip_build != 'true'
        uses: actions/setup-python@v4
        with:
          python-version: "3.13.2"

      # ... (repeat the 'if: steps.cooldown.outputs.skip_build != 'true'' condition on ALL remaining steps after this one)
```

{% endraw %}

#### Key Changes Explained

1. **API Query**:
   - Uses `curl` to hit the GitHub Actions API endpoint for workflow runs.
   - Filters for `status=completed` and `conclusion=success` to get only finished, successful runs.
   - Limits to `per_page=1` and sorts by `timestamp desc` for the most recent one.
   - Extracts `completed_at` (the exact end time of the previous run).

2. **Time Calculation**:
   - Converts both current time and last completion time to Unix timestamps using `date`.
   - Computes the difference in seconds.
   - If `< 1800` seconds, sets `skip_build=true` and exits the step early.

3. **Conditional Execution**:
   - Add `if: steps.cooldown.outputs.skip_build != 'true'` to **every subsequent step** (e.g., Python setup, Install Dependencies, all the way to Sync built site).
   - This ensures the job reports "skipped" in GitHub UI if the cooldown triggers, but still logs the reason.

4. **Edge Cases Handled**:
   - No previous runs: Proceeds (first build).
   - Failed/in-progress previous runs: Ignores them and proceeds.
   - API errors: Falls back to proceeding (safe default).
   - `jq` is pre-installed on `ubuntu-latest`, so no extra setup needed.

#### Testing the Change

- Commit this to your `main` branch (it will trigger the workflow).
- Trigger multiple quick pushes/dispatches: The second one within 30 min should skip.
- Monitor the job logs for the "Build skipped" message.
- If you want to adjust the gap (e.g., 1 hour), change `1800` to `3600`.

#### Alternatives

- **Schedule Trigger**: If you want *periodic* builds every 30 min (regardless of pushes), add this to the `on:` section:

  ```yaml
  schedule:
    - cron: '*/30 * * * *'  # Every 30 minutes
  ```

  But this doesn't enforce a gap on push triggers—use it alongside the cooldown step if needed.
- **Custom Action**: For reusability, wrap the cooldown logic in a reusable workflow or composite action.
- **Limitations**: This checks run completion time, not start time. If a previous run is still running >30 min, concurrency will cancel it anyway.

If this doesn't fit your exact intent (e.g., you meant scheduling *at least* every 30 min), provide more details!
