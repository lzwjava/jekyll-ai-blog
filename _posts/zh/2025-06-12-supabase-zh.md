---
audio: false
generated: true
lang: zh
layout: post
title: 基于Supabase的打卡提醒功能
translated: true
type: note
---

我将修改现有的 GitHub Actions 工作流程和 Python 脚本，实现周三到周五的打卡提醒功能，在 SGT 时间中午 12 点到下午 3 点（上班打卡）和晚上 6 点到 9 点（下班打卡）期间每 5 分钟发送提醒，当通过 Telegram 收到 "punch" 消息时停止提醒。我们将使用 Supabase 跟踪打卡状态以防止重复提醒。

以下是完整的说明和代码：

---

### GitHub Actions 工作流程

工作流程需要在 SGT (UTC+8) 指定时间窗口内每 5 分钟运行一次：

- 上班打卡：中午 12 点到下午 3 点 SGT = 4 AM 到 7 AM UTC
- 下班打卡：晚上 6 点到 9 点 SGT = 10 AM 到 1 PM UTC
- 日期：周三到周五 (cron 语法中的 3-5)

我们将使用单个 cron 调度组合这些时间，并让脚本确定具体操作。

{% raw %}

```yaml
name: 打卡提醒

on:
  schedule:
    # 在 UTC 时间 4-7 AM 和 10 AM-1 PM 期间每 5 分钟运行，周三到周五
    # 4-7 AM UTC = 12 PM-3 PM SGT, 10 AM-1 PM UTC = 6 PM-9 PM SGT
    - cron: '*/5 4-7,10-13 * * 3-5'

  workflow_dispatch:
    inputs:
      job_name:
        description: '要运行的作业 (punch_reminder, send_message)'
        required: true
        default: 'punch_reminder'
      message:
        description: 'send_message 作业的自定义消息（可选）'
        required: false
        default: '这是来自 GitHub Actions 的手动触发测试消息。'

  push:
    branches: ["main"]
    paths:
      - 'scripts/release/location_bot.py'
      - '.github/workflows/location.yml'

concurrency:
  group: 'punch_reminder'
  cancel-in-progress: false

jobs:
  punch_reminder_job:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_LOCATION_BOT_API_KEY: ${{ secrets.TELEGRAM_LOCATION_BOT_API_KEY }}
      SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
      SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}

    steps:
    - name: 检出仓库
      uses: actions/checkout@v4
      with:
        fetch-depth: 5

    - name: 设置 Python 3.13.2
      uses: actions/setup-python@v4
      with:
        python-version: "3.13.2"

    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.simple.txt

    - name: 运行打卡提醒脚本（计划任务）
      run: python scripts/release/location_bot.py --job punch_reminder
      if: github.event_name == 'schedule'

    - name: 运行打卡提醒脚本（手动触发）
      run: python scripts/release/location_bot.py --job punch_reminder
      if: github.event_name == 'workflow_dispatch' && github.event.inputs.job_name == 'punch_reminder'

    - name: 运行 Telegram 脚本发送自定义消息（手动触发）
      run: python scripts/release/location_bot.py --job send_message --message "${{ github.event.inputs.message }}"
      if: github.event_name == 'workflow_dispatch' && github.event.inputs.job_name == 'send_message'

    - name: 推送至 main 分支时通知
      run: python scripts/release/location_bot.py --job send_message --message "打卡提醒机器人的代码变更已推送至 main 分支。"
      if: github.event_name == 'push'
```

{% endraw %}

---

### Python 脚本

该脚本将：

- 检查当前 SGT 时间以确定是否在上班或下班打卡窗口
- 使用 Supabase 跟踪打卡状态
- 获取 Telegram 更新以查找 "punch" 消息
- 如果尚未记录打卡，则发送提醒

更新你的 `requirements.simple.txt` 以包含：

```
requests
supabase
pytz
```

以下是修改后的脚本：

