---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: 100 Key Mobile Development Study Points
translated: false
type: note
---

To help you prepare for the **Mobile Application Development Technology (Course Code: 14567)** exam, I have organized 100 essential knowledge points based on the syllabus. These are divided into logical modules to match the structure of the national self-study examination.

Question: Can you provide 100 key knowledge points for the China National Higher Education Self-Study Examination course "Mobile Application Development Technology" (14567)?

Answer:

### Module 1: Introduction & Environment (1-10)

1. **Definition of Mobile Development:** The process of creating software for handheld devices.
2. **Native Apps:** Apps built specifically for one platform (e.g., Java/Kotlin for Android).
3. **Web Apps:** Mobile-optimized websites running in a browser.
4. **Hybrid Apps:** Web apps wrapped in a native container (e.g., Cordova).
5. **Cross-Platform Frameworks:** Tools like Flutter or React Native that use one codebase for multiple OSs.
6. **Android OS Architecture:** Comprised of the Linux Kernel, Hardware Abstraction Layer (HAL), Native Libraries/Android Runtime, Java API Framework, and System Apps.
7. **ART vs. Dalvik:** ART (Android Runtime) uses ahead-of-time (AOT) compilation for better performance.
8. **JDK (Java Development Kit):** Required to compile Java-based Android apps.
9. **Android Studio:** The official Integrated Development Environment (IDE).
10. **ADB (Android Debug Bridge):** A command-line tool used to communicate with an emulator or device.

---

### Module 2: Android Core Components (11-25)

11. **Activity:** Represents a single screen with a user interface.
12. **Service:** Runs in the background to perform long-running operations (no UI).
13. **Broadcast Receiver:** Responds to system-wide broadcast announcements.
14. **Content Provider:** Manages access to a central repository of data.
15. **Intent:** An asynchronous message used to request an action from another component.
16. **Explicit Intent:** Specifies the exact component to start by name.
17. **Implicit Intent:** Declares a general action to perform, letting the system find a match.
18. **Activity Lifecycle:** States include onCreate, onStart, onResume, onPause, onStop, onRestart, and onDestroy.
19. **Fragment:** A modular portion of an Activity’s user interface.
20. **Fragment Lifecycle:** Includes specific callbacks like onAttach and onCreateView.
21. **Context:** An interface to global information about an application environment.
22. **The Manifest File (AndroidManifest.xml):** Essential file describing app components, permissions, and hardware requirements.
23. **R.java:** An auto-generated file that acts as an index to all resources in the project.
24. **Resources Folder (res/):** Contains layouts (layout/), strings (values/), and images (drawable/).
25. **Task Backstack:** The "Last In, First Out" (LIFO) stack of Activities.

---

### Module 3: UI Design & Layouts (26-45)

26. **View:** The basic building block for UI components (widgets).
27. **ViewGroup:** An invisible container that holds other Views (layouts).
28. **LinearLayout:** Aligns children horizontally or vertically.
29. **RelativeLayout:** Positions views relative to each other or the parent.
30. **ConstraintLayout:** Allows complex layouts without nesting; uses constraints for positioning.
31. **FrameLayout:** Designed to block out an area on the screen to display a single item.
32. **TableLayout:** Arranges elements into rows and columns.
33. **Match_parent:** View expands to match the size of its parent.
34. **Wrap_content:** View expands only as much as needed to contain its content.
35. **dp (Density-independent Pixels):** Used for layout dimensions to ensure screen density independence.
36. **sp (Scale-independent Pixels):** Used for font sizes (respects user settings).
37. **TextView:** Displays text to the user.
38. **EditText:** A text field for user input.
39. **Button:** Triggers an action when clicked.
40. **ImageView:** Displays image resources.
41. **CheckBox/RadioButton:** For selecting options from a list.
42. **ListView:** Displays a vertically scrollable list of items (older).
43. **RecyclerView:** A more advanced and flexible version of ListView for large data sets.
44. **Adapter:** Bridges the UI component and the data source.
45. **Event Listeners:** Interfaces like `OnClickListener` to handle user interactions.

---

### Module 4: Data Storage (46-60)

