---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Update Pipeline Breakdown
translated: false
type: note
---

Now I have a thorough understanding. Here's the full breakdown:

---

**How `hermes update` works -- it's more sophisticated than it looks.**

The entire flow lives in `hermes_cli/main.py`, primarily `_cmd_update_impl()` (line 7737). Here's the pipeline, step by step:

**1. Hangup Protection** (`_install_hangup_protection`, line 7317)

Before anything else, it installs SIGHUP=SIG_IGN and wraps stdout/stderr to mirror to `~/.hermes/logs/update.log`. This prevents SSH disconnects from killing a mid-update pip install, leaving the venv half-broken. SIGINT (Ctrl-C) and SIGTERM are intentionally left alone -- those are legitimate cancellations.

**2. Pre-update Backup** (`_run_pre_update_backup`, line 7590)

Gated on `updates.pre_update_backup` config (default off). Can be forced with `--backup` flag. Creates a full zip snapshot of HERMES_HOME. Off by default because large installs make the zip take minutes.

**3. Install Method Detection** (line 7760)

Three paths:
- **No .git directory** -> on Windows, falls back to ZIP download; on Linux/macOS, checks `detect_install_method()` -- if `pip`, routes to `_cmd_update_pip()` which does `uv pip install --upgrade hermes-agent` (or plain pip if uv isn't available)
- **.git exists** -> proceeds with git-based update

**4. Fork Detection** (`_is_fork`, line 6604)

Compares the `origin` remote URL against `OFFICIAL_REPO_URLS` (the NousResearch/hermes-agent repo). If it doesn't match, you're on a fork -- it prints a warning and enables upstream sync logic later.

**5. Git Update** (line 7811)

- `git fetch origin`
- Detect current branch; if not `main`, auto-stash local changes and checkout main
- `git rev-list HEAD..origin/main --count` to count new commits
- If 0 new commits: restore stash, switch back to original branch, print "Already up to date"
- **Pre-update snapshot**: calls `create_quick_snapshot(label="pre-update")` -- this is a lightweight state snapshot (state.db, config, pairing JSONs) stored in HERMES_HOME, recoverable via `/snapshot list` / `/snapshot restore <id>`. This is what produced the `20260516-010419-pre-update` line in your output.

**6. Git Pull** (line 7927)

- `git pull --ff-only origin main` -- clean fast-forward
- If ff-only fails (diverged history): `git reset --hard origin/main` -- nukes local divergence, since the stash already saved uncommitted work
- Restore stashed changes after pull, prompting the user if interactive

**7. Bytecode Cache Cleanup** (`_clear_bytecode_cache`, line 5647)

Recursively removes `__pycache__/` directories. Prevents ImportError when updated source references names that didn't exist in the old compiled .pyc files. This is the "Cleared 63 stale __pycache__ directories" you saw.

**8. Fork Upstream Sync** (`_sync_with_upstream_if_needed`, line 6699)

Only for forks. The clever bit:
- If no `upstream` remote exists, asks user to add it (one-time, remembers declination)
- Fetches upstream, compares `origin/main` vs `upstream/main`
- If origin has commits not on upstream: **skips** -- won't trample your fork's custom commits
- If origin is strictly behind: merges from upstream and force-pushes-with-lease to origin
- This is why you saw "Fork is up to date with upstream"

**9. Python Dependencies** (line 7994)

- Prefers `uv pip install -e .[all]` (if uv is available)
- Falls back to `python -m pip install -e .[all]`
- Has a special `_install_python_dependencies_with_optional_fallback` that tries `.[all]` first; if one optional extra breaks (e.g. a C dep that won't compile), it installs `.` (base) and then re-adds the remaining extras individually -- so one broken optional doesn't strip all optional capabilities
- Termux/Android gets a curated `termux-all` profile with prebuilt psutil compatibility

**10. Lazy Backend Refresh** (`_refresh_active_lazy_features`, line 7006)

Most optional backends (providers, platforms, etc.) are "lazy deps" -- installed on first use, not in pyproject.toml's `[all]`. The problem: `uv pip install -e .[all]` doesn't touch already-installed lazy deps, so if a lazy dep pin is bumped (CVE, bug fix), users keep the stale version forever. This step finds which lazy features the user has previously activated and reinstalls them under current pins. This is the "Refreshing 22 active lazy backend(s)... 14 refreshed" you saw.

**11. Node.js Dependencies** (`_update_node_dependencies`, line 7212)

Runs `npm install` in the TUI directory (`ui-tui/`) if `package.json` exists.

**12. Skills Sync** (line 8059)

Copies new bundled skills to `~/.hermes/skills/`, updates changed ones, but respects user modifications (won't overwrite a user-edited skill). Then syncs to all profiles.

**13. Config Migration** (line 8131)

Checks for missing env vars, new config fields, and config version bumps. Offers interactive migration (or auto-migration in non-interactive/gateway mode). This ensures new features that need config keys get them.

**14. Gateway Auto-Restart** (line 8275)

If running in gateway mode (`--gateway`), after the code update:
- Writes exit code 0 to `.update_exit_code` *before* attempting restart (so the new gateway sees success even if the process is killed during restart)
- Attempts graceful SIGUSR1 restart (lets in-flight messages drain for up to 60s)
- Falls back to `systemctl restart` for systemd-managed gateways
- Handles multi-profile setups, restarting all running gateway processes

**What makes it innovative:**

- **Self-healing git**: ff-only with hard-reset fallback + stash/restore means it never leaves you in a broken state
- **Fork awareness**: auto-detects forks, adds upstream remote, syncs without trampling custom commits
- **Lazy dep refresh**: tracks which optional backends the user actually uses and only upgrades those -- avoids both "stale CVE version forever" and "reinstall 100 unused packages every update"
- **Hangup-proof**: SIGHUP protection + output mirroring means SSH disconnects can't corrupt the update
- **Snapshot belt-and-suspenders**: quick snapshot before pull (lightweight, ~instant) + optional full zip backup before everything -- two recovery paths
- **Graceful gateway restart**: drain in-flight messages before restarting, with a watchdog that detects the new gateway coming up
- **Optional-fallback pip install**: if one optional extra breaks, the rest still get installed instead of all-or-nothing