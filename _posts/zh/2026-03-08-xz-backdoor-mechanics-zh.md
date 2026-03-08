---
audio: false
generated: true
image: false
lang: zh
layout: post
title: XZ 后门发现与机制
translated: true
type: note
---

**问题：** Andres Freund 是如何发现 500ms 的 SSH 登录延迟，并随后在 XZ Utils 中发现隐藏后门的？请提供全面解释，包括后门的技术工作原理。

---

**答案：**

## XZ Utils 后门 (CVE-2024-3094)：完整的故事

---

### 1. Andres Freund 是谁？

Andres Freund 是 Microsoft 员工和 PostgreSQL 开发者。他并不是专职安全研究员——他几乎是偶然发现了 Linux 历史上最危险的供应链攻击之一。

---

### 2. 他是如何注意到问题的

2024 年 3 月，在 Debian Sid 上对 PostgreSQL 进行基准测试时，Freund 注意到 SSH 登录需要 500ms，而不是正常的 100ms。这个看似微不足道的半秒差异是伪装下的第一个裂缝。

他还注意到 `sshd` 进程即使因用户名错误立即失败，也消耗了惊人的 CPU。

作为一名谨慎的工程师，他运行了 Valgrind——一个内存调试工具——它在受影响系统上抛出了错误。他将问题追溯到 XZ Utils 提供的压缩库 `liblzma`。

2024 年 3 月 29 日，Freund 在 oss-security 邮件列表上分享了信息，识别出命令行工具 XZ 的恶意提交，影响 Linux 版本 5.6.0 和 5.6.1。

---

### 3. 背后的多年社会工程攻击

这不是简单的黑客攻击。这是一场**历时数年、国家级水准的操作**。

后续调查发现，插入后门的活动是大约三年努力的顶峰，从 2021 年 11 月到 2024 年 2 月，由一名化名为 “Jia Tan”（GitHub 用户名 JiaT75）的人执行，他努力在项目中获得信任职位。

该活动涉及：

**步骤 1 — 建立信誉。** Jia Tan 从 2022 年初开始向 XZ Utils 提交合法、有帮助的补丁。代码质量良好。贡献持续一致。

**步骤 2 — 通过假身份施压。** 在对创始人兼首席维护者施压一段时间后，通过明显的傀儡账户，要求移交项目控制权，Jia Tan 获得了 XZ Utils 联合维护者的职位。涉嫌假账户包括用户名如 “Jigar Kumar”、“krygorin4545” 和 “misoeater91”。

**步骤 3 — 武器化发布流程。** 修改后的 `build-to-host.m4` 文件仅存在于上传到 GitHub 的发布 tarball 中，从不在 git 仓库中。任何审查源代码的人都会看到干净的提交，而分发的软件包含后门。

**步骤 4 — 掩盖踪迹。** Jia Tan 以 tarball 形式发布了 XZ Utils 5.6.0，其中包含以二进制（非纯文本）形式的后门“测试”文件，使其更加混淆。随后，他们匆忙发布 5.6.1 来修复后门被发现前出现的一些故障。

---

### 4. 后门如何隐藏（构建系统注入）

注入极其巧妙且多阶段：

`m4/build-to-host.m4` 宏在构建过程中执行。它“修复”一个伪装成代码测试的畸形 XZ 文件（`bad-3-corrupt_lzma2.xz`）。之后，从另一个诱饵测试存档（`good-large-compressed.lzma`）中提取并解密一个恶意的 Bash 脚本。该 Bash 脚本然后提取一个二进制文件、解密它，并将其保存为 `liblzma_la-crc64-fast.o`，并将其添加到 liblzma 编译过程中。

恶意脚本还检查各种条件，如机器架构——它仅针对 `x86_64 linux-gnu` 系统。

调查确认这是针对特定系统集的休眠恶意软件：具体为 `x86_64` 架构，需要 systemd 和 sshd。它不针对 BSD、Android 手机、Wi-Fi 路由器、IoT 设备或 Raspberry Pi——本质上，必须是标准 Linux 服务器。

---

### 5. 后门实际工作原理（技术深入剖析）

这是最复杂部分。这里是后门实现**无认证远程代码执行 (RCE)** 的方式：

#### 步骤 A — 进入 sshd 而无需触碰 OpenSSH 源代码

OpenSSH 通常不加载 `liblzma`，但几个 Linux 发行版使用的常见第三方补丁导致它加载 `libsystemd`，后者反过来加载 `liblzma`。后门代码使用 glibc 的 IFUNC 机制替换 OpenSSH 中的现有函数 `RSA_public_decrypt` 为恶意版本。

#### 步骤 B — IFUNC 是什么？

IFUNC（间接函数）是 glibc 的一项功能，允许根据硬件能力在运行时选择优化的函数实现。2023 年 6 月，Jia Tan 通过看似合法的提交引入了 IFUNC 解析器（`crc32_resolve`、`crc64_resolve`）。这些解析器随后被利用，在运行时替换 OpenSSH 的 `RSA_public_decrypt` 函数。因为 IFUNC 在进程初始化早期运行，它特别隐蔽。