46. **SharedPreferences:** Stores small amounts of primitive data in key-value pairs.
47. **Internal Storage:** Private data stored on the device's file system.
48. **External Storage:** Shared files (SD card or public folders).
49. **SQLite Database:** A lightweight, relational database for structured data.
50. **SQLiteOpenHelper:** A helper class to manage database creation and version management.
51. **CRUD Operations:** Create, Read, Update, Delete.
52. **Cursor:** An object providing read-write access to the result set returned by a database query.
53. **Room Persistence Library:** An abstraction layer over SQLite for easier database access.
54. **Content URIs:** Strings used by Content Providers to identify data.
55. **Asset Manager:** Used to access raw files bundled with the app (assets/ folder).
56. **JSON (JavaScript Object Notation):** Common format for data exchange.
57. **XML Parsing:** Interpreting data in XML format.
58. **GSON/Jackson:** Libraries used to convert Java objects to/from JSON.
59. **SQL Injection:** A security risk where malicious code is inserted into queries.
60. **Permissions:** Declared in the Manifest to access sensitive data (e.g., READ_CONTACTS).

---

### Module 5: Networking & Services (61-75)

61. **HTTP/HTTPS:** Protocols used for web communication.
62. **Retrofit:** A popular type-safe HTTP client for Android.
63. **Volley:** A networking library designed to make networking for Android apps easier and faster.
64. **RESTful API:** An architectural style for networked applications.
65. **AsyncTask:** (Deprecated but often tested) Class for performing background operations and publishing results on the UI thread.
66. **Main Thread (UI Thread):** Where all UI operations must occur.
67. **NetworkOnMainThreadException:** Occurs when network operations are attempted on the UI thread.
68. **Handler/Looper:** Used for communication between threads.
69. **WorkManager:** Recommended for persistent background work.
70. **Broadcast Intents:** Sent by the system (e.g., "Battery Low") or apps.
71. **Sticky Broadcast:** A broadcast that stays around after it is finished (deprecated for security).
72. **NotificationManager:** System service to manage status bar notifications.
73. **PendingIntent:** A token you give to a foreign application which allows it to use your application's permissions to execute a predefined piece of code.
74. **Foreground Service:** A service the user is actively aware of (shows a notification).
75. **Bound Service:** A service that allows other components to bind to it and interact with it.

---

### Module 6: Multimedia & Sensors (76-85)

76. **MediaPlayer:** Used to play audio and video files.
77. **SurfaceView:** Used for drawing graphics or playing video outside the UI thread.
78. **Camera API / CameraX:** Tools for capturing photos and videos.
79. **SensorManager:** System service to access device sensors.
80. **Accelerometer:** Measures the acceleration force applied to the device.
81. **Gyroscope:** Measures the rate of rotation around the device's axes.
82. **GPS (Global Positioning System):** Used for location tracking.
83. **LocationManager:** Provides access to system location services.
84. **Geocoding:** Converting an address into geographic coordinates.
85. **Runtime Permissions:** Permissions requested while the app is running (Android 6.0+).

---

### Module 7: Advanced Concepts & Optimization (86-100)

86. **Material Design:** Google's design language for consistent UI/UX.
87. **WebView:** A View that displays web pages within an app.
88. **ProGuard/R8:** Tools for shrinking, optimizing, and obfuscating code.
89. **Memory Leak:** Occurs when an object is no longer used but still referenced, preventing garbage collection.
90. **ANR (Application Not Responding):** Dialog shown when the UI thread is blocked for too long (usually 5 seconds).
91. **Unit Testing:** Testing individual components (JUnit).
92. **Instrumented Testing:** Testing UI and components on a real device/emulator (Espresso).
93. **Gradle:** The build automation system used by Android Studio.
94. **APK (Android Package):** The file format used to distribute and install apps.
95. **App Bundle (.aab):** Modern publishing format that optimizes APK generation for different devices.
96. **Signing an App:** Required for publishing to ensure the author's identity.
97. **MVC/MVP/MVVM:** Architectural patterns for organizing code logic and UI.
98. **Jetpack:** A suite of libraries to help developers follow best practices.
99. **Version Control (Git):** Managing changes to the source code.
100. **Deployment:** The process of submitting an app to a store like Google Play or Huawei AppGallery.

References:

* [Android Developer Fundamentals](https://www.google.com/search?q=https://developer.android.com/courses/fundamentals-training/overview-v2)
* [Standard National Self-Study Guidelines - Computer Science](https://www.neea.edu.cn/)

Would you like me to explain any of these specific points in more detail or provide a sample practice exam based on these topics?