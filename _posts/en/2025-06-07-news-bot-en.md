---
audio: false
generated: false
image: false
lang: en
layout: post
title: Automated News Summarization Bot
translated: false
type: post
---

This post showcases a Python-based news bot that scrapes and summarizes top stories from Hacker News, GitHub Trending, and NYTimes (Chinese) using the Mistral API. It sends concise daily reports via Telegram, with a GitHub Actions workflow for automated execution. Ideal for staying updated on tech and global news effortlessly. Below is an example of a daily news summary.

---

Daily News Summary - 2025-06-07

Hacker News
-----------
1. The webpage indicates that Facebook is incompatible with the current browser and suggests updating to a supported browser to continue using the service.

2. Hate radio in Rwanda incited genocide by using coded language to urge listeners to kill Tutsis.

3. Railway is introducing Railpack to replace Nixpacks, aiming to address scalability and dependency management issues that hindered 200k users, enabling a smoother transition to support 100M users.

4. The article delves into the legacy of Radiant AI, a controversial and ambitious AI system promised for "The Elder Scrolls IV: Oblivion" that was largely cut from the final game.

5. The Washington Post advises users to enhance privacy by stopping the use of Chrome and deleting Meta's apps.


GitHub Trending
---------------
1. Cognee enables the creation of dynamic memory for AI agents using scalable, modular ECL pipelines in just five lines of code.

2. NetBird simplifies secure, private networking by combining a peer-to-peer WireGuard-based overlay network with centralized, granular access controls.

3. NoteGen is an AI-powered, cross-platform Markdown note-taking app that integrates recording and writing to organize fragmented knowledge into coherent notes.

4. Scrapy is a fast, high-level web crawling and scraping framework for Python, designed to extract structured data from websites.

5. React Bits offers a free, open-source collection of animated, interactive, and customizable React components to enhance web interfaces.


NYTimes (Chinese)
-----------------
1. After a phone call between Chinese President Xi Jinping and U.S. President Trump, both countries agreed to further trade negotiations to ease tensions over tariffs and rare earth supply.

2. The recent controversies in China highlight widespread public frustration over perceived social inequality and the belief that connections, rather than merit, often determine success.

3. China's intensified crackdown on rare earth metal smuggling is causing severe supply disruptions for global industries, as Beijing tightens controls to leverage these critical resources as a strategic tool.

4. The escalating conflict between Trump and Musk could have significant repercussions, with both figures leveraging their influence and resources to counter each other.

5. China's temporary halt on exporting seven rare earth metals and their magnets has caused severe shortages, potentially leading to factory closures in the U.S. and Europe.

---

