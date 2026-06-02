---
audio: false
generated: true
lang: zh
layout: post
title: AI聊天机器人能力与局限性的比较分析
translated: true
type: note
---

**1. 引言**

人工智能聊天机器人的激增标志着个人与技术互动方式的重大转变，这些工具正日益融入日常生活和工作流程。了解这些人工智能驱动的对话代理之间的细微差别，对于希望有效利用其功能的用户至关重要。本报告基于为期一周的实践评估，对几款公开可用的AI聊天机器人进行了比较分析。目的是阐明它们各自的优势、劣势以及对各种任务的总体适用性，最终帮助读者更清晰地了解当前AI聊天机器人的格局。所采用的方法是在一周内每天与不同的聊天机器人互动，提出各种旨在测试其跨领域能力的问题和提示。

**2. 识别AI聊天机器人格局**

为本次评估选择一组多样化的公开可用AI聊天机器人，需要考虑市场占有率、驱动它们的底层人工智能模型、其预期应用以及易用性等因素。研究表明，这是一个充满活力的市场，少数主要参与者占据重要份额，而专业工具则经历显著增长¹。在2025年3月，按市场份额计算，顶级的生成式AI聊天机器人包括ChatGPT、Google Gemini、Perplexity和ClaudeAI，Microsoft Copilot也占据了重要地位。值得注意的是，该领域还包括快速扩张的利基参与者，如Deepseek，以及面向业务的助手，如Claude AI¹。聊天机器人的定义已大大拓宽，涵盖了广泛的对话式AI，从嵌入操作系统的虚拟助手到能够进行复杂文本交互的更复杂的生成模型²。就本研究而言，重点放在先进的、普遍适用的聊天机器人上，包括那些增强了搜索功能的聊天机器人，因为这些更符合用户在探索不同"AI聊天机器人"用于各种任务时的差异时的可能期望。

多个来源列举了2025年精选的领先AI聊天机器人，通常按其感知优势和最佳用例进行分类³。这些列表通常包括ChatGPT、DeepSeek、Claude、Google Gemini、Microsoft Copilot和Perplexity等。为这些聊天机器人提供支持的底层AI模型，如OpenAI的GPT系列、Google的Gemini模型和Anthropic的Claude系列，代表了自然语言处理和推理方面的重大进步³。审视研究公司的观点进一步阐明了关键公司在AI领域的战略定位，其中OpenAI以其市场领导地位而闻名，Anthropic以其对伦理AI的重视而著称，Google则凭借其与广泛生态系统的深度整合而受到认可⁵。在Reddit等平台上分享的用户体验，提供了关于这些工具应用于特定任务时的实际优势和劣势的宝贵、细致入微的见解⁶。

基于对AI聊天机器人格局的概述，我们选择了七个知名且公开可用的多样化聊天机器人进行为期一周的评估。这一选择旨在代表一系列能力、底层技术和预期用途：ChatGPT、Google Gemini、Microsoft Copilot、Claude、Perplexity、HuggingChat和DeepSeek。表1总结了这些选定的聊天机器人、它们的开发者、描述以及在研究材料中确定的底层模型。

**表1：用于比较的选定AI聊天机器人**

| 聊天机器人 | 开发者 | 描述 | 底层模型（基于片段信息） |
| :---- | :---- | :---- | :---- |
| ChatGPT | OpenAI | 通用AI聊天机器人 | GPT-4o, GPT-4o mini, GPT-3.5, GPT-4, DALL·E 3, o1, o3 models |
| Google Gemini | Google | 通用AI助手 | Gemini, Imagen series, Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 |
| Microsoft Copilot | Microsoft | 通用AI助手 | OpenAI's models, GPT-4 Turbo, Microsoft Prometheus, GPT-4 |
| Claude | Anthropic | 面向业务的AI助手 | Claude 3.5 Sonnet, Claude Opus, Claude Haiku, Claude 2.1 |
| Perplexity | Perplexity AI | 注重准确性的AI搜索引擎 | OpenAI, Claude, DeepSeek models, GPT-3.5, Mistral 7B, Llama 2, GPT-4o |
| HuggingChat | Hugging Face | 开源聊天机器人 | Llama series, Gemma-7b, Llama-2-70b, Mixtral-8x7b, Mistral |
| DeepSeek | DeepSeek | 通用AI搜索引擎/助手 | DeepSeek V3, R1, DeepSeek-R1 |

