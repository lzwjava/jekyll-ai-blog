---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 人工智能驱动的Git提交信息
translated: true
type: post
---

这个 Python 脚本应该放在系统 PATH 中的目录下，例如 `~/bin`。

```python
import subprocess
import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse
import requests

load_dotenv()

def call_mistral_api(prompt):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("错误: MISTRAL_API_KEY 环境变量未设置。")
        return None

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if response_json and response_json['choices']:
            return response_json['choices'][0]['message']['content']
        else:
            print(f"Mistral API 错误: 无效的响应格式: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API 错误: {e}")
        if e.response:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return None

def call_gemini_api(prompt):
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("错误: GEMINI_API_KEY 环境变量未设置。")
        return None
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    params = {"key": gemini_api_key}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()  # 对于错误状态码抛出异常
        response_json = response.json()
        if response_json and 'candidates' in response_json and response_json['candidates']:
            return response_json['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Gemini API 错误: 无效的响应格式: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Gemini API 错误: {e}")
        if e.response:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return None

def call_deepseek_api(prompt):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: DEEPSEEK_API_KEY 环境变量未设置。")
        return None

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        if response and response.choices:
            commit_message = response.choices[0].message.content.strip()
            commit_message = commit_message.replace('`', '')
            return commit_message
        else:
            print("错误: API 无响应。")
            return None
    except Exception as e:
        print(f"API 调用时出错: {e}")
        print(e)
        return None

def gitmessageai(push=True, only_message=False, api='deepseek'):
    # 暂存所有更改
    subprocess.run(["git", "add", "-A"], check=True)

    # 获取更改的简要摘要
    files_process = subprocess.run(["git", "diff", "--staged", "--name-only"], capture_output=True, text=True, check=True)
    changed_files = files_process.stdout

    if not changed_files:
        print("无更改提交。")
        return

    # 为 AI 准备提示
    prompt = f"""
生成简洁的提交消息，格式为 Conventional Commits，针对以下代码更改。
使用以下类型之一: feat, fix, docs, style, refactor, test, chore, perf, ci, build, 或 revert。
如适用，包含一个括号中的范围，描述受影响的代码库部分。
提交消息不应超过 70 个字符。

更改的文件:
{changed_files}

提交消息:
"""

    if api == 'deepseek':
        commit_message = call_deepseek_api(prompt)
        if not commit_message:
            return
    elif api == 'gemini':
        commit_message = call_gemini_api(prompt)
        if not commit_message:
            print("错误: Gemini API 无响应。")
            return
    elif api == 'mistral':
        commit_message = call_mistral_api(prompt)
        if not commit_message:
            print("错误: Mistral API 无响应。")
            return
    else:
        print(f"错误: 指定的 API 无效: {api}")
        return

    # 检查提交消息是否为空
    if not commit_message:
        print("错误: 生成的提交消息为空。中止提交。")
        return

    if only_message:
        print(f"建议的提交消息: {commit_message}")
        return

    # 使用生成的消息提交
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # 推送更改
    if push:
        subprocess.run(["git", "push"], check=True)
    else:
        print("更改已提交到本地，但未推送。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用 AI 生成提交消息并提交更改。")
    parser.add_argument('--no-push', dest='push', action='store_false', help='在本地提交更改而不推送。')
    parser.add_argument('--only-message', dest='only_message', action='store_true', help='仅打印 AI 生成的提交消息。')
    parser.add_argument('--api', type=str, default='deepseek', choices=['deepseek', 'gemini', 'mistral'], help='用于生成提交消息的 API (deepseek, gemini 或 mistral)。')
    args = parser.parse_args()
    gitmessageai(push=args.push, only_message=args.only_message, api=args.api)
```

可以使用不同的 API 调用此脚本。例如:

```bash
python ~/bin/gitmessageai.py
python ~/bin/gitmessageai.py --no-push
python ~/bin/gitmessageai.py --only-message
python ~/bin/gitmessageai.py --api gemini
python ~/bin/gitmessageai.py --api mistral --no-push
python ~/bin/gitmessageai.py --api deepseek --only-message
```

然后，在你的 `~/.zprofile` 文件中添加以下内容:

```bash
alias gpa='python ~/bin/gitmessageai.py'
alias gca='python ~/bin/gitmessageai.py --no-push'
alias gm='python ~/bin/gitmessageai.py --only-message'
```

有几个改进。

* 一个改进是只发送文件名更改，而不使用 `git diff` 读取文件的详细更改。我们不想给 AI 服务 API 提供太多细节。在这种情况下，我们不需要它，因为很少有人会仔细阅读提交消息。

* 有时 Deepseek API 会失败，因为最近它非常受欢迎。我们可能需要改用 Gemini。
