---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 移动开发的100个核心学习点
translated: true
type: note
---

为了帮助你准备**移动应用开发技术（课程代码：14567）**考试，我根据教学大纲整理了 100 个核心知识点。这些知识点被划分为逻辑模块，以匹配国家自考的结构。

问题：你能提供中国高等教育自学考试“移动应用开发技术”（14567）课程的 100 个核心知识点吗？

回答：

### 模块 1：导论与环境 (1-10)

1. **Mobile Development 定义：** 为手持设备创建软件的过程。
2. **Native Apps：** 专门为特定平台构建的应用（例如使用 Java/Kotlin 开发 Android 应用）。
3. **Web Apps：** 在浏览器中运行的针对移动端优化的网站。
4. **Hybrid Apps：** 包装在原生容器中的 Web 应用（例如使用 Cordova）。
5. **Cross-Platform Frameworks：** 像 Flutter 或 React Native 这样使用一套代码库支持多个 OS 的工具。
6. **Android OS 架构：** 由 Linux Kernel、Hardware Abstraction Layer (HAL)、Native Libraries/Android Runtime、Java API Framework 和 System Apps 组成。
7. **ART vs. Dalvik：** ART (Android Runtime) 使用 ahead-of-time (AOT) 编译以获得更好的性能。
8. **JDK (Java Development Kit)：** 编译基于 Java 的 Android 应用所必需的工具包。
9. **Android Studio：** 官方的集成开发环境 (IDE)。
10. **ADB (Android Debug Bridge)：** 用于与模拟器或设备通信的命令行工具。

---

### 模块 2：Android 核心组件 (11-25)

11. **Activity：** 代表一个具有用户界面的单一屏幕。
12. **Service：** 在后台运行以执行长时间运行的操作（无 UI）。
13. **Broadcast Receiver：** 响应系统范围内的广播通知。
14. **Content Provider：** 管理对中央数据仓库的访问。
15. **Intent：** 一种异步消息，用于请求另一个组件执行操作。
16. **Explicit Intent（显式意图）：** 通过名称指定要启动的确切组件。
17. **Implicit Intent（隐式意图）：** 声明要执行的一般操作，让系统寻找匹配项。
18. **Activity 生命周期：** 状态包括 onCreate, onStart, onResume, onPause, onStop, onRestart, 和 onDestroy。
19. **Fragment：** Activity 用户界面中模块化的部分。
20. **Fragment 生命周期：** 包括特定的回调，如 onAttach 和 onCreateView。
21. **Context：** 访问应用程序环境全局信息的接口。
22. **The Manifest File (AndroidManifest.xml)：** 描述应用组件、权限和硬件要求的重要文件。
23. **R.java：** 自动生成的文件，作为项目中所有资源的索引。
24. **Resources 文件夹 (res/)：** 包含布局 (layout/)、字符串 (values/) 和图像 (drawable/)。
25. **Task Backstack：** Activity 的“后进先出”(LIFO) 堆栈。

---

### 模块 3：UI 设计与布局 (26-45)

26. **View：** UI 组件（widgets）的基本构建块。
27. **ViewGroup：** 包含其他 View 的不可见容器（layouts）。
28. **LinearLayout：** 水平或垂直排列子元素。
29. **RelativeLayout：** 相对于彼此或父元素定位视图。
30. **ConstraintLayout：** 允许在不嵌套的情况下构建复杂布局；使用约束进行定位。
31. **FrameLayout：** 旨在屏蔽屏幕上的一个区域以显示单个项目。
32. **TableLayout：** 将元素排列成行和列。
33. **Match_parent：** 视图扩展以匹配其父级的大小。
34. **Wrap_content：** 视图仅根据包含内容所需的程度进行扩展。
35. **dp (Density-independent Pixels)：** 用于布局尺寸，以确保屏幕密度无关性。
36. **sp (Scale-independent Pixels)：** 用于字体大小（遵循用户设置）。
37. **TextView：** 向用户显示文本。
38. **EditText：** 用于用户输入的文本字段。
39. **Button：** 点击时触发操作。
40. **ImageView：** 显示图像资源。
41. **CheckBox/RadioButton：** 用于从列表中选择选项。
42. **ListView：** 显示垂直滚动的项目列表（较旧）。
43. **RecyclerView：** ListView 的进阶版本，用于处理大数据集，更加灵活。
44. **Adapter：** 连接 UI 组件和数据源的桥梁。
45. **Event Listeners：** 处理用户交互的接口，如 `OnClickListener`。

---

### 模块 4：数据存储 (46-60)

