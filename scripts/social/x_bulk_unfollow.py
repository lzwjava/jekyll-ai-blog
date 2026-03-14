"""
Bulk unfollow script for X/Twitter using Playwright.

Usage:
    python x_bulk_unfollow.py --count 500
    python x_bulk_unfollow.py --count 500 --headless
    python x_bulk_unfollow.py --count 500 --delay 3

Prerequisites:
    pip install playwright
    playwright install chromium
"""

import argparse
import time
import random

from playwright.sync_api import sync_playwright


FOLLOWING_URL_TEMPLATE = "https://x.com/{username}/following"
DEFAULT_DELAY = 2  # seconds between unfollows
DEFAULT_SCROLL_PAUSE = 1.5


def login_manually(page):
    """Navigate to X and wait for user to log in manually."""
    page.goto("https://x.com/login")
    print("Please log in to your X account in the browser window.")
    print("Press Enter here once you are logged in and see your home feed...")
    input()


def get_username(page):
    """Extract the logged-in username from the page."""
    page.goto("https://x.com/home")
    page.wait_for_timeout(3000)
    # Click on profile link to get username from URL
    nav_link = page.locator('a[data-testid="AppTabBar_Profile_Link"]')
    href = nav_link.get_attribute("href")
    username = href.strip("/")
    print(f"Detected username: @{username}")
    return username


def scroll_and_collect_buttons(page, needed):
    """Scroll the following page and collect unfollow buttons."""
    buttons = page.locator('button[data-testid$="-unfollow"]')
    count = buttons.count()

    attempts = 0
    while count < needed and attempts < 30:
        page.evaluate("window.scrollBy(0, 800)")
        page.wait_for_timeout(int(DEFAULT_SCROLL_PAUSE * 1000))
        count = buttons.count()
        attempts += 1

    return buttons


def unfollow_batch(page, username, count, delay):
    """Unfollow `count` accounts from the following page."""
    page.goto(FOLLOWING_URL_TEMPLATE.format(username=username))
    page.wait_for_timeout(3000)

    unfollowed = 0

    while unfollowed < count:
        # Find all "Following" buttons (they have data-testid ending in -unfollow)
        buttons = page.locator('button[data-testid$="-unfollow"]')
        visible_count = buttons.count()

        if visible_count == 0:
            # Scroll to load more
            page.evaluate("window.scrollBy(0, 800)")
            page.wait_for_timeout(int(DEFAULT_SCROLL_PAUSE * 1000))
            buttons = page.locator('button[data-testid$="-unfollow"]')
            visible_count = buttons.count()
            if visible_count == 0:
                print("No more unfollow buttons found. Stopping.")
                break

        # Click the first available unfollow button
        try:
            buttons.first.click()
            page.wait_for_timeout(500)

            # Confirm the unfollow in the dialog
            confirm_button = page.locator(
                'button[data-testid="confirmationSheetConfirm"]'
            )
            if confirm_button.is_visible(timeout=3000):
                confirm_button.click()

            unfollowed += 1
            print(f"Unfollowed {unfollowed}/{count}")

            # Random delay to look more human
            jitter = random.uniform(0.5, 1.5)
            time.sleep(delay * jitter)

        except Exception as e:
            print(f"Error clicking unfollow button: {e}")
            # Scroll past the problematic entry
            page.evaluate("window.scrollBy(0, 200)")
            page.wait_for_timeout(1000)

        # Every 50 unfollows, take a longer break
        if unfollowed > 0 and unfollowed % 50 == 0:
            pause = random.uniform(15, 30)
            print(f"Pausing for {pause:.0f}s to avoid rate limits...")
            time.sleep(pause)

    return unfollowed


def main():
    parser = argparse.ArgumentParser(
        description="Bulk unfollow accounts on X/Twitter using Playwright."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=500,
        help="Number of accounts to unfollow (default: 500).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=f"Base delay in seconds between unfollows (default: {DEFAULT_DELAY}).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (not recommended for first run — you need to log in).",
    )
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        login_manually(page)
        username = get_username(page)

        print(f"\nStarting to unfollow {args.count} accounts...")
        print(f"Base delay: {args.delay}s between unfollows\n")

        total = unfollow_batch(page, username, args.count, args.delay)

        print(f"\nDone! Unfollowed {total} accounts.")
        browser.close()


if __name__ == "__main__":
    main()
