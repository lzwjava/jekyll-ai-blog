---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 阿里云函数计算
translated: true
type: post
---

我正在使用阿里云的函数计算（Function Compute）来生成看似正常的流量，这有助于掩盖我的代理服务器在GFW（中国国家防火墙）下的活动。我在代理服务器旁边部署了一个带宽服务器，而这个函数计算函数每分钟都会向带宽API发起请求。这样就形成了正常流量和代理流量的混合。

```python
from flask import Flask, request, jsonify
import requests
import concurrent.futures

REQUEST_ID_HEADER = 'x-fc-request-id'

app = Flask(__name__)

# 调用外部API的函数
def call_bandwidth_api():
    try:
        response = requests.get('https://www.lzwjava.xyz/bandwidth')
        response.raise_for_status()  # 抛出HTTP错误异常
        return True  # 表示成功
    except Exception as e:
        print("获取带宽数据时出错:", e)
        return False  # 表示失败

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world(path):
    # 记录请求ID和其他详细信息
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC 调用开始 RequestId: " + rid)
    data = request.stream.read()
    print("路径: " + path)
    print("数据: " + str(data))

    # 初始化计数器
    total_calls = 10  # 总共要进行的API调用次数
    successful_calls = 0  # 跟踪成功的API调用

    # 使用ThreadPoolExecutor并发调用API 10次
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 向执行器提交任务
        futures = [executor.submit(call_bandwidth_api) for _ in range(total_calls)]

        # 等待所有任务完成并统计成功次数
        for future in concurrent.futures.as_completed(futures):
            if future.result():  # 如果调用成功
                successful_calls += 1

    # 记录请求结束
    print("FC 调用结束 RequestId: " + rid)

    # 返回调用次数和成功次数
    return jsonify({
        "message": "Hello, World!",
        "total_calls": total_calls,
        "successful_calls": successful_calls
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
```
