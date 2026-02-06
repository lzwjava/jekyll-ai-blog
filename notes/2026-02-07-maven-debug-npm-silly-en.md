---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Maven Debug Logging Like npm Silly
translated: false
type: note
---

Yes, Maven does have verbose logging similar to npm's silly log level, though it uses different terminology.

In Maven, you can control logging verbosity with these flags:

**`-X` or `--debug`** - This is Maven's equivalent to npm's silly/verbose logging. It shows detailed debug output including:
- Full stack traces for errors
- Detailed plugin execution information
- Dependency resolution details
- Internal Maven processes

**`-e` or `--errors`** - Shows error stack traces (less verbose than debug)

**`-q` or `--quiet`** - Minimal output, only errors

Example usage:
```bash
mvn clean install -X
```

The debug output from `-X` can be quite extensive, showing you pretty much everything Maven is doing under the hood - similar to how npm's `--loglevel silly` floods you with information.

If you need even more control over logging, Maven uses SLF4J under the hood, so you can also configure logging levels in a `simplelogger.properties` file, but the `-X` flag is usually what you want for troubleshooting, just like you'd use `npm --loglevel silly` when debugging npm issues.