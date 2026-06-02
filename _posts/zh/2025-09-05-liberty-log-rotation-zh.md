---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自由日志轮转配置指南
translated: true
type: note
---

以下是简短说明，以及可粘贴到 `server.xml` 中的配置示例。

### Liberty 日志轮转工作原理

* **轮转对象：** `messages.log` 和 `trace.log`
  支持**基于大小**和/或**基于时间**的轮转（[openliberty.io][1]）
* **不轮转对象：** `console.log`（仅为标准输出/错误流）。可通过配置减少或禁用（[openliberty.io][2], [IBM][3]）
* **配置位置：** `server.xml` 中的 `<logging …/>` 元素（相同配置也可通过 `bootstrap.properties`/环境变量设置，使其在 `server.xml` 加载前生效）（[openliberty.io][2]）
* **访问日志：** HTTP 访问日志在 `httpAccessLogging` / `accessLogging` 下有独立的基于时间轮转设置（[openliberty.io][4]）
* **双重策略：** 现代 Liberty 同时支持基于时间和基于大小的轮转方案，可单独或组合使用（`console.log` 除外）（[IBM][5]）

---

### 常用 `server.xml` 配置方案

#### 1) 基于大小的轮转（经典方案）

保留最多 10 个文件，单个文件最大 256 MB

```xml
<logging
  logDirectory="${server.output.dir}/logs"
  maxFileSize="256"
  maxFiles="10"/>
```

效果：当 `messages.log` 或 `trace.log` 超过 256 MB 时，Liberty 会将其轮转为带时间戳的文件，最多保留 10 个历史文件（不影响 `console.log`）（[openliberty.io][1]）

#### 2) 基于时间的轮转（例如每日午夜）

```xml
<logging
  rolloverStartTime="00:00"
  rolloverInterval="1d"/>
```

效果：`messages.log` 和 `trace.log` 每日 00:00 进行轮转。也可使用分钟（`m`）或小时（`h`）单位，例如 `30m` 或 `6h`（[openliberty.io][2]）

#### 3) 大小与时间组合（典型生产环境）

```xml
<logging
  logDirectory="${server.output.dir}/logs"
  maxFileSize="256"
  maxFiles="14"
  rolloverStartTime="00:00"
  rolloverInterval="1d"/>
```

效果：满足任一条件（达到大小限制或到达轮转时间）即触发轮转，并保留 14 个历史文件（[IBM][5]）

#### 4) 控制或禁用 `console.log` 增长

`console.log` 不支持轮转；可通过关闭并依赖 `messages.log` 来管理

```xml
<logging
  consoleLogLevel="OFF"
  copySystemStreams="false"/>
```

注意：关闭控制台日志仅会停止 Liberty 自身向 `console.log` 的日志复制，JVM 仍可能将 `-verbose:gc` 等信息写入标准输出/错误流（[openliberty.io][2]）

#### 5) 命名/格式调整（可选）

```xml
<logging
  messageFileName="messages.log"
  traceFileName="trace.log"
  messageFormat="JSON"/>
```

JSON 格式便于接入日志分析栈；如无特殊需求建议保持默认设置（[openliberty.io][1]）

---

### HTTP 访问日志（独立配置）

启用访问日志并设置每日午夜轮转：

```xml
<httpAccessLogging id="accessLogging"
  rolloverStartTime="00:00"
  rolloverInterval="1d"/>

<httpEndpoint id="defaultHttpEndpoint"
  httpPort="9080" httpsPort="9443"
  accessLoggingRef="accessLogging"/>
```

（也可直接将 `rolloverStartTime`/`rolloverInterval` 配置在 `httpEndpoint` 的 `<accessLogging …/>` 子元素中）（[openliberty.io][4]）

---

### 快速核查清单

* 使用 **`maxFileSize` + `maxFiles`** 实现基于大小的轮转（[openliberty.io][1]）
* 使用 **`rolloverStartTime` + `rolloverInterval`** 实现基于时间的轮转（[openliberty.io][2]）
* **不要期待 `console.log` 会轮转**；如需避免控制台文件过大，可设置 `consoleLogLevel="OFF"` 和 `copySystemStreams="false"`（[openliberty.io][2], [IBM][3]）

如需定制具体参数，请提供当前 `server.xml` 片段或留存需求（例如“保留约7天”或“总量控制在2 GB”），我将为您提供精确配置值。

[1]: https://openliberty.io/docs/latest/reference/config/logging.html "日志配置 (logging) :: Open Liberty 文档"
[2]: https://openliberty.io/docs/latest/log-trace-configuration.html "日志与跟踪配置 :: Open Liberty 文档"
[3]: https://www.ibm.com/support/pages/how-turn-console-logging-prevent-excess-file-growth-and-use-only-message-log-rotation-liberty-profile-or-open-liberty?utm_source=chatgpt.com "如何关闭控制台日志以防止文件过度增长..."
[4]: https://openliberty.io/docs/latest/access-logging.html "HTTP 访问日志 :: Open Liberty 文档"
[5]: https://www.ibm.com/support/pages/how-setup-liberty-log-rollover-both-time-based-and-size-based-options-similar-traditional-websphere-0?utm_source=chatgpt.com "如何配置同时支持基于时间和基于大小的 Liberty 日志轮转..."
