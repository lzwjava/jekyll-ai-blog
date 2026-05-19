---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 使用Telegram位置机器人自动化打卡
translated: true
type: post
---

你是否也希望每天的“打卡”不再那么麻烦？我确实这么想。所以我构建了一个个人Telegram机器人，利用位置追踪自动发送办公室到达通知，并提醒我那些关键打卡。本文将介绍我如何将Python与GitHub Actions结合，打造一个无缝、免手动的系统，在我需要时及时通知我，这一切都基于我的位置。

```yml
name: 每小时位置检查

on:
  schedule:
    # 每小时运行一次，整点执行，时间范围：上午11点到晚上11点，工作日（周一至周五）
    # 时间采用UTC。新加坡时间（SGT）为UTC+8。
    # 因此，上午11点SGT对应UTC 03:00，晚上11点SGT对应UTC 15:00。
    # 所以我们需要安排从UTC 03:00到15:00。
    - cron: '0 3-15 * * 1-5'

    # 提醒开始共享实时位置：周三上午11点SGT（UTC 3点）
    # 当前时间：2025年6月8日，周日，下午5:10:58 +08（SGT）
    # 周三上午11点SGT（UTC+8）：11 - 8 = UTC 3点
    - cron: '0 3 * * 3' # 3 代表周三

    # 提醒停止共享实时位置：周五晚上11点SGT（UTC 15点）
    # 当前时间：2025年6月8日，周日，下午5:10:58 +08（SGT）
    # 周五晚上11点SGT（UTC+8）：23 - 8 = UTC 15点
    - cron: '0 15 * * 5' # 5 代表周五

  workflow_dispatch:  # 允许手动触发工作流
  push:
    branches: ["main"]
    paths:
      - 'scripts/release/location_bot.py' # 修正为你的脚本路径
      - '.github/workflows/location.yml' # 此工作流文件的路径

concurrency:
  group: 'location'
  cancel-in-progress: false

jobs:
  check_and_notify:
    runs-on: ubuntu-latest
    env:
      TELEGRAM_LOCATION_BOT_API_KEY: ${{ secrets.TELEGRAM_LOCATION_BOT_API_KEY }}

    steps:
    - name: 检出仓库
      uses: actions/checkout@v4
      with:
        fetch-depth: 5 # 只拉取最近5次提交以提高效率

    - name: 设置Python 3.13.2
      uses: actions/setup-python@v4
      with:
        python-version: "3.13.2" # 指定精确的Python版本

    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        # 假设你的仓库根目录下有一个requirements.simple.txt文件
        # 如果没有，请使用：pip install requests python-dotenv
        pip install -r requirements.simple.txt 

    - name: 运行位置检查脚本（定时执行）
      run: python scripts/release/location_bot.py --job check_location
      # 此步骤将在定时触发时运行，用于每小时检查
      if: github.event.schedule == '0 3-15 * * 1-5' # 匹配每小时cron计划

    - name: 提醒开始共享实时位置
      run: python scripts/release/location_bot.py --job start_sharing_message
      if: github.event.schedule == '0 3 * * 3' # 匹配周三上午11点SGT的cron

    - name: 提醒停止共享实时位置
      run: python scripts/release/location_bot.py --job stop_sharing_message
      if: github.event.schedule == '0 15 * * 5' # 匹配周五晚上11点SGT的cron

    - name: 运行Telegram脚本发送测试消息（手动触发）
      run: python scripts/release/location_bot.py --job send_message --message "这是来自GitHub Actions的手动触发测试消息。"
      if: github.event_name == 'workflow_dispatch'

    - name: 推送到main分支时运行Telegram脚本
      run: python scripts/release/location_bot.py --job send_message --message "位置机器人代码已推送到main分支。"
      if: github.event_name == 'push'
```