46. **SharedPreferences：** 以键值对形式存储少量原始数据。
47. **Internal Storage：** 存储在设备文件系统中的私有数据。
48. **External Storage：** 共享文件（SD 卡或公共文件夹）。
49. **SQLite Database：** 用于结构化数据的轻量级关系型数据库。
50. **SQLiteOpenHelper：** 用于管理数据库创建和版本管理的辅助类。
51. **CRUD 操作：** Create (创建), Read (读取), Update (更新), Delete (删除)。
52. **Cursor：** 提供对数据库查询返回的结果集进行读写访问的对象。
53. **Room Persistence Library：** SQLite 之上的抽象层，用于更轻松地访问数据库。
54. **Content URIs：** Content Providers 用来标识数据的字符串。
55. **Asset Manager：** 用于访问随应用打包的原始文件（assets/ 文件夹）。
56. **JSON (JavaScript Object Notation)：** 常用的数据交换格式。
57. **XML Parsing：** 解析 XML 格式的数据。
58. **GSON/Jackson：** 用于在 Java 对象与 JSON 之间转换的库。
59. **SQL Injection：** 将恶意代码插入查询的安全风险。
60. **Permissions：** 在 Manifest 中声明以访问敏感数据（如 READ_CONTACTS）。

---

### 模块 5：网络与服务 (61-75)

61. **HTTP/HTTPS：** 用于网络通信的协议。
62. **Retrofit：** Android 中流行的类型安全 HTTP 客户端。
63. **Volley：** 旨在使 Android 网络操作更轻松、更快速的网络库。
64. **RESTful API：** 网络应用的一种架构风格。
65. **AsyncTask：** （已过时但常考）用于执行后台操作并在 UI 线程发布结果的类。
66. **Main Thread (UI Thread)：** 所有 UI 操作必须发生的线程。
67. **NetworkOnMainThreadException：** 当尝试在 UI 线程上进行网络操作时发生的异常。
68. **Handler/Looper：** 用于线程间通信。
69. **WorkManager：** 推荐用于持久性后台工作的工具。
70. **Broadcast Intents：** 由系统（如“电量低”）或应用发送。
71. **Sticky Broadcast：** 完成后仍驻留的广播（出于安全原因已弃用）。
72. **NotificationManager：** 管理状态栏通知的系统服务。
73. **PendingIntent：** 交给外部应用的令牌，允许其使用你应用的权限执行预定义代码。
74. **Foreground Service：** 用户能明显感知到的服务（显示通知）。
75. **Bound Service：** 允许其他组件绑定并与之交互的服务。

---

### 模块 6：多媒体与传感器 (76-85)

76. **MediaPlayer：** 用于播放音频和视频文件。
77. **SurfaceView：** 用于在 UI 线程之外绘制图形或播放视频。
78. **Camera API / CameraX：** 用于拍摄照片和视频的工具。
79. **SensorManager：** 访问设备传感器的系统服务。
80. **Accelerometer（加速度计）：** 测量作用于设备的加速度。
81. **Gyroscope（陀螺仪）：** 测量设备绕轴旋转的速率。
82. **GPS (Global Positioning System)：** 用于位置追踪。
83. **LocationManager：** 提供对系统位置服务的访问。
84. **Geocoding：** 将地址转换为地理坐标。
85. **Runtime Permissions：** 应用运行时请求的权限（Android 6.0+）。

---

### 模块 7：高级概念与优化 (86-100)

86. **Material Design：** Google 的设计语言，旨在实现一致的 UI/UX。
87. **WebView：** 在应用内显示网页的视图。
88. **ProGuard/R8：** 用于收缩、优化和混淆代码的工具。
89. **Memory Leak（内存泄漏）：** 当对象不再使用但仍被引用，导致无法进行垃圾回收时发生。
90. **ANR (Application Not Responding)：** 当 UI 线程阻塞时间过长（通常为 5 秒）时显示的对话框。
91. **Unit Testing：** 测试单个组件（JUnit）。
92. **Instrumented Testing：** 在真实设备/模拟器上测试 UI 和组件（Espresso）。
93. **Gradle：** Android Studio 使用的构建自动化系统。
94. **APK (Android Package)：** 用于分发和安装应用的文件格式。
95. **App Bundle (.aab)：** 现代发布格式，可针对不同设备优化 APK 生成。
96. **Signing an App：** 发布应用所必需的，用以确保作者身份。
97. **MVC/MVP/MVVM：** 组织代码逻辑和 UI 的架构模式。
98. **Jetpack：** 帮助开发者遵循最佳实践的一套库。
99. **Version Control (Git)：** 管理源代码变更。
100. **Deployment：** 将应用提交到 Google Play 或 Huawei AppGallery 等商店的过程。

参考资料：

* [Android Developer Fundamentals](https://www.google.com/search?q=https://developer.android.com/courses/fundamentals-training/overview-v2)
* [国家教育考试院自学考试指导](https://www.neea.edu.cn/)