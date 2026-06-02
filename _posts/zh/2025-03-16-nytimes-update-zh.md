---
audio: true
generated: false
image: false
lang: zh
layout: post
title: NYTimes新闻（CN）文章更新触发器
translated: true
type: post
---

点击下方按钮以更新 [NYTimes CN 文章](./notes/2025-03-14-nytimes-en)。

<script async src="../assets/js/nytimes.js"></script>

<div class="nytimes" ></div>

此页面允许您触发更新 NYTimes CN 文章。点击按钮将启动一个工作流，获取最新文章，翻译它们，并更新本站内容。请注意，更新触发后可能需要几分钟才能看到变更。

Python 代码：

```python
import requests
from bs4 import BeautifulSoup
import os
import ssl
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def call_mistral_api(prompt, model="mistral-small-2501"):
    """调用 Mistral API 翻译文本。"""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("错误：MISTRAL_API_KEY 环境变量未设置。")
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
        print(f"使用模型调用 Mistral API: {model}")
        print(f"发送的提示: {prompt[:1000]}...")  # 打印提示的前 1000 个字符
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        print(f"Mistral API 响应: {response_json}")
        if response_json and response_json['choices']:
            content = response_json['choices'][0]['message']['content']
            print(f"Mistral API 内容: {content}")
            return content
        else:
            print(f"Mistral API 错误: 无效响应格式: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API 错误: {e}")
        if e.response:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return None

def fetch_html_content(url):
    """获取给定 URL 的 HTML 内容。"""
    try:
        # 创建未验证的 SSL 上下文
        context = ssl._create_unverified_context()
        print(f"从 {url} 获取 HTML 内容")
        response = requests.get(url, verify=False)
        response.raise_for_status()  # 对于错误响应（4xx 或 5xx）引发 HTTPError
        print(f"成功从 {url} 获取 HTML 内容")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"无法获取 URL: {url} - {e}")
        return None

def extract_links(html):
    """从 cn.nytimes.com 主页提取链接。"""
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        url = a['href']
        if url.startswith('https://cn.nytimes.com/'):
            links.append({
                'url': url,
                'text': a.text.strip()
            })
    print(f"从主页提取了 {len(links)} 个链接。")
    return links

def translate_title(title):
    """使用 Mistral 将标题从中文翻译成英文"""
    base_prompt = "将以下标题翻译成 {target_language}。仅提供翻译后的标题，不附加任何说明或解释。不要重复或提及输入文本。\n"
    prompt = base_prompt.format(target_language="English") + f"{title}"
    print(f"翻译标题: {title}")
    translated_title = call_mistral_api(prompt)
    if translated_title:
        translated_title = translated_title.strip()
        print(f"翻译后的标题: {translated_title}")
        return translated_title
    else:
        raise Exception(f"翻译标题失败: {title}")

def summarize_article(html):
    """使用 Mistral API 总结文章内容，以英文输出。"""
    soup = BeautifulSoup(html, 'html.parser')
    title_element = soup.select_one('.article-area .article-content .article-header header h1')
    title = title_element.text.strip() if title_element else ''
    print(f"提取的标题: {title}")

    # 提取主文章文本
    article_area = soup.find('div', class_='article-area')
    if article_area:
        article_text = article_area.get_text(separator='\n', strip=True)
    else:
        article_text = None

    if not article_text:
        print("无法提取文章文本。")
        return None, None

    # 为 Mistral 创建总结提示
    prompt = f"总结以下文章，重点突出主要观点，避免使用类似 'Summary:' 或 'This article is about:' 的引言。\n\n{article_text[:30000]}\n\n"  # 将文章文本限制为 30000 个字符
    print(f"为标题创建总结: {title}")
    summary = call_mistral_api(prompt)

    if summary:
        # 清理总结，移除前导的 "Summary:" 或类似短语
        summary = summary.replace("Summary:", "").strip()
        print(f"生成的总结: {summary}")
        return title, summary
    else:
        print(f"为标题生成总结失败: {title}")
        return None, None

def generate_markdown_list(articles):
    """从文章总结列表生成 Markdown 列表。"""
    if not articles:
        return '* 未找到文章。\n'

    markdown_list = ''
    for article in articles:
        title, summary = article
        translated_title = translate_title(title)
        markdown_list += f'## {translated_title}\n\n{summary}\n\n'
    print("生成 Markdown 列表。")
    return markdown_list

def update_markdown_file(filename, markdown_content):
    """使用给定内容更新 Markdown 文件。"""
    try:
        # 读取文件的现有内容
        print(f"从 {filename} 读取现有内容")
        with open(filename, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        # 查找初始元数据后内容的起始和结束位置
        start_index = existing_content.find('---', 3) + 4  # 查找第二个 '---' 并移动到其后面
        end_index = len(existing_content)

        # 构建更新后的内容
        updated_content = existing_content[:start_index].strip() + '\n\n'  # 保留元数据并添加换行符
        updated_content += markdown_content.strip() + '\n'  # 添加新的 Markdown 列表
        # updated_content += existing_content[end_index:].strip() # 如果存在，追加列表后的任何内容

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"成功更新 {filename}")
        markdown_changed = existing_content != updated_content
        print(f"Markdown 已更改: {markdown_changed}")
        return markdown_changed
    except Exception as e:
        print(f"更新 {filename} 时出错: {e}")
        return False

def main():
    """主函数，用于获取、处理和更新 Markdown 文件。"""
    nytimes_url = 'https://m.cn.nytimes.com'
    print(f'从 {nytimes_url} 获取 NYTimes 链接')

    html_content = fetch_html_content(nytimes_url)
    if not html_content:
        print("获取主页内容失败。")
        return

    links = extract_links(html_content)
    print(f'在主页上找到 {len(links)} 个链接。正在提取链接...')

    all_articles = []
    for i, link in enumerate(links):
        url = link["url"]
        if not url.endswith('/dual/'):
            if not url.endswith('/'):
                url = url + '/dual/'
            else:
                url = url + 'dual/'

        print(f'处理链接 {i + 1} 共 {len(links)} 个: {url}')
        article_html = fetch_html_content(url)
        if article_html:
            title, summary = summarize_article(article_html)
            if title and summary:
                all_articles.append((title, summary))
        else:
            print(f'无法从 {link["url"]} 获取内容')

    markdown_list = generate_markdown_list(all_articles)

    filename = 'original/2025-03-14-nytimes-en.md'
    markdown_changed = update_markdown_file(filename, markdown_list)

    if markdown_changed:
        print("Markdown 文件已更新为新链接。")
        sys.exit(0)
    else:
        print("Markdown 文件未更新（无变更）。")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

前端代码：

```javascript
const nytimesDiv = document.querySelector('.nytimes');

if (nytimesDiv) {
    const updateButton = document.createElement('button');
    updateButton.textContent = '更新 NYTimes 文章';
    nytimesDiv.appendChild(updateButton);

    updateButton.addEventListener('click', () => {
        fetch('https://api.github.com/repos/lzwjava/lzwjava.github.io/actions/workflows/nytimes.yml/dispatches', {
            method: 'POST',
            headers: {
                'Accept': 'application/vnd.github+json',
                'Authorization': 'Bearer token',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ref: 'main' })
        })
        .then(response => {
            if (response.status === 204) {
                alert('更新已成功触发！请等待几分钟查看结果。');
            } else {
                alert(`更新失败。状态码: ${response.status}`);
                console.error('更新失败:', response);
            }
        })
        .catch(error => {
            alert('更新失败。请检查控制台以获取错误。');
            console.error('触发更新时出错:', error);
        });
    });
} else {
    console.error("未找到 nytimes div!");
}
```