```python
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import datetime
import sys
import re
import time

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "610574272")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

TELEGRAM_MAX_LENGTH = 4096

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_API_KEY or TELEGRAM_CHAT_ID not set.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    url_pattern = re.compile(r'(https?://[^\s]+)')
    # Remove all asterisks (for bold/italic) from the message
    message_no_stars = message.replace('*', '')
    # Remove links from the message
    message_no_links = url_pattern.sub('', message_no_stars)
    messages = []
    msg = message_no_links
    while len(msg) > TELEGRAM_MAX_LENGTH:
        split_idx = msg.rfind('\n', 0, TELEGRAM_MAX_LENGTH)
        if split_idx == -1 or split_idx < TELEGRAM_MAX_LENGTH // 2:
            split_idx = TELEGRAM_MAX_LENGTH
        messages.append(msg[:split_idx])
        msg = msg[split_idx:]
    messages.append(msg)
    success = True
    for part in messages:
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": part,
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            print(f"Successfully sent Telegram message part ({len(part)} chars).")
        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            success = False
    return success

def fetch_html_content(url):
    try:
        print(f"Fetching HTML content from: {url}")
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status()
        print(f"Successfully fetched HTML content from: {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch URL: {url} - {e}")
        return None

def extract_hacker_news_links(html, max_links=5):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    seen = set()
    for item in soup.select('.titleline > a'):
        url = item['href']
        title = item.text.strip()
        if url.startswith('item?id='):
            url = f"https://news.ycombinator.com/{url}"
        if url not in seen and title:
            links.append({'url': url, 'text': title})
            seen.add(url)
        if len(links) >= max_links:
            break
    print(f"Extracted {len(links)} links from Hacker News.")
    return links

def extract_github_trending(html, max_links=5):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for repo in soup.select('article.Box-row h2 a'):
        url = f"https://github.com{repo['href']}"
        title = re.sub(r'\s+', ' ', repo.text).strip()
        if title and url:
            links.append({'url': url, 'text': title})
        if len(links) >= max_links:
            break
    print(f"Extracted {len(links)} trending repositories from GitHub.")
    return links

def call_mistral_api(prompt, model="mistral-small-latest"):
    api_key = MISTRAL_API_KEY
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        return None

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        print(f"Calling Mistral API with model: {model}")
        print(f"Prompt being sent: {prompt[:1000]}...")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        print(f"Mistral API Response: {response_json}")
        if response_json and response_json.get('choices'):
            content = response_json['choices'][0]['message']['content']
            print(f"Mistral API Content: {content}")
            return content
        else:
            print(f"Mistral API Error: Invalid response format: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None

def fetch_and_summarize(url, fallback_title=None):
    print(f"Summarizing: {url}")
    html = fetch_html_content(url)
    if not html:
        return {"url": url, "summary": "Could not fetch content.", "title": fallback_title or url}
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.text.strip() if soup.title else (fallback_title or url)
    paragraphs = soup.find_all('p')
    text_content = "\n".join(p.get_text() for p in paragraphs)
    if not text_content or len(text_content) < 100:
        text_content = soup.get_text(separator="\n")
    text_content = text_content.strip()
    if len(text_content) > 3000:
        text_content = text_content[:3000]
    summary = ai_summarize(text_content, url, title)
    return {"url": url, "summary": summary, "title": title}

def limit_to_n_words(text, n):
    words = text.strip().split()
    if len(words) <= n:
        return text.strip()
    return ' '.join(words[:n]) + "..."

def ai_summarize(text, url=None, title=None):
    if not MISTRAL_API_KEY:
        print("No MISTRAL_API_KEY set. Returning first 15 words as summary.")
        return limit_to_n_words(text, 15)
    prompt = (
        "If the original text is in Chinese, summarize it in English. "
        "Summarize the following web page content in clear, concise English. "
        "Focus on the single most important point or insight. "
        "Your summary should be around 300 characters. "
        "Output only the summary sentence:\n"
        f"Title: {title if title else ''}\n"
        f"{text}\n"
        f"{'Original link: ' + url if url else ''}"
    )
    summary = call_mistral_api(prompt)
    if summary is None:
        return limit_to_n_words(text, 15)
    # Truncate to 300 chars as a last resort
    return summary.strip()[:300]

def generate_summarized_report(summaries, source_name):
    text = f"{source_name}\n"
    text += "-" * len(source_name) + "\n"
    if not summaries:
        text += "No items found.\n\n"
        return text
    url_pattern = re.compile(r'(https?://[^\s]+)')
    for idx, item in enumerate(summaries, 1):
        summary = item.get('summary', '').replace('\n', ' ').replace('\r', ' ').strip()
        summary = summary.replace('*', '')
        summary = url_pattern.sub('', summary)
        # Truncate each summary to 300 chars as a last resort
        summary = summary[:300]
        text += f"{idx}. {summary}\n\n"  # Add an extra newline between summaries
    text += "\n"
    return text

# --- NYTimes (m.cn.nytimes.com) integration ---

def extract_nytimes_links(html, max_links=5):
    """
    Extracts links from the main page of cn.nytimes.com.
    Only includes links that start with 'https://cn.nytimes.com/'.
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        url = a['href']
        if url.startswith('https://cn.nytimes.com/'):
            links.append({
                'url': url,
                'text': a.text.strip()
            })
        if len(links) >= max_links:
            break
    print(f"Extracted {len(links)} links from main page.")
    return links

def summarize_nytimes_article(url):
    html = fetch_html_content(url)
    if not html:
        return {"url": url, "summary": "Could not fetch content.", "title": url}
    soup = BeautifulSoup(html, 'html.parser')
    # Try to extract the main article title
    title_element = soup.select_one('.article-area .article-content .article-header header h1')
    title = title_element.text.strip() if title_element else (soup.title.text.strip() if soup.title else url)
    # Extract the main article text
    article_area = soup.find('section', class_='article-body')
    if article_area:
        article_text = article_area.get_text(separator='\n', strip=True)
    else:
        article_text = soup.get_text(separator='\n', strip=True)
    if not article_text or len(article_text) < 100:
        article_text = soup.get_text(separator='\n', strip=True)
    if len(article_text) > 3000:
        article_text = article_text[:3000]
    summary = ai_summarize(article_text, url, title)
    return {"url": url, "summary": summary, "title": title}

def main():
    # Check for --test argument
    is_test = "--test" in sys.argv

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    report = f"Daily News Summary - {today}\n\n"

    if is_test:
        # Only scrape one link and send one summary (NYTimes Chinese)
        ny_html = fetch_html_content('https://m.cn.nytimes.com')
        ny_links = []
        ny_summaries = []
        if ny_html:
            ny_links = extract_nytimes_links(ny_html, max_links=1)
            if ny_links:
                link = ny_links[0]
                summary = summarize_nytimes_article(link['url'])
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
        hn_html = fetch_html_content('https://news.ycombinator.com')
        hn_links = []
        hn_summaries = []
        if hn_html:
            hn_links = extract_hacker_news_links(hn_html)
            for link in hn_links:
                summary = fetch_and_summarize(link['url'], fallback_title=link['text'])
                hn_summaries.append(summary)
                time.sleep(2)
        report += generate_summarized_report(hn_summaries, "Hacker News")

        # --- GitHub Trending ---
        gh_html = fetch_html_content('https://github.com/trending')
        gh_links = []
        gh_summaries = []
        if gh_html:
            gh_links = extract_github_trending(gh_html)
            for link in gh_links:
                summary = fetch_and_summarize(link['url'], fallback_title=link['text'])
                gh_summaries.append(summary)
                time.sleep(2)
        report += generate_summarized_report(gh_summaries, "GitHub Trending")

        # --- NYTimes (cn.nytimes.com) ---
        ny_html = fetch_html_content('https://m.cn.nytimes.com')
        ny_links = []
        ny_summaries = []
        if ny_html:
            ny_links = extract_nytimes_links(ny_html, max_links=5)
            for link in ny_links:
                summary = summarize_nytimes_article(link['url'])
                ny_summaries.append(summary)
                time.sleep(2)
        report += generate_summarized_report(ny_summaries, "NYTimes (Chinese)")

        if any([hn_summaries, gh_summaries, ny_summaries]):
            if len(report) > TELEGRAM_MAX_LENGTH:
                print(f"Report exceeds {TELEGRAM_MAX_LENGTH} chars, will be split into multiple messages.")
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
```

```yml
name: News Bot

on:
  schedule:
    # Runs every day at 9 AM Beijing time (1 AM UTC).
    - cron: '0 1 * * *'
  workflow_dispatch:  # Allows manual triggering
  push:
    # Only trigger if BOTH files change in the same commit/push
    # This requires a filter job below to check for both files
    paths:
      - scripts/nytimes/news_bot.py
      - .github/workflows/news.yml

concurrency:
  group: 'news'
  cancel-in-progress: false

jobs:
  send-news:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_BOT_API_KEY: ${{ secrets.TELEGRAM_BOT_API_KEY }}
      MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}    

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: Set up Python 3.10.x
        uses: actions/setup-python@v4
        with:
          python-version: "3.10.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.simple.txt

      - name: Run news bot script
        run: python scripts/nytimes/news_bot.py
              
```