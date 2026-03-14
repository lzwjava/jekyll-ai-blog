"""
Bulk unfollow script for X/Twitter using Playwright + normal Chrome via CDP.
Uses LLM (via OpenRouter) to decide who to unfollow based on their profile.

Usage:
    1. Close all Chrome windows first
    2. python x_bulk_unfollow.py --count 500
    3. python x_bulk_unfollow.py --count 500 --delay 3 --dry-run

Prerequisites:
    pip install playwright python-dotenv
    export OPENROUTER_API_KEY=your_key

Note: Launches your real Chrome via remote debugging (no automation flags),
      then connects Playwright via CDP. This avoids bot detection.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import random
from datetime import datetime

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

# Add llm dir to path for openrouter_client
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "llm"))
from openrouter_client import call_openrouter_api_with_messages

FOLLOWING_URL_TEMPLATE = "https://x.com/{username}/following"
DEFAULT_DELAY = 2
DEFAULT_SCROLL_PAUSE = 1.5
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_PORT = 9222
REPORT_FILE = os.path.join(os.path.dirname(__file__), "unfollowed_report.json")

LLM_SYSTEM_PROMPT = """You are helping decide whether to unfollow someone on X/Twitter.
The user is a software engineer interested in AI, engineering, and tech.

Given a profile, decide: should the user UNFOLLOW this person?

Criteria to UNFOLLOW (higher priority first):
1. Bio is primarily in Chinese — likely unfollow
2. Not related to engineering, AI, tech, science, startups, or programming — likely unfollow
3. No professional title or job mentioned, looks like a casual/personal account — likely unfollow
4. Low-quality or spam-looking account — likely unfollow

Criteria to KEEP:
1. Related to AI, engineering, programming, tech, science, startups, VC
2. Has a clear professional title/role (engineer, researcher, founder, etc.)
3. Has Premium/verified status — slight bonus to keep
4. Well-known figure in tech or science

