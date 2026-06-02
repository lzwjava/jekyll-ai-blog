---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Apache Bench Web Server Testing Guide
translated: false
type: note
---

### What is Apache Bench (ab)?

Apache Bench (ab) is a simple command-line tool included with Apache HTTP Server for benchmarking the performance of web servers. It sends a specified number of HTTP requests to a URL and measures metrics like requests per second, time per request, transfer rates, and error rates. It's great for quick load testing but limited for complex scenarios (e.g., no support for HTTPS by default or advanced scripting—consider tools like JMeter for those).

### Installation

ab comes bundled with Apache HTTP Server. Here's how to install it:

- **On Ubuntu/Debian (Linux)**:

  ```
  sudo apt update
  sudo apt install apache2-utils
  ```

- **On macOS (via Homebrew)**:

  ```
  brew install httpd
  ```

- **On Windows**:
  Download Apache HTTP Server from the official site and add its `bin` directory to your PATH.

- **Verify installation**:
  Run `ab -V` to check the version.

### Basic Usage

The core command syntax is:

```
ab [options] URL
```

- **URL format**: Must be a full HTTP URL, e.g., `http://example.com/`. (For HTTPS, use a wrapper like `openssl s_client` or switch to tools like `wrk`.)

Key options:

- `-n <requests>`: Number of requests to perform (default: 1). Start with 100–1000 for testing.
- `-c <concurrency>`: Number of multiple requests to make at a time (default: 1). Keep it low (e.g., 10–50) to avoid overwhelming your server.
- `-t <seconds>`: Run for a specified time instead of requests.
- `-k`: Enable HTTP Keep-Alive (reuses connections).
- `-H "Header: Value"`: Add custom headers (e.g., for authentication).
- `-p <file>`: POST data from a file.
- `-T <content-type>`: Content-type for POST requests.
- `-l`: Accept variable document lengths (for dynamic content).

### Step-by-Step Example

1. **Test a simple GET request**:
   Simulate 100 requests with 10 concurrent users against a local server:

   ```
   ab -n 100 -c 10 http://localhost:8080/
   ```

   Output sample:

   ```
   Server Software:        Apache/2.4.41
   Server Hostname:        localhost
   Server Port:            8080

   Document Path:          /
   Document Length:        1234 bytes

   Concurrency Level:      10
   Time taken for tests:   1.234 seconds
   Complete requests:      100
   Failed requests:        0
   Requests per second:    81.03 [#/sec] (mean)
   Time per request:       123.456 [ms] (mean)
   ```

2. **Test with POST data** (e.g., form submission):
   Create a `postdata.txt` file with your payload (e.g., `key=value`).

   ```
   ab -n 50 -c 5 -p postdata.txt -T application/x-www-form-urlencoded http://example.com/api/endpoint
   ```

3. **Run for a duration**:

   ```
   ab -n 10000 -c 20 -t 30 http://example.com/  # Up to 10k requests or 30 seconds
   ```

### Interpreting Results

- **Requests per second**: Higher is better (throughput).
- **Time per request**: Lower is better (latency).
- **Transfer rate**: Bandwidth efficiency.
- Watch for "Failed requests" or "Non-2xx responses" to spot issues.
- Run multiple times and average results, as caching/network can skew single runs.

### Tips and Limitations

- **Run from a separate machine**: Don't test against localhost if possible, to simulate real traffic.
- **Warm-up**: Send a few requests first to prime caches.
- **Scaling**: For higher loads, use tools like `wrk`, `siege`, or Locust.
- **HTTPS**: ab doesn't support it natively; use `ab -n 100 -c 10 http://example.com/` with a proxy or alternatives.
- **Errors**: If you see "socket: Too many open files," increase your OS file descriptor limit (e.g., `ulimit -n 4096`).

For more details, check the man page (`man ab`) or official docs.

[Apache Bench Documentation](https://httpd.apache.org/docs/2.4/programs/ab.html)
