---
audio: false
generated: false
image: false
lang: en
layout: post
title: A Conversation with the Founder of Yotta Labs
translated: false
---

The two participants are [Zhiwei Li](https://lzwjava.com), an AI full-stack engineer, and [Daniel Da Li](https://www.linkedin.com/in/danielbit/), founder of [Yotta Labs](https://www.yottalabs.ai).

---

They discussed posting the interview transcript for later review, and one participant mentioned that they could share it after converting it using the local Whisper model on an RTX 4070 with Whisper. The other agreed, saying they had no issue with that.

The conversation turned to supporting heterogeneous hardware acceleration. One participant noted that while most work was currently focused on NVIDIA, AMD was growing quickly. They discussed why there was a need for heterogeneous support, pointing out that NVIDIA's hardware could be hard to get, and in terms of performance per token, NVIDIA not have an advantage in every scenario. It was argued that this required a more detailed classification of use cases. Someone suggested that a single company dominating the market was unlikely to be sustainable, given that models themselves had not converged and AI scenarios were proliferating, naturally requiring different hardware for different tasks. The main reason people used NVIDIA now, it was raised, was because its software experience was particularly good.

One participant explained that Yotta Labs aimed to abstract away the differences at the lower level, so that users could come to them for inference, use their framework, and get deployed without worrying about the underlying hardware. The complexity below would be handled by Yotta Labs. Another participant asked whether multimodal models, with components like tokenizers, VAE decoders, and diffusion steps, would introduce additional challenges. They discussed whether it might be necessary to place different parts of the multimodal pipeline—such as the VAE on one machine and the diffusion on another—on separate hardware. The response was that for now, such fine-grained separation was not necessary, and the goal was to abstract away those differences.

The discussion then turned to the level of abstraction. One participant argued that the more abstract the system, the simpler and more usable it was for the user, but the user also lost control over the underlying details. They gave the example of a "token factory," where the user would simply buy tokens without needing to know what hardware was running underneath. Another participant questioned whether this abstraction was necessary, suggesting that hardware vendors could simply deploy their own NVIDIA and AMD solutions with a gateway to route traffic. The response was that Yotta Labs would provide optimization for their software, otherwise there would be nothing to deploy. It was clarified that the deployment would be Yotta Labs' optimized SGLang, focused on operator optimization.

They considered whether they could imagine a more ambitious scenario. One participant noted that the world was currently short on compute—both AMD and NVIDIA GPUs were hard to get due to limited supply, which might be a more pressing need. Inference cost was also deemed important. When asked how much Yotta Labs could save users on inference, the response was that it depended on the scenario, but the target was to save 30%-40%. It was mentioned that they had customers who were interested and in active discussions.

When asked how these savings would actually be achieved, the response was that a significant part came from the routing layer: requests are intelligently routed across heterogeneous hardware so that each request lands on the silicon that serves it cheapest and fastest for that scenario. Combined with operator-level optimization on the runtime side, this is how the 30%-40% cost reduction target is reached.

The conversation also touched on hiring. Yotta Labs is currently looking for engineers in three areas: first, operator and CUDA optimization, doing low-level kernel work to squeeze performance out of the hardware; second, inference engine engineers, working on the serving and runtime layer itself; and third, ops and Kubernetes engineers for AI inference, supporting the infrastructure side of the AI inference platform, GPU rental, and inference routing.

One participant also raised a broader industry argument (Movva's central argument): the entire AI stack—from GPU kernels all the way to data center power sourcing—has been built around interactive chatbots that demand low latency, while the real growth market is background agents that run for hours or days without supervision. For these workloads, latency is irrelevant and cost per token is everything. The response was that this is exactly the direction Yotta Labs is building for: when the customer is a background agent running around the clock, nobody cares whether a single token comes back in 50ms or 500ms—they care about the total bill. That changes the optimization target completely, and it is precisely where heterogeneous hardware and smart routing shine, since latency that is not needed can be traded for cost that is.

The conversation turned to the company's founding motivation. One participant explained that they wanted to solve AI inference or AI infrastructure, and cited two main reasons: first, that existing NeoClouds were "too garbage," and software was a critical component; second, that NVIDIA's dominance felt unsustainable.

Another participant brought up the concept of Pivotal Cloud Foundry (PCF) and OpenShift, describing how they allowed users to deploy on AWS, Azure, or Google Cloud without being locked into a single vendor. The user, such as a bank, could run microservices on PCF or OpenShift without knowing which cloud provider was underneath, enabling cost management and migration. They asked whether Yotta Labs could provide a similar "lock-free" experience for hardware. The response was that this was the intention, but hardware lock-free was different from cloud platform lock-free, because each vendor's hardware was quite different. One participant noted that the current priority was less about abstracting differences and more about solving the basic problem of whether models could even run on AMD hardware, since many could not. It was agreed that AMD's ROCm ecosystem was far behind.

Toward the end, one participant asked if the other had any questions. The other said no, noting it was late, and suggested they could continue the conversation another time. They agreed to learn more about each other's companies and explore potential collaboration. They exchanged thanks and goodbyes.

## About Yotta Labs

Yotta Labs is building the next generation multi-silicon AI cloud and runtime platform to power the world's most demanding AI workloads. We enable training and inference across NVIDIA GPUs, AMD GPUs, and AWS Trainium, helping AI companies achieve the best performance and economics across heterogeneous hardware. Our mission is to provide high-performance AI computing and Model API services, enabling AI companies, research labs, and enterprises to train, deploy and integrate cutting-edge models at scale.

![Yotta Labs](yottalabs.jpg)
