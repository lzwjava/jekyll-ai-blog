---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 有争议的安卓开发观点
translated: true
type: note
---

问题：关于 Android 开发，有哪些不受欢迎或有争议的观点？

回答：

以下是一些真正不受欢迎（或至少备受争议）的观点，它们经常在 Android 社区中引发强烈反应。这些观点通常由经验丰富的开发者在 Reddit、X/Twitter、Medium 和会议上表达，即使它们被踩或遭到反对：

* **Kotlin 被过分吹捧，并且常常让代码更难阅读**
    许多资深开发者私下认为 Kotlin 的可空性、扩展函数、协程和 DSL 让许多代码库看起来像“只写”代码。他们认为 Java 更明确，并且能产出更易于维护的大型应用程序。

* **Jetpack Compose 对于简单 UI 以外的任何场景都是一个错误**
    少数人认为 Compose 的响应式模型导致不可预测的重组、糟糕的调试体验和巨大的 APK 膨胀。他们声称 XML + ViewBinding + 自定义 View 在复杂应用（银行、Uber 规模的 UI 等）中更快、性能更高且更容易理解。

* **官方 Android 文档在“Hello World”阶段之后基本无用**
    实际的 Android 开发是从 Stack Overflow、随机的 GitHub 仓库以及逆向工程 AOSP 或 Google 自己的应用中学到的，而不是从 developer.android.com。

* **Google 不关心第三方开发者**
    每年 Google 都会发布一些只有他们自己的应用（Gmail、Maps、Photos）才能实际正常使用的功能，原因包括隐藏 API、预安装权限或不合理的电池优化白名单。

* **RxJava 在大多数用例中比 Kotlin Flow/Coroutines 更好**
    惊人数量的资深开发者怀念 RxJava 丰富的操作符、背压处理和可测试性，并认为 Flow 是一个半成品替代品，之所以胜出只是因为 Google 推广它。

* **MVVM 是一种糟糕的架构，并且已经毁了 Android 代码库**
    强行分离成 ViewModel → Repository → UseCase → DataSource 的链式结构造成了样板代码地狱和间接性噩梦。许多人认为干净的 MVC 或 MVI（具有单向数据流）更优越。

* **Fragment 仍然是构建复杂 UI 的正确方法；单 Activity 架构只是一种时尚**
    多 Activity + Fragment 比当前“一个巨大的 Activity 带一个 NavGraph”的信条更模块化且内存效率更高。

* **Dagger/Hilt 是不必要的复杂性**
    对于 80-90% 的应用程序来说，手动依赖注入或轻量级库（Koin、Codgen）比 Dagger 的注解处理地狱更快且痛苦少得多。

* **大多数 Android 开发者不再能编写高性能代码**
    转向 Kotlin + Compose + 协程很好地隐藏了垃圾回收和线程问题，以至于初级开发者（和许多资深开发者）不再理解内存、线程或视图系统——直到应用开始在大规模使用时卡顿。

* **Firebase 是一个陷阱**
    它会把你锁定在 Google 生态中，扼杀你的后端技能，并且一旦流量增加就会变得异常昂贵。自托管或其他 BaaS 解决方案从长远来看更好。

* **在 2025 年，使用 Flutter 或 React Native 编写应用程序通常比原生 Android 更好**
    特别是对于初创公司和非 Google Play 独占应用。生态系统的碎片化、Google 不断变化的 API 以及“原生”优势的缩小使得跨平台不再像五年前那样是一种妥协。

这些观点确实不受欢迎——如果你在大多数 Android 子版块或 Slack 群组中大声说出来，你会被踩到无底深渊——但它们被相当数量身经百战的资深 Android 工程师所持有。
