---
audio: false
generated: false
image: false
lang: en
layout: post
title: Weekly Stock Investments with TigerOpen API
translated: false
type: post
---

I developed a Python script and a GitHub Actions workflow to automate my weekly investment strategy, purchasing one NVIDIA stock every Wednesday at 10:35 PM China Standard Time (CST). I chose Wednesdays because, in 2025, there are no holidays on that day, ensuring consistent execution.

## Overview

The script uses the TigerOpen API to place a market order for NVIDIA stock and monitors its status. The GitHub Actions workflow runs the script on a schedule, handling setup and authentication securely. Below are the details of both components.

## Python Script

This script places a buy order for one NVIDIA stock, checks its status for up to 60 seconds, and cancels it if not filled.

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


# Function to place an order
def place_order():
    client_config = get_client_config()
    trade_client = TradeClient(client_config)
    account = client_config.account  # Store account for later use

    contract = stock_contract(symbol='NVDA', currency='USD')
    stock_order = market_order(
        account=account, contract=contract, action='BUY', quantity=1
    )
    # Place the order
    order_id = trade_client.place_order(stock_order)
    print(f"Order placed with ID: {order_id}")

    # Track time
    start_time = time.time()
    while time.time() - start_time < 60:  # 1 minute timeout
        # Get the order and find the one we just placed
        order = trade_client.get_order(id=order_id)
        if str(order.id) == str(order_id):
            print(f"Order ID matched! Checking order status: {order.status}")
            # Check order status using OrderStatus enum values
            if order.status == OrderStatus.FILLED:
                print("Order completed successfully.")
                return
            elif order.status == OrderStatus.REJECTED:
                print(f"Order rejected: {order_id}")
                raise Exception(f"Order {order_id} was rejected")
            elif order.status in [
                OrderStatus.PENDING_NEW,
                OrderStatus.NEW,
                OrderStatus.HELD,
                OrderStatus.PENDING_CANCEL
            ]:
                print(f"Order is pending, status: {order.status}")
            else:
                print(f"Order status is: {order.status}")

        # Sleep before checking again
        time.sleep(5)  # Check every 5 seconds

    # If the order is not completed in 1 minute, cancel it
    print("Order not completed within 1 minute. Cancelling the order.")
    trade_client.cancel_order(id=order_id)
    print(f"Order cancelled: {order_id}")


if __name__ == '__main__':
    place_order()

```

## GitHub Actions Workflow

The workflow runs every Wednesday at 14:35 UTC (10:35 PM UTC) and sets up the environment, installs dependencies, and executes the script.

```yaml
name: Regular Invest

on:
  schedule:
    - cron: '35 14 * * 3'  # Run every Wednesday at 14:35 UTC
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
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 5
          
      - name: Set up Python 3.13.2
        uses: actions/setup-python@v4
        with:
          python-version: "3.13.2"
          
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Setup Tiger PEM File
        run: |
          echo "${{ secrets.TIGER_PEM_CONTENT }}" > tiger.pem
          chmod 600 tiger.pem
          
      - name: Run Tiger Script
        id: tiger_update
        run: python invest.py
        env:
          TIGER_TIGER_ID: ${{ secrets.TIGER_TIGER_ID }}
          TIGER_ACCOUNT: ${{ secrets.TIGER_ACCOUNT }}
          TIGER_PEM: "tiger.pem"
```