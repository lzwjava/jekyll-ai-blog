---
audio: false
generated: true
lang: zh
layout: post
title: Python Requests库
translated: true
type: note
---

要完全用 Python 的 `requests` 库替代 Postman，你可以执行所有常见的 HTTP 操作，例如发送不同类型的请求、处理请求头、处理 JSON 数据、上传文件、使用代理以及断言响应。下面，我将逐步为你演示这些功能的示例，确保你获得完整且实用的指南。

### 第一步：安装 Requests 库

开始之前，请确保已安装 `requests` 库。在终端中运行以下命令：

```bash
pip install requests
```

现在，让我们深入示例。

---

### 发送 HTTP 请求

`requests` 库支持所有 HTTP 方法，如 GET、POST、PUT、DELETE 等。以下是发送简单 GET 和 POST 请求的方法：

#### GET 请求

```python
import requests

# 发送 GET 请求
response = requests.get('https://api.example.com/data')

# 打印状态码和响应体
print("状态码:", response.status_code)
print("响应体:", response.text)
```

#### POST 请求

```python
# 发送无数据的 POST 请求
response = requests.post('https://api.example.com/submit')

print("状态码:", response.status_code)
print("响应体:", response.text)
```

---

### 添加请求头

请求头常用于身份验证、内容类型或自定义元数据。将其作为字典传递给 `headers` 参数。

```python
# 定义自定义请求头
headers = {
    'Authorization': 'Bearer my_token',
    'Content-Type': 'application/json',
    'User-Agent': 'MyApp/1.0'
}

# 发送带请求头的 GET 请求
response = requests.get('https://api.example.com/data', headers=headers)

print("状态码:", response.status_code)
print("响应头:", response.headers)
print("响应体:", response.text)
```

---

### 发送 JSON 数据

要在 POST 请求中发送 JSON 数据（类似于在 Postman 的 body 选项卡中选择 JSON），请使用 `json` 参数。这会自动将 `Content-Type` 设置为 `application/json`。

```python
# 定义 JSON 数据
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# 发送带 JSON 数据的 POST 请求
response = requests.post('https://api.example.com/submit', json=data, headers=headers)

print("状态码:", response.status_code)
print("响应 JSON:", response.json())
```

---

### 上传文件

要上传文件（类似于 Postman 的 form-data 选项），请使用 `files` 参数。以二进制模式（`'rb'`）打开文件，并可选择包含额外的表单数据。

#### 简单文件上传

```python
# 准备上传的文件
files = {
    'file': open('myfile.txt', 'rb')
}

# 发送带文件的 POST 请求
response = requests.post('https://api.example.com/upload', files=files)

print("状态码:", response.status_code)
print("响应体:", response.text)

# 手动关闭文件
files['file'].close()
```

#### 带表单数据的文件上传（推荐方法）

使用 `with` 语句可确保文件自动关闭：

```python
# 额外的表单数据
form_data = {
    'description': '我的文件上传'
}

# 打开并上传文件
with open('myfile.txt', 'rb') as f:
    files = {
        'file': f
    }
    response = requests.post('https://api.example.com/upload', data=form_data, files=files)

print("状态码:", response.status_code)
print("响应体:", response.text)
```

---

### 使用代理

要通过代理路由请求（类似于 Postman 的代理设置），请使用 `proxies` 参数并传入字典。

```python
# 定义代理设置
proxies = {
    'http': 'http://myproxy:8080',
    'https': 'https://myproxy:8080'
}

# 通过代理发送请求
response = requests.get('https://api.example.com/data', proxies=proxies)

print("状态码:", response.status_code)
print("响应体:", response.text)
```

---

### 处理和断言响应

`requests` 库提供了便捷的方法来访问响应详情，如状态码、JSON 数据、请求头和 Cookie。你可以使用 Python 的 `assert` 语句来验证响应，类似于 Postman 的测试脚本。

#### 解析 JSON 响应

```python
response = requests.get('https://api.example.com/data')

# 检查状态码并解析 JSON
if response.status_code == 200:
    data = response.json()  # 将响应转换为 Python 字典/列表
    print("JSON 数据:", data)
else:
    print("错误:", response.status_code)
```

#### 断言响应详情

```python
response = requests.get('https://api.example.com/data')

# 断言状态码
assert response.status_code == 200, f"预期 200，实际为 {response.status_code}"

# 解析 JSON 并断言内容
data = response.json()
assert 'key' in data, "响应中未找到 key"
assert data['key'] == 'expected_value', "值不匹配"

# 检查响应头
assert 'Content-Type' in response.headers, "缺少 Content-Type 头"
assert response.headers['Content-Type'] == 'application/json', "意外的 Content-Type"

# 检查 Cookie
cookies = response.cookies
assert 'session_id' in cookies, "缺少 Session ID Cookie"

print("所有断言通过！")
```

#### 处理错误

将请求包装在 `try-except` 块中以捕获网络或 HTTP 错误：

```python
try:
    response = requests.get('https://api.example.com/data')
    response.raise_for_status()  # 对于 4xx/5xx 错误抛出异常
    data = response.json()
    print("数据:", data)
except requests.exceptions.RequestException as e:
    print("请求失败:", e)
```

---

### 综合示例

以下是一个结合了请求头、文件上传、代理和响应断言的完整示例：

```python
import requests

# 定义请求头
headers = {
    'Authorization': 'Bearer my_token'
}

# 表单数据和文件
form_data = {
    'description': '我的文件上传'
}

# 代理设置
proxies = {
    'http': 'http://myproxy:8080',
    'https': 'https://myproxy:8080'
}

# 发送带文件上传的请求
try:
    with open('myfile.txt', 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'https://api.example.com/upload',
            headers=headers,
            data=form_data,
            files=files,
            proxies=proxies
        )
        response.raise_for_status()  # 检查 HTTP 错误

        # 解析并断言响应
        data = response.json()
        assert 'upload_id' in data, "响应中未找到 upload_id"
        print("上传成功，ID:", data['upload_id'])

except requests.exceptions.RequestException as e:
    print("请求失败:", e)
```

---

### 可重用函数（替代 Postman 集合）

要模拟 Postman 的保存请求或集合，请将逻辑封装在函数中：

```python
def upload_file(file_path, description, token, proxy=None):
    headers = {'Authorization': f'Bearer {token}'}
    data = {'description': description}
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                'https://api.example.com/upload',
                headers=headers,
                data=data,
                files=files,
                proxies=proxies
            )
            response.raise_for_status()
            data = response.json()
            assert 'upload_id' in data, "未找到 upload_id"
            return data['upload_id']
    except requests.exceptions.RequestException as e:
        print("请求失败:", e)
        return None

# 使用示例
upload_id = upload_file('myfile.txt', '我的文件上传', 'my_token', 'http://myproxy:8080')
if upload_id:
    print("上传成功，ID:", upload_id)
```

---

### 附加功能

- **会话**：使用 `requests.Session()` 在多个请求间持久化 Cookie 或请求头。
- **超时**：在请求中添加 `timeout=5`（秒）以避免挂起。
- **重定向**：通过 `allow_redirects=True/False` 控制重定向。

---

### 总结

使用 `requests` 库，你可以：

- 发送 HTTP 请求（`get`、`post` 等）
- 包含请求头、JSON 数据和文件上传
- 使用代理
- 解析和断言响应（状态码、JSON、请求头、Cookie）
- 将代码组织成可重用的函数

这为你提供了一个可编程、灵活的 Postman 替代方案，适用于脚本编写和自动化！
