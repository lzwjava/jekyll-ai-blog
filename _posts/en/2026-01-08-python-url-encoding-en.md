---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Encoding Special Characters in Python URLs
translated: false
type: note
---

Question: Sometimes we need to use URL encoding in URLs like http://username:password@someproxy endpoint, right? If the password contains characters like # or ., then Python may complain about parse failure.

Answer: 

Yes, when constructing URLs that include authentication credentials (username:password@host), special characters in the username or password must be percent-encoded (URL-encoded) to avoid parsing issues.

### Why This Happens
Python's `urllib.parse.urlparse` (or similar parsers in libraries like `requests`) splits the URL into components. Delimiters like `:`, `@`, `/`, `?`, and `#` have special meanings:
- `:` separates username from password.
- `@` separates credentials from the host.
- `#` starts the fragment.
- `?` starts the query.
- `.` is usually fine in passwords, but other characters can cause misinterpretation.

If the password contains `#`, the parser may treat everything after `#` as a fragment, leading to incorrect netloc (network location) and parse errors or failures (e.g., ValueError for invalid port or host).

This is a known behavior in Python's urllib (see related bugs like treating `#` or `?` as delimiters unless encoded).

### Correct Solution
Percent-encode the username and/or password using `urllib.parse.quote` (or `quote_plus` for some cases, but `quote` is safer here as it doesn't replace spaces with `+`).

**Recommended way: Build the URL manually with encoding**

```python
from urllib.parse import quote

username = "myuser"
password = "pass#word.with.dots"  # Contains # and .

encoded_username = quote(username, safe='')
encoded_password = quote(password, safe='')

proxy_url = f"http://{encoded_username}:{encoded_password}@proxyhost:port/"

# Example output: http://myuser:pass%23word.with.dots@proxyhost:port/
```

- Use `safe=''` to encode even characters like `/` if present (though rare in credentials).
- Do **not** encode the `:` or `@` separators themselves.

### For Proxies in `requests` Library
If using proxies:

```python
import requests
from urllib.parse import quote

password = "pass#word.with.dots"
encoded_password = quote(password, safe='')

proxies = {
    "http": f"http://username:{encoded_password}@proxyhost:port/",
    "https": f"http://username:{encoded_password}@proxyhost:port/",
}

response = requests.get("https://example.com", proxies=proxies)
```

Many reports confirm that encoding `#` as `%23`, `@` as `%40`, etc., resolves parsing errors in `requests` proxies.

### Alternative: Avoid Embedding Credentials in URL
For security and simplicity:
- Use separate auth for proxies if supported (e.g., `requests` allows `auth` for some proxies, but for HTTP proxies, URL is common).
- Or use environment variables like `HTTP_PROXY` with encoded credentials.

Encoding ensures the full credential string is treated correctly before the host part.

References:  

- [https://bugs.python.org/issue18140](https://bugs.python.org/issue18140)  
- [https://github.com/python/cpython/issues/62340](https://github.com/python/cpython/issues/62340)  
- [https://docs.python.org/3/library/urllib.parse.html](https://docs.python.org/3/library/urllib.parse.html)  
- [https://stackoverflow.com/questions/30299973/http-request-through-proxy-in-python-having-in-password](https://stackoverflow.com/questions/30299973/http-request-through-proxy-in-python-having-in-password)  
- [https://stackoverflow.com/questions/73034574/how-to-use-password-with-special-character-in-basic-auth](https://stackoverflow.com/questions/73034574/how-to-use-password-with-special-character-in-basic-auth)