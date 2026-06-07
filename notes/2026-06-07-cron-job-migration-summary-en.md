---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cron Job Migration Summary
translated: false
type: note
---

Comprehensive Summary:

  WHAT WE DID
  ───────────
  1. Created a Hermes cron job to run `ww appearance smart-auto` every 2 minutes
  2. Updated `weekly-repo-update` schedule from "every Sunday 9AM" to "every hour"
  3. Migrated both jobs from Hermes internal scheduler to macOS system crontab
  4. Analyzed privacy implications of webcam-based smart-auto

  CURRENT SYSTEM CRONTAB
  ──────────────────────
  */2 * * * * /opt/homebrew/bin/ww appearance smart-auto
  0 * * * * /opt/homebrew/bin/ww projects update

  HOW `ww appearance smart-auto` WORKS
  ─────────────────────────────────────
  Source: /Users/lzwjava/projects/ww/ww/display/appearance.py (lines 96-181)

  Step 1 — Capture: Uses `imagesnap` (preferred) or `ffmpeg` to grab one
           frame from webcam at 640x480 resolution
  Step 2 — Convert: Opens image with PIL, converts to grayscale ("L" mode)
  Step 3 — Analyze: Calculates average pixel brightness via numpy (0-255 scale)
  Step 4 — Decide:  brightness < 80 (threshold) → dark mode
                    brightness >= 80 → light mode
  Step 5 — Cleanup: Deletes temp JPEG in `finally` block (always runs)

  PRIVACY ANALYSIS
  ────────────────
  ✓ 100% local processing — no network calls, no API keys, no LLM
  ✓ Image deleted immediately after brightness calculation
  ✓ No data leaves the machine
  ✓ Webcam LED blinks during capture (visual indicator)
  ⚠ Every 2 minutes is frequent — green light will flicker often
  ⚠ If `imagesnap`/`ffmpeg` missing, command fails with error

  WHAT `ww projects update` DOES
  ──────────────────────────────
  Pulls latest changes for 60 configured open source repos in ~/projects/

  HERMES vs SYSTEM CRON
  ─────────────────────
  - Hermes cron: internal scheduler, stored in ~/.hermes/, managed via agent
  - System cron: macOS crond, managed via `crontab -l` / `crontab -e`
  - Both are independent — Hermes jobs don't appear in system crontab
  - We moved to system cron for transparency and direct CLI access

  VERIFY / MANAGE
  ───────────────
  Check:    crontab -l
  Edit:     crontab -e
  Remove:   crontab -r (removes all)
