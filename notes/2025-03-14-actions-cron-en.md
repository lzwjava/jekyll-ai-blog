---
audio: false
generated: true
lang: en
layout: post
title: GitHub Actions Cron Scheduling
translated: false
type: note
---

Yes, a GitHub workflow can be configured to execute once every day using a cron schedule in GitHub Actions.

### Explanation
GitHub Actions allows you to automate tasks within your repository through workflows, which are defined in YAML files located in the `.github/workflows` directory. One way to trigger a workflow is by using the `schedule` event, which employs a cron-like syntax to specify when the workflow should run. The cron syntax in GitHub Actions follows the standard POSIX format, consisting of five fields: minute, hour, day of month, month, and day of week.

To run a workflow once every day, you can use a cron expression such as `0 0 * * *`, which translates to "every day at 00:00 UTC." Here’s how it breaks down:
- **Minute (0)**: 0 minutes past the hour
- **Hour (0)**: 00:00 (midnight) UTC
- **Day of month (*)**: Every day of the month
- **Month (*)**: Every month
- **Day of week (*)**: Every day of the week

### Example Configuration
Below is a sample GitHub Actions workflow configuration that runs once daily:

```yaml
name: Daily Workflow
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  example-job:
    runs-on: ubuntu-latest
    steps:
      - name: Print message
        run: echo "This runs once a day!"
```

This workflow will execute at midnight UTC every day.

### Key Considerations
- **Time Zone**: The schedule operates in UTC, so adjust the cron expression if you need it to run at a specific time in your local time zone.
- **Default Branch**: By default, scheduled workflows run on the repository’s default branch (e.g., `main` or `master`) unless otherwise specified.
- **Reliability**: While GitHub Actions aims to run workflows at the specified time, slight delays may occur due to infrastructure load, though this is rare.
- **Usage Limits**: For free GitHub accounts, there are limits on Actions usage (e.g., minutes per month), but a single daily run is typically well within these constraints.

### Conclusion
With a properly configured cron expression in the workflow file, GitHub Actions can indeed execute a workflow once every day. Thus, the answer to your query is **yes**.
