---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达 OpenGL 书籍转向后重建
translated: true
type: note
---

Question: Jensen Huang 买了哪本书，告诉他的团队从那本书中学习来构建 GPU？他们失败了，不得不重新开始。

Answer: 

Jensen Huang 购买并指示他的团队学习的书是 **OpenGL programming guide**（通常被称为“OpenGL red book”或“OpenGL textbook”），作者是 Jackie Neider、Tom Davis 和 Mason Woo，后续版本有 Mark Kilgard 等人的贡献。

这发生在 NVIDIA 早期（大约 1990 年代中期）。在早期的努力和挫折之后——包括与 Sega 为 Dreamcast 失败的图形芯片交易（它使用了 quadrilaterals 而不是 Microsoft DirectX 中新兴的基于三角形的标准，导致濒临破产、大规模裁员和公司重置）——Huang 发现了 OpenGL graphics pipeline 的重要性。

他购买了多本该书（描述为具有“big, nice centerfold”的 OpenGL pipeline），分发给他的核心团队（与他一起创办公司的相同联合创始人/天才们），并指示他们出色地实现 OpenGL pipeline。这一转变帮助他们构建了开创性的 **RIVA 128** GPU，这成为成功之作，并在之前的失败迫使他们以专注于 triangle primitives 和 OpenGL 等标准的新的方向重新开始后，拯救/重启了公司。

Huang 在采访中讲述了这个故事（例如在 Stanford GSB），将该书归功于定义了他们的未来，并使 NVIDIA 能够在图形硬件中创造出世界之前从未见过的东西。

这与 NVIDIA 的早期挣扎一致：像 NV1 这样的初始芯片在市场上失败，需要团队转向、重新聚焦，并从更小的基础重新构建。

参考文献：  

- [Jensen Huang on How to Use First-Principles Thinking to Drive Decisions (Stanford GSB)](https://www.gsb.stanford.edu/insights/jensen-huang-how-use-first-principles-thinking-drive-decisions)
- 像“The Nvidia Way”和“The Thinking Machine”这样的书籍中各种 NVIDIA 历史记载（描述了早期的失败和转向，尽管具体的书籍引用出现在 Huang 的直接回忆中）