Respond with ONLY valid JSON (no markdown, no code fences):
{"decision": "unfollow" or "keep", "reason": "brief reason in 10 words or less"}"""


def launch_chrome():
    profile_dir = os.path.expanduser("~/.chrome-playwright-debug-profile")
    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    return proc


def login_manually(page):
    page.goto("https://x.com/login")
    print("Please log in to your X account in the browser window.")
    print("Press Enter here once you are logged in and see your home feed...")
    input()


def get_username(page):
    page.goto("https://x.com/home")
    page.wait_for_timeout(3000)
    nav_link = page.locator('a[data-testid="AppTabBar_Profile_Link"]')
    href = nav_link.get_attribute("href")
    username = href.strip("/")
    print(f"Detected username: @{username}")
    return username


def extract_profile_info(cell):
    """Extract profile info from a UserCell element."""
    info = {}

    # Username / handle
    try:
        link = cell.locator('a[role="link"]').first
        href = link.get_attribute("href") or ""
        info["handle"] = href.strip("/")
    except Exception:
        info["handle"] = "unknown"

    # Display name
    try:
        # The first link typically contains the display name
        name_el = cell.locator('a[role="link"] span').first
        info["name"] = name_el.inner_text()
    except Exception:
        info["name"] = ""

    # Bio - usually in a div after the name/handle section
    try:
        bio_el = cell.locator('[data-testid="UserDescription"]')
        if bio_el.count() > 0:
            info["bio"] = bio_el.first.inner_text()
        else:
            info["bio"] = ""
    except Exception:
        info["bio"] = ""

    # Premium / verified badge
    try:
        verified = cell.locator('[data-testid="icon-verified"]')
        info["premium"] = verified.count() > 0
    except Exception:
        info["premium"] = False

    return info


def ask_llm_should_unfollow(profile_info):
    """Ask LLM whether to unfollow this person."""
    profile_text = (
        f"Handle: @{profile_info.get('handle', 'unknown')}\n"
        f"Name: {profile_info.get('name', '')}\n"
        f"Bio: {profile_info.get('bio', '(empty)')}\n"
        f"Premium/Verified: {'Yes' if profile_info.get('premium') else 'No'}"
    )

    messages = [
        {"role": "system", "content": LLM_SYSTEM_PROMPT},
        {"role": "user", "content": profile_text},
    ]

    try:
        response = call_openrouter_api_with_messages(
            messages, model="gemini-flash", max_tokens=100
        )
        result = json.loads(response.strip())
        return result.get("decision", "keep"), result.get("reason", "")
    except Exception as e:
        print(f"  LLM error: {e}, defaulting to keep")
        return "keep", "llm_error"


def load_report():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            return json.load(f)
    return {"unfollowed": [], "kept": [], "run_date": ""}


def save_report(report):
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def unfollow_with_llm(page, username, count, delay, dry_run=False):
    """Scroll through following list, ask LLM for each, unfollow if recommended."""
    page.goto(FOLLOWING_URL_TEMPLATE.format(username=username))
    page.wait_for_timeout(3000)

    report = load_report()
    report["run_date"] = datetime.now().isoformat()
    unfollowed = 0
    evaluated = 0
    already_seen = set()

    while unfollowed < count:
        # Find user cells
        cells = page.locator('[data-testid="UserCell"]')
        cell_count = cells.count()

        if cell_count == 0:
            page.evaluate("window.scrollBy(0, 800)")
            page.wait_for_timeout(int(DEFAULT_SCROLL_PAUSE * 1000))
            cells = page.locator('[data-testid="UserCell"]')
            cell_count = cells.count()
            if cell_count == 0:
                print("No more user cells found. Stopping.")
                break

        processed_any = False

        for i in range(cell_count):
            if unfollowed >= count:
                break

            try:
                cell = cells.nth(i)
                if not cell.is_visible():
                    continue

                profile = extract_profile_info(cell)
                handle = profile.get("handle", "unknown")

                if handle in already_seen:
                    continue
                already_seen.add(handle)
                processed_any = True
                evaluated += 1

                # Ask LLM
                decision, reason = ask_llm_should_unfollow(profile)
                print(
                    f"[{evaluated}] @{handle} — {decision.upper()} — {reason}"
                    f" | bio: {profile.get('bio', '')[:60]}"
                )

                if decision == "unfollow":
                    entry = {
                        "handle": handle,
                        "name": profile.get("name", ""),
                        "bio": profile.get("bio", ""),
                        "premium": profile.get("premium", False),
                        "reason": reason,
                    }

                    if dry_run:
                        print(f"  [DRY RUN] Would unfollow @{handle}")
                        report["unfollowed"].append(entry)
                        unfollowed += 1
                        continue

                    # Click the unfollow button within this cell
                    unfollow_btn = cell.locator('button[data-testid$="-unfollow"]')
                    if unfollow_btn.count() > 0:
                        unfollow_btn.first.click()
                        page.wait_for_timeout(500)

                        confirm = page.locator(
                            'button[data-testid="confirmationSheetConfirm"]'
                        )
                        if confirm.is_visible(timeout=3000):
                            confirm.click()

                        report["unfollowed"].append(entry)
                        unfollowed += 1
                        print(f"  Unfollowed @{handle} ({unfollowed}/{count})")

                        jitter = random.uniform(0.5, 1.5)
                        time.sleep(delay * jitter)
                    else:
                        print(f"  No unfollow button found for @{handle}, skipping")
                else:
                    report["kept"].append({"handle": handle, "reason": reason})

            except Exception as e:
                print(f"  Error processing cell {i}: {e}")

            if unfollowed > 0 and unfollowed % 50 == 0:
                pause = random.uniform(15, 30)
                save_report(report)
                print(f"Pausing for {pause:.0f}s to avoid rate limits...")
                time.sleep(pause)

        # Scroll to load more
        if not processed_any or unfollowed < count:
            page.evaluate("window.scrollBy(0, 800)")
            page.wait_for_timeout(int(DEFAULT_SCROLL_PAUSE * 1000))

        save_report(report)

    save_report(report)
    return unfollowed, evaluated


def main():
    parser = argparse.ArgumentParser(
        description="Smart bulk unfollow on X/Twitter using LLM decisions."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=500,
        help="Target number of accounts to unfollow (default: 500).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=f"Base delay in seconds between unfollows (default: {DEFAULT_DELAY}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Evaluate profiles with LLM but don't actually unfollow.",
    )
    args = parser.parse_args()

    print("Launching Chrome with remote debugging...")
    print("(Close all other Chrome windows first!)\n")
    chrome_proc = launch_chrome()

    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
            context = browser.contexts[0]
            page = context.new_page()

            login_manually(page)
            username = get_username(page)

            mode = "DRY RUN" if args.dry_run else "LIVE"
            print(f"\n[{mode}] Starting smart unfollow (target: {args.count})...")
            print(f"Base delay: {args.delay}s | Report: {REPORT_FILE}\n")

            total, evaluated = unfollow_with_llm(
                page, username, args.count, args.delay, args.dry_run
            )

            print(f"\nDone! Evaluated {evaluated} profiles, unfollowed {total}.")
            print(f"Report saved to: {REPORT_FILE}")
            browser.close()
    finally:
        chrome_proc.terminate()


if __name__ == "__main__":
    main()
