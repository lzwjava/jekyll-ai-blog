---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 快速掌握 curl 命令选项
translated: true
type: note
---

`curl` (Client URL) 是一个强大的命令行工具，用于使用各种网络 protocols 传输数据。以下是其最常用选项的详细指南。

## Basic Usage

```bash
curl https://example.com
```

这将获取并显示该 URL 的内容。

## Essential Options

**-o, --output <file>** — 将输出保存到文件而不是 stdout：

```bash
curl -o page.html https://example.com
```

**-O, --remote-name** — 使用与远程文件相同的文件名保存：

```bash
curl -O https://example.com/file.zip
```

**-L, --location** — 跟随 redirects（对许多现代 URL 至关重要）：

```bash
curl -L https://example.com
```

**-i, --include** — 在输出中包含 HTTP response headers：

```bash
curl -i https://example.com
```

**-I, --head** — 仅获取 headers（HEAD request）：

```bash
curl -I https://example.com
```

**-v, --verbose** — 显示有关 request/response 的详细信息：

```bash
curl -v https://example.com
```

**-s, --silent** — 静默模式，不显示进度或错误信息：

```bash
curl -s https://example.com
```

## HTTP Methods

**-X, --request <method>** — 指定 HTTP method：

```bash
curl -X POST https://api.example.com/data
curl -X DELETE https://api.example.com/resource/123
```

**-d, --data <data>** — 发送 POST 数据（自动设置 POST method）：

```bash
curl -d "name=John&age=30" https://api.example.com/users
curl -d @data.json https://api.example.com/users  # from file
```

**--data-urlencode <data>** — 在发送前进行 URL-encode 数据：

```bash
curl --data-urlencode "name=John Doe" https://api.example.com
```

## Headers

**-H, --header <header>** — 添加自定义 headers：

```bash
curl -H "Content-Type: application/json" https://api.example.com
curl -H "Authorization: Bearer TOKEN" -H "Accept: application/json" https://api.example.com
```

**-A, --user-agent <string>** — 设置 User-Agent header：

```bash
curl -A "Mozilla/5.0" https://example.com
```

**-e, --referer <URL>** — 设置 Referer header：

```bash
curl -e "https://google.com" https://example.com
```

## Authentication

**-u, --user <user:password>** — HTTP Basic Authentication：

```bash
curl -u username:password https://api.example.com
curl -u username https://api.example.com  # 提示输入密码
```

**--oauth2-bearer <token>** — OAuth 2.0 Bearer Token：

```bash
curl --oauth2-bearer "your_token_here" https://api.example.com
```

## Cookies

**-b, --cookie <data>** — 发送 cookies：

```bash
curl -b "session=abc123" https://example.com
curl -b cookies.txt https://example.com  # from file
```

**-c, --cookie-jar <file>** — 将 cookies 保存到文件：

```bash
curl -c cookies.txt https://example.com
```

## File Uploads

**-F, --form <name=content>** — 提交表单数据（multipart/form-data）：

```bash
curl -F "file=@document.pdf" https://api.example.com/upload
curl -F "name=John" -F "avatar=@photo.jpg" https://api.example.com/profile
```

**-T, --upload-file <file>** — 通过 PUT 上传文件：

```bash
curl -T file.txt https://example.com/upload
```

## Download Options

**-C, --continue-at <offset>** — 断点续传：

```bash
curl -C - -O https://example.com/largefile.zip  # 自动检测 offset
```

**--limit-rate <speed>** — 限制传输速度：

```bash
curl --limit-rate 100K https://example.com/file.zip
```

**-r, --range <range>** — 仅下载特定范围的字节：

```bash
curl -r 0-999 https://example.com/file.zip  # 前 1000 字节
```

## SSL/TLS Options

**-k, --insecure** — 跳过 SSL 证书校验（谨慎使用）：

```bash
curl -k https://self-signed.example.com
```

**--cacert <file>** — 指定 CA 证书：

```bash
curl --cacert ca-bundle.crt https://example.com
```

**--cert <certificate>** — 使用客户端证书：

```bash
curl --cert client.pem https://example.com
```

## Timeouts and Retries

**--connect-timeout <seconds>** — 最大连接时间：

```bash
curl --connect-timeout 10 https://example.com
```

**-m, --max-time <seconds>** — 最大总操作时间：

```bash
curl -m 30 https://example.com
```

**--retry <num>** — 重试次数：

```bash
curl --retry 5 https://example.com
```

## Proxy

**-x, --proxy <[protocol://]host[:port]>** — 使用代理：

```bash
curl -x http://proxy.example.com:8080 https://example.com
curl -x socks5://localhost:9050 https://example.com
```

**-U, --proxy-user <user:password>** — 代理身份验证：

```bash
curl -x proxy.example.com:8080 -U user:pass https://example.com
```

## Output Formatting

**-w, --write-out <format>** — 显示自定义信息：

```bash
curl -w "Status: %{http_code}\nTime: %{time_total}s\n" https://example.com
```

有用的格式化变量包括 `%{http_code}`, `%{time_total}`, `%{size_download}`, `%{speed_download}`。

**--compressed** — 请求压缩响应：

```bash
curl --compressed https://example.com
```

## Multiple URLs

**-Z, --parallel** — 并行处理多个 URL：

```bash
curl -Z https://example.com/file1 https://example.com/file2
```

你也可以使用花括号扩展：

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

**带有进度条的下载：**

```bash
curl -# -o file.zip https://example.com/file.zip
```

**检查网站响应时间：**

```bash
curl -w "@curl-format.txt" -o /dev/null -s https://example.com
```

其中 `curl-format.txt` 包含：

```
time_namelookup:  %{time_namelookup}s
time_connect:     %{time_connect}s
time_total:       %{time_total}s
```

这涵盖了最常用的 curl 选项。如需完整列表，请在系统中运行 `curl --help` 或 `man curl`。
