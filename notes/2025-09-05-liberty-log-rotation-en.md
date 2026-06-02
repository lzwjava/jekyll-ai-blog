---
audio: false
generated: true
image: false
lang: en
layout: post
title: Liberty Log Rotation Configuration Guide
translated: false
type: note
---

Here’s the short version, then examples you can paste into `server.xml`.

### How Liberty log rotation works

* **What rotates:** `messages.log` and `trace.log`.
  Rotation can be **size-based** and/or **time-based**. ([openliberty.io][1])
* **What does not rotate:** `console.log` (it’s just stdout/stderr). You can reduce/disable it instead. ([openliberty.io][2], [IBM][3])
* **Where to configure:** the `<logging …/>` element in `server.xml`. (You can also set the same values in `bootstrap.properties`/env vars if you need them to apply *before* `server.xml` loads.) ([openliberty.io][2])
* **Access logs:** the HTTP access log has its **own** time-based rollover settings under `httpAccessLogging` / `accessLogging`. ([openliberty.io][4])
* **Both size + time:** modern Liberty supports time-based rollover in addition to the classic size-based option, so you can use either or both (except for `console.log`). ([IBM][5])

---

### Common `server.xml` recipes

#### 1) Size-based rotation (classic)

Keeps up to 10 files, each up to 256 MB.

```xml
<logging
  logDirectory="${server.output.dir}/logs"
  maxFileSize="256"
  maxFiles="10"/>
```

Effect: when `messages.log` or `trace.log` exceeds 256 MB, Liberty rolls it to a timestamped file and keeps at most 10 such files. (Doesn’t affect `console.log`.) ([openliberty.io][1])

#### 2) Time-based rotation (e.g., daily at midnight)

```xml
<logging
  rolloverStartTime="00:00"
  rolloverInterval="1d"/>
```

Effect: `messages.log` and `trace.log` roll over every day at 00:00. You can use minutes (`m`) or hours (`h`) too, e.g., `30m` or `6h`. ([openliberty.io][2])

#### 3) Combine size + time (typical production)

```xml
<logging
  logDirectory="${server.output.dir}/logs"
  maxFileSize="256"
  maxFiles="14"
  rolloverStartTime="00:00"
  rolloverInterval="1d"/>
```

Effect: roll over **whichever comes first** (size or schedule), and keep a 14-file history. ([IBM][5])

#### 4) Tame or disable `console.log` growth

`console.log` can’t rotate; reduce or turn it off and rely on `messages.log`.

```xml
<logging
  consoleLogLevel="OFF"
  copySystemStreams="false"/>
```

Notes: turning console off stops Liberty’s own log copy to `console.log`, but the JVM may still write things like `-verbose:gc` to stdout/stderr. ([openliberty.io][2])

#### 5) Name/format tweaks (optional)

```xml
<logging
  messageFileName="messages.log"
  traceFileName="trace.log"
  messageFormat="JSON"/>
```

JSON is handy for shipping to a log stack; leave defaults if you don’t need it. ([openliberty.io][1])

---

### HTTP access log (separate from the above)

Enable access logging and roll it daily at midnight:

```xml
<httpAccessLogging id="accessLogging"
  rolloverStartTime="00:00"
  rolloverInterval="1d"/>

<httpEndpoint id="defaultHttpEndpoint"
  httpPort="9080" httpsPort="9443"
  accessLoggingRef="accessLogging"/>
```

(Or put `rolloverStartTime`/`rolloverInterval` directly on an `<accessLogging …/>` child of `httpEndpoint`.) ([openliberty.io][4])

---

### Quick checklist

* Use **`maxFileSize` + `maxFiles`** for size-based rollover. ([openliberty.io][1])
* Use **`rolloverStartTime` + `rolloverInterval`** for time-based rollover. ([openliberty.io][2])
* **Don’t expect `console.log` to rotate**; set `consoleLogLevel="OFF"` and `copySystemStreams="false"` if you want to avoid large console files. ([openliberty.io][2], [IBM][3])

If you share your current `server.xml` snippet or your retention goals (e.g., “keep \~7 days” or “cap at 2 GB”), I’ll tailor the exact values.

[1]: https://openliberty.io/docs/latest/reference/config/logging.html "Logging (logging) :: Open Liberty Docs"
[2]: https://openliberty.io/docs/latest/log-trace-configuration.html "Log and trace configuration :: Open Liberty Docs"
[3]: https://www.ibm.com/support/pages/how-turn-console-logging-prevent-excess-file-growth-and-use-only-message-log-rotation-liberty-profile-or-open-liberty?utm_source=chatgpt.com "How to turn off Console logging, prevent excess file growth ..."
[4]: https://openliberty.io/docs/latest/access-logging.html "HTTP access logging :: Open Liberty Docs"
[5]: https://www.ibm.com/support/pages/how-setup-liberty-log-rollover-both-time-based-and-size-based-options-similar-traditional-websphere-0?utm_source=chatgpt.com "How to setup Liberty Log Rollover with both Time-Based ..."