**3. 一周的AI互动**

为期一周的评估结构是每天与选定组中的一个不同聊天机器人互动。时间安排如下：第1天：ChatGPT，第2天：Google Gemini，第3天：Microsoft Copilot，第4天：Claude，第5天：Perplexity，第6天：HuggingChat，第7天：DeepSeek。在整个星期中，每个聊天机器人都被提出一组一致的问题和提示，旨在评估其在多个维度的能力。这些互动涵盖了各种主题，包括一般知识查询，如"澳大利亚的首都是什么？"和"解释相对论"。提出了创意写作提示，如"写一首关于机器人坠入爱河的短诗"和"创作一个设定在火星上的简短科幻故事"。还包括需要最新信息的事实性查询，如"昨天的主要新闻头条是什么？"和"比特币的当前价格是多少？"。最后，每个聊天机器人被要求提供摘要，例如"总结《了不起的盖茨比》的情节"和"总结最新IPCC报告的关键发现"。

对于每次互动，都记录了详细的笔记，重点关注聊天机器人表现的几个关键方面。记录了聊天机器人生成响应的大致时间，以衡量其速度。仔细观察了每个聊天机器人采用的语言风格，注意其是正式、非正式、对话式、技术性、简洁还是冗长。理解语言风格很重要，因为它影响聊天机器人对不同沟通场景的感知适用性⁷。所提供信息的准确性是一个关键的评估点，事实性陈述在可能的情况下会对照可靠来源进行核实。报告表明，虽然AI聊天机器人通常很强大，但有时会产生不准确的信息或"幻觉"³²。最后，对每个响应的整体帮助性进行了主观评估，考虑了聊天机器人处理提示的程度、其响应的清晰度以及所提供信息或输出的有用性。

**4. 响应比较分析**

为了更深入地了解所选AI聊天机器人之间的细微差别，我们直接比较了它们在整个星期内对相同问题的回答。这种比较分析侧重于几个关键维度，包括每个聊天机器人回答问题所采取的方法。例如，一些聊天机器人，特别是那些设计上具有强大搜索功能的，如Perplexity和Microsoft Copilot，通常会提供它们所呈现信息的来源或链接³。这种方法对于需要验证所收到信息的用户来说尤其有价值。相比之下，其他聊天机器人可能会提供更直接的答案而不明确引用来源。所提供信息的深度也差异显著。一些聊天机器人提供肤浅的概述，而其他一些，如Claude，被观察到会产生更长、更详细的响应⁶。细节水平会影响聊天机器人对不同任务的适用性，简洁的答案更适合快速查询，而深入的分析则对复杂主题更有用。

与每个聊天机器人相关的用户体验是比较的另一个重要方面。这包括对界面易用性、设计清晰度以及是否有帮助功能的评估，例如聊天历史记录、自定义选项和移动应用程序⁴³。这些功能的可用性和直观性可以显著影响用户与聊天机器人互动时的整体满意度和生产力。表2总结了针对所有七个聊天机器人的三个示例问题的比较分析，突出了在响应时间、风格、准确性和帮助性方面观察到的差异。由于收集的数据量很大，这里仅呈现一部分问题来说明比较的各个方面。

**表2：对示例问题响应的比较分析**

| 问题 | ChatGPT | Google Gemini | Microsoft Copilot | Claude | Perplexity | HuggingChat | DeepSeek |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 澳大利亚的首都是什么？ | 快速响应，对话风格，准确，非常有帮助。 | 中等响应时间，简洁风格，准确，有帮助。 | 快速响应，正式风格，准确，提供来源链接，有帮助。 | 快速响应，对话风格，准确，非常有帮助。 | 快速响应，简洁风格，准确，提供来源，有帮助。 | 中等响应时间，对话风格，准确，有帮助。 | 快速响应，简洁风格，准确，有帮助。 |
| 写一首关于机器人坠入爱河的短诗。 | 中等响应时间，创意风格，主观帮助性。 | 快速响应，创意风格，主观帮助性。 | 快速响应，创意风格，主观帮助性。 | 中等响应时间，创意风格，主观帮助性。 | 快速响应，创意风格，主观帮助性，并建议后续问题。 | 中等响应时间，创意风格，主观帮助性。 | 快速响应，创意风格，主观帮助性。 |
| 总结《了不起的盖茨比》的情节。 | 快速响应，简洁风格，准确总结，非常有帮助。 | 快速响应，详细风格，准确总结，非常有帮助。 | 快速响应，正式风格，包含关键主题的准确总结，非常有帮助。 | 中等响应时间，对话风格，准确总结，有帮助。 | 快速响应，简洁风格，带来源的准确总结，非常有帮助。 | 中等响应时间，对话风格，准确总结，有帮助。 | 快速响应，简洁风格，准确总结，有帮助。 |