```python
import os
import requests
import datetime
import pytz
from supabase import create_client
import argparse

# 加载环境变量
TELEGRAM_LOCATION_BOT_API_KEY = os.environ.get("TELEGRAM_LOCATION_BOT_API_KEY")
TELEGRAM_CHAT_ID = "610574272"  # 你的聊天 ID

def send_telegram_message(bot_token, chat_id, message):
    """使用 Telegram Bot API 向 Telegram 聊天发送消息。"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"发送 Telegram 消息时出错：{response.status_code} - {response.text}")

def send_reminder(action):
    """发送打卡提醒消息。"""
    message = f"⏰ *提醒：* 请通过向此机器人发送 'punch' 来{action.replace('_', ' ')}。"
    send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)

def main():
    parser = argparse.ArgumentParser(description="Telegram 打卡提醒机器人")
    parser.add_argument('--job', choices=['punch_reminder', 'send_message'], required=True, help="要执行的任务")
    parser.add_argument('--message', type=str, help="用于 'send_message' 任务的消息")
    args = parser.parse_args()

    if args.job == 'send_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = args.message if args.message else "来自你的机器人的默认测试消息！"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print(f"消息已发送：{message}")
        else:
            print("未设置 TELEGRAM_LOCATION_BOT_API_KEY 和 TELEGRAM_CHAT_ID。")
        return

    elif args.job == 'punch_reminder':
        # 初始化 Supabase
        supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

        # 获取 SGT (UTC+8) 当前时间
        sgt = pytz.timezone('Asia/Singapore')
        now_utc = datetime.datetime.utcnow()
        now_sgt = now_utc.replace(tzinfo=pytz.utc).astimezone(sgt)
        today_sgt = now_sgt.date()

        # 定义时间窗口
        punch_in_start = datetime.time(12, 0)  # 中午 12 点 SGT
        punch_in_end = datetime.time(15, 0)    # 下午 3 点 SGT
        punch_out_start = datetime.time(18, 0) # 晚上 6 点 SGT
        punch_out_end = datetime.time(21, 0)   # 晚上 9 点 SGT

        current_time = now_sgt.time()

        # 确定当前窗口
        if punch_in_start <= current_time <= punch_in_end:
            window = 'punch_in'
        elif punch_out_start <= current_time <= punch_out_end:
            window = 'punch_out'
        else:
            window = None

        if not window:
            print("不在打卡提醒时间窗口内。")
            return

        # 获取今天的打卡记录
        response = supabase.table('punch_records').select('*').eq('date', str(today_sgt)).execute()
        punch_record = response.data[0] if response.data else None

        # 检查是否已打卡
        if window == 'punch_in' and punch_record and punch_record['punch_in_time']:
            print("今天已上班打卡。")
            return
        if window == 'punch_out' and punch_record and punch_record['punch_out_time']:
            print("今天已下班打卡。")
            return

        # 获取最后处理的 Telegram 更新 ID
        state_response = supabase.table('telegram_state').select('last_update_id').eq('id', 1).execute()
        last_update_id = state_response.data[0]['last_update_id'] if state_response.data else 0

        # 获取新的 Telegram 更新
        url = f"https://api.telegram.org/bot{TELEGRAM_LOCATION_BOT_API_KEY}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 0}
        response = requests.get(url, params=params)
        updates = response.json().get('result', [])

        max_update_id = last_update_id
        for update in updates:
            if update['update_id'] > max_update_id:
                max_update_id = update['update_id']
            if ('message' in update and
                update['message'].get('text', '').lower() == 'punch' and
                str(update['message']['chat']['id']) == TELEGRAM_CHAT_ID):
                # 处理 "punch" 消息
                if window == 'punch_in':
                    if not punch_record:
                        supabase.table('punch_records').insert({
                            'date': str(today_sgt),
                            'punch_in_time': now_utc.isoformat()
                        }).execute()
                    else:
                        supabase.table('punch_records').update({
                            'punch_in_time': now_utc.isoformat()
                        }).eq('date', str(today_sgt)).execute()
                elif window == 'punch_out':
                    if not punch_record:
                        supabase.table('punch_records').insert({
                            'date': str(today_sgt),
                            'punch_out_time': now_utc.isoformat()
                        }).execute()
                    else:
                        supabase.table('punch_records').update({
                            'punch_out_time': now_utc.isoformat()
                        }).eq('date', str(today_sgt)).execute()

        # 更新 last_update_id
        if max_update_id > last_update_id:
            supabase.table('telegram_state').update({
                'last_update_id': max_update_id
            }).eq('id', 1).execute()

        # 重新获取打卡记录以检查最新状态
        response = supabase.table('punch_records').select('*').eq('date', str(today_sgt)).execute()
        punch_record = response.data[0] if response.data else None

        # 如果未记录打卡，则发送提醒
        if window == 'punch_in' and (not punch_record or not punch_record['punch_in_time']):
            send_reminder('punch_in')
        elif window == 'punch_out' and (not punch_record or not punch_record['punch_out_time']):
            send_reminder('punch_out')

if __name__ == '__main__':
    main()
```