```python
import os
import requests
from dotenv import load_dotenv
import json
import subprocess
import argparse
import math
import time # 用于未来可能的持续监控

load_dotenv()

# 新：为位置机器人单独设置API密钥
TELEGRAM_LOCATION_BOT_API_KEY = os.environ.get("TELEGRAM_LOCATION_BOT_API_KEY") # 确保已在.env中设置
TELEGRAM_CHAT_ID = "610574272" # 此聊天ID用于发送通知消息

# 定义你的办公室坐标
OFFICE_LATITUDE = 23.135368
OFFICE_LONGITUDE = 113.32952

# 接近半径（米）
PROXIMITY_RADIUS_METERS = 300

def send_telegram_message(bot_token, chat_id, message):
    """使用Telegram Bot API向指定聊天发送消息。"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown" # 使用Markdown使消息中的文字加粗
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"发送Telegram消息时出错：{response.status_code} - {response.text}")

def get_latest_location(bot_token):
    """从机器人获取最新的实时位置更新。"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    # 偏移量设置为仅获取自上次处理后的新更新（用于持续轮询）
    # 对于简单的单次运行脚本，我们只获取最新的；但对于轮询，需要管理偏移量
    params = {"offset": -1} # 获取最后一条更新
    response = requests.get(url, params=params)
    print("GetUpdates响应：", response) # 调试
    if response.status_code == 200:
        updates = response.json()
        print("GetUpdates JSON：", json.dumps(updates, indent=4)) # 调试
        if updates['result']:
            last_update = updates['result'][-1]
            # 优先处理经过编辑的消息（用于实时位置）
            if 'edited_message' in last_update and 'location' in last_update['edited_message']:
                return last_update['edited_message']['location'], last_update['edited_message']['chat']['id']
            elif 'message' in last_update and 'location' in last_update['message']:
                # 处理初始实时位置消息或静态位置分享
                return last_update['message']['location'], last_update['message']['chat']['id']
    return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    使用哈弗辛公式计算地球上两点之间的距离。
    返回以米为单位的距离。
    """
    R = 6371000  # 地球半径（米）

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def main():
    parser = argparse.ArgumentParser(description="Telegram机器人脚本")
    # 更新后的--job参数选项
    parser.add_argument('--job', choices=['get_chat_id', 'send_message', 'check_location', 'start_sharing_message', 'stop_sharing_message'], required=True, help="要执行的任务")
    # 为'send_message'任务添加--message参数
    parser.add_argument('--message', type=str, help="用于'send_message'任务的消息内容")
    # 为'check_location'任务添加--test参数
    parser.add_argument('--test', action='store_true', help="对于'check_location'任务，强制发送消息（无论是否在接近范围内）。")
    args = parser.parse_args()

    if args.job == 'get_chat_id':
        bot_token = TELEGRAM_LOCATION_BOT_API_KEY
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json()
            print(json.dumps(updates, indent=4))
            if updates['result']:
                last_update = updates['result'][-1]
                chat_id = None
                if 'message' in last_update and 'chat' in last_update['message']:
                    chat_id = last_update['message']['chat']['id']
                elif 'edited_message' in last_update and 'chat' in last_update['edited_message']:
                    chat_id = last_update['edited_message']['chat']['id']
                elif 'channel_post' in last_update and 'chat' in last_update['channel_post']:
                    chat_id = last_update['channel_post']['chat']['id']
                elif 'edited_channel_post' in last_update and 'chat' in last_update['edited_channel_post']:
                    chat_id = last_update['edited_channel_post']['chat']['id']

                if chat_id:
                    print(f"聊天ID：{chat_id}")
                else:
                    print("无法从最后一条更新中获取聊天ID。")
            else:
                print("未找到任何更新。")
        else:
            print(f"获取更新时出错：{response.status_code} - {response.text}")

    elif args.job == 'send_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = args.message if args.message else "这是来自你的Telegram机器人脚本的默认测试消息！"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print(f"消息发送成功：{message}")
        else:
            print("未设置TELEGRAM_LOCATION_BOT_API_KEY和TELEGRAM_CHAT_ID。")

    elif args.job == 'start_sharing_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = "⚠️ *提醒：* 请开始向机器人共享你的实时位置！"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print("已发送开始共享提醒。")
        else:
            print("未设置TELEGRAM_LOCATION_BOT_API_KEY和TELEGRAM_CHAT_ID。")

    elif args.job == 'stop_sharing_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = "✅ *提醒：* 现在可以停止共享你的实时位置了。"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print("已发送停止共享提醒。")
        else:
            print("未设置TELEGRAM_LOCATION_BOT_API_KEY和TELEGRAM_CHAT_ID。")

    elif args.job == 'check_location':
        if not TELEGRAM_LOCATION_BOT_API_KEY or not TELEGRAM_CHAT_ID:
            print("位置检查必须设置TELEGRAM_LOCATION_BOT_API_KEY和TELEGRAM_CHAT_ID。")
            return

        user_location, location_chat_id = get_latest_location(TELEGRAM_LOCATION_BOT_API_KEY)

        if user_location:
            current_latitude = user_location['latitude']
            current_longitude = user_location['longitude']

            distance = haversine_distance(
                OFFICE_LATITUDE, OFFICE_LONGITUDE,
                current_latitude, current_longitude
            )

            print(f"当前位置：({current_latitude}, {current_longitude})")
            print(f"距离办公室：{distance:.2f}米")

            needs_punch_card = distance <= PROXIMITY_RADIUS_METERS

            if needs_punch_card:
                print(f"你已进入办公室周围{PROXIMITY_RADIUS_METERS}米范围内！")
                notification_message = (
                    f"🎉 *到达办公室！* 🎉\n"
                    f"请在WeCom中打卡。\n"
                    f"你当前距离办公室：{distance:.2f}米。"
                )
            else:
                print(f"你位于办公室周围{PROXIMITY_RADIUS_METERS}米范围之外。")
                # 在半径外时的消息
                notification_message = (
                    f"📍 你*不在*办公室接近范围内（{PROXIMITY_RADIUS_METERS}米）。\n"
                    f"此时无需打卡。\n"
                    f"你当前距离办公室：{distance:.2f}米。"
                )

            # 如果在接近范围内或使用了--test标志，则发送消息
            if needs_punch_card or args.test:
                send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, notification_message)
            else:
                # 如果不在接近范围内且非测试模式，仅输出到控制台（不发送Telegram消息）
                print("不在接近范围内且非测试模式，未发送消息到Telegram。")
        else:
            print("无法获取你的最新位置。请确保你正在向机器人共享实时位置。")

if __name__ == '__main__':
    main()
```

---

更新：这个方案不够好，因为你必须向机器人共享你的实时位置。