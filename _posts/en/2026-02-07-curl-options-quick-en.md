---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Mastering curl Command Options Quickly
translated: false
type: note
---

`curl` (Client URL) is a powerful command-line tool for transferring data using various network protocols. Here's a thorough guide to its most useful options.

## Basic Usage

```bash
curl https://example.com
```

This fetches and displays the content from the URL.

## Essential Options

**-o, --output <file>** — Save output to a file instead of stdout:
```bash
curl -o page.html https://example.com
```

**-O, --remote-name** — Save with the same filename as the remote file:
```bash
curl -O https://example.com/file.zip
```

**-L, --location** — Follow redirects (essential for many modern URLs):
```bash
curl -L https://example.com
```

**-i, --include** — Include HTTP response headers in output:
```bash
curl -i https://example.com
```

**-I, --head** — Fetch headers only (HEAD request):
```bash
curl -I https://example.com
```

**-v, --verbose** — Show detailed information about the request/response:
```bash
curl -v https://example.com
```

**-s, --silent** — Silent mode, no progress or error information:
```bash
curl -s https://example.com
```

## HTTP Methods

**-X, --request <method>** — Specify HTTP method:
```bash
curl -X POST https://api.example.com/data
curl -X DELETE https://api.example.com/resource/123
```

**-d, --data <data>** — Send POST data (automatically sets POST method):
```bash
curl -d "name=John&age=30" https://api.example.com/users
curl -d @data.json https://api.example.com/users  # from file
```

**--data-urlencode <data>** — URL-encode data before sending:
```bash
curl --data-urlencode "name=John Doe" https://api.example.com
```

## Headers

**-H, --header <header>** — Add custom headers:
```bash
curl -H "Content-Type: application/json" https://api.example.com
curl -H "Authorization: Bearer TOKEN" -H "Accept: application/json" https://api.example.com
```

**-A, --user-agent <string>** — Set User-Agent header:
```bash
curl -A "Mozilla/5.0" https://example.com
```

**-e, --referer <URL>** — Set Referer header:
```bash
curl -e "https://google.com" https://example.com
```

## Authentication

**-u, --user <user:password>** — HTTP Basic Authentication:
```bash
curl -u username:password https://api.example.com
curl -u username https://api.example.com  # prompts for password
```

**--oauth2-bearer <token>** — OAuth 2.0 Bearer Token:
```bash
curl --oauth2-bearer "your_token_here" https://api.example.com
```

## Cookies

**-b, --cookie <data>** — Send cookies:
```bash
curl -b "session=abc123" https://example.com
curl -b cookies.txt https://example.com  # from file
```

**-c, --cookie-jar <file>** — Save cookies to file:
```bash
curl -c cookies.txt https://example.com
```

## File Uploads

**-F, --form <name=content>** — Submit form data (multipart/form-data):
```bash
curl -F "file=@document.pdf" https://api.example.com/upload
curl -F "name=John" -F "avatar=@photo.jpg" https://api.example.com/profile
```

**-T, --upload-file <file>** — Upload file via PUT:
```bash
curl -T file.txt https://example.com/upload
```

## Download Options

**-C, --continue-at <offset>** — Resume a download:
```bash
curl -C - -O https://example.com/largefile.zip  # auto-detect offset
```

**--limit-rate <speed>** — Limit transfer speed:
```bash
curl --limit-rate 100K https://example.com/file.zip
```

**-r, --range <range>** — Download only a range of bytes:
```bash
curl -r 0-999 https://example.com/file.zip  # first 1000 bytes
```

## SSL/TLS Options

**-k, --insecure** — Skip SSL certificate verification (use cautiously):
```bash
curl -k https://self-signed.example.com
```

**--cacert <file>** — Specify CA certificate:
```bash
curl --cacert ca-bundle.crt https://example.com
```

**--cert <certificate>** — Use client certificate:
```bash
curl --cert client.pem https://example.com
```

## Timeouts and Retries

**--connect-timeout <seconds>** — Maximum connection time:
```bash
curl --connect-timeout 10 https://example.com
```

**-m, --max-time <seconds>** — Maximum total operation time:
```bash
curl -m 30 https://example.com
```

**--retry <num>** — Number of retry attempts:
```bash
curl --retry 5 https://example.com
```

## Proxy

**-x, --proxy <[protocol://]host[:port]>** — Use proxy:
```bash
curl -x http://proxy.example.com:8080 https://example.com
curl -x socks5://localhost:9050 https://example.com
```

**-U, --proxy-user <user:password>** — Proxy authentication:
```bash
curl -x proxy.example.com:8080 -U user:pass https://example.com
```

## Output Formatting

**-w, --write-out <format>** — Display custom information:
```bash
curl -w "Status: %{http_code}\nTime: %{time_total}s\n" https://example.com
```

Useful format variables include `%{http_code}`, `%{time_total}`, `%{size_download}`, `%{speed_download}`.

**--compressed** — Request compressed response:
```bash
curl --compressed https://example.com
```

## Multiple URLs

**-Z, --parallel** — Process multiple URLs in parallel:
```bash
curl -Z https://example.com/file1 https://example.com/file2
```

You can also use brace expansion:
```bash
curl https://example.com/file[1-10].txt
curl https://example.com/{page1,page2,page3}.html
```

## Practical Examples

**JSON API request:**
```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"John","email":"john@example.com"}'
```

**Download with progress bar:**
```bash
curl -# -o file.zip https://example.com/file.zip
```

**Check website response time:**
```bash
curl -w "@curl-format.txt" -o /dev/null -s https://example.com
```

Where `curl-format.txt` contains:
```
time_namelookup:  %{time_namelookup}s
time_connect:     %{time_connect}s
time_total:       %{time_total}s
```

This covers the most commonly used curl options. For the complete list, run `curl --help` or `man curl` on your system.