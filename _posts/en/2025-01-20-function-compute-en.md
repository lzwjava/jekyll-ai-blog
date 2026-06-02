---
audio: false
generated: false
image: false
lang: en
layout: post
title: Function Compute on Alibaba Cloud
translated: false
type: post
---

I'm using Alibaba Cloud's Function Compute to generate normal-looking traffic, which helps to obscure my proxy server's activity from the GFW. I've deployed a bandwidth server alongside my proxy, and this Function Compute function makes a request to the bandwidth API every minute. This creates a mix of normal and proxy traffic.

```python
from flask import Flask, request, jsonify
import requests
import concurrent.futures

REQUEST_ID_HEADER = 'x-fc-request-id'

app = Flask(__name__)

# Function to call the external API
def call_bandwidth_api():
    try:
        response = requests.get('https://www.lzwjava.xyz/bandwidth')
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True  # Indicate success
    except Exception as e:
        print("Error fetching bandwidth data:", e)
        return False  # Indicate failure

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world(path):
    # Log the request ID and other details
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)
    data = request.stream.read()
    print("Path: " + path)
    print("Data: " + str(data))

    # Initialize counters
    total_calls = 10  # Total number of API calls to make
    successful_calls = 0  # Track successful API calls

    # Use ThreadPoolExecutor to call the API 10 times concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(call_bandwidth_api) for _ in range(total_calls)]

        # Wait for all tasks to complete and count successes
        for future in concurrent.futures.as_completed(futures):
            if future.result():  # If the call was successful
                successful_calls += 1

    # Log the end of the request
    print("FC Invoke End RequestId: " + rid)

    # Return the number of calls and successful calls
    return jsonify({
        "message": "Hello, World!",
        "total_calls": total_calls,
        "successful_calls": successful_calls
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
```