#### 步骤 C — 通过 rtld-audit 进行函数钩子

攻击者利用 IFUNC 和 `rtld-audit` 机制实现 `RSA_public_decrypt()` 函数的劫持替换。后门设置了三个钩子函数以提高成功率：`RSA_public_decrypt()`、`EVP_PKEY_set1_RSA()` 和 `RSA_get0_key()`。如果任何一个成功钩住，进程会退出并清理 `rtld-audit` 的痕迹。

#### 步骤 D — 通过 RSA 密钥传递恶意负载

通过此钩子，二进制文件检查传递到 RSA 结构体中的 RSA 公钥模数（“N” 值）。该值使用硬编码解密密钥解码，并使用 **Ed448 椭圆曲线签名算法** 检查数据的有效性。

钩住的 `RSA_public_decrypt` 使用固定 Ed448 密钥验证服务器主机密钥上的签名，然后将负载传递给 `system()`。这是 RCE——不仅仅是认证绕过——负载受限且不可重放。负载从传递给 `RSA_public_decrypt` 的 N 值（公钥）中提取，使用简单指纹检查，并使用固定的 ChaCha20 密钥解密，然后进行 Ed448 签名验证。

这意味着：**只有攻击者**持有对应的 Ed448 私钥才能触发此后门。

#### 步骤 E — 不留日志

成功利用时，OpenSSH 不会写入 INFO 级别或更高的日志消息。这使得在生产环境中通过日志分析检测极不可能。

#### 步骤 F — 防重放保护

攻击者设置了防重放功能，以避免后门通信被捕获或劫持。后门还在主钩子函数完成后，将传入的 RSA 公钥替换为空，以避免记录任何来自攻击者的恶意数据。

---

### 6. 可能发生什么

此后门几乎成为有史以来最广泛和有效的入侵启用器之一——将超过 SolarWinds 后门。攻击者几乎能够立即访问运行受感染发行版的任何 Linux 机器，包括 Fedora、Ubuntu 和 Debian。

Alex Stamos 指出，这可能是“有史以来在任何软件产品中植入的最广泛和有效后门”。如果未被发现，它将为其创建者提供受影响服务器的主密钥。

---

### 7. 为什么及时被抓获

标准静态分析和漏洞扫描工具无法捕获此后门。恶意代码仅存在于发布 tarball（非 Git）中，跨多个二进制测试文件混淆，并使用合法构建系统机制。检测需要观察运行时行为异常——500ms 的 SSH 延迟。

后门已进入 Debian Sid、Fedora 41 和 Fedora Rawhide 等发行版的测试发布，但被捕获前未传播到更广泛使用的稳定发布。

---

### 8. 归因

安全研究员 Dave Aitel 指出，该活动的多年耐心、操作安全性和复杂性与 APT29（Cozy Bear）的手法一致，该组织与俄罗斯对外情报局 (SVR) 相关。虽然归因尚未确认，但该活动投入的资源和时间超过典型个人或犯罪行为者。

---

### 总结流程图

```
Jia Tan (2021–2024)
  └─► 作为 XZ 维护者获得信任
      └─► 仅在发布 tarball 中注入恶意代码（非 git）
          └─► 构建过程秘密地将后门编译进 liblzma
              └─► sshd 加载 libsystemd → 加载 liblzma（无意中）
                  └─► IFUNC 钩子在运行时替换 RSA_public_decrypt
                      └─► 攻击者发送带有嵌入负载的 SSH 证书（在 RSA N 值中）
                          └─► Ed448 签名验证 → system() 执行攻击者命令
                              └─► 服务器完整 RCE，预认证，无日志
```

---

**参考资料：**

- [Elastic Security Labs — 500ms to Midnight](https://www.elastic.co/security-labs/500ms-to-midnight)
- [Wikipedia — XZ Utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)
- [Akamai — XZ Utils Backdoor Everything You Need to Know](https://www.akamai.com/blog/security-research/critical-linux-backdoor-xz-utils-discovered-what-to-know)
- [SoftwareSeni — Multi-Year Social Engineering Campaign](https://www.softwareseni.com/the-xz-utils-backdoor-cve-2024-3094-and-the-multi-year-social-engineering-campaign-behind-it/)
- [GitHub — xz-utils backdoor situation (thesamesam)](https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27)
- [Pentest-Tools — CVE-2024-3094 Technical Analysis](https://pentest-tools.com/blog/xz-utils-backdoor-cve-2024-3094)
- [Securelist — XZ Backdoor Hook Analysis](https://securelist.com/xz-backdoor-part-3-hooking-ssh/113007/)
- [Red Hat — Understanding Red Hat's Response](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident)
- [Datadog Security Labs — CVE-2024-3094](https://securitylabs.datadoghq.com/articles/xz-backdoor-cve-2024-3094/)