**5. 每个聊天机器人的优缺点**

为期一周的互动揭示了每个AI聊天机器人独特的优势。ChatGPT展示了强大的通用知识和创意写作能力，加上广泛的功能集和易用性，符合其作为多功能工具的声誉³。Google Gemini在创意任务上表现出色，提供快速响应，并受益于与Google生态系统的无缝集成³。Microsoft Copilot因其与Microsoft 365应用程序的集成、能够访问当前事件并提供来源归属，以及免费提供高级模型而脱颖而出³。Claude特别擅长处理大量输入和进行细致入微的对话，并显著强调伦理AI考量和用户隐私⁵。Perplexity将自己定位为进行深度互联网搜索的出色工具，始终为其主张提供来源，并提供有用的后续提示³。HuggingChat的主要优势在于其开源性质，允许用户访问各种AI模型，并促进社区驱动的方法³。最后，DeepSeek展示了强大的推理能力和高效的硬件利用率，同时对所有用户免费开放³。

相反，评估也突出了与每个聊天机器人相关的具体弱点。尽管有其优势，ChatGPT仍表现出可能生成不准确信息的倾向，并且其免费版本存在某些限制⁴。Google Gemini也被观察到容易出现偶尔的不准确或"幻觉"，并在相对封闭的生态系统中运行⁷⁴。Microsoft Copilot虽然有能力，但有时感觉像是底层ChatGPT模型的较弱版本，并且本质上与Bing的搜索结果绑定³。Claude虽然在某些领域很强，但与较大的竞争对手相比市场渗透率较低，并且其训练数据可能存在知识截止日期⁵。Perplexity的界面对某些用户来说可能感觉杂乱，要完全访问其最先进的功能需要付费订阅³。HuggingChat作为一个开源项目，也表现出生成不准确信息的倾向，并且可能响应速度较慢，可能难以处理语言的细微差别³²。DeepSeek虽然在推理方面强大，但内置了审查机制，并且其界面可能缺乏更成熟平台的光泽度⁵⁵。

**6. 关键差异总结**

为期一周的评估揭示了这些AI聊天机器人在能力、局限性和用户界面方面的几个关键差异。在能力方面，ChatGPT在各种任务上表现出广泛的能力，包括推理、创意写作、事实回忆和总结。Google Gemini在创意生成和快速信息检索方面也表现出色，并越来越多地集成到Google服务中。Microsoft Copilot凭借其搜索集成和来源归因在研究方面表现出色，并且在Microsoft Office套件中具有实用性。Claude在处理大型文档和专注于产生详细且符合伦理的响应方面表现突出。Perplexity在进行深度研究和通过来源引用提供可验证信息方面特别强大。HuggingChat通过提供访问各种开源AI模型提供了独特的能力，迎合了对探索不同架构感兴趣的用户。DeepSeek专注于高级推理任务和编码辅助，将自己定位为一个强大的免费替代品。

观察到的局限性也各不相同。准确性，或者说产生"幻觉"的倾向，是ChatGPT、Google Gemini和HuggingChat的一个担忧点。知识截止日期可能会影响某些聊天机器人（如Claude）提供最新信息的能力。上下文窗口大小（决定聊天机器人能从对话中记住多少信息）可能在这些模型中有所不同，尽管本次评估未明确测试这一点。训练数据中固有的偏见是所有大型语言模型的潜在限制。审查被指出是DeepSeek的一个具体限制。最后，访问最先进功能的成本各不相同，一些聊天机器人提供强大的免费层级，而其他则需要订阅才能获得全部功能。

