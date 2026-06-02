---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 按粉丝数排名最高的HuggingFace用户
translated: true
type: note
---

**问题：** Hugging Face 上关注人数最多/影响力最大的前十位个人用户是谁？**回答：**

Hugging Face 并未以官方形式发布清晰的“关注者排行榜”——但社区有一个跟踪该数据的空间。根据已知数据和社区追踪，以下是按关注人数排名靠前的个人用户（截至 2025 年早期至中期），分为 **HF 员工**和**社区贡献者**，因为这两类差异很大。

---

## 头部 HF 员工/内部成员（按关注人数）

| 用户标识 | 姓名 | 角色 | 大约关注数 |
|---|---|---|---|
| **thomwolf** | Thomas Wolf | HF 联合创始人/首席科学官 | ~30,000+ |
| **pcuenq** | Pedro Cuenca | HF 研究工程师 | ~20,000+ |
| **merve** | Merve Noyan | HF 开发者倡导者 | ~15,000+ |
| **osanseviero** | Omar Sanseviero | HF 幕僚长 | ~12,000+ |
| **clem** | Clément Delangue | HF 首席执行官 | ~10,000+ |

Thomas Wolf 很可能是关注人数最多的个人用户——他是 HF 技术形象的代言人，共同撰写了最初的 Transformers 库论文，并且从一开始就在 HF 工作。

---

## 头部社区贡献者（非 HF 员工）

| 用户标识 | 姓名 | 知名原因 | 大约关注数 |
|---|---|---|---|
| **teknium** | Nathan Cooper | OpenHermes、Hermes 系列、NousResearch | ~7,300 |
| **TheBloke** | Tom Jobbins | 量化模型上传（GGUF、GPTQ） | ~6,000+ |
| **bartowski** | — | GGUF 量化、LM Studio | ~5,000+ |
| **mradermacher** | — | 量化 LLM 变体 | ~4,000+ |
| **Weyaxi** | — | 社区排行榜、工具 | ~3,000+ |

---

## 关键洞察

TheBloke 因量化模型版本而闻名——其最成功的作品是 phi-2-GGUF，尽管自 2024 年以来他未再发布新模型。类似地，mradermacher 的下载量主要来自量化 LLM，并且截至 2025 年仍活跃。

就原始**下载影响力**（这可能比关注数更重要）而言，下载量最高的 50 个实体占据了 Hub 总下载量的 80% 以上——而该榜单由 Google、Meta、Microsoft 和 Sentence-Transformers 等组织主导，而非个人用户。

Hugging Face 上真正有影响力的用户按关注数来看是 HF 员工 + 少数社区量化者和微调者（如 Teknium）。Teknium 的 7,300 关注者在社区（非员工）个人中属于真正精英级别。

---

**注：** 实时排行榜可访问 [huggingface.co/spaces/Weyaxi/followers-leaderboard](https://huggingface.co/spaces/Weyaxi/followers-leaderboard)——如需实时数据，值得收藏。

参考来源：

- [Hugging Face 上 50 个下载最多实体的模型统计](https://huggingface.co/blog/lbourdois/huggingface-models-stats)
- [Weyaxi 的关注者排行榜空间](https://huggingface.co/spaces/Weyaxi/followers-leaderboard)
