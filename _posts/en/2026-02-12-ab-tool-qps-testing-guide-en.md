---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AB Tool Guide for QPS Testing
translated: false
type: note
---

Question: Provide a comprehensive introduction to AB performance testing, the AB command, the AB tool, and how to test QPS.

Answer:

**ApacheBench (ab)** is a simple, lightweight, command-line benchmarking and load testing tool included with the **Apache HTTP Server** distribution. It is designed to measure the **performance** of HTTP/HTTPS servers by sending a large number of requests and reporting key metrics.

Despite being originally created for testing Apache, **ab** works very well with **any HTTP server** (Nginx, Node.js/Express, Go, Java Spring, Python Flask/FastAPI, etc.).

### Main Purpose of ab
- Quickly estimate **how many requests per second (QPS / RPS)** your server can handle
- Measure **response latency** under different levels of concurrency
- Identify rough **breaking points** or saturation points of a single endpoint
- Compare performance before/after code or configuration changes

**ab is not** a full-featured load testing tool (compared to JMeter, Locust, k6, Gatling, wrk, etc.). It has limitations:
- Only supports **HTTP/1.0 and HTTP/1.1** (no HTTP/2 or HTTP/3)
- No advanced scripting or complex scenarios
- Single machine only (no distributed testing)
- Very simple request body support

Still, it remains extremely popular for quick smoke tests, CI/CD pipeline checks, and basic QPS validation.

### How to Install ab
Most Linux distributions include it in the `apache2-utils` or `httpd-tools` package.

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install apache2-utils

# CentOS / Rocky / AlmaLinux
sudo dnf install httpd-tools    # or yum install httpd-tools

# macOS (via Homebrew)
brew install httpd

# Windows: usually installed via XAMPP / WAMP or copy ab.exe from Apache bin folder
```

Check version:
```bash
ab -V
# ApacheBench, Version 2.3 <$Revision: ... $>
```

### Basic Usage & Core Parameters for QPS Testing
```bash
ab [options] [http[s]://]hostname[:port]/path
```

Most important options for QPS testing:

| Option       | Meaning                              | Typical usage for QPS test                  |
|--------------|--------------------------------------|---------------------------------------------|
| `-n NUMBER`  | Total requests to send               | `-n 1000` or `-n 5000` or `-n 20000`        |
| `-c NUMBER`  | Concurrency (simultaneous connections) | `-c 10`, `-c 50`, `-c 200`, `-c 500` ...   |
| `-k`         | Use HTTP Keep-Alive (very important!) | Almost always use `-k`                      |
| `-t SECONDS` | Max benchmark time (instead of -n)   | `-t 30` (run for 30 seconds)                |
| `-s SECONDS` | Socket timeout per request           | `-s 10` (default 30)                        |
| `-p FILE`    | POST data file                       | For POST/PUT requests                       |
| `-T type`    | Content-Type for POST data           | `-T application/json`                       |
| `-C cookie`  | Add Cookie header                    | `-C "session=abc123"`                       |
| `-H header`  | Custom header                        | `-H "Authorization: Bearer xyz"`            |
| `-g FILE`    | Output gnuplot-compatible data       | Useful for graphing later                   |

### Classic QPS Testing Patterns

1. **Quick smoke test** (small load)
```bash
ab -n 1000 -c 20 -k https://your-api.com/health
```

2. **Typical realistic API test**
```bash
ab -n 5000 -c 100 -k \
   -H "Authorization: Bearer eyJhb..." \
   https://api.example.com/v1/users/profile
```

3. **POST JSON test**
```bash
# Prepare postdata.json
echo '{"username":"test","password":"123456"}' > postdata.json

ab -n 2000 -c 50 -k \
   -p postdata.json -T application/json \
   https://api.example.com/login
```

4. **Find approximate max QPS**
Run several tests gradually increasing concurrency:

```bash
ab -n 10000 -c  50 -k https://...
ab -n 10000 -c 100 -k https://...
ab -n 10000 -c 200 -k https://...
ab -n 10000 -c 400 -k https://...
# ... until throughput stops growing or errors appear
```

### Understanding the Most Important Output Lines

```
Server Software:        nginx/1.24.0
Server Hostname:        example.com
Server Port:            443
SSL/TLS Protocol:       TLSv1.3,TLS_AES_256_GCM_SHA384,...

Document Path:          /api/products
Document Length:        1245 bytes

Concurrency Level:      100
Time taken for tests:   12.348 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      13250000 bytes
HTML transferred:       12450000 bytes

**Requests per second:  809.85 [#/sec] (mean)**     ← This is QPS!
**Time per request:     123.456 [ms] (mean)**       ← Average latency
**Time per request:     1.235 [ms] (mean, across all concurrent requests)**
Transfer rate:          1048.12 [Kbytes/sec] received

Percentage of the requests served within a certain time (ms)
  50%    118
  66%    125
  75%    132
  80%    138
  90%    156
  95%    189
  98%    245
  99%    312
 100%    456 (longest request)
```

Key metrics to watch:
- **Requests per second (mean)** → main QPS number
- **Time per request (mean)** → average latency seen by client
- **Failed requests** → should be 0 (or very low)
- **90%/95%/99% latency** → tail latency (very important for user experience)
- When **QPS stops growing** significantly while increasing `-c` → saturation point

### Recommendations & Best Practices
- Always use `-k` (Keep-Alive) for realistic HTTP/1.1 testing
- Run multiple times and take median/average (avoid outliers)
- Test from a machine with good network to target (low latency)
- Increase concurrency gradually until errors appear or latency spikes
- Compare same test before/after optimization
- For serious production testing → consider wrk, k6, Locust, or Gatling

**ab** remains one of the fastest ways to get a rough but useful QPS/latency picture of any HTTP endpoint.

References:

- [Official ApacheBench documentation](https://httpd.apache.org/docs/2.4/programs/ab.html)
- [Datadog guide on using ApacheBench](https://www.datadoghq.com/blog/apachebench)
- [Baeldung tutorial on load testing with ab](https://www.baeldung.com/linux/ab-apachebench-load-testing)