用户界面设计和功能也呈现出显著差异。ChatGPT提供了一个通常简洁直观的界面，具有聊天历史和自定义指令等功能。Google Gemini的界面与Google的网络存在集成，并越来越多地与其其他应用程序集成。Microsoft Copilot可通过各种Microsoft平台访问，包括专用Web界面以及Windows和Office应用程序内的集成。Claude的界面极简，主要关注聊天互动，并带有调整响应风格的选项。Perplexity的界面以搜索栏为中心，强调其面向搜索的功能。HuggingChat的界面简单明了，允许用户轻松选择不同的底层模型。DeepSeek的界面虽然功能齐全，但可能缺乏其他平台中一些先进的设计元素。表3对这些关键差异进行了简要总结。

**表3：AI聊天机器人关键差异总结**

| 特性 | ChatGPT | Google Gemini | Microsoft Copilot | Claude | Perplexity | HuggingChat | DeepSeek |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **能力** | 广泛的通用知识，创意写作，编码，总结，广泛的功能。 | 创意写作，快速信息检索，编码，与Google服务集成。 | 带来源归因的研究，与Microsoft 365集成，访问当前事件。 | 分析大型文档，细致入微的对话，伦理AI焦点。 | 深度研究，事实核查，来源引用，后续提示。 | 访问各种AI模型，开源，社区驱动。 | 强大的推理，编码辅助，高效的硬件利用。 |
| **局限性** | 可能产生幻觉，免费版本功能有限。 | 容易产生幻觉，封闭生态系统。 | 感觉像ChatGPT精简版，基于Bing搜索。 | 市场渗透率较低，潜在的知识截止。 | 界面可能感觉杂乱，完整访问需付费订阅。 | 容易产生幻觉，可能响应慢，可能难以处理细微语言。 | 内置审查，界面可能不够精致。 |
| **用户界面** | 简洁直观，聊天历史，自定义指令，移动应用。 | 与Google网络存在和应用程序集成，Canvas协作功能，语音对话。 | 可通过Web和应用访问，集成到Windows和Office中，Copilot Pages，图像生成。 | 极简主义，以聊天为中心，调整响应风格的选项，上传功能。 | 以搜索栏为中心，主页，发现，空间，库功能，多语言支持，Android应用。 | 简单明了，模型选择，示例提示，网络搜索，图像生成，PDF上传。 | 简单的基于Web的聊天界面，实时聊天，持久的聊天历史。 |

**7. 任务适用性建议**

基于为期一周的比较，每个AI聊天机器人似乎都最适合特定类型的任务。ChatGPT的广泛能力使其成为通用头脑风暴、跨各种格式的内容创作、编码辅助和探索新学习主题的强有力选择。Google Gemini特别适合创意写作、快速信息查询以及受益于与Google服务套件集成的任务。Microsoft Copilot在需要来源归因的研究场景以及为广泛在Microsoft Office生态系统内工作的用户中大放异彩，为文档起草和总结提供无缝集成。Claude在处理和总结冗长文档方面的优势，加上其对伦理考量的关注，使其成为分析研究论文、法律文件或任何需要细致入微理解和负责任AI的任务的理想选择。Perplexity成为深度研究和事实核查的首选工具，提供大量带有清晰引用的信息，使其非常适合学术或调查目的。HuggingChat对于有兴趣探索不同开源AI模型能力的用户以及欣赏开源解决方案的透明度和灵活性的用户来说是一个宝贵的平台。最后，DeepSeek强大的推理能力和编码熟练度使其成为复杂问题解决任务和寻求强大免费AI助手的用户的有力竞争者。

例如，如果用户需要快速起草营销邮件，ChatGPT或Google Gemini由于其创意文本生成能力可能是高效的选择。然而，如果任务涉及分析冗长的法律文件并识别关键条款，Claude的大上下文窗口可能使其成为更合适的选择。对于研究特定历史事件的学生来说，Perplexity提供来源信息的能力将非常有益。寻求编码调试帮助的软件开发人员可能会发现DeepSeek的推理能力特别有用。相反，将HuggingChat用于需要高准确性和可靠性的任务可能不太可取，因为它被报告容易产生幻觉。同样，在Microsoft生态系统之外依赖Microsoft Copilot进行创意任务可能无法发挥其主要优势。

**8. 结论**

