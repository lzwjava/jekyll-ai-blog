---
audio: false
generated: true
lang: zh
layout: post
title: Rust生态百大影响力Crate榜单
translated: true
type: note
---

要提供基于实时下载量的精确“前100名”列表颇具挑战，因为 Crates.io 并未以如此细粒度的方式公开动态排名数据。不过，根据普遍受欢迎程度、在项目中的广泛使用以及对 Rust 生态系统的贡献，以下列出的是具有高度影响力和广泛使用的 Rust 库（crate），每个库都附有简要说明。此列表综合考虑了直接下载量（来自 Lib.rs/Crates.io 的数据，尽管这些数据会波动）、传递依赖（有多少其他库依赖它们）以及社区认可度等因素。

**注意：** Lib.rs（收集 Crates.io 的数据）提供的下载量是不断变化的。以下数字为截至 2025 年 7 月初的近似值，旨在提供一个量级概念。

---

## 按影响力和受欢迎程度排序的顶级 Rust 库（约 100 个）

1. **`serde`**：通用的序列化/反序列化框架。（下载量：24.9M）
2. **`serde_json`**：基于 `serde` 构建的 JSON 序列化文件格式。（下载量：21.7M）
3. **`thiserror`**：用于轻松实现 `std::error::Error` trait 的派生宏。（下载量：27.7M）
4. **`rand`**：随机数生成器及其他随机性功能。（下载量：30.7M）
5. **`clap`**：一个高效且功能齐全的命令行参数解析器。（下载量：20.9M）
6. **`syn`**：Rust 源代码解析器，广泛用于过程宏。（下载量：42.7M）
7. **`tokio`**：用于异步应用程序的事件驱动、非阻塞 I/O 平台。（下载量：16.3M）
8. **`log`**：一个轻量级的 Rust 日志门面。（下载量：23.1M）
9. **`anyhow`**：基于 `std::error::Error` 构建的灵活具体错误类型，简化错误处理。（下载量：17.1M）
10. **`quote`**：用于生成 Rust 代码的准引用宏。（下载量：29.1M）
11. **`regex`**：保证线性时间匹配的正则表达式库。（下载量：20.1M）
12. **`proc-macro2`**：编译器 `proc_macro` API 的替代实现。（下载量：29.3M）
13. **`base64`**：将 base64 编码和解码为字节或 UTF-8。（下载量：29.6M）
14. **`itertools`**：额外的迭代器适配器、方法和函数。（下载量：32.3M）
15. **`chrono`**：一个全面的 Rust 日期和时间库。（下载量：14.5M）
16. **`reqwest`**：一个更高级的 HTTP 客户端库。（下载量：12.5M）
17. **`libc`**：到平台库（如 libc）的原始 FFI 绑定。（下载量：28.2M）
18. **`once_cell`**：单次赋值单元格和惰性值。（下载量：23.8M）
19. **`tracing`**：用于 Rust 的应用程序级追踪。（下载量：14.7M）
20. **`futures`**：提供流、零分配 future 和类似迭代器的接口。（下载量：13.2M）
21. **`lazy_static`**：用于声明惰性求值静态变量的宏。（下载量：19.2M）
22. **`tempfile`**：用于管理临时文件和目录。（下载量：14.3M）
23. **`bitflags`**：用于生成行为类似于位标志的结构的宏。（下载量：33.9M）
24. **`url`**：基于 WHATWG URL 标准的 URL 解析和操作库。（下载量：14.2M）
25. **`toml`**：用于 TOML 格式文件的本机 Rust 编码器和解码器。（下载量：15.0M）
26. **`bytes`**：用于处理字节的类型和 trait，针对 I/O 进行了优化。（下载量：17.0M）
27. **`uuid`**：生成和解析 UUID。（下载量：14.4M）
28. **`indexmap`**：具有一致顺序和快速迭代的哈希表。（下载量：29.0M）
29. **`env_logger`**：通过环境变量配置的 `log` 日志实现。（下载量：12.1M）
30. **`async-trait`**：为异步 trait 方法启用类型擦除。（下载量：11.9M）
31. **`num-traits`**：用于通用数学的数值 trait。（下载量：19.0M）
32. **`sha2`**：SHA-2 哈希函数的纯 Rust 实现。（下载量：14.1M）
33. **`rustls`**：一个用 Rust 编写的现代、安全且快速的 TLS 库。
34. **`hyper`**：一个快速且正确的 Rust HTTP 实现。
35. **`actix-web`**：一个强大、实用且极快的 Web 框架。
36. **`diesel`**：一个安全、可扩展的 Rust ORM 和查询构建器。
37. **`rayon`**：一个数据并行库，用于轻松并行化计算。
38. **`sqlx`**：一个异步的纯 Rust SQL 工具包。
39. **`axum`**：一个专注于人体工程学和模块化的 Web 应用程序框架。
40. **`tonic`**：基于 Hyper 和 Tower 构建的 HTTP/2 gRPC 实现。
41. **`tracing-subscriber`**：用于实现和组合 `tracing` 订阅者的实用工具。
42. **`crossbeam`**：用于 Rust 并发编程的工具。
43. **`parking_lot`**：高度并发且公平的常见同步原语实现。
44. **`dashmap`**：一个社区驱动的并发哈希映射。
45. **`flate2`**：`miniz_oxide` 和 `zlib` 压缩库的包装器。
46. **`ring`**：用 Rust 和汇编编写的加密函数。
47. **`cc`**：用于编译 C/C++ 代码的构建时依赖项。
48. **`bindgen`**：自动生成到 C（和 C++）库的 Rust FFI 绑定。
49. **`wasm-bindgen`**：促进 Wasm 模块和 JavaScript 之间的高级交互。
50. **`web-sys`**：到 Web API 的原始 Rust 绑定。
51. **`console_error_panic_hook`**：一个用于将 panic 错误记录到浏览器控制台的钩子。
52. **`console_log`**：一个将日志打印到浏览器控制台的 `log` crate 日志后端。
53. **`nalgebra`**：Rust 的线性代数库。
54. **`image`**：图像处理库。
55. **`egui`**：一个易于使用的即时模式 GUI 库。
56. **`winit`**：一个跨平台窗口创建库。
57. **`wgpu`**：一个安全且可移植的 GPU 抽象层。
58. **`bevy`**：一个极其简单的数据驱动游戏引擎。
59. **`glium`**：一个安全易用的 OpenGL 包装器。
60. **`vulkano`**：Vulkan 图形 API 的 Rust 包装器。
61. **`glutin`**：OpenGL 的 Rust 包装器，用于窗口化和上下文。
62. **`rodio`**：一个简单易用的音频播放库。
63. **`nalgebra-glm`**：一个类似 GLSL 的图形数学库。
64. **`tui`**：一个终端用户界面库。
65. **`indicatif`**：一个进度条库。
66. **`color-eyre`**：一个彩色且具有上下文感知的错误报告 crate。
67. **`async-std`**：一个社区驱动的、符合语言习惯的异步运行时。
68. **`smol`**：一个小而快的异步运行时。
69. **`tarpc`**：一个使用 `tokio` 的 Rust RPC 框架。
70. **`prost`**：Rust 的 Protocol Buffers 实现。
71. **`grpcio`**：Rust 的 gRPC 库。
72. **`jsonrpsee`**：一个 JSON-RPC 2.0 客户端/服务器实现。
73. **`validator`**：一个用于验证数据的轻量级库。
74. **`argon2`**：Argon2 密码哈希。
75. **`uuid-b64`**：编码为 Base64 的 UUID。
76. **`csv`**：一个 CSV 解析和写入库。
77. **`calamine`**：一个用于读取 Excel 文件的纯 Rust 库。
78. **`polars`**：一个用 Rust 编写的极快 DataFrame 库。
79. **`ndarray`**：Rust 的 N 维数组。
80. **`faiss-rs`**：Facebook AI 相似性搜索的 Rust 绑定。
81. **`tract`**：一个神经网络推理框架。
82. **`candle`**：一个机器学习框架。
83. **`tch-rs`**：Libtorch (PyTorch) 的 Rust 绑定。
84. **`cobertura`**：代码覆盖率数据解析。
85. **`criterion`**：一个基准测试工具。
86. **`proptest`**：一个基于属性的测试框架。
87. **`insta`**：一个快照测试库。
88. **`mockall`**：一个 Rust 的模拟库。
89. **`arbitrary`**：一个用于模糊测试和属性测试的数据生成库。
90. **`walkdir`**：递归遍历目录。
91. **`fs_extra`**：扩展的文件系统操作。
92. **`zip`**：一个 zip 归档创建和提取库。
93. **`tar`**：一个 tar 归档创建和提取库。
94. **`xz2`**：用于 XZ 压缩的 `liblzma` 库的 Rust 绑定。
95. **`lz4`**：LZ4 压缩和解压缩。
96. **`crc32fast`**：快速 CRC32 计算。
97. **`chrono-tz`**：`chrono` 的时区定义。
98. **`ipnet`**：IP 网络地址操作。
99. **`nix`**：到 Unix/Linux 系统调用的 Rust 绑定。
100. **`windows`**：Windows API 的官方 Rust 绑定。

---

此列表试图涵盖 Rust 生态系统中广泛常见用例和基本实用工具，既反映了原始受欢迎程度，也反映了对开发工作流程的重大影响。
