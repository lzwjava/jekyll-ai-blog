---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Gunicorn Production Deployment Guide
translated: false
type: note
---

Gunicorn (Green Unicorn) is a popular WSGI HTTP server for Python web applications. It is widely used in production to serve applications built with frameworks like Flask, Django, FastAPI, or any WSGI-compliant app. Unlike development servers (e.g., Flask's built-in server), Gunicorn is robust, efficient, and designed for real-world deployment.

---

## What is WSGI?

**WSGI** (Web Server Gateway Interface) is a Python standard (PEP 333) that defines how web servers communicate with Python web applications. Gunicorn acts as a WSGI server—it receives HTTP requests from clients (via a reverse proxy like Nginx) and passes them to your Python app.

```
Client → Nginx (reverse proxy) → Gunicorn → Your WSGI App (e.g., Flask/Django)
```

---

## Why Use Gunicorn?

| Feature | Benefit |
|-------|--------|
| **Production-ready** | Handles multiple concurrent requests efficiently |
| **Worker models** | Supports sync, async, threading, and gevent workers |
| **Pre-fork model** | Spawns worker processes to handle requests in parallel |
| **Zero-downtime reload** | Graceful restarts with `SIGHUP` |
| **Integration** | Works seamlessly with Nginx, systemd, Docker |

> **Note**: Gunicorn does **not** serve static files efficiently—use Nginx or CDN for that.

---

## Installation

```bash
pip install gunicorn
```

For async support:
```bash
pip install gunicorn[gevent]    # or [eventlet], [tornado]
```

---

## Basic Usage

### Command Line

```bash
gunicorn [OPTIONS] MODULE_NAME:VARIABLE_NAME
```

Example with Flask:
```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 run:app
```

- `run:app` → `run.py` file, `app` is the Flask/FastAPI instance
- `--workers 3` → 3 worker processes
- `--bind 0.0.0.0:8000` → listen on all interfaces, port 8000

---

## Worker Types

Gunicorn supports different worker classes depending on your app's needs:

| Worker Type | Command | Use Case |
|-----------|--------|---------|
| **sync** (default) | `gunicorn -k sync` | CPU-bound or simple apps |
| **gevent** | `gunicorn -k gevent` | High concurrency, I/O-heavy (e.g., APIs, websockets) |
| **eventlet** | `gunicorn -k eventlet` | Similar to gevent, good for async |
| **tornado** | `gunicorn -k tornado` | Real-time apps |
| **threads** | `gunicorn -k sync --threads 4` | Mixed I/O + CPU, but beware GIL |

> **Recommendation**: Use `gevent` or `eventlet` for most web APIs.

---

## Key Configuration Options

| Option | Description | Example |
|------|-------------|--------|
| `--bind` | Host and port | `--bind 0.0.0.0:8000` |
| `--workers` | Number of worker processes | `--workers 4` |
| `--worker-class` | Worker type | `-k gevent` |
| `--threads` | Threads per sync worker | `--threads 2` |
| `--timeout` | Worker timeout (seconds) | `--timeout 30` |
| `--keep-alive` | Keep-alive timeout | `--keep-alive 2` |
| `--max-requests` | Restart worker after N requests | `--max-requests 1000` |
| `--max-requests-jitter` | Randomize restart | `--max-requests-jitter 100` |
| `--preload` | Load app before forking | `--preload` (faster startup, shared memory) |
| `--log-level` | Log level | `--log-level debug` |

---

## How Many Workers?

General rule of thumb:

```text
workers = (2 × CPU cores) + 1
```

For gevent/eventlet (async):
```text
workers = number of CPU cores
threads = 100–1000 (depending on concurrency)
```

Example:
```bash
gunicorn -k gevent --workers 2 --threads 200 run:app
```

> Use `nproc` or `htop` to check CPU cores.

---

## Configuration File (`gunicorn-cfg.py`)

Instead of long CLI args, use a config file (as in your Dockerfile):

```python
# gunicorn-cfg.py
bind = "0.0.0.0:8000"
workers = 3
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
loglevel = "info"
accesslog = "-"
errorlog = "-"
preload_app = False
```

Then run:
```bash
gunicorn --config gunicorn-cfg.py run:app
```

> Your Dockerfile uses this exact pattern—**excellent practice**.

---

## Logging

Gunicorn logs access and errors:

```python
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "warning"
```

Or log to stdout (Docker-friendly):
```python
accesslog = "-"
errorlog = "-"
```

Log format:
```python
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```

---

## Graceful Reload & Zero Downtime

1. **Reload workers** (new code):
   ```bash
   kill -HUP <gunicorn_pid>
   ```

2. **Restart gracefully**:
   ```bash
   kill -TERM <gunicorn_pid>
   ```

3. **With systemd**:
   ```ini
   [Service]
   ExecReload=/bin/kill -HUP $MAINPID
   ```

---

## Running Behind Nginx (Recommended)

### Nginx Config Snippet

```nginx
upstream app_server {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://app_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static/;
    }
}
```

---

## Docker Best Practices (Your Dockerfile is Great!)

```dockerfile
FROM python:3.9
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
```

**Why this is good**:
- `PYTHONUNBUFFERED=1` → real-time logs
- `PYTHONDONTWRITEBYTECODE=1` → no `.pyc` files
- `--no-cache-dir` → smaller image
- Config file → clean CMD

**Optional improvements**:
```dockerfile
# Use non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
```

---

## Systemd Service Example

```ini
# /etc/systemd/system/gunicorn.service
[Unit]
Description=Gunicorn instance
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn \
          --config gunicorn-cfg.py \
          run:app
ExecReload=/bin/kill -HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn
```

---

## Common Issues & Debugging

| Issue | Solution |
|------|----------|
| **Worker timeout** | Increase `--timeout` or optimize code |
| **Too many open files** | Increase `ulimit -n` or use async workers |
| **Memory leaks** | Use `--max-requests` to restart workers |
| **502 Bad Gateway** | Check Gunicorn is running, port binding |
| **Slow startup** | Use `--preload` if memory allows |

---

## Monitoring

- **Logs**: Tail access/error logs
- **Metrics**: Use `prometheus-client` + Gunicorn exporter
- **Health endpoint**:
  ```python
  @app.route("/health")
  def health():
      return "OK", 200
  ```

---

## Advanced: Async Views (FastAPI Example)

```python
# run.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}
```

Run with:
```bash
gunicorn -k uvicorn.workers.UvicornWorker run:app
```

Install:
```bash
pip install "uvicorn[standard]"
```

---

## Summary Checklist

| Task | Done? |
|------|-------|
| Use config file (`gunicorn-cfg.py`) | Yes |
| Set `workers` based on CPU | Yes |
| Use async workers for I/O | Yes |
| Run behind Nginx | Yes |
| Log to stdout in Docker | Yes |
| Set timeouts & max-requests | Yes |
| Graceful reload with `HUP` | Yes |

---

## References

- [Gunicorn Official Docs](https://docs.gunicorn.org/)
- [Gunicorn Settings Reference](https://docs.gunicorn.org/en/stable/settings.html)
- [DigitalOcean Gunicorn Tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)
- [Uvicorn + Gunicorn for FastAPI](https://fastapi.tiangolo.com/deployment/server-workers/)
