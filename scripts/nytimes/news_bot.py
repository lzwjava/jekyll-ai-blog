import datetime
import sys
import time
from news_bot_utils import (
    send_telegram_message,
    fetch_html_content,
    extract_hacker_news_links,
    extract_github_trending,
    fetch_and_summarize,
    generate_summarized_report,
    extract_nytimes_links,
    summarize_nytimes_article,
    TELEGRAM_MAX_LENGTH,
)


def main():
    # Check for --test argument
    is_test = "--test" in sys.argv

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    report = f"Daily News Summary - {today}\n\n"

    if is_test:
        # Only scrape one link and send one summary (NYTimes Chinese)
        ny_html = fetch_html_content("https://m.cn.nytimes.com")
        ny_links = []
        ny_summaries = []
        if ny_html:
            ny_links = extract_nytimes_links(ny_html, max_links=1)
            if ny_links:
                link = ny_links[0]
                summary = summarize_nytimes_article(link["url"])
                ny_summaries.append(summary)
        report = generate_summarized_report(ny_summaries, "NYTimes (Chinese)")
        if ny_summaries:
            if send_telegram_message(report):
                print("Test summary sent to Telegram successfully.")
                sys.exit(0)
            else:
                print("Failed to send test summary to Telegram.")
                sys.exit(1)
        else:
            print("No news collected, nothing sent to Telegram.")
            sys.exit(1)
    else:
        # --- Hacker News ---
        hn_html = fetch_html_content("https://news.ycombinator.com")
        hn_links = []
        hn_summaries = []
        if hn_html:
            hn_links = extract_hacker_news_links(hn_html)
            for link in hn_links:
                summary = fetch_and_summarize(link["url"], fallback_title=link["text"])
                hn_summaries.append(summary)
                time.sleep(2)
        report += generate_summarized_report(hn_summaries, "Hacker News")

        # --- GitHub Trending ---
        gh_html = fetch_html_content("https://github.com/trending")
        gh_links = []
        gh_summaries = []
        if gh_html:
            gh_links = extract_github_trending(gh_html)
            for link in gh_links:
                summary = fetch_and_summarize(link["url"], fallback_title=link["text"])
                gh_summaries.append(summary)
                time.sleep(2)
        report += generate_summarized_report(gh_summaries, "GitHub Trending")

        # --- NYTimes (cn.nytimes.com) ---
        ny_html = fetch_html_content("https://m.cn.nytimes.com")
        ny_links = []
        ny_summaries = []
        if ny_html:
            ny_links = extract_nytimes_links(ny_html, max_links=5)
            for link in ny_links:
                summary = summarize_nytimes_article(link["url"])
                ny_summaries.append(summary)
                time.sleep(2)
        report += generate_summarized_report(ny_summaries, "NYTimes (Chinese)")

        if any([hn_summaries, gh_summaries, ny_summaries]):
            if len(report) > TELEGRAM_MAX_LENGTH:
                print(
                    f"Report exceeds {TELEGRAM_MAX_LENGTH} chars, will be split into multiple messages."
                )
            if send_telegram_message(report):
                print("Daily news report sent to Telegram successfully.")
                sys.exit(0)
            else:
                print("Failed to send daily news report to Telegram.")
                sys.exit(1)
        else:
            print("No news collected, nothing sent to Telegram.")
            sys.exit(1)


if __name__ == "__main__":
    main()
