---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Certifi SSL Certificate Guide
translated: false
type: note
---

The **`certifi`** package on PyPI is a small library that provides **Mozilla’s trusted root certificates** in a bundle. It’s commonly used by Python libraries like `requests`, `urllib3`, or any HTTPS client that needs to validate SSL/TLS certificates.

Here’s how to use it:

---

### 1. Install `certifi`

```bash
pip install certifi
```

---

### 2. Get the CA bundle path

In Python:

```python
import certifi

print(certifi.where())
```

This will print the full path to the CA certificate bundle (a `.pem` file). For example:

```
/usr/local/lib/python3.11/site-packages/certifi/cacert.pem
```

---

### 3. Use with `requests` or `urllib3`

```python
import requests
import certifi

response = requests.get("https://example.com", verify=certifi.where())
print(response.status_code)
```

By default, `requests` already uses `certifi` internally, but explicitly passing `verify=certifi.where()` ensures it uses the updated bundle.

---

### 4. Use in other HTTPS libraries

If you’re working with `urllib3` directly:

```python
import urllib3
import certifi

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)

response = http.request("GET", "https://example.com")
print(response.status)
```

---

### 5. System-wide usage (optional)

Sometimes you might want to point an app to use certifi’s CA bundle:

```bash
export SSL_CERT_FILE=$(python -m certifi)
```

---

👉 In short:

* Install with `pip install certifi`
* Use `certifi.where()` to get the certificate bundle path
* Pass it to libraries that need certificate validation

---

Do you want me to also show you **how to make your entire Python environment use certifi’s certificates by default**, so you don’t need to configure each library individually?
