---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: WorkManager实现可靠的Android后台任务
translated: true
type: note
---

WorkManager 是一个用于 Android **可延期、有保障的后台工作**的库。它是 Google 推荐的解决方案，适用于需要可靠运行的任务，即使用户离开您的应用或设备重启。

以下是 WorkManager 成为首选方案的原因及其如何处理网络可用性等约束条件的解析：

-----

## 🛠️ 核心概念与优势

### 1. 可延期性

WorkManager 允许您将工作**推迟**到满足特定条件时执行（例如网络可用）。您定义任务运行的*时间*和*方式*，WorkManager 负责调度安排。它**不适用于**实时操作或需要在应用处于前台时立即执行的任务。

### 2. 执行保障性

这是最关键的特性。WorkManager 将您的工作请求存储在内部数据库中，确保工作**必定会被执行**，即使：

* 用户退出应用
* 应用进程被终止
* 设备重启

### 3. 兼容不同 API 与设备

WorkManager 会根据设备的 API 级别和当前状态，选择最合适的方式运行您的任务，底层使用 **JobScheduler**（API 23+）或 **AlarmManager** 与 **BroadcastReceivers**（旧版本）。您只需编写一次代码，WorkManager 即可确保其在不同 Android 版本上正确运行。

### 4. 约束条件支持

您可以定义工作运行前必须满足的**约束条件**。这对于高效利用电池和确保可靠执行至关重要。

-----

## 📶 处理网络与其他约束条件

使用 `Constraints` 构建器来定义执行条件。

| 约束条件 | 描述 | 使用场景示例 |
| :--- | :--- | :--- |
| **`setRequiredNetworkType()`** | 需要特定类型的网络连接。 | 仅在 **Wi-Fi** 环境下上传高清视频。 |
| **`setRequiresCharging()`** | 需要设备处于充电状态。 | 仅在**充电时**运行数据备份或同步。 |
| **`setRequiresDeviceIdle()`** | 需要设备处于空闲状态（例如在 Doze 模式）。 | 低优先级的日志文件清理。 |
| **`setRequiresStorageNotLow()`** | 需要设备存储空间充足。 | 下载大文件。 |

### 网络约束示例

要确保任务仅在**任何**网络连接可用时（Wi-Fi 或移动数据）运行，您可以这样构建约束条件：

```kotlin
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED) // 仅在网络可用时执行工作
    .build()

val workRequest = OneTimeWorkRequest.Builder(MyUploadWorker::class.java)
    .setConstraints(constraints)
    .build()

WorkManager.getInstance(context).enqueue(workRequest)
```

WorkManager 会持续监控网络状态。如果初始时网络不可用，它会**等待**并在连接建立的瞬间自动执行任务，确保工作在其条件满足后**必定完成**。

-----

您是否需要查看 WorkManager 定期运行任务的简要代码示例？
