---
audio: false
generated: true
image: false
lang: en
layout: post
title: Persistent HTTP Sessions with Python Requests
translated: false
type: note
---

A `Session` in Python's `requests` library is a way to persist certain parameters, such as cookies, headers, and authentication, across multiple HTTP requests. It provides a convenient interface for making repeated requests to the same server or related endpoints while maintaining state, improving efficiency, and simplifying code. Below, I’ll explain how `requests.Session` works, its key features, and provide examples to illustrate its usage.

## What is a `requests.Session`?

The `requests` library is widely used for making HTTP requests in Python. While you can use standalone functions like `requests.get()` or `requests.post()`, a `Session` object allows you to create a persistent session that retains configurations (e.g., cookies, headers, or authentication credentials) across multiple requests. This is particularly useful for interacting with websites or APIs that require stateful interactions, such as maintaining a login session or reusing TCP connections.

A `Session` object:
- Persists cookies across requests.
- Reuses underlying TCP connections (via connection pooling) for better performance when making multiple requests to the same host.
- Allows you to set default parameters (e.g., headers, timeouts) that apply to all requests made with the session.
- Supports authentication and custom configurations.

## How Does `Session` Work?

When you create a `Session` object, it acts as a container for your HTTP requests. Here’s a breakdown of how it functions:

1. **Persistent Cookies**: When you make a request with a `Session`, any cookies set by the server (e.g., session cookies after logging in) are stored in the session and automatically sent in subsequent requests. This is key for maintaining state, such as staying logged in.

2. **Connection Pooling**: For requests to the same host, the `Session` reuses the same TCP connection, reducing latency and overhead compared to creating new connections for each request.

3. **Default Parameters**: You can set attributes like headers, authentication, or timeouts on the `Session` object, and they will apply to all requests made with that session unless overridden.

4. **Customizable**: You can configure proxies, SSL verification, or even mount custom adapters (e.g., for retries or custom transport) to control how requests are handled.

## Basic Usage

Here’s a simple example of how to use `requests.Session`:

```python
import requests

# Create a session
session = requests.Session()

# Set default headers for all requests in this session
session.headers.update({'User-Agent': 'MyApp/1.0'})

# Make a GET request
response1 = session.get('https://api.example.com/data')
print(response1.json())

# Make another request; cookies and headers are reused
response2 = session.post('https://api.example.com/submit', data={'key': 'value'})
print(response2.json())

# Close the session to release resources
session.close()
```

In this example:
- A `Session` is created, and a custom `User-Agent` header is set for all requests.
- The session handles cookies automatically, so if `response1` sets a cookie, it’s sent with `response2`.
- The session reuses the connection to `api.example.com`, improving performance.

## Key Features and Examples

### 1. **Persisting Cookies**
Sessions are particularly useful for websites that use cookies to maintain state, such as login sessions.

```python
import requests

# Create a session
session = requests.Session()

# Log in to a website
login_data = {'username': 'user', 'password': 'pass'}
response = session.post('https://example.com/login', data=login_data)

# Access a protected page; the session automatically sends the login cookie
protected_page = session.get('https://example.com/protected')
print(protected_page.text)

# Close the session
session.close()
```

Here, the session stores the authentication cookie from the login request and sends it with the subsequent request to the protected page.

### 2. **Setting Default Parameters**
You can set default headers, authentication, or other parameters for all requests in the session.

```python
import requests

session = requests.Session()

# Set default headers
session.headers.update({
    'Authorization': 'Bearer my_token',
    'Accept': 'application/json'
})

# Set default timeout
session.request = functools.partial(session.request, timeout=5)

# Make requests; headers and timeout are automatically applied
response1 = session.get('https://api.example.com/endpoint1')
response2 = session.get('https://api.example.com/endpoint2')

session.close()
```

### 3. **Connection Pooling**
When making multiple requests to the same host, `Session` reuses connections, which is more efficient than standalone requests.

```python
import requests
import time

# Without session
start = time.time()
for _ in range(5):
    requests.get('https://api.example.com/data')
print(f"Without session: {time.time() - start} seconds")

# With session
session = requests.Session()
start = time.time()
for _ in range(5):
    session.get('https://api.example.com/data')
print(f"With session: {time.time() - start} seconds")
session.close()
```

The session-based requests are typically faster because they reuse the TCP connection.

### 4. **Authentication**
Sessions simplify handling authentication, such as HTTP Basic Auth or custom token-based authentication.

```python
import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth('user', 'pass')

# All requests will include Basic Auth
response = session.get('https://api.example.com/protected')
print(response.json())

session.close()
```

### 5. **Custom Adapters**
You can mount custom adapters to control things like retries or connection pooling behavior.

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

# Configure retries
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Make a request with retry logic
response = session.get('https://api.example.com/unstable_endpoint')
print(response.json())

session.close()
```

This example sets up automatic retries for specific HTTP error codes.

## When to Use `Session`

Use `requests.Session` when:
- You need to maintain state (e.g., cookies) across multiple requests, such as for authentication.
- You’re making multiple requests to the same host and want to benefit from connection pooling.
- You want to apply consistent configurations (headers, timeouts, etc.) across requests.
- You’re interacting with APIs or websites that require session-based interactions.

If you’re making a single request or don’t need to persist state, standalone `requests.get()` or `requests.post()` is sufficient.

## Closing a Session

Always close a session when you’re done to release resources (e.g., connections):

```python
session.close()
```

Alternatively, use a session as a context manager to ensure it’s closed automatically:

```python
with requests.Session() as session:
    session.headers.update({'User-Agent': 'MyApp/1.0'})
    response = session.get('https://api.example.com/data')
    print(response.json())
# Session is automatically closed when the block exits
```

## Advanced Notes
- **Thread Safety**: `Session` objects are not thread-safe. If you’re using multithreading, create a separate `Session` for each thread.
- **Proxies**: You can set proxies on a session with `session.proxies = {'http': 'http://proxy.com', 'https': 'https://proxy.com'}`.
- **SSL Verification**: By default, `Session` verifies SSL certificates. To disable (not recommended for production), use `session.verify = False`.

## References
[Requests Documentation](https://requests.readthedocs.io/en/latest/)
[Requests Session Objects](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects)
