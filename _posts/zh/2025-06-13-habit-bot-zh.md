---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 用Mistral打造习惯养成机器人
translated: true
type: post
---

在这篇博客中，我们将探讨如何利用Python和GitHub Actions创建一个习惯养成机器人，用于发送自动化提醒。该机器人通过Telegram API实现消息推送，并集成Mistral AI生成情境相关的提示内容。借助GitHub Actions的任务调度功能，机器人能通过定时通知帮助用户培养持之以恒的习惯。我们将从环境配置开始，逐步介绍脚本编写到部署的全过程，为您提供一套自动化习惯追踪系统的实用指南。

## 代码

```python
import os
import requests
import argparse
import re
import datetime
from dotenv import load_dotenv
import random

# 从.env文件加载环境变量
load_dotenv()

# 环境变量
TELEGRAM_HABIT_BOT_API_KEY = os.environ.get("TELEGRAM_HABIT_BOT_API_KEY")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

# Telegram消息长度限制
TELEGRAM_MAX_LENGTH = 4096

def send_telegram_message(bot_token, chat_id, message):
    """通过Telegram Bot API向指定聊天发送消息"""
    if not bot_token or not chat_id:
        print("错误：未设置TELEGRAM_HABIT_BOT_API_KEY或TELEGRAM_CHAT_ID")
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # 移除Markdown星号和URL确保Telegram兼容性
    message_no_stars = message.replace('*', '')
    url_pattern = re.compile(r'(https?://[^\s]+)')
    message_no_links = url_pattern.sub('', message_no_stars)
    # 当消息超过Telegram长度限制时进行分割
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
            "chat_id": chat_id,
            "text": part,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            print(f"成功发送Telegram消息片段（{len(part)}字符）")
        except requests.exceptions.RequestException as e:
            print(f"发送Telegram消息出错：{e}")
            success = False
    return success


def call_mistral_api(prompt, model="mistral-large-latest"):
    """调用Mistral API生成响应"""
    if not MISTRAL_API_KEY:
        print("错误：未设置MISTRAL_API_KEY环境变量")
        return None
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,  # 调整创造性参数
        "max_tokens": 300  # 限制响应长度
    }
    try:
        print(f"调用Mistral API，模型：{model}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('choices'):
            content = response_json['choices'][0]['message']['content']
            print(f"Mistral API返回内容：{content}")
            return content
        print(f"Mistral API错误：{e}")
        return None

def generate_copilot_message():
    """通过Mistral API生成鼓励使用Copilot的技术提示语句"""
    prompt = (
        f"为后端工程师生成一个独特、具体的技术提示语句"
        "随机选择以下技术之一：Java、Spring Boot、Control-M、IBM WebSphere、Maven、多线程、Nexus、Windows、JVM、Service-NOW、Python、AI或DevOps、Linux、算法和银行系统"
        "格式为'遇到[具体挑战]？试试Copilot！'或'正在处理[任务]？让Copilot帮你！'"
        "确保挑战类型多样（如配置、调试、优化等）"
        "保持300字符以内，避免Markdown或URL，仅输出语句"
    )
    message = call_mistral_api(prompt)
    if message:
        return message.strip()[:300]
    return "遇到Control-M订单日期配置问题？试试Copilot！"

def main():
    parser = argparse.ArgumentParser(description="Telegram习惯提醒机器人")
    parser.add_argument("--job", choices=["send_reminder", "send_message"], required=True, help="执行任务类型")
    parser.add_argument("--message", type=str, help="'send_message'任务的消息内容")
    args = parser.parse_args()

    if args.job == "send_reminder":
        if TELEGRAM_HABIT_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = generate_copilot_message()
            send_telegram_message(TELEGRAM_HABIT_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
        else:
            print("错误：未设置TELEGRAM_HABIT_BOT_API_KEY或TELEGRAM_CHAT_ID")
    elif args.job == "send_message":
        if TELEGRAM_HABIT_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = args.message if args.message else "机器人发送的默认测试消息！"
            send_telegram_message(TELEGRAM_HABIT_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
        else:
            print("错误：未设置TELEGRAM_HABIT_BOT_API_KEY或TELEGRAM_CHAT_ID")

if __name__ == "__main__":
    main()
```

## GitHub Action

{% raw %}
```yaml
name: 习惯养成

on:
  schedule:
    # 每周一至周五UTC时间05:00–13:00（北京时间13:00–21:00）每10分钟运行一次
    - cron: '0,10,20,30,40,50 5-13 * * 1-5'

  workflow_dispatch:
    # 允许手动触发测试
    inputs:
      message:
        description: '测试用自定义消息（可选）'
        required: false
        default: '来自GitHub Actions的测试消息'
      job:
        description: '运行任务（可选）'
        required: false
        default: 'send_message'

  push:
    branches: ["main"]
    paths:
      - 'scripts/bot/habit_bot.py'
      - '.github/workflows/habit_reminder.yml'

concurrency:
  group: 'habit_reminder'
  cancel-in-progress: false

jobs:
  习惯提醒任务:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_HABIT_BOT_API_KEY: ${{ secrets.TELEGRAM_HABIT_BOT_API_KEY }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}

    steps:
      - name: 检出仓库
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: 设置Python 3.13环境
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 运行习惯提醒脚本（定时触发）
        run: python scripts/bot/habit_bot.py --job send_reminder
        if: github.event_name == 'schedule'

      - name: 运行习惯提醒脚本（手动触发）
        run: python scripts/bot/habit_bot.py --job ${{ github.event.inputs.job }} --message "${{ github.event.inputs.message }}"
        if: github.event_name == 'workflow_dispatch'

      - name: 主分支推送通知
        run: python scripts/bot/habit_bot.py --job send_message --message "习惯机器人代码已推送至主分支"
        if: github.event_name == 'push'
```
{% endraw %}