---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: LLM训练文本数据采集
translated: true
type: note
---

### 如何获取用于训练大语言模型的大规模文本数据

训练大语言模型（LLM）需要海量多样化、高质量的文本数据——通常来自书籍、网站、代码等渠道的数万亿个词元。关键挑战在于规模（TB到PB级）、质量（过滤噪声、重复和低价值内容）以及合法性（尊重版权，使用公共领域或授权数据）。以下是获取数据的步骤指南：

1. **从公共网络爬虫数据入手**：这是大多数LLM训练的支柱，它们捕获了互联网的快照。
   - 使用CC-Net或Dedup等工具（通过Hugging Face提供的Python库）过滤出干净文本。
   - 分块处理以应对数据规模——使用云存储（如AWS S3）进行下载。

2. **使用精选数据集**：来自研究团队的预过滤集合，通过API或直接链接下载。
   - 专注于多语言、特定领域（如代码、科学）的子集以满足需求。
   - 使用Hugging Face Datasets库等工具轻松加载：`from datasets import load_dataset`。

3. **补充特定领域数据源**：
   - 书籍：古登堡计划（公共领域）。
   - 维基百科：语言转储文件。
   - 代码：GitHub存档（通过BigCode）。
   - 生成合成数据：使用现有模型（如通过OpenAI API）创建推理链，但需清理以避免污染。

4. **法律与道德提示**：
   - 坚持使用开放许可（如CC-BY、MIT）。
   - 去重（使用MinHash等工具）并移除个人身份信息（PII）。
   - 对于定制训练，先从小规模开始（如1-10GB微调）再扩展。
   - 计算成本：即使是适度训练也需数百GPU小时；使用Colab或RunPod进行测试。

5. **处理流程**：
   - 下载 → 清理（移除HTML、非文本内容） → 词元化（如使用TikToken） → 训练。
   - 库工具：Pandas用于采样，spaCy/NLTK用于预处理。

公共数据集免费且规模庞大——适合爱好者或研究人员。对于生产环境，公司通常需授权专有数据。

### 特定模型的训练数据来源

像OpenAI、Anthropic和DeepSeek这样的专有模型出于竞争原因对具体配方保密，但它们通过论文、博客和泄露信息分享了高层细节。开源模型（如Llama、Mistral）更透明，常发布数据集蓝图。

- **OpenAI的GPT模型（如GPT-4o）**：
  训练数据混合了公开可用的互联网数据（过滤后的网络爬虫）、书籍、文章和代码。早期GPT大量使用Common Crawl；后期更强调高质量的STEM/编程资源。总计：数万亿词元，并进行了大量去重。他们还纳入了授权数据和用户交互（提供退出选项）。未完全公开，但本质上是“整个互联网”——经过抓取、过滤和增强。

- **Anthropic的模型（如Claude 3.5）**：
  专注于安全、有益的数据：公共网络文本、书籍以及为对齐生成的合成示例（如宪法AI）。他们使用来自Claude的用户聊天记录（提供退出选项）和HH-RLHF等RLHF数据集。强调多样化、无毒来源；关于抓取YouTube转录存在一些争议。总规模：类似的数万亿，但更注重道德筛选。

- **DeepSeek模型（如DeepSeek-V3、R1）**：
  中国半开源模型使用纯网页、电子书和代码仓库。V3在14.8T词元上预训练，未刻意使用合成数据，但R1通过拒绝采样增加了60万合成推理样本（由先前模型生成）。来源：网络爬虫 + 技术文档；专有混合，但在论文中透明公开。

- **开源模型（如Llama 3、BLOOM、GPT-J）**：
  明确使用公共数据集，如The Pile（800GB多语言混合）、C4（Colossal Clean Crawled Corpus，750GB英文网页）或OSCAR（多语言Common Crawl）。BLOOM使用了ROOTS（1.6TB，46种语言）。它们避免专有数据，专注于可复现性——可在Hugging Face的模型卡中查看具体分类。

简而言之：所有模型都依赖网络规模数据，但专有模型通过过滤/授权/合成数据提升质量。开源模型依赖社区策划的公共资源。

### 大型公共文本数据集下载链接

以下是顶级的免费可下载来源（大小近似；请检查更新）。如果存储有限，可从子集开始。

- **Common Crawl**：月度网页快照（总计PB级）。使用CC-MAIN索引过滤。[Common Crawl档案](https://commoncrawl.org/get-started)
- **The Pile**：800GB多样化英文文本（书籍、代码、arXiv等）。[EleutherAI The Pile on Hugging Face](https://huggingface.co/datasets/EleutherAI/pile)
- **C4（Colossal Clean Crawled Corpus）**：750GB清理后的英文网页（用于T5/GPT）。[TensorFlow Datasets C4](https://www.tensorflow.org/datasets/catalog/c4)
- **OSCAR（Open Super-large Crawled Aggregated coRpus）**：多语言网页（22种语言，约10TB）。[OSCAR on Hugging Face](https://huggingface.co/datasets/oscar-corpus/OSCAR-2201)
- **维基百科转储**：全文提取（英文约20GB）。[Wikimedia下载](https://dumps.wikimedia.org/enwiki/latest/)
- **BooksCorpus/OpenWebText**：11GB书籍 + 40GB Reddit/网页（GPT-2时代）。[OpenWebText on GitHub](https://github.com/jcpeterson/openwebtext)
- **RedPajama**：1T+词元，从Llama论文复现。[TogetherAI RedPajama on HF](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T)
- **LLMDataHub**：100+数据集的精选列表（聊天、代码等）。[GitHub LLMDataHub](https://github.com/Zjh-819/LLMDataHub)

更多资源请浏览Hugging Face Datasets中心：[Hugging Face Datasets](https://huggingface.co/datasets)。务必核实许可！

**参考文献**
[ChatGPT及我们的基础模型是如何开发的](https://help.openai.com/en/articles/7842364-how-chatgpt-and-our-language-models-are-developed)
[GPT-oss泄露了OpenAI训练数据的哪些信息](https://www.lesswrong.com/posts/iY9584TRhqrzawhZg/what-gpt-oss-leaks-about-openai-s-training-data)
[Anthropic将使用Claude聊天记录作为训练数据](https://www.wired.com/story/anthropic-using-claude-chats-for-training-how-to-opt-out/)
[Anthropic的HH-RLHF数据集](https://huggingface.co/datasets/Anthropic/hh-rlhf)
[DeepSeek-R1训练用了哪些数据？](https://epoch.ai/gradient-updates/what-went-into-training-deepseek-r1)
[DeepSeek模型完整指南：从V3到R1及更高版本](https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond)
[LLMDataHub：LLM训练优质数据集集锦](https://github.com/Zjh-819/LLMDataHub)
[LLM训练的开源数据集](https://kili-technology.com/large-language-models-llms/9-open-sourced-datasets-for-training-large-language-models)
[LLM训练数据：8大主要公共数据源](https://oxylabs.io/blog/llm-training-data)
