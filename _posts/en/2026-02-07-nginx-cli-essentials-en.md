---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Nginx Command Line Essentials
translated: false
type: note
---

Nginx (pronounced "engine-x") is controlled primarily through the `nginx` command-line executable. Here's a thorough guide to its command options and how to use them effectively.

## Basic Command Syntax

```bash
nginx [-?hqTtVv] [-c file] [-g directives] [-p prefix] [-s signal]
```

## Core Command Options

**`-?` or `-h`** — Display help information about available command-line options.

**`-v`** — Show the nginx version number only.

**`-V`** — Show the nginx version, compiler version, and configuration parameters used during the build. This is extremely useful for troubleshooting and understanding what modules are compiled in.

**`-t`** — Test the configuration file syntax without starting nginx. This checks for errors in your nginx.conf and related configuration files. Always run this before reloading or restarting nginx in production.

**`-T`** — Test the configuration file and dump the entire validated configuration to standard output. This shows the final parsed configuration, which is helpful for debugging includes and understanding how nginx interprets your config.

**`-q`** — Suppress non-error messages during configuration testing. Useful in scripts when you only want to see errors.

**`-p prefix`** — Set the nginx prefix path (default is typically `/usr/local/nginx` or `/etc/nginx`). This overrides the compiled-in prefix and determines where nginx looks for configuration files and other resources.

**`-c file`** — Specify an alternative configuration file instead of the default (usually `/etc/nginx/nginx.conf`). This lets you maintain multiple configurations or test new configs.

**`-g directives`** — Set global configuration directives from the command line. These override settings in the configuration file. For example: `nginx -g "daemon off;"` runs nginx in the foreground.

**`-s signal`** — Send a signal to the nginx master process. This is the primary way to control a running nginx instance.

## Signal Options (used with `-s`)

**`nginx -s stop`** — Fast shutdown. Immediately terminates all worker processes without waiting for current requests to complete.

**`nginx -s quit`** — Graceful shutdown. Waits for worker processes to finish serving current requests before stopping.

**`nginx -s reload`** — Reload the configuration file. Nginx tests the new config, then gracefully restarts worker processes with the new configuration while maintaining service availability. This is the most common command for applying configuration changes.

**`nginx -s reopen`** — Reopen log files. Useful for log rotation, typically called after log files have been moved or renamed.

## Practical Usage Examples

**Start nginx:**

```bash
nginx
```

**Test configuration before applying changes:**

```bash
nginx -t
```

**Reload configuration after making changes:**

```bash
nginx -s reload
```

**Check nginx version and compiled modules:**

```bash
nginx -V
```

**Run nginx with a custom config file:**

```bash
nginx -c /path/to/custom/nginx.conf
```

**Run nginx in foreground (useful for containers):**

```bash
nginx -g 'daemon off;'
```

**Graceful shutdown:**

```bash
nginx -s quit
```

**View complete parsed configuration:**

```bash
nginx -T
```

## Process Management Notes

Nginx uses a master-worker process model. The master process reads configuration and manages worker processes, while workers handle actual requests. When you send signals via `nginx -s`, you're communicating with the master process, which then coordinates the workers accordingly.

For production environments, the typical workflow is: modify configuration files → run `nginx -t` to validate → run `nginx -s reload` to apply changes without downtime.

You can also send signals directly to the nginx master process using standard Unix signals (`kill` command), but using `nginx -s` is the recommended approach as it's more portable and explicit.
