---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Scheduling Daily Jobs in BMC Control-M
translated: false
type: note
---

In BMC Control-M, to make a job run every day at exactly 1:00 AM, you have several options. The most common and recommended ways are:

### Method 1: Use a Simple Cyclic Job with “Run every 1 Days” + Specific Time (Easiest & Most Common)

1. Open your job definition in Control-M Desktop or Control-M Web (Planning domain).
2. Go to the Scheduling tab.
3. In the Basic Scheduling section:
   - Set Calendar = your regular calendar (or leave as Regular if no special days).
   - Set Schedule = Every Day (or select the days you want, usually all 7 days).
4. In the When section (or Time Settings):
   - From: 01:00
   - To: (leave blank or set a wide window, e.g., 23:59)
   - Time Zone: choose the appropriate one (usually server or site time zone)
5. Go to the Cyclic tab:
   - Check Run as Cyclic job
   - Select “Run every” → 1 Days
   - Optionally check “Rerun every” if you want retries, but usually not needed for once-a-day jobs.
6. Save and order/force the folder or job.

→ This will order the job every day at 01:00 AM exactly.

### Method 2: Use “Specific Times” (Very Precise)

In the Scheduling tab → When section:

- Instead of From/To, click Add → Specific Times
- Add 01:00
- You can add multiple times if needed, but for once a day just put 01:00
- Schedule = every day (or the days you select)

This is the cleanest way if you only want the job to run once per day at exactly 1 AM.

### Method 3: Using Control-M Calendar + Rule-Based Calendar (RBC)

If you want more control (e.g., only business days at 1 AM):

1. Create or use a Rule-Based Calendar.
2. Add a rule: Daily at 01:00.
3. In the job, reference that calendar and use “Specific Times” or “At calendar time”.

### Method 4: Using Control-M Automation API or CCM (for many jobs)

If you have hundreds of jobs, you can define it in JSON/DEF file like this:

```json
{
  "MyDailyJob": {
    "Type": "Job:Command",
    "Command": "echo Hello",
    "When": {
      "RuleBasedCalendars": [{"Name": "Daily"}],
      "Time": "01:00"
    }
  }
}
```

### Summary – Recommended for “run every day at 1 AM”

Best practice in most environments:

- Scheduling tab → Schedule → every day you need
- When → Specific Times → 01:00
(or From 01:00 with cyclic every 1 day if you prefer that style)

That’s it — the job will be ordered automatically every day at 1:00 AM server time (or the time zone you selected).

Let me know which Control-M version you are on (9.0.20+, 9.0.21+, Control-M/EM 9.0.00, etc.) if you need screenshots or exact field names, because the interface changed a bit between versions.
