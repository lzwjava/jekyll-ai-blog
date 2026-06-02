---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 通过Telegram简化提醒设置
translated: true
type: post
---

在这个项目中，我利用GitHub Actions和Telegram机器人搭建了一套自动化提醒系统，用于管理我的日常和月度任务。通过配置cron定时任务，我设置了工作相关事项的提醒，如企业微信打卡、提交工时表和查收工资，以及个人事务，比如探望家人、京东购物，甚至与伴侣一起看电视。系统通过Python脚本调用Telegram的Bot API发送消息，敏感的环境变量则安全地存储在GitHub Secrets中。这一机制确保我不会错过任何重要截止日期或个人承诺，将科技与日常生活无缝融合，实现效率最大化。

{% raw %}

```yaml
name: 提醒系统

on:
  schedule:
    # 每周三至周五北京时间12点至20点间每2小时运行一次
    - cron: '0 4,6,8,10,12 * * 3-5'
    # 每月27日中午12点（北京时间）运行
    - cron: '0 4 27 * *'
    # 每月30日下午2点（北京时间）运行
    - cron: '0 6 30 * *'
    # 每日凌晨1点（北京时间）运行
    - cron: '0 17 * * *'
    # 每日上午11点（北京时间）运行
    - cron: '0 3 * * *'
    # 每周二、三、四晚9点（北京时间）提醒次日去父母家
    - cron: '0 13 * * 2-4'
    # 每周日、一、五、六晚9点（北京时间）提醒次日回自己家
    - cron: '0 13 * * 0,1,5,6'
    # 每周三晚9点（北京时间）提醒在京东购买生鲜
    - cron: '0 13 * * 3'
    # 每周五晚9点（北京时间）提醒在京东购买速食
    - cron: '0 13 * * 5'
    # 每年3、4、9、10月每周一中午1点（北京时间）提醒大专考试报名
    - cron: '0 5 * 3,4,9,10 1'
    # 每周五下午5点（台北时间）提醒提交Clarity工时表
    - cron: '0 9 * * 5'
    # 每月25日午夜12点（台北时间）提醒提交供应商工时表
    - cron: '0 16 25 * *'
    # 每月16日晚9点（台北时间）提醒家人协助房贷还款
    - cron: '0 13 16 * *'
    # 每周五、六、日晚10点（台北时间）提醒与伴侣看电视
    - cron: '0 14 * * 5,6,0'
    # 每周三、四、五凌晨2点（北京时间）提醒移除车窗停车证
    - cron: '0 18 * * 3,4,5'
  workflow_dispatch:  # 支持手动触发

concurrency:
  group: 'reminders'
  cancel-in-progress: false

jobs:
  发送提醒:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_BOT2_API_KEY: ${{ secrets.TELEGRAM_BOT2_API_KEY }}

    steps:
      - name: 检出代码库
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: 配置Python 3.10.x环境
        uses: actions/setup-python@v4
        with:
          python-version: "3.10.x"

      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.simple.txt

      - name: 执行企业微信打卡提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得在企业微信打卡"
        if: github.event.schedule == '0 4,6,8,10,12 * * 3-5'

      - name: 执行房贷还款提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "准备房贷扣款"
        if: github.event.schedule == '0 4 27 * *'

      - name: 执行查收工资提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得查收工资"
        if: github.event.schedule == '0 6 30 * *'

      - name: 执行睡眠提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "该睡觉啦！"
        if: github.event.schedule == '0 17 * * *'

      - name: 执行起床提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "该起床啦！"
        if: github.event.schedule == '0 3 * * *'

      - name: 执行父母家提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "明天记得去父母家！"
        if: github.event.schedule == '0 13 * * 2-4'

      - name: 执行自家提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "明天记得回自己家！"
        if: github.event.schedule == '0 13 * * 0,1,5,6'

      - name: 执行京东生鲜采购提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得在京东购买生鲜！"
        if: github.event.schedule == '0 13 * * 3'

      - name: 执行京东速食采购提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得在京东购买速食！"
        if: github.event.schedule == '0 13 * * 5'

      - name: 执行大专考试提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得报名大专考试"
        if: github.event.schedule == '0 5 * 3,4,9,10 1'

      - name: 执行Clarity工时表提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得提交Clarity工时表"
        if: github.event.schedule == '0 9 * * 5'

      - name: 执行供应商工时表提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得提交供应商工时表"
        if: github.event.schedule == '0 16 25 * *'

      - name: 执行家人协助房贷提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得请家人协助房贷还款"
        if: github.event.schedule == '0 13 16 * *'

      - name: 执行伴侣观影提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "到点和伴侣一起看电视啦！"
        if: github.event.schedule == '0 14 * * 5,6,0'

      - name: 执行车窗停车证移除提醒
        run: python scripts/release/reminders_bot.py --job send_message --message "记得移除车窗上的停车证"
        if: github.event.schedule == '0 18 * * 3,4,5'

      - name: 执行测试消息发送
        run: python scripts/release/reminders_bot.py --job send_message --message "这是来自GitHub Actions的测试消息"
        if: github.event_name == 'workflow_dispatch'
```

{% endraw %}

```python
import os
import requests
from dotenv import load_dotenv
import json
import argparse

load_dotenv()

TELEGRAM_BOT2_API_KEY = os.environ.get("TELEGRAM_BOT2_API_KEY")
TELEGRAM_CHAT_ID = "610574272"

def send_telegram_message(bot_token, chat_id, message):
    """通过Telegram Bot API向指定聊天发送消息"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"发送Telegram消息出错: {response.status_code} - {response.text}")

def get_chat_id(bot_token):
    """获取最近发送给机器人的消息聊天ID"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        print(json.dumps(updates, indent=4))
        if updates['result']:
            chat_id = updates['result'][-1]['message']['chat']['id']
            return chat_id
    return None

def send_reminder(message):
    """发送提醒消息至Telegram"""
    if TELEGRAM_BOT2_API_KEY and TELEGRAM_CHAT_ID:
        send_telegram_message(TELEGRAM_BOT2_API_KEY, TELEGRAM_CHAT_ID, f"提醒: {message}")
    else:
        print("未设置TELEGRAM_BOT2_API_KEY和TELEGRAM_CHAT_ID")

def main():
    parser = argparse.ArgumentParser(description="Telegram机器人脚本")
    parser.add_argument('--job', choices=['get_chat_id', 'send_message'], required=True, help="选择操作类型")
    parser.add_argument('--message', help="自定义发送消息", default=None)
    args = parser.parse_args()

    if args.job == 'get_chat_id':
        bot_token = TELEGRAM_BOT2_API_KEY
        chat_id = get_chat_id(bot_token)
        if chat_id:
            print(f"聊天ID: {chat_id}")
        else:
            print("无法获取聊天ID")

    elif args.job == 'send_message':
        if args.message:
            send_reminder(args.message)
        else:
            print("未提供发送消息内容")

if __name__ == '__main__':
    main()
```
