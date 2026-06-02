---
audio: false
generated: true
lang: zh
layout: post
title: Java日期与时间操作指南
translated: true
type: note
---

### 核心要点
- 要使用 `org.joda.time`，可能需要将其添加到 Java 项目并导入相关类以进行日期时间操作。
- 研究表明可通过 Maven 引入 2.13.1 版本库，或下载 JAR 文件后使用 `DateTime`、`LocalDate` 等类。
- 证据表明 Joda-Time 适用于处理时区、日历系统和时间间隔，例如创建日期对象并进行修改。

### 什么是 Joda-Time 及其配置方法
Joda-Time 是 Java 中处理日期时间的库，在 Java 8 之前尤为实用，它提供了直观的 API 以替代旧版线程安全性较差的 `Date` 和 `Calendar` 类。使用时需先在项目中引入该库。若使用 Maven，请在 `pom.xml` 中添加以下依赖：
```xml
<dependency>
    <groupId>joda-time</groupId>
    <artifactId>joda-time</artifactId>
    <version>2.13.1</version>
</dependency>
```
也可从[该网站](https://www.joda.org/joda-time/download.html)下载 JAR 文件，并将其添加到项目的类路径中，例如在 Eclipse 中创建 "libs" 文件夹并通过项目属性链接 JAR。

### 基础使用示例
配置完成后，导入 `org.joda.time.DateTime` 或 `org.joda.time.LocalDate` 等类。以下是一些示例：
- 创建当前日期时间：`DateTime now = new DateTime();`
- 访问字段：`int year = now.getYear(); String monthName = now.monthOfYear().getAsText();`
- 修改：`DateTime future = now.plusDays(5);`

### 高级功能
Joda-Time 支持时区（例如 `DateTimeZone.forID("America/New_York")`）和不同日历系统（例如通过 `CopticChronology.getInstance()` 使用科普特历）。它还支持处理时间间隔和持续时间，例如 `Interval interval = new Interval(startDt, endDt);`。

一个值得注意的细节是，Joda-Time 被视为“已完成”的项目，Java 8 的 `java.time` 包被推荐用于新项目，但在遗留系统或特定需求中它仍然适用。

---

### 调研笔记：使用 `org.joda.time` 的完整指南

本节详细探讨如何使用 `org.joda.time` 库，在直接答案的基础上扩展了额外背景和技术深度，适合需要全面理解的开发者。内容包括配置方法、使用示例、关键特性及进一步资源，确保为实现提供完整参考。

#### Joda-Time 简介
Joda-Time 由 joda.org 开发，是一个广泛使用的日期时间处理库，尤其在 Java 8 发布之前。它通过使用不可变类解决了 Java `Date` 和 `Calendar` 类的设计问题，例如线程安全性担忧。在 Java 8 之前，`Date` 类和 `SimpleDateFormatter` 并非线程安全，且诸如日/月/年偏移等操作反直觉（例如天数从 0 开始，月份从 1 开始，需使用 `Calendar`）。Joda-Time 提供了清晰、流畅的 API，并支持八种日历系统，而 Java 仅支持两种（公历和日本历法）。Java 8 之后，作者认为 Joda-Time 基本已完成，推荐新项目迁移至 `java.time`（JSR-310），但在遗留系统或特定用例中仍具价值。

#### 配置 Joda-Time
使用 Joda-Time 前，需先将其引入 Java 项目。截至 2025 年 3 月 3 日，最新版本为 2.13.1，确保稳定性和与 JDK 1.5 或更高版本的兼容性。Maven 用户请在 `pom.xml` 中添加以下依赖：
```xml
<dependency>
    <groupId>joda-time</groupId>
    <artifactId>joda-time</artifactId>
    <version>2.13.1</version>
</dependency>
```
可在 [Maven 仓库](https://mvnrepository.com/artifact/joda-time/joda-time) 找到。非 Maven 项目请从[该网站](https://www.joda.org/joda-time/download.html)下载 `.tar.gz` 文件，解压后将 `joda-time-2.13.1.jar` 添加到项目的类路径中。例如在 Eclipse 中，创建 "libs" 文件夹，复制 JAR 文件，并通过属性 -> Java 构建路径 -> 库 -> 添加 JAR 进行链接。使用 `DateTime test = new DateTime();` 测试配置以确保功能正常。

#### 基础使用及示例
引入后，从 `org.joda.time` 导入类，如 `DateTime`、`LocalDate`、`LocalTime` 和 `LocalDateTime`，这些类均为不可变以确保线程安全。以下是详细示例：

- **创建日期时间对象：**
  - 从当前时间：`DateTime now = new DateTime();` 使用默认时区和 ISO 日历。
  - 从 Java `Date`：`java.util.Date juDate = new Date(); DateTime dt = new DateTime(juDate);` 以实现互操作性。
  - 从特定值：构造函数接受 `Long`（毫秒）、`String`（ISO8601）或其他 Joda-Time 对象，例如 `DateTime dt = new DateTime(2025, 3, 3, 8, 39);`。

- **访问字段：**
  - 使用 getter 方法：`int year = now.getYear(); int month = now.getMonthOfYear();` 其中一月为 1，十二月为 12。
  - 获取文本表示：`String dayName = now.dayOfWeek().getAsText();` 输出如 2025 年 3 月 3 日的 "Monday"。
  - 检查属性：`boolean isLeap = now.year().isLeap();` 对 2025 年返回 `false`。

- **修改日期时间：**
  - 创建修改后的新实例：`DateTime newDt = now.withYear(2025);` 或 `DateTime future = now.plusDays(5);`。
  - 添加持续时间：`DateTime later = now.plusHours(2);` 用于添加两小时，返回新实例。

GeeksforGeeks 的一个实用示例说明用法：
```java
import org.joda.time.DateTime;
import org.joda.time.LocalDateTime;
public class JodaTime {
    public static void main(String[] args) {
        DateTime now = new DateTime();
        System.out.println("当前日期: " + now.dayOfWeek().getAsText());
        System.out.println("当前月份: " + now.monthOfYear().getAsText());
        System.out.println("当前年份: " + now.year().getAsText());
        System.out.println("当前年份是否为闰年: " + now.year().isLeap());
        LocalDateTime dt = LocalDateTime.now();
        System.out.println(dt);
    }
}
```
对于 2025 年 3 月 3 日，输出可能包括 "当前日期: Monday"、"当前月份: March"、"当前年份: 2025"、"当前年份是否为闰年: false" 以及类似 "2025-03-03T08:39:00.000" 的时间戳。

#### 关键特性及高级用法
Joda-Time 为复杂日期时间操作提供了强大功能，详细如下：

- **时区：**
  - 通过 `DateTimeZone` 管理，支持命名时区（例如 "Asia/Tokyo"）和固定偏移。示例：
    ```java
    DateTimeZone zone = DateTimeZone.forID("America/New_York");
    DateTime nyTime = new DateTime(zone);
    ```
  - 默认时区与 JDK 一致，但可通过 `DateTimeZone.setDefault(zone);` 覆盖。时区数据每年手动更新数次，基于 [global-tz](https://github.com/JodaOrg/global-tz)。

- **日历系统：**
  - 支持七种系统：佛历、科普特历、埃塞俄比亚历、公历、公历-儒略历、伊斯兰历、儒略历，并可自定义系统。示例：
    ```java
    Chronology coptic = CopticChronology.getInstance();
    LocalDate copticDate = new LocalDate(coptic);
    ```
  - 默认为 ISO 日历，1583 年之前历史精度不足，但适用于现代民用场景。

- **间隔、持续时间和周期：**
  - `Interval`：表示时间范围，半开区间（起点包含，终点不包含），例如 `Interval interval = new Interval(startDt, endDt);`。
  - `Duration`：精确的毫秒时间，例如 `Duration duration = new Duration(interval);`，适用于添加到时间点。
  - `Period`：以字段（年、月、日等）定义，毫秒不精确，例如 `Period period = new Period(startDt, endDt);`。示例差异：在夏令时添加 1 天（例如 2005-03-26 12:00:00），使用 `plus(Period.days(1))` 添加 23 小时，而 `plus(new Duration(24L*60L*60L*1000L))` 添加 24 小时，凸显周期与持续时间的区别。

快速入门指南提供了总结主要类和用例的表格：
| **方面**                  | **详情**                                                                                     |
|---------------------------|----------------------------------------------------------------------------------------------|
| **主要日期时间类**         | Instant、DateTime、LocalDate、LocalTime、LocalDateTime（5 个类，均不可变）                   |
| **Instant 用例**           | 事件时间戳，无日历系统或时区                                                                 |
| **LocalDate 用例**         | 出生日期，无需具体时间                                                                       |
| **LocalTime 用例**         | 一天中的时间，例如店铺开关门时间，无日期                                                     |
| **DateTime 用例**          | 通用用途，替代 JDK Calendar，包含时区信息                                                    |
| **构造函数类型**           | 对象构造函数接受：Date、Calendar、String（ISO8601）、Long（毫秒）、Joda-Time 类              |
| **示例转换**               | `java.util.Date` 转 `DateTime`：`DateTime dt = new DateTime(new Date());`                    |
| **字段访问方法**           | `getMonthOfYear()`（1=一月，12=十二月）、`getYear()`                                          |
| **修改方法**               | `withYear(2000)`、`plusHours(2)`                                                             |
| **属性方法示例**           | `monthOfYear().getAsText()`、`monthOfYear().getAsShortText(Locale.FRENCH)`、`year().isLeap()`、`dayOfMonth().roundFloorCopy()` |
| **默认日历系统**           | ISO 日历系统（事实上的民用日历，1583 年前历史精度不足）                                       |
| **默认时区**               | 与 JDK 默认相同，可覆盖                                                                      |
| **Chronology 类**          | 支持多种日历系统，例如 `CopticChronology.getInstance()`                                      |
| **时区示例**               | `DateTimeZone zone = DateTimeZone.forID("Asia/Tokyo");`、`GJChronology.getInstance(zone)`    |
| **Interval 类**            | `Interval` - 保存开始和结束日期时间，基于范围的操作                                          |
| **Period 类**              | `Period` - 保存如 6 个月、3 天、7 小时的周期，可从间隔派生                                   |
| **Duration 类**            | `Duration` - 精确的毫秒持续时间，可从间隔派生                                                |
| **周期与持续时间示例**     | 在夏令时添加 1 天（2005-03-26 12:00:00）：`plus(Period.days(1))` 添加 23 小时，`plus(new Duration(24L*60L*60L*1000L))` 添加 24 小时 |

一个有趣的细节是对象构造函数的可扩展性，允许直接传递 JDK `Date` 或 `Calendar` 进行转换，简化了从遗留代码迁移的过程。

#### 进一步学习与资源
如需深入探索，请参考官方文档 [Joda-Time 用户指南](https://www.joda.org/joda-time/userguide.html)，其中涵盖了格式化和解析等高级主题。快速入门指南 [Joda-Time 快速入门](https://www.joda.org/joda-time/quickstart.html) 提供了简洁介绍。其他教程可在 [Baeldung Joda-Time](https://www.baeldung.com/joda-time) 和 [GeeksforGeeks Joda-Time](https://www.geeksforgeeks.org/joda-time/) 找到，包含代码示例和配置说明。API 文档 [Joda-Time API 文档](https://www.joda.org/joda-time/apidocs/index.html) 适用于技术参考，但更为专业。

#### 结论
Joda-Time 为日期时间操作提供了强大、线程安全的替代方案，广泛支持时区、日历系统和时间计算。尽管在 Java 8 之后被视为已完成，但在遗留系统中仍具价值，可通过 Maven 或手动引入 JAR 进行配置，并通过 `DateTime` 和 `LocalDate` 等不可变类使用。本指南确保开发者拥有从基础示例到高级功能的所有必要信息，并辅以全面资源支持。

### 关键引用
- [Joda-Time 主页及通用信息](https://www.joda.org/joda-time/)
- [Joda-Time 快速入门指南](https://www.joda.org/joda-time/quickstart.html)
- [Baeldung Joda-Time 使用教程](https://www.baeldung.com/joda-time)
- [GeeksforGeeks Joda-Time 示例文章](https://www.geeksforgeeks.org/joda-time/)
- [Joda-Time 用户指南详细参考](https://www.joda.org/joda-time/userguide.html)
- [Joda-Time 下载与安装页面](https://www.joda.org/joda-time/download.html)
- [Maven 仓库 Joda-Time 依赖](https://mvnrepository.com/artifact/joda-time/joda-time)
- [Joda-Time API 文档技术参考](https://www.joda.org/joda-time/apidocs/index.html)
