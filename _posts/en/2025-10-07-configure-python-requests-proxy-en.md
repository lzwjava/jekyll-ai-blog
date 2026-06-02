---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configure Python Requests Proxy via .env
translated: false
type: note
---

### Using a `.env` File to Set HTTP/HTTPS Proxies for Python Requests

The `requests` library in Python automatically honors standard environment variables like `HTTP_PROXY` and `HTTPS_PROXY` for proxy configuration. To manage these securely (e.g., without hardcoding in your script), you can store them in a `.env` file and load them using the `python-dotenv` library. This keeps sensitive proxy details out of your code.

#### Step 1: Install Required Packages

You'll need `requests` (if not already installed) and `python-dotenv` for loading the `.env` file.

```bash
pip install requests python-dotenv
```

#### Step 2: Create a `.env` File

In your project root, create a file named `.env` (no extension) and add your proxy settings. Use the format `http://` or `https://` for the proxy URL, including username/password if required.

Example `.env` content:

```
HTTP_PROXY=http://username:password@proxy-host:port
HTTPS_PROXY=https://username:password@proxy-host:port
NO_PROXY=localhost,127.0.0.1,example.com  # Optional: Exclude domains from proxying
```

- `HTTP_PROXY`: For HTTP traffic.
- `HTTPS_PROXY`: For HTTPS traffic (often the same as HTTP_PROXY).
- `NO_PROXY`: Comma-separated list of hosts/IPs to bypass the proxy.
- Note: Environment variables are case-insensitive, but uppercase is conventional.

Add `.env` to your `.gitignore` to avoid committing sensitive info.

#### Step 3: Load the `.env` File in Your Python Script

At the top of your script, load the environment variables:

```python
from dotenv import load_dotenv
import requests

# Load variables from .env file
load_dotenv()  # Looks for .env in the current directory by default

# Now make a request – proxies are automatically applied
response = requests.get('https://httpbin.org/ip')
print(response.json())
```

- `load_dotenv()` reads the `.env` file and sets the variables in `os.environ`.
- `requests` will detect `HTTP_PROXY`/`HTTPS_PROXY` automatically—no need to pass a `proxies` dict unless overriding.

#### Step 4: Verify Proxy Usage (Optional)

To confirm proxies are working, test with a service like httpbin.org:

```python
import requests
from dotenv import load_dotenv

load_dotenv()

proxies = requests.utils.get_environ_proxies('https://httpbin.org/ip')  # Inspect loaded proxies
print("Loaded proxies:", proxies)

response = requests.get('https://httpbin.org/ip')
print("Your IP via proxy:", response.json())
```

This should show the proxy server's IP if configured correctly.

#### Common Issues and Tips

- **Proxy Authentication**: Include `username:password@` in the URL if needed.
- **SOCKS Proxies**: Use `socks5://` prefix (requires `requests[socks]` extra: `pip install requests[socks]`).
- **Overriding Per-Request**: If you need different proxies for a specific call, pass a dict:

  ```python:disable-run
  proxies = {'http': 'http://custom-proxy:port', 'https': 'https://custom-proxy:port'}
  response = requests.get('url', proxies=proxies)
  ```

- **Environment**: Works on Windows/Linux/macOS. On Windows, use `set` in cmd or PowerShell equivalents.
- **Security**: Never commit `.env` to version control.

This setup is simple, secure, and follows best practices for environment-based configuration.

[Requests Documentation: Proxies](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)
[python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

```
