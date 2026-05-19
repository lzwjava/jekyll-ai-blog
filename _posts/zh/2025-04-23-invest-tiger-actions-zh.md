---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 每周股票投资与TigerOpen API
translated: true
type: post
---

我开发了一段 Python 脚本和一个 GitHub Actions 工作流，用于自动化我的每周投资策略，每周三晚上 10:35 中国标准时间（CST）购买一只 NVIDIA 股票。我选择周三是因为 2025 年没有任何假期，确保一致执行。

## 概述

该脚本使用 TigerOpen API 下单 NVIDIA 股票并监控其状态。GitHub Actions 工作流按计划运行脚本，安全地处理设置和认证。以下是两个组件的详细信息。

## Python 脚本

该脚本下单购买一只 NVIDIA 股票，检查其状态最多 60 秒，如果未成交则取消。

```python
import time
import os
from tigeropen.common.consts import Language, OrderStatus
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.util.order_utils import market_order
from tigeropen.common.util.contract_utils import stock_contract

def get_client_config(sandbox=False):
    client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
    client_config.private_key = read_private_key(os.environ.get('TIGER_PEM'))
    client_config.tiger_id = os.environ.get('TIGER_TIGER_ID')
    client_config.account = os.environ.get('TIGER_ACCOUNT')
    client_config.language = Language.zh_CN
    return client_config

# 下单函数
def place_order():
    client_config = get_client_config()
    trade_client = TradeClient(client_config)
    account = client_config.account  # 存储账户以便后续使用

    contract = stock_contract(symbol='NVDA', currency='USD')
    stock_order = market_order(
        account=account, contract=contract, action='BUY', quantity=1
    )
    # 下单
    order_id = trade_client.place_order(stock_order)
    print(f"已下单，订单 ID: {order_id}")

    # 记录时间
    start_time = time.time()
    while time.time() - start_time < 60:  # 1 分钟超时
        # 获取订单并找到刚刚下的订单
        order = trade_client.get_order(id=order_id)
        if str(order.id) == str(order_id):
            print(f"订单 ID 匹配！检查订单状态: {order.status}")
            # 使用 OrderStatus 枚举值检查订单状态
            if order.status == OrderStatus.FILLED:
                print("订单成功完成。")
                return
            elif order.status == OrderStatus.REJECTED:
                print(f"订单被拒绝: {order_id}")
                raise Exception(f"订单 {order_id} 被拒绝")
            elif order.status in [
                OrderStatus.PENDING_NEW,
                OrderStatus.NEW,
                OrderStatus.HELD,
                OrderStatus.PENDING_CANCEL
            ]:
                print(f"订单正在等待，状态: {order.status}")
            else:
                print(f"订单状态是: {order.status}")

        # 等待后再次检查
        time.sleep(5)  # 每 5 秒检查一次

    # 如果订单在 1 分钟内未完成，取消订单
    print("订单在 1 分钟内未完成。取消订单。")
    trade_client.cancel_order(id=order_id)
    print(f"订单已取消: {order_id}")

if __name__ == '__main__':
    place_order()
```

## GitHub Actions 工作流

该工作流每周三 14:35 UTC（10:35 PM UTC）运行一次，设置环境，安装依赖项，并执行脚本。

{% raw %}
```yaml
name: Regular Invest

on:
  schedule:
    - cron: '35 14 * * 3'  # 每周三 14:35 UTC 运行
  workflow_dispatch:

concurrency:
  group: 'trading'
  cancel-in-progress: false

permissions:
  id-token: write
  contents: write
  pages: write

jobs:
  invest:
    runs-on: ubuntu-latest
    steps:
      - name: 检出仓库
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: 设置 Python 3.13.2
        uses: actions/setup-python@v4
        with:
          python-version: "3.13.2"

      - name: 安装依赖项
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 设置 Tiger PEM 文件
        run: |
          echo "${{ secrets.TIGER_PEM_CONTENT }}" > tiger.pem
          chmod 600 tiger.pem

      - name: 运行 Tiger 脚本
        id: tiger_update
        run: python invest.py
        env:
          TIGER_TIGER_ID: ${{ secrets.TIGER_TIGER_ID }}
          TIGER_ACCOUNT: ${{ secrets.TIGER_ACCOUNT }}
          TIGER_PEM: "tiger.pem"
```
{% endraw %}