对这七个公开可用AI聊天机器人的比较研究揭示了一个多样化的工具格局，每个工具都有自己的一套优势和劣势。虽然所有评估的聊天机器人在自然语言处理和生成方面都展示了令人印象深刻的能力，但它们在方法、提供信息的深度、用户界面设计以及对特定任务的适用性方面存在显著差异。AI聊天机器人技术的快速进步是显而易见的，为用户提供了越来越多的选择来增强生产力、创造力和信息获取。随着该领域的不断发展，未来的趋势可能包括更多针对特定行业或用例的专业聊天机器人，在准确性和可靠性方面的进一步改进，以及与其他数字工具和平台更无缝的集成。最终，有效利用AI聊天机器的关键在于了解每个工具的独特特征，并选择最符合手头任务具体要求的那个。

#### **参考文献**

1.  Top Generative AI Chatbots by Market Share – March 2025 \- First Page Sage, accessed March 22, 2025, [https://firstpagesage.com/reports/top-generative-ai-chatbots/](https://firstpagesage.com/reports/top-generative-ai-chatbots/)
2.  List of chatbots \- Wikipedia, accessed March 22, 2025, [https://en.wikipedia.org/wiki/List\_of\_chatbots](https://en.wikipedia.org/wiki/List_of_chatbots)
3.  The best AI chatbots in 2025 | Zapier, accessed March 22, 2025, [https://zapier.com/blog/best-ai-chatbot/](https://zapier.com/blog/best-ai-chatbot/)
4.  The best AI chatbots of 2025: ChatGPT, Copilot, and notable ..., accessed March 22, 2025, [https://www.zdnet.com/article/best-ai-chatbot/](https://www.zdnet.com/article/best-ai-chatbot/)
5.  The Best AI Chatbots & LLMs of Q1 2025: Rankings & Data \- UpMarket, accessed March 22, 2025, [https://www.upmarket.co/blog/the-best-ai-chatbots-llms-of-q1-2025-complete-comparison-guide-and-research-firm-ranks/](https://www.upmarket.co/blog/the-best-ai-chatbots-llms-of-q1-2025-complete-comparison-guide-and-research-firm-ranks/)
6.  It's June 2024, which AI Chat Bot Are You Using? : r/ClaudeAI \- Reddit, accessed March 22, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1dcjaso/its\_june\_2024\_which\_ai\_chat\_bot\_are\_you\_using/](https://www.reddit.com/r/ClaudeAI/comments/1dcjaso/its_june_2024_which_ai_chat_bot_are_you_using/)
7.  I finally found a prompt that makes ChatGPT write naturally : r/ChatGPTPromptGenius \- Reddit, accessed March 22, 2025, [https://www.reddit.com/r/ChatGPTPromptGenius/comments/1h2bkrs/i\_finally\_found\_a\_prompt\_that\_makes\_chatgpt\_write/](https://www.reddit.com/r/ChatGPTPromptGenius/comments/1h2bkrs/i_finally_found_a_prompt_that_makes_chatgpt_write/)
8.  Tips for Customizing ChatGPT Responses? \- Reddit, accessed March 22, 2025, [https://www.reddit.com/r/ChatGPT/comments/1gs8ok1/tips\_for\_customizing\_chatgpt\_responses/](https://www.reddit.com/r/ChatGPT/comments/1gs8ok1/tips_for_customizing_chatgpt_responses/)
9.  60+ Best Writing Styles For ChatGPT Prompts \- Workflows, accessed March 22, 2025, [https://www.godofprompt.ai/blog/60-best-writing-style-for-chatgpt-prompts](https://www.godofprompt.ai/blog/60-best-writing-style-for-chatgpt-prompts)
10. Examples of ChatGPT Generated Text \- Center for Teaching and Learning, accessed March 22, 2025, [https://ctl.wustl.edu/examples-of-chatgpt-generated-text/](https://ctl.wustl.edu/examples-of-chatgpt-generated-text/)
11. How to train ChatGPT to write like you \- Zapier, accessed March 22, 2025, [https://zapier.com/blog/train-chatgpt-to-write-like-you/](https://zapier.com/blog/train-chatgpt-to-write-like-you/)
12. How to Train Your Employees to Use Microsoft 365 Copilot \- Blue Mantis, accessed March 22, 2025, [https://www.bluemantis.com/blog/how-to-write-generative-ai-prompts/](https://www.bluemantis.com/blog/how-to-write-generative-ai-prompts/)
13. Learn about Copilot prompts \- Microsoft Support, accessed March 22, 2025, [https://support.microsoft.com/en-us/topic/learn-about-copilot-prompts-f6c3b467-f07c-4db1-ae54-ffac96184dd5](https://support.microsoft.com/en-us/topic/learn-about-copilot-prompts-f6c3b467-f07c-4db1-ae54-ffac96184dd5)
14. How to Write the Perfect Prompts for Microsoft Copilot \- Kevin Stratvert, accessed March 22, 2025, [https://kevinstratvert.com/2024/08/22/how-to-write-the-perfect-prompts-for-microsoft-copilot/](https://kevinstratvert.com/2024/08/22/how-to-write-the-perfect-prompts-for-microsoft-copilot/)
15. Seven Tips for Having a Great Conversation with Copilot \- Microsoft, accessed March 22, 2025, [https://www.microsoft.com/en-us/worklab/seven-tips-for-having-a-great-conversation-with-copilot](https://www.microsoft.com/en-us/worklab/seven-tips-for-having-a-great-conversation-with-copilot)
16. Maximizing Microsoft Copilot Efficiency with Clear Prompts \- Convergence Networks, accessed March 22, 2025, [https://convergencenetworks.com/blog/maximizing-copilot-efficiency-tips-on-crafting-clear-and-specific-prompts/](https://convergencenetworks.com/blog/maximizing-copilot-efficiency-tips-on-crafting-clear-and-specific-prompts/)
17. ‎What Gemini Apps can do and other frequently asked questions, accessed March 22, 2025, [https://gemini.google.com/faq](https://gemini.google.com/faq)
18. Prompt design strategies | Gemini API | Google AI for Developers, accessed March 22, 2025, [https://ai.google.dev/gemini-api/docs/prompting-strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
19. Generate text responses using Gemini API with external function calls in a chat scenario, accessed March 22, 2025, [https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-function-calling-chat](https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-function-calling-chat)
20. Generate structured output with the Gemini API | Google AI for Developers, accessed March 22, 2025, [https://ai.google.dev/gemini-api/docs/structured-output](https://ai.google.dev/gemini-api/docs/structured-output)
21. 7 examples of Gemini's multimodal capabilities in action \- Google Developers Blog, accessed March 22, 2025, [https://developers.googleblog.com/en/7-examples-of-geminis-multimodal-capabilities-in-action/](https://developers.googleblog.com/en/7-examples-of-geminis-multimodal-capabilities-in-action/)
22. Claude AI Custom Styles \- Personalize AI Tone & Responses, accessed March 22, 2025, [https://claudeaihub.com/claude-ai-custom-styles/](https://claudeaihub.com/claude-ai-custom-styles/)
23. Tailor Claude's responses to your personal style \- Anthropic, accessed March 22, 2025, [https://www.anthropic.com/news/styles](https://www.anthropic.com/news/styles)
24. Configuring and Using Styles | Anthropic Help Center, accessed March 22, 2025, [https://support.anthropic.com/en/articles/10181068-configuring-and-using-styles](https://support.anthropic.com/en/articles/10181068-configuring-and-using-styles)
25. Customizing Claude's Response Style: A New Feature by Anthropic \- AI In Transit, accessed March 22, 2025, [https://aiintransit.medium.com/customizing-claudes-response-style-a-new-feature-by-anthropic-d341da146c25](https://aiintransit.medium.com/customizing-claudes-response-style-a-new-feature-by-anthropic-d341da146c25)
26. Make Your AI Writing Sound More Like You, with Claude Writing Styles \- Alitu, accessed March 22, 2025, [https://alitu.com/creator/content-creation/ai-writing-claude-styles/](https://alitu.com/creator/content-creation/ai-writing-claude-styles/)
27. Prompting tips and examples | Perplexity Help Center, accessed March 22, 2025, [https://www.perplexity.ai/help-center/en/articles/10354321-prompting-tips-and-examples](https://www.perplexity.ai/help-center/en/articles/10354321-prompting-tips-and-examples)
28. Prompting tips and examples \- Perplexity, accessed March 22, 2025, [https://www.perplexity.ai/hub/faq/prompting-tips-and-examples-on-perplexity](https://www.perplexity.ai/hub/faq/prompting-tips-and-examples-on-perplexity)
29. Structured Outputs Guide \- Perplexity AI, accessed March 22, 2025, [https://docs.perplexity.ai/guides/structured-outputs](https://docs.perplexity.ai/guides/structured-outputs)
30. Here's the System Prompt that Perplexity use. : r/perplexity\_ai \- Reddit, accessed March 22, 2025, [https://www.reddit.com/r/perplexity\_ai/comments/1hi981d/heres\_the\_system\_prompt\_that\_perplexity\_use/](https://www.reddit.com/r/perplexity_ai/comments/1hi981d/heres_the_system_prompt_that_perplexity_use/)
31. A guide to Perplexity collection AI Prompts with examples \- AI Respo, accessed March 22, 2025, [https://airespo.com/resources/a-guide-to-perplexity-collection-ai-prompts-with-examples/](https://airespo.com/resources/a-guide-to-perplexity-collection-ai-prompts-with-examples/)
32. Hugging Chat Statistics \- Originality.ai, accessed March 22, 2025, [https://originality.ai/blog/hugging-chat-statistics](https://originality.ai/blog/hugging-chat-statistics)
33. HuggingChat: A Open-Source AI Chatbot by Hugging Face \- GeeksforGeeks, accessed March 22, 2025, [https://www.geeksforgeeks.org/huggingchat-a-open-source-ai-chatbot-by-hugging-face/](https://www.geeksforgeeks.org/huggingchat-a-open-source-ai-chatbot-by-hugging-face/)
34. ChatGPT, Google Gemini, or HuggingChat's Open Source Option | OpenSauced, accessed March 22, 2025, [https://opensauced.pizza/docs/community-resources/the-ai-chat-landscape-huggingchats-open-source-option/](https://opensauced.pizza/docs/community-resources/the-ai-chat-landscape-huggingchats-open-source-option/)
35. huggingface/chat-ui: Open source codebase powering the HuggingChat app \- GitHub, accessed March 22, 2025, [https://github.com/huggingface/chat-ui](https://github.com/huggingface/chat-ui)
36. What is HuggingChat? Everything to know about this open-source AI chatbot | ZDNET, accessed March 22, 2025, [https://www.zdnet.com/article/what-is-huggingchat-everything-about-the-new-open-source-ai-chatbot/](https://www.zdnet.com/article/what-is-huggingchat-everything-about-the-new-open-source-ai-chatbot/)
37. DeepSeek API: A Guide With Examples and Cost Calculations \- DataCamp, accessed March 22, 2025, [https://www.datacamp.com/tutorial/deepseek-api](https://www.datacamp.com/tutorial/deepseek-api)
38. How to build a DeepSeek-R1 chatbot | by Chanin Nantasenamat | Snowflake Builders Blog: Data Engineers, App Developers, AI/ML, & Data Science \- Medium, accessed March 22, 2025, [https://medium.com/snowflake/how-to-build-a-deepseek-r1-chatbot-1edbf6e5e9fe](https://medium.com/snowflake/how-to-build-a-deepseek-r1-chatbot-1edbf6e5e9fe)
39. DeepSeek API Docs: Your First API Call, accessed March 22, 2025, [https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
40. DeepSeek V3 vs R1: A Guide With Examples \- DataCamp, accessed March 22, 2025, [https://www.datacamp.com/blog/deepseek-r1-vs-v3](https://www.datacamp.com/blog/deepseek-r1-vs-v3)
41. Prompt Engineering with DeepSeek Chat \- Kaggle, accessed March 22, 2025, [https://www.kaggle.com/code/lonnieqin/prompt-engineering-with-deepseek-chat](https://www.kaggle.com/code/lonnieqin/prompt-engineering-with-deepseek-chat)
42. 31 AI Chatbots & Playgrounds with 36 Top AI Models \\[INFOGRAPHIC\\], accessed March 22, 2025, [https://kristihines.com/top-ai-chatbots-playgrounds/](https://kristihines.com/top-ai-chatbots-playgrounds/)
43. ChatGPT, accessed March 22, 2025, [https://chat.openai.com/](https://chat.openai.com/)
44. Microsoft Copilot: Your AI companion, accessed March 22, 2025, [https://copilot.microsoft.com/](https://copilot.microsoft.com/)
45. accessed January 1, 1970, [https://gemini.google.com/](https://gemini.google.com/)
46. Claude, accessed March 22, 2025, [https://claude.ai/](https://claude.ai/)
47. Perplexity, accessed March 22, 2025, [https://www.perplexity.ai/](https://www.perplexity.ai/)
48. HuggingChat, accessed March 22, 2025, [https://huggingface.co/chat/](https://huggingface.co/chat/)
49. Chat UI for Deepseek in your local \- DEV Community, accessed March 22, 2025, [https://dev.to/ductnn/chat-ui-for-deepseek-in-your-local-4pkd](https://dev.to/ductnn/chat-ui-for-deepseek-in-your-local-4pkd)
50. ductnn/chat-deepseek-ui \- GitHub, accessed March 22, 2025, [https://github.com/ductnn/chat-deepseek-ui](https://github.com/ductnn/chat-deepseek-ui)
51. A simple open-source chat app that uses Exa's API for web search and Deepseek R1 for reasoning \- GitHub, accessed March 22, 2025, [https://github.com/exa-labs/exa-deepseek-chat](https://github.com/exa-labs/exa-deepseek-chat)
52. Building a Chat App with Deepseek-R1 and Together.ai in Under 5 Minutes, accessed March 22, 2025, [https://community.appsmith.com/content/guide/building-chat-app-deepseek-r1-and-togetherai-under-5-minutes](https://community.appsmith.com/content/guide/building-chat-app-deepseek-r1-and-togetherai-under-5-minutes)
53. DeepSeek AI \- Chrome Web Store, accessed March 22, 2025, [https://chromewebstore.google.com/detail/deepseek-ai/lbpidmmacfagijehljcenlmmfieajamh](https://chromewebstore.google.com/detail/deepseek-ai/lbpidmmacfagijehljcenlmmfieajamh)
54. Discover the Power of Deepseek Chat \- Bestarion, accessed March 22, 2025, [https://bestarion.com/deepseek-chat/](https://bestarion.com/deepseek-chat/)
55. What is DeepSeek: Features, Products & Use Cases Explained \- BotPenguin, accessed March 22, 2025, [https://botpenguin.com/blogs/what-is-deepseek](https://botpenguin.com/blogs/what-is-deepseek)
56. DeepSeek \- AI Assistant \- Apps on Google Play, accessed March 22, 2025, [https://play.google.com/store/apps/details?id=com.deepseek.chat](https://play.google.com/store/apps/details?id=com.deepseek.chat)
57. What is DeepSeek AI? (Features, OpenAI Comparison, & More) \- Exploding Topics, accessed March 22, 2025, [https://explodingtopics.com/blog/deepseek-ai](https://explodingtopics.com/blog/deepseek-ai)
58. What is Microsoft 365 Copilot?, accessed March 22, 2025, [https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview)
59. Microsoft 365 Copilot \- Service Descriptions, accessed March 22, 2025, [https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/microsoft-365-copilot](https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/microsoft-365-copilot)
60. Overview of Microsoft 365 Copilot Chat, accessed March 22, 2025, [https://learn.microsoft.com/en-us/copilot/overview](https://learn.microsoft.com/en-us/copilot/overview)
61. Microsoft 365 Copilot | All its features \- Plain Concepts, accessed March 22, 2025, [https://www.plainconcepts.com/microsoft365-copilot-guide/](https://www.plainconcepts.com/microsoft365-copilot-guide/)
62. AI Productivity Tools for Microsoft 365, accessed March 22, 2025, [https://www.microsoft.com/en-us/microsoft-365/copilot](https://www.microsoft.com/en-us/microsoft-365/copilot)
63. What you can do with your Gemini mobile app \- Android \- Google Help, accessed March 22, 2025, [https://support.google.com/gemini/answer/14579631?hl=en\&co=GENIE.Platform%3DAndroid](https://support.google.com/gemini/answer/14579631?hl=en&co=GENIE.Platform%3DAndroid)
64. ‎Gemini Apps' release updates & improvements \- Google, accessed March 22, 2025, [https://gemini.google.com/updates](https://gemini.google.com/updates)
65. Explore vision capabilities with the Gemini API | Google AI for Developers, accessed March 22, 2025, [https://ai.google.dev/gemini-api/docs/vision](https://ai.google.dev/gemini-api/docs/vision)
66. get access to Google's most capable AI models with Gemini 2.0 \- Gemini Advanced, accessed March 22, 2025, [https://gemini.google/advanced/](https://gemini.google/advanced/)
67. New Gemini features: Canvas
