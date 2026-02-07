---
audio: false
generated: true
image: false
lang: zh
layout: post
model: none
title: Google Cloud - 对话
translated: true
type: note
---

A: 我们这里有一套大量的 Cloud Developer 考试题。与其死记硬背，我认为理解 Cloud Run、Cloud Functions 和 Spanner 等服务背后的设计逻辑更有价值。你会从哪里开始？

B: 我会从 Cloud Run 开始，因为它在考试中无处不在。从实践角度来看，Cloud Run 关乎 stateless containers、快速迭代，以及将 scaling 和 load balancing 等 infrastructure 问题委托给 Google。许多问题都在间接考察你是否理解 Cloud Run 是根据 revision 和 traffic 进行扩展的，而不是由你管理的 instances。

A: 没错，特别是那些关于 canary releases 和 traffic splitting 的问题。在实践中，团队很少重新部署独立的服务——他们只是在 revision 之间切换流量。

B: 正是如此。这就是为什么考试强调 revision。每个 revision 都是不可变的，这意味着 environment variables 等配置更改会强制生成新的 revision。这也是你在不中断服务的情况下进行渐进式发布的方式。

A: 那么关于 authentication 的问题呢？有很多场景涉及 service accounts、Workload Identity，以及避免使用 key files。

B: 这是 GCP 的核心理念：避免长效 secrets。将 service accounts 绑定到 Cloud Run 或为 GKE 使用 Workload Identity 是首选模式。考试经常测试你是否知道 service account keys 是最后的手段。

A: 我注意到数据库问题中也有类似的模式。例如，Spanner 与 Firestore 以及 Cloud SQL 的对比。

B: 是的，关键在于理解权衡（trade-offs）。当你需要 global strong consistency 和 horizontal scaling 时，Spanner 就会出现。Firestore 更多用于 document 访问和 event-driven systems。Cloud SQL 是大家熟悉的，但在扩展性上有限制。

A: 一些题目还考察了运维思维，比如处理大文件上传或 background jobs。

B: 那些都是实践中的陷阱。直接将大文件上传到 Cloud Run 是个坏主意——指向 Cloud Storage 的 signed URLs 才是现实世界的解决方案。对于 background processing，考试希望你考虑使用 Cloud Run jobs 或 Pub/Sub 等托管服务，而不是手动管理的 VMs。

A: 那 observability 呢？有多个服务——Logging、Monitoring、Trace、Profiler——很容易混淆。

B: 考试测试的是关注点分离（separation of concerns）。Logging 用于 events，Monitoring 用于 metrics，Trace 用于跨服务的 request latency，而 Profiler 用于观察一段时间内的 CPU 和 memory 行为。在真实系统中，你通常会同时使用这四者。

A: Security 似乎也无处不在：Binary Authorization、Secret Manager、IAM roles、API Gateway。

B: 这反映了真实的生产系统。Binary Authorization 确保了 supply chain 的信任，Secret Manager 将敏感配置外部化，而 IAM 则是关于 least privilege。考试很少考偏僻的细节——它考察你是否选择了受管理的、安全的默认方案。

A: 所以总的来说，考试并不是真的为了出脑筋急转弯？

B: 并不是。它考察的是架构判断力。如果你像一个追求 minimal ops、strong security 和 managed scalability 的 Cloud Developer 一样思考，大多数答案就会变得显而易见——即使没有死记硬背。

A: 这很有帮助。听起来掌握 GCP 服务的心智模型比刷题更重要。

B: 绝对是。题目只是从不同角度测试相同的原则：serverless first、identity over secrets、managed services 优于 self-managed infrastructure。

A: 我认为考生低估的一个领域是 CI/CD。有几道题同时提到了 Cloud Build、Artifact Registry 和 Binary Authorization。人们应该如何在脑海中连接这些？

B: 把它想象成一个供应链。Cloud Build 是工厂，Artifact Registry 是仓库，而 Binary Authorization 是门口的保安。在实践中，你构建一次、扫描一次、签名一次，然后在部署时强制执行信任。

A: 很有道理。考试还在不断推行 build triggers 而不是 manual builds。

B: 没错。Google 希望你以声明式（declaratively）的方式思考。与代码库绑定的 Cloud Build trigger 反映了真实团队的工作方式——每一次 commit 都是可复现、可审计且自动化的。本地的手动 gcloud 构建固然可以，但不能作为一个系统。

A: 聊聊 Pub/Sub 吧。关于 ordering、exactly-once delivery 和 high throughput 有很多问题。

B: Pub/Sub 问题通常测试对规模的直觉。如果你看到每秒数百万个 events，标准的 Pub/Sub 就很合适。如果每个实体的严格顺序（strict ordering）很重要，就需要用到 ordering keys。Exactly-once 更多是关于 billing 和 deduplication 的保证，而不是业务逻辑。

A: 即使有了 exactly-once delivery，idempotency（幂等性）仍然很重要，对吧？

B: 永远如此。在真实系统中，重试无处不在——网络故障、超时、重新部署。这就是为什么考试经常暗示要在 Firestore 或数据库中存储已处理的 IDs 或使用 idempotency keys。

