---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在IntelliJ IDEA中查看JAR源码
translated: true
type: note
---

在 IntelliJ IDEA 中，您可以轻松查看 JAR 文件的源代码。根据 JAR 文件是否包含源文件或仅包含编译后的 `.class` 文件，有几种不同的方法：

---

### 1. 在 IDEA 中直接打开 JAR

* 前往 **文件 > 打开…**
* 选择 JAR 文件
* IDEA 会将其作为常规归档文件在 **项目视图** 中打开
* 若 JAR 包含 `.java` 源文件，可直接浏览
* 若仅包含 `.class` 文件，IDEA 会自动将其反编译为可读的 Java 代码

---

### 2. 为库 JAR 附加源码

若 JAR 属于项目依赖库（如 Maven 或 Gradle 依赖）：

* 前往 **文件 > 项目结构 > 库**（或模块级配置：**模块 > 依赖项**）
* 选择目标 JAR
* 点击 **附加源码…** 并指定对应的 `-sources.jar` 文件（如有）
* 此后 IDEA 将显示原始源码而非反编译的字节码

---

### 3. 快速导航

* 按住 **Ctrl（macOS 为 Cmd）** 并点击来自 JAR 的类或方法
* 若未附加源码，IDEA 将显示反编译版本
* 若已附加源码，您将看到原始 Java 代码

---

### 4. 外部反编译器插件（可选）

IDEA 已内置反编译器，但您也可以安装 **Fernflower** 或 **CFR** 等插件来获得替代反编译方案

---

👉 通常对于 Maven/Gradle 管理的依赖，IDEA 会自动从仓库下载并附加 `-sources.jar`。若是独立 JAR 文件，则需要手动附加源码或依赖反编译器功能。

您是否需要进一步了解 **如何在 IDEA 外部提取 JAR 源码**（使用 `jd-gui` 或 `jar xf` 等工具），还是主要关注在 IDEA 内的操作方式？
