---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 飞行试验作为工程系统
translated: true
type: note
---

**是的。实际上，我会把这当作一个工程系统来对待，而不仅仅是“录一些视频”。**

对于像大疆（DJI）这类飞控/无人机公司来说，有价值的知识往往是**程序性的和视觉化的**：

*   正常测试是什么样的？
*   危险的振荡看起来/听起来是什么样的？
*   操作员在故障发生前立即做了什么？
*   同一时刻遥测数据显示了什么？
*   当时的环境条件是什么？
*   哪些调试步骤是有效的？
*   哪些“明显”的修复被证明是错误的？
*   有经验的测试工程师能注意到哪些新工程师注意不到的地方？

笔记本记录的是**人们记得的东西**。
视频记录的是**实际发生的事情**。
遥测数据记录的是**机器的行为**。
照片记录的是**物理构型/环境**。

真正的价值来自于将它们整合在一起。

### 我会围绕每个有意义的测试构建一个“试飞案例”

例如：

```text
flight-tests/
  2026-09-15/
    FT-2026-0915-037/
      manifest.yaml
      briefing.md
      preflight/
        aircraft.jpg
        propellers.jpg
        wiring.jpg
        payload.jpg
      video/
        ground-camera.mp4
        onboard-camera.mp4
      telemetry/
        flight.ulg
        flight.csv
      audio/
        radio.wav
      photos/
        site-01.jpg
        aircraft-after-flight.jpg
      debrief.md
      incidents.md
      analysis/
        plots.png
        analysis.ipynb
```

而 `manifest.yaml` 包含机器可读的上下文：

```yaml
test_id: FT-2026-0915-037
aircraft: A17
firmware: fc-2.8.14
controller: position-controller-v4
battery: B204
operator: engineer-042

objective:
  - validate position hold after controller change

environment:
  wind_mps: 7.2
  temperature_c: 23
  location: TEST_SITE_A

software_changes:
  - "increase yaw damping from 0.12 to 0.15"

result: PASS_WITH_NOTES
```

那么，汇报总结不应该是长篇大论。可以这样：

```markdown
# FT-2026-0915-037

## Objective
Validate position hold after yaw damping change.

## Result
PASS_WITH_NOTES

## What happened

00:00:00 - preflight
00:03:21 - takeoff
00:04:10 - position hold enabled
00:04:17 - small yaw oscillation begins
00:04:23 - oscillation disappears
00:06:02 - landing

## Observations

- Yaw response is noticeably faster than previous firmware.
- Small oscillation appears only during first transition.
- No safety issue observed.

## Evidence

- `video/ground-camera.mp4`
- `telemetry/flight.ulg`
- `photos/aircraft-after-flight.jpg`

## Engineer interpretation

Likely transient caused by the new damping parameter interacting
with the position-hold transition.

## Follow-up

Repeat with:
- 4 m/s wind
- 10 m/s wind
- old firmware as control

## Lessons

Do not judge the parameter solely from steady-state behavior.
The transition is where the new behavior appears.
```

这样，你就创造了一些比“John在笔记本上写了这架无人机有点怪”更强大的东西。

### 重要的是：使用时间同步所有内容

我认为这是系统真正变得有价值的地方。

想象一下，一个未来的工程师问：

> “我们为什么不再使用v4.2控制器了？”

而不是在Slack里搜索三个小时：

```text
Controller v4.2
       │
       ├── 17 flight tests
       │
       ├── 3 anomalies
       │
       ├── FT-2025-0821-014
       │       ├── video.mp4
       │       ├── telemetry.ulg
       │       ├── photos/
       │       └── debrief.md
       │
       └── conclusion
             "unstable during high-wind transition"
```

他们几乎可以直接在观看遥测数据的同时，看到失败的过程。

这就是**组织记忆**。

### 并且不要只记录失败

这是一个微妙但重要的观点。

你需要：

```text
GOOD flight
BAD flight
EDGE CASE
RECOVERY
NORMAL PROCEDURE
EXPERIMENT
```

否则，知识库就会变成“灾难博物馆”。

新工程师需要看到：

> “这是正确的飞行前检查的样子。”

以及：

> “这是错误的样子。”

视频对于**隐性知识**尤其有用。

例如，一位经验丰富的工程师可能会说：

> “电机声音听起来有点不对。”

这作为文本几乎没有用处。

但如果你有：

```text
normal_motor.wav
vs
bearing_problem_001.wav
```

并且有经验的工程师解释：

> “听00:13左右。这个谐波在正常运行时是不存在的。”

你就把隐性知识转化成了可以教授的东西。

### 我实际上会捕获4个层面

把公司的知识想象成：

```text
                 COMPANY KNOWLEDGE
                        │
          ┌─────────────┼─────────────┐
          │             │             │
       MACHINE       HUMAN          CONTEXT
          │             │             │
      telemetry       video       environment
      logs            voice       configuration
      sensors         actions     photos
      firmware        decisions   test setup
          │             │             │
          └─────────────┼─────────────┘
                        │
                    TEST CASE
                        │
                  ENGINEERING
                   CONCLUSION
                        │
                   KNOWLEDGE
```

**测试用例**是原子单位。

不是：

```text
random videos/
random photos/
random PDFs/
random Notion pages/
```

而是：

```text
test case
  ├── machine evidence
  ├── human evidence
  ├── environmental evidence
  ├── conclusion
  └── follow-up
```

### 然后，在上面加一个AI层

这对于一家AI原生的公司来说尤其有趣。

一旦你有了成千上万个这样的数据：

```text
10,000 flights
50,000 hours of video
10 TB telemetry
thousands of incident reports
firmware history
hardware revisions
test procedures
```

你就可以建立一个内部工程智能体。

工程师：

> “我们以前见过这种偏航振荡吗？”

智能体：

```text
Found 23 related flight tests.

Most similar:
  FT-2026-0412-008
  similarity: 0.91

Observed behavior:
  yaw oscillation during position-hold transition

Relevant configuration:
  firmware 2.7.x
  wind 6–8 m/s

Resolution:
  reduced transition gain by 12%

Evidence:
  00:04:17–00:04:31 in ground video
  telemetry channels yaw_rate / desired_yaw_rate

Related engineers:
  ...
```

这就是你“记录一切”的理念转化为**复利工程资产**的时候。

关键是**不要把存储与知识管理混为一谈**。

将10,000个视频录制到S3存储桶中并不是知识。

流程应该是：

```text
TEST
 ↓
CAPTURE
 ↓
SYNC
 ↓
ANNOTATE
 ↓
DEBRIEF
 ↓
LINK TO HARDWARE/FIRMWARE/CONFIG
 ↓
STORE
 ↓
INDEX
 ↓
SEARCH
 ↓
AI RETRIEVAL
 ↓
NEW ENGINEER
 ↓
KNOWLEDGE COMPOUNDS
```

而另一个主要好处是：**人员离职时，不会把整个组织的记忆带走。**

这可能是硬件/机器人公司早期可以构建的ROI最高的东西之一。

我还可以画出一个具体的**“试飞知识系统”架构**——摄像头 + 遥测 + 存储 + 元数据模式 + 自动视频/遥测索引 + RAG/智能体层——主要使用开源组件。