A: 我还注意到反复强调在 compute services 中避免 state（状态）。

B: 是的，这是基础。Cloud Run、Cloud Functions、App Engine——它们都假设 instances 是 ephemeral（瞬态的）。任何重要的东西都要存入托管存储：数据库、对象存储或像 Memorystore 这样的缓存。

A: 说到缓存，Redis 的问题看起来很简单，但其深层含义是什么？

B: 延迟控制（Latency control）。Memorystore 的存在是为了让你不至于在 hot paths 上滥用数据库。在考试和现实生活中，如果你看到对延迟容忍度低的重复读取，Redis 就是提示——哪怕它增加了一个组件。

A: 什么是 monitoring signals？有些问题提到了 CPU metrics 触发 scaling。

B: 这些是测试你是否知道什么是自动的，什么是可观测的。Cloud Run 是根据请求而不是直接根据 CPU 进行扩展的，但 CPU metrics 会告诉你为什么要进行扩展。Monitoring 是为了获取洞察（insight），而不是为了让你手动调节控制回路。

A: Cloud Tasks 和 Pub/Sub 之间也存在某种哲学差异，这在题目中也有体现。

B: 对。Cloud Tasks 关乎控制——rate limiting、重试、目标端点。Pub/Sub 关乎 fan-out 和规模。如果问题提到 back-pressure 或精准的重试定时，Cloud Tasks 就是对应的选择。

A: 即便 Cloud Run 更加现代，App Engine 仍然会出现。

B: App Engine 的问题大多关于 legacy 和流量管理概念——versions、services 和 dispatch rules。Google 希望你能识别它，不一定非要在新项目中首选它。

A: 那么，如果有人认真准备这个考试，他们的学习策略应该是怎样的？

B: 构建心智场景。不要问“什么是 Cloud Run？”，而要问“为什么这里我会拒绝 Compute Engine？”考试奖励的是架构本能，而不是琐碎的知识点。

A: 这也符合实际工作。在生产环境中，知道定义并不能加分。

B: 正是如此。如果你内化了这些原则——managed 优于 manual、identity 优于 secrets、stateless 优于 stateful——正确答案几乎会呼之欲出。

A: 我在题目中看到的另一个模式是倾向于平台原生解决方案，而不是第三方工具。你认为考试是否偏向于生态系统锁定（lock-in）？

B: 并不完全是锁定——更多是关于运维责任。Google Cloud 服务的存在是为了减轻认知负荷。考试假设如果 Google 提供了一个托管的原语（primitive），除非有充分的理由，否则它通常就是正确的默认方案。

A: 所以是为了最小化运维表面积（operational surface area）？

B: 没错。每个 self-managed 组件都增加了补丁、监控、扩展和安全工作。考试不断奖励那些将复杂性外部化到平台的设计。

A: 这在存储决策中也有体现。例如，选择用于上传的 signed URLs，而不是通过计算服务代理数据。

B: 是的，这是一个经典的模式。Data plane 直接去存储，control plane 经过计算。这降低了成本、延迟和故障域。

A: 我在 API 设计问题中看到了类似的情况——API Gateway、Endpoints、Apigee。考试似乎在测试治理（governance），而不仅仅是路由。

B: 正确。API 管理关乎策略执行：auth、quotas、logging、versioning。路由是问题中最小的部分。这就是为什么这些服务在企业架构中很重要。

A: 那 GKE 的问题呢？它们似乎较少见，但一旦出现，就非常具体。

B: GKE 被视为“你确实需要控制权”的选项。如果问题涉及 GPUs、自定义网络、sidecars 或复杂的编排，Kubernetes 就会出现。否则，Cloud Run 通常会胜出。

A: 所以 Cloud Run 是默认的抽象，而 GKE 是逃生舱。

B: 这是一个很好的心智模型。Serverless 第一，containers 第二，VMs 最后。

A: 一些题目还考察了成本意识，比如 preemptible VMs 与托管服务的对比。

B: 是的，逻辑在于 workload 的形状。具有容错能力的批处理作业 → preemptible 或 spot。长时间运行的 APIs → managed services。事件驱动的工作负载 → serverless。

A: 考生应该如何思考这些问题中的可靠性？

B: 可靠性等于设计，而不是英雄主义。Multi-region 存储、托管数据库、重试语义、幂等性和无状态服务。考试始终青睐系统性的可靠性，而不是手动恢复。

A: 所以隐藏的课程大纲其实是云原生（cloud-native）思维。

B: 是的。不是“我如何在 Google Cloud 上运行服务器？”，而是“我如何假设服务器是可丢弃的（disposable）来设计系统？”

A: 这也解释了为什么 configuration management 和 feature flags 会出现。

B: 没错。现代系统将部署（deploy）与发布（release）分离。你部署代码，但通过配置、标志和版本来控制行为。这是成熟的工程实践，考试反映了这一点。

A: 如果让你用一句话总结这种心态？

B: 将针对变化、故障和规模的设计作为默认模式，而不是例外。

A: 这实际上是一个非常扎实的备考框架。

B: 也是构建真实系统的框架。如果你把考试当作架构培训而不是证书准备，你会获得更多的长期价值。