---

### Supabase 设置

我们将在 Supabase 中创建两个表来管理打卡状态和 Telegram 更新。

#### SQL 说明

在 Supabase SQL 编辑器中运行以下 SQL 命令：

```sql
-- 存储每日打卡记录的表
CREATE TABLE punch_records (
    date DATE PRIMARY KEY,
    punch_in_time TIMESTAMP,
    punch_out_time TIMESTAMP
);

-- 表用于存储 Telegram 机器人状态
CREATE TABLE telegram_state (
    id INTEGER PRIMARY KEY,
    last_update_id BIGINT NOT NULL DEFAULT 0
);

-- 使用单行初始化 telegram_state
INSERT INTO telegram_state (id, last_update_id) VALUES (1, 0);
```

#### 执行步骤

1. 登录你的 Supabase 仪表板。
2. 导航到 **SQL Editor**。
3. 粘贴并运行上面的 SQL 代码以创建和初始化表。

---

### 环境变量

确保在你的 GitHub 仓库的 **Settings > Secrets and variables > Actions > Secrets** 下设置以下机密信息：

- `TELEGRAM_LOCATION_BOT_API_KEY`：你的 Telegram 机器人令牌。
- `SUPABASE_URL`：你的 Supabase 项目 URL（例如 `https://xyz.supabase.co`）。
- `SUPABASE_KEY`：你的 Supabase anon 密钥（在 **Settings > API** 中找到）。

---

### 工作原理

1. **调度**：工作流程在周三到周五的 SGT 时间中午 12 点到下午 3 点和晚上 6 点到 9 点（已调整为 UTC）期间每 5 分钟运行一次。
2. **时间检查**：脚本检查当前 SGT 时间以确定是否在上班或下班打卡窗口内。
3. **状态管理**：
   - 检查 `punch_records` 中今天的打卡记录。
   - 如果已打卡（例如，在中午 12 点到下午 3 点期间设置了 `punch_in_time`），则不发送提醒。
4. **Telegram 更新**：
   - 获取自上次处理的 `update_id` 以来的更新。
   - 如果找到 "punch" 消息，则使用当前时间更新 `punch_records` 中的上班或下班打卡时间。
   - 使用最新的 `update_id` 更新 `telegram_state`。
5. **提醒**：如果当前窗口的打卡尚未记录，则每 5 分钟发送一次提醒。

---

### 测试

- **手动触发**：使用 `workflow_dispatch` 和 `job_name: punch_reminder` 手动测试。
- **Telegram**：在时间窗口内向你的机器人发送 "punch" 以停止该时间段的提醒。
- **Supabase**：检查 `punch_records` 表以验证打卡时间是否已记录。

此设置将基于位置的逻辑替换为基于时间的打卡提醒，利用 Supabase 在 GitHub Actions 的限制内进行持久状态管理。
