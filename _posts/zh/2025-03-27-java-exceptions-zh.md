---
audio: false
generated: true
lang: zh
layout: post
title: Java异常处理
translated: true
type: note
---

以下是 Java 异常的详细列表，分为**受检异常、非受检异常（运行时异常）和错误**三类。

---

## **1. 受检异常（必须处理或用 `throws` 声明）**
1. **IOException** – 通用 I/O 故障
2. **FileNotFoundException** – 文件缺失或无法访问
3. **InterruptedException** – 线程被中断
4. **SQLException** – 数据库访问问题
5. **ParseException** – 数据格式解析错误
6. **MalformedURLException** – URL 格式无效
7. **ClassNotFoundException** – 运行时未找到类
8. **InstantiationException** – 无法实例化抽象类或接口
9. **IllegalAccessException** – 无权访问类、方法或字段
10. **NoSuchMethodException** – 方法不存在
11. **NoSuchFieldException** – 类中不存在该字段
12. **TimeoutException** – 阻塞操作超时
13. **UnsupportedEncodingException** – 不支持的编码格式
14. **URISyntaxException** – URI 语法无效
15. **NotBoundException** – RMI 注册表中未找到名称
16. **AlreadyBoundException** – 名称已绑定至 RMI 注册表
17. **CloneNotSupportedException** – 对象未实现 `Cloneable`
18. **DataFormatException** – 压缩数据格式无效
19. **EOFException** – 意外到达文件末尾
20. **NotSerializableException** – 对象不可序列化
21. **LineUnavailableException** – 音频线路不可用
22. **UnsupportedAudioFileException** – 不支持的音频文件格式
23. **PrinterException** – 打印操作失败
24. **ReflectiveOperationException** – 反射操作通用错误
25. **ExecutionException** – 并发任务执行期间异常
26. **ScriptException** – 脚本执行问题
27. **TransformerException** – XML 转换失败
28. **XPathExpressionException** – XPath 表达式无效
29. **SAXException** – XML 解析问题
30. **JAXBException** – XML 绑定问题
31. **MarshalException** – 序列化 XML 数据时出错
32. **UnmarshalException** – 反序列化 XML 数据时出错
33. **DatatypeConfigurationException** – XML 数据类型配置无效
34. **GSSException** – GSS 安全操作问题
35. **KeyStoreException** – Java 密钥库问题
36. **CertificateException** – 证书处理问题
37. **InvalidKeyException** – 加密操作中的密钥无效
38. **NoSuchAlgorithmException** – 请求的加密算法不可用
39. **NoSuchProviderException** – 请求的安全提供者不可用
40. **UnrecoverableKeyException** – 无法从密钥库恢复密钥
41. **IllegalBlockSizeException** – 加密块大小无效
42. **BadPaddingException** – 加密填充错误

---

## **2. 非受检异常（运行时异常）**
43. **NullPointerException** – 访问空对象引用
44. **ArrayIndexOutOfBoundsException** – 访问无效的数组索引
45. **StringIndexOutOfBoundsException** – 访问无效的字符串索引
46. **ArithmeticException** – 数学错误（如除零）
47. **NumberFormatException** – 将无效字符串转换为数字
48. **ClassCastException** – 类型转换无效
49. **IllegalArgumentException** – 向方法传递无效参数
50. **IllegalStateException** – 在无效状态下调用方法
51. **UnsupportedOperationException** – 不支持该方法
52. **ConcurrentModificationException** – 并发修改集合
53. **NoSuchElementException** – 尝试访问集合中不存在的元素
54. **IllegalMonitorStateException** – 线程同步错误
55. **NegativeArraySizeException** – 创建负大小的数组
56. **StackOverflowError** – 无限递归导致栈溢出
57. **OutOfMemoryError** – JVM 内存耗尽
58. **SecurityException** – 检测到安全违规
59. **MissingResourceException** – 未找到资源包
60. **EmptyStackException** – 尝试从空栈访问元素
61. **TypeNotPresentException** – 运行时未找到类型
62. **EnumConstantNotPresentException** – 无效的枚举常量
63. **UncheckedIOException** – `IOException` 的非受检版本
64. **DateTimeException** – Java 日期时间 API 相关错误
65. **InvalidClassException** – 反序列化类时出现问题
66. **IllegalCharsetNameException** – 字符集名称无效
67. **UnsupportedCharsetException** – 不支持的字符集
68. **ProviderNotFoundException** – 缺少所需的服务提供者
69. **PatternSyntaxException** – 正则表达式语法无效
70. **InvalidPathException** – 文件路径无效
71. **ReadOnlyBufferException** – 尝试修改只读缓冲区
72. **BufferUnderflowException** – 缓冲区下溢
73. **BufferOverflowException** – 缓冲区上溢
74. **FileSystemAlreadyExistsException** – 文件系统已存在
75. **FileSystemNotFoundException** – 未找到文件系统
76. **ClosedWatchServiceException** – 监视服务已关闭
77. **UncheckedExecutionException** – 并发任务执行问题

---

## **3. 错误（不应捕获的严重问题）**
78. **StackOverflowError** – 递归方法调用过多
79. **OutOfMemoryError** – JVM 内存耗尽
80. **VirtualMachineError** – 关键 JVM 错误
81. **InternalError** – 意外的 JVM 内部错误
82. **UnknownError** – 未知关键错误
83. **AssertionError** – `assert` 断言失败
84. **NoClassDefFoundError** – 运行时缺少类定义
85. **IncompatibleClassChangeError** – 类发生不兼容变更
86. **AbstractMethodError** – 抽象方法未实现
87. **InstantiationError** – 实例创建失败
88. **IllegalAccessError** – 非法访问类或方法
89. **NoSuchMethodError** – 未找到方法
90. **NoSuchFieldError** – 未找到字段
91. **ClassFormatError** – 类格式无效
92. **UnsupportedClassVersionError** – 使用不支持的 Java 版本编译的类
93. **AnnotationFormatError** – Java 注解问题
94. **ExceptionInInitializerError** – 静态初始化块中出现异常
95. **ThreadDeath** – 线程被强制终止
96. **ServiceConfigurationError** – 服务提供者配置问题
97. **BootstrapMethodError** – 动态语言支持错误
98. **VerifierError** – 字节码验证失败
99. **FactoryConfigurationError** – XML 工厂配置错误

---

### **结语**
这是 Java 异常和错误的完整列表。如需了解特定异常的更多详细信息，请随时告知！🚀
