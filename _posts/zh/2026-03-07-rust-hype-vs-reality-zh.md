---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust 炒作 vs 现实：神话破灭
translated: true
type: note
---

问题：这篇文章关于“所谓的内存安全语言”的主要论点是什么，我们应该如何批判性地理解它？

回答：

## 概述

这篇文章由**Wang Yin (王垠)**撰写，他是一位著名的且备受争议的中国程序员/博主，表达了对 Rust 和“内存安全语言”炒作的批判性——有时甚至是轻蔑的——观点。Weibo 链接需要登录，但完整文章文本已提供在您的文档中。下面是对其论点的全面剖析，以及如何评估它们。

---

## 他的核心论点

### 1. “内存安全语言”并非 Rust 独有

Wang Yin 认为，大多数人误读了 White House/NSA 报告，认为它特别推崇 Rust，实际上**几乎所有带有自动内存管理（GC 或 RC）的语言已经是内存安全的**——包括 Java、Python、JavaScript、Ruby、C#、Swift、Lisp，甚至 Fortran。Rust 只是该列表中的最新成员，且可能是按字母顺序或为了吸引注意力而排在首位。

**这是正确的吗？** — **是的，大体上正确。** NSA 的“内存安全语言”类别确实包括 Java、C#、Go、Python 等。Rust 并未被 singled out 为唯一的安全选项。然而，关键区别在于 Rust 在*没有* garbage collector 的情况下实现了内存安全，这使其特别适合系统级编程，而 GC 语言在这些场景中不切实际。

---

### 2. Rust 的创新只是 C++ smart pointers 加上静态检查

他声称 Rust 的 ownership/borrow 模型本质上是 C++ 中的 `unique_ptr` 和 `shared_ptr`，只是添加了编译时强制执行。

**这是正确的吗？** — **部分正确。** 概念上的重叠确实存在——两者都受 RAII 和 linear/affine type theory 启发。然而，Rust 的**borrow checker 是语言级别的强制执行**，而非可选的库特性。在 C++ 中，程序员仍可自由混合使用 raw pointers；在 Rust 中，不能（在 safe code 中）。强制执行内置于 compiler 中，这是关键区别，而非概念本身。

---

### 3. Rust 的内存安全并不能解决所有安全问题

Wang Yin 正确指出，**内存安全只是软件安全的一个小Subset**。逻辑 bug、高层次的 race conditions、injection attacks、认证缺陷——这些都不会被内存安全阻止。

**这是正确的吗？** — **绝对正确，这是广泛认可的。** 即使 Rust 社区和 NSA 报告也承认这一点。内存安全消除了*特定、非常常见的*漏洞类别（buffer overflows、use-after-free 等），这些漏洞占 C/C++ 代码库中约 60–70% 的 critical CVEs——但它不是银弹。

---

### 4. Rust 的认知开销过高

他认为 Rust 通过 ownership 规则施加了巨大的心智负担，与（或比）C++ smart pointers 相当，这种认知负载分散了对真实问题的注意力。

**这是一个公平的观点吗？** — **这有争议，且取决于上下文。** Rust 的确有陡峭的学习曲线——尤其是 borrow checker。然而，许多工程师报告称，一旦心智模型内化，Rust 实际上*减少了*调试时间，因为错误在 compile time 而非 runtime 被捕获。权衡取决于项目类型和团队经验。对于应用级软件，GC 语言几乎总是更高效。对于系统软件，Rust 的开销通常被认为值得。

---

### 5. 遗留代码无法也不应重写为 Rust

他提出了一个务实的观点：数十亿行 C/C++（甚至 COBOL）代码体现了数十年辛苦积累的领域知识和 bug 修复。重写它们会引入新风险。

**这是正确的吗？** — **是的，这是软件工程中公认的可靠原则。** “重写有风险”已被充分理解。现实路径是在新组件中逐步采用 Rust，而不是完整重写。

---

### 6. White House 报告的时机可疑

他质疑为什么报告在 Rust 流行后才出现，而不是数十年前 C/C++ 内存问题早已众所周知时。

**分析：** 这带有推测性和某种阴谋论色彩。更平凡的解释是，该报告受现代高调漏洞（政府关键软件中的 exploits）、Rust 的行业势头以及内存相关 CVEs 的日益成本所驱动。政策文件滞后于技术现实并不罕见。

---

## 如何整体理解这篇文章

Wang Yin 提出了几个**合法且重要的观点**，值得内化：

- Rust 并非唯一内存安全语言，GC 语言值得同等认可。
- 内存安全 ≠ 软件安全。
- Rust 的认知开销真实且非 trivial。
- 盲目重写遗留代码库危险且浪费。

然而，文章也有明显的**弱点**：

- 它低估了 Rust 在*系统编程* niche 中的独特价值，在该领域 GC 不可行（OS kernels、embedded firmware、game engines、databases）。
- 它夸大了 C++ smart pointers 与 Rust borrow checker 的等价性——enforcement model 有实质区别。
- 对 White House 报告的阴谋论语气削弱了原本合理的的技术论点。
- 这种轻蔑带有某种意识形态色彩，受其对 GC 语言（他是 functional/Lisp 风格语言的知名倡导者）的偏好影响。

---

## 底线

这篇文章最好被视为对 **Rust 炒作的纠偏**，而非平衡的技术评估。其最强点是提醒（1）内存安全并非 Rust 独有，（2）它不能解决所有安全问题，（3）认知开销很重要。其最弱点是对 Rust 独特 niche 价值的轻视以及推测性的政治评论。

参考资料：

- [NSA Memory Safety Guidance (related)](https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/3215760/nsa-releases-guidance-on-how-to-protect-against-software-memory-safety-issues/)
- [Rust memory safety study - Huawei Cloud](https://bbs.huaweicloud.com/blogs/193974)
- [Blue team perspective: What is memory safety really?](https://deathking.github.io/2020/08/03/blue-team-rust-what-is-memory-safety-really/)
