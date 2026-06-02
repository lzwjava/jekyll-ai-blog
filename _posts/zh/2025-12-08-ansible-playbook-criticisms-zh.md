---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 对Ansible Playbooks的批评
translated: true
type: note
---

问题：关于 Ansible playbook 有哪些冷门观点？

答案：

Ansible playbook 虽然因简化基础设施自动化而广受好评，但在 DevOps 从业者的小众讨论中也招致了一些尖锐的批评。以下是来自社区帖子和讨论串的一些冷门观点，重点关注它们的局限性、误用和替代方案。这些观点常常挑战该工具“无代理简化”的宣传：

*   **冗长的 playbook 与简单的脚本相比简直是噩梦**：YAML 作为配置格式很出色，但作为编程语言却一塌糊涂。任何超过 500 行（更不用说 3,400 行）的 playbook 都会变成难以维护的意大利面条式代码，充斥着嵌套循环、Jinja2 模板地狱和条件膨胀。到了这种程度，不如切换到 Python 脚本甚至 Bash——它读起来、调试起来和重写起来都更快。Ansible 的“声明式”承诺在真正的复杂性面前土崩瓦解，使其比命令式脚本更糟糕。

*   **Playbook 不适合编程——将逻辑委托给其他地方**：Ansible 擅长副作用（例如，安装软件包或配置服务），但在算法、条件或任何真正的计算方面却很糟糕。将决策卸载到像 Python 这样的适当语言中，在那里你可以对逻辑进行单元测试，然后将结果输入到一个简单的 playbook 中。将 playbook 视为代码库会导致脆弱、难以测试的混乱，它们“神奇地”掩盖错误而不是暴露错误。

*   **对于大多数用例来说，“事实真相”的执念被高估了**：Ansible 社区对集中式“事实真相”的执着（例如，从每台服务器拉取事实来验证状态）效率低下且不必要。对于环境，只需在角色中定义所需的软件包/服务并应用它们——除非你处于像纯网络这样的超复杂设置中，否则不要查询实时系统。这种“拉取一切”的心态浪费了周期，忽略了 playbook 作为基于推送的执行器会更好。

*   **幂等性在实践中是个神话，导致隐性故障**：Playbook 被宣传为幂等（重复运行不会改变任何东西），但复杂的 playbook 通常会因未处理的边缘情况而漂移，例如循环中的部分故障或特定于操作系统的怪癖。建议“运行两次以验证”暴露了这一点——这不是一个特性，而是一个 hack。实际上，这助长了草率的测试，你最好使用会大声失败的工具（例如 Terraform），而不是 Ansible 安静的“它奏效了……大部分”。

*   **YAML 的语法和冗长降低了生产力**：Ansible 对 YAML 的依赖使得即使是简单的任务也因缩进之争和冗长的块而显得臃肿。它不是“人类可读”的——它是一个假装是 DSL 的配置文件。对于除了即时命令之外的任何事情，样板代码都超过了好处，特别是当异步处理或错误日志感觉像是附加的并且容易出错时。专业人士坚持即时模式，其余的则转向脚本。

*   **角色与 playbook 的区别是武断且令人困惑的**：除了目录结构和变量优先级之外，“角色”和“playbook”之间没有真正的区别——它们都只是解构的 YAML。这导致了过度工程：人们将所有东西都塞进单一的 playbook 中而不是模块化的角色，反之亦然，从而创建了僵硬的意大利面条式代码。为了可维护性，保持扁平化，使用许多小型 playbook，而不是一个涵盖所有内容的“上帝 playbook”。

*   **Ansible 对于现代云原生工作流来说已经过时了**：在一个 Kubernetes、Terraform 和不可变基础设施的世界中，playbook 对于声明式编排来说显得笨重。它们非常适用于本地 SSH 推送，但在云环境中添加了不必要的抽象层，因为云提供商原生处理配置。如果你完全采用 AWS/GCP，请完全跳过 Ansible——专注于与 CI/CD 更好地集成而无需 YAML 负担的 IaC 工具。

这些观点强调了 Ansible 在快速、无代理自动化方面的优势，但也凸显了将其扩展为成熟系统时的挫败感。如果你正在构建 playbook，请优先考虑简单性：使用模块而不是 shell 命令，严格测试幂等性，并知道何时转向代码。

参考资料:
- [Ansible Playbooks with 3,400 lines aren't better than bash](https://x.com/brankopetric00/status/1997053364690211182)
- [Open Source Collection of Ansible Good and Bad Practices](https://www.reddit.com/r/ansible/comments/xw588g/open_source_collection_of_ansible_good_and_bad/)
- [Source of Truth is not important](https://www.reddit.com/r/ansible/comments/1dqtjja/source_of_truth_is_not_important/)
- [Good Practices for Ansible - The Zen of Ansible](https://redhat-cop.github.io/automation-good-practices/)
- [The ultimate guide for writing high-quality Ansible Playbooks](https://steampunk.si/spotter/blog/ultimate-guide-for-high-quality-ansible-playbooks/)
- [What is "best"? One playbook doing everything, or many?](https://www.reddit.com/r/ansible/comments/11m70hi/what_is_best_one_playbook_doing_everything_or/)
