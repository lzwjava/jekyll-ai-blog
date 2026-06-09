---
audio: false
generated: false
image: false
lang: en
layout: post
title: "Technical Discussion: Game Server Development, Programming Languages, and AI-Assisted Coding"
translated: false
---

Two participants: A game developer and [lzwjava](https://github.com/lzwjava).

The following conversation was transcribed using Whisper on an RTX 4070, then refined and organized with the help of AI tools. The original conversation was in Chinese.

Note: Because both transcription and refinement were AI-assisted, some details may be inaccurate or paraphrased. Please verify any important information independently before relying on it.

---

This meeting covered a wide-ranging technical discussion between two backend engineers, focusing on game server development, programming languages (C++, Go), network protocols (TCP vs. UDP), data structures in gaming, and the increasing role of AI in software development workflows. The conversation also touched on technical interview approaches, infrastructure considerations, and the evolving landscape of AI-assisted coding tools like Web Coding and Cline.

## Background and Context

The participants began by establishing their respective backgrounds. One participant works primarily on server-side development, with experience across multiple companies and projects in the gaming industry. The other participant also works on the server side, though in a different domain — primarily at a large financial institution, with past experience at companies including a gaming company in China. Both participants are backend engineers, though their specific industry focuses differ — one in gaming, the other in financial services.

The meeting was initially framed as a technical discussion rather than a formal interview. One participant mentioned that they would record the conversation, manually remove any sensitive material, share the cleaned version with the other participant for approval, and then potentially publish it online.

## Programming Languages and Experience

### Core Languages Used

When asked about programming languages, one participant shared their background: they started their career working heavily with C++, then later used Go extensively. Beyond these languages, they have used almost nothing else. When pressed on which language they are most proficient in, they were hesitant to claim expertise in any — especially C++, noting that anyone claiming to be a "C++ expert" is likely exaggerating. They described themselves as "competent enough" with Go for practical work.

The other participant mentioned their professional background: they use Java at their company on a daily basis but have been exploring other languages in personal projects and AI-assisted coding work. They have also recently started experimenting with Rust, having written roughly 2,000 lines of Rust code as a learning exercise, though they acknowledged they are still early in the learning curve.

### Language Philosophy

One participant expressed the view that programming languages are fundamentally tools for getting work done, and the choice depends entirely on the project's existing tech stack. They framed C++ as essentially "C with object-oriented features added." This pragmatic, project-driven approach to language selection was a recurring theme throughout the discussion.

### C++ Challenges

The discussion briefly touched on common C++ pain points — pointers, null pointers, and memory leaks. One participant noted that C++ has a notoriously high barrier to entry compared to other languages, which is part of why Go has found a niche. Go sits between C++ and more dynamic languages, offering good performance while maintaining a relatively low learning curve. The other participant agreed that these issues are fundamentally syntactic concerns, not architectural ones.

### Coding Style and Paradigms

When asked about their coding style — whether they lean toward functional programming, object-oriented programming, or procedural programming — one participant said they have no fixed style. Their approach is dictated entirely by the project. They estimated that procedural programming is the most common pattern in their C++ and Go code. They also mentioned having worked on pure C projects that had no object-oriented features at all.

The participants noted that in game development specifically, there is a major tension between traditional OOP (with inheritance hierarchies) and a different paradigm called **ECS (Entity-Component-System)** . ECS is a architectural pattern where components are composed into entities, rather than building deep inheritance trees. One participant confirmed that ECS is widely used in game development, particularly with Lua-based frameworks.

## Game Server Architecture and Networking

### The Need for Game-Specific Backend Frameworks

One participant explained why game servers typically require specialized frameworks rather than using general-purpose solutions like Spring Boot, which is ubiquitous in internet application development. The key difference lies in the nature of the data being transmitted and the specific requirements of real-time gameplay — for example, the need to synchronize state among multiple players in a session. This is why game companies often develop their own internal server frameworks, rather than relying on broadly shared open-source solutions.

### Skynet and Big World

The discussion touched on two notable game server frameworks:

- **Skynet** is an open-source Lua-based framework. However, one participant noted that despite being open-source and having a community of users, it is not widely used — their past game companies did not adopt it. Smaller studios sometimes use it to ship products quickly.
- **Big World** (Big World Engine) is a commercial engine/framework specifically designed for building massively multiplayer online (MMO) games. It includes built-in infrastructure for synchronization between many players. This framework is older and less commonly used today, but it is documented and findable online.

One participant clarified that in the gaming world, these are typically called "engines," not "frameworks."

### TCP vs. UDP in Game Networking

A significant portion of the discussion centered on the choice between TCP and UDP for game networking. One participant mentioned that in their experience, the usage of TCP vs. UDP in game projects is roughly 50/50, depending on the game type and specific requirements.

TCP provides reliable, ordered delivery through three-way handshakes, acknowledgments (ACKs), retransmission mechanisms, and conservative timeout behavior. It guarantees that data will arrive. UDP, on the other hand, is lighter-weight and can achieve higher throughput but does not guarantee delivery, ordering, or reliability. UDP is commonly used for real-time applications like video streaming and gaming.

One participant raised the question: given modern 4G/5G networks and fast home internet, could TCP simply replace UDP in most game scenarios? The response was that UDP is not about raw speed — it is about handling **weak network conditions**. In poor network environments, TCP's conservative behavior (retransmissions, exponential backoff of timeouts) can actually degrade the player experience further. For an individual player in a weak network situation, TCP can make things worse, not better. This is why some games choose UDP for real-time gameplay, especially in combat scenarios.

### Common Patterns in Real-Time Multiplayer Games

One participant discussed common networking patterns in large-scale real-time multiplayer games:

- Most such games use **long-lived persistent connections**, not HTTP polling.
- Those persistent connections are typically **not** WebSocket — they use custom protocols over raw TCP or UDP.
- For **in-battle operations** (combat, skill usage), games typically use **UDP** because low latency is critical. Dropping a few packets is preferable to waiting for TCP retransmission. Combat operations are extremely time-sensitive.
- For **out-of-battle operations** (menu interactions, lobby management), games often use **TCP**, because a slight delay is acceptable. These operations are not latency-sensitive.

One participant described how packet loss manifests in gameplay: during intense combat moments when many players are active simultaneously, there can be a sudden surge of network data. Some packets may be lost. However, they emphasized that the goal of all network optimization is to minimize this. No game wants players to experience skill loss or rubber-banding. Games invest heavily in network optimization for scenarios like entering/leaving elevators or subways (where connectivity changes).

### Anti-Cheating and External Tools

When asked about cheating and external tools (e.g., AI bots that play competitive games on behalf of human players), one participant explained the server-side approach to anti-cheating:

- The fundamental principle is: **never trust any data sent by the client**. All client-submitted data must be strictly validated on the server.
- There are different categories of cheating. Historically, a common type was **memory modification** (editing game memory on the client). Techniques like client-side obfuscation and code hardening have made this type of cheating less prevalent.
- The server can also detect anomalous behavior patterns — for example, if a client is sending requests at an abnormally high rate, the server can simply reject those requests.

## AI in Game Development and Software Engineering

### AI-Assisted Gameplay and Cheating

One participant asked whether AI could be used to write bots that "solve" competitive games (e.g., strategy or MOBA games) to the point where human players stop playing. The response was that this scenario is very rare in practice. While there are AI systems used in competitive gaming, the idea of widespread AI-generated bots making human play obsolete was dismissed as unlikely.

### AI-Assisted Coding (Web Coding / Cline)

The conversation shifted to how both participants use AI for development. One participant noted that they use AI-assisted programming extensively in their workflow. Common use cases include:

- Debugging and error log analysis — errors are automatically passed through AI tools before being routed to developers.
- General productivity improvements in the development toolchain.

The other participant described a more aggressive approach: they rely on **Web Coding** (also referred to as Cline) for the majority of their coding. Their workflow involves:

- Letting the AI agent run autonomously, executing potentially hundreds of commands in sequence.
- Using Git to track every code change mid-process.
- After the AI finishes, performing a retrospective review: reading through the AI's reasoning steps and the Git history to understand what happened and why.
- If something goes wrong, tracing back through the recorded process to find where the error occurred.

They described this as "letting it run until it breaks, then going back to see what went wrong."

### AI Tool Adoption and Risk Tolerance

One participant noted that at their current company (a large financial institution with relatively small user volumes — tens of thousands), they are comfortable letting AI write code autonomously because the risk is lower. However, if they were working on a system with millions of users and involving financial assets, they would take a different approach: they would first design the overall architecture themselves, then "discuss" the design with the AI tool to converge on an optimal solution, and only then let the AI implement it.

### Bugs and Incident Management

One participant asked whether the other had ever caused bugs that impacted hundreds of thousands or millions of users, and whether the company held it against them. The response was that yes, production bugs happen. Impact is assessed based on scope and duration. Major incidents may be classified as "accidents" and trigger formal processes, but in practice, the personal consequences are usually not severe.

## Data Structures, Optimization, and Low-Level Details

### Role of Bitwise Operations and Memory Optimization

One participant, who had an OI (Olympiad in Informatics) background, asked about the importance of bitwise operations, bit manipulation (XOR, bit sets), and low-level memory layout (how many bits in a byte, string memory footprint) in game development. They wanted to understand whether these techniques from competitive programming were commonly used in production game servers.

The response was that yes, these techniques are used — but they are considered **basic tools**, not special achievements. Bitwise optimization is applied when a function needs to meet a specific performance target under load testing. However, the participant felt the question was somewhat misaligned with the conversation's focus: "I can't quite get the point of your question — these are just optimizations, part of daily work, not something particularly significant."

### Data Structures in Games

One participant emphasized that data structures are extremely important in game development — the shape of objects, their relationships, and how data is structured. The other participant agreed, but noted that game server development is not fundamentally different from other server-side development. The same core tools are used: Redis, message queues, databases. The specific data structures depend on the game's data model.

## Infrastructure and Deployment

### Cluster Deployment vs. Single Machine

One participant asked whether game servers are deployed on single powerful machines (e.g., 32 GB or 64 GB RAM, high-end CPU) or as clusters. The answer was emphatically: **clusters**. They pushed back gently, saying: "I think you might have some bias about game development. If a service has high traffic, it cannot be a single-machine deployment — the same applies in gaming." Different services within the game may have different scaling requirements — some need to scale up (more instances), others do not. This is managed through container orchestration tools like **Kubernetes (K8s)** .

However, one participant admitted they are not personally familiar with Kubernetes cluster management — that domain typically falls to SRE (Site Reliability Engineering) teams in their experience. Their own focus is on CI/CD pipelines and local development workflows, not cluster operations.

### Local Development and Mock Data

When asked about local development workflows — particularly how they handle dependencies on other services (microservice architecture) — one participant described the approach in financial services. In a microservice architecture, a single service (e.g., a mutual fund service) might need to call both an `account-user` service and a `transaction` service. In local development, they would set up local mocks, redirect the URLs to local endpoints, and test with mock data.

The other participant responded that in game development, the approach is different: they simply bring up all required services locally if possible. If that is not feasible (e.g., a dependency is missing), they either mock the data or construct test data manually in the database (which could be MySQL or PostgreSQL). They emphasized that "it depends on the specific business scenario" — if the service needs a user account, they would just register one.

## Databases and Middleware

Both participants agreed on the core infrastructure stack:

- **Redis** is used extensively for sorted sets, leaderboards, message queues, and other common patterns.
- **Kafka** is used in some projects but not all. The decision depends on whether there is a genuine need for a message queue and whether the project's existing tech stack (e.g., Redis already serving as a message queue) makes adding Kafka unnecessary.
- **Databases** include MySQL and PostgreSQL. One participant mentioned they use MySQL primarily, with some PostgreSQL as well.

One participant noted that asking about Redis usage patterns (e.g., "do you use sorted sets?") is essentially meaningless because every backend engineer uses Redis according to business needs — "what you use, I also use — it's all based on the scenario."

## Reflection on the Discussion

### AI and the Changing Industry

One participant reflected on the broader industry shift driven by AI. They noted that since the release of powerful large language models in late 2023, companies have been pushing AI-assisted coding much more aggressively. Before that, employers were not particularly interested in it — now it is a hot topic. They noted that some prominent figures in the AI space have spent over a million dollars annually on tokens, framing the current era as one where "whoever has money to buy tokens and GPUs will occupy a strong position in the AI ecosystem."

### The Nature of the Conversation

Toward the end, one participant reflected that the conversation was quite scattered, jumping between many topics — programming languages, networking protocols, data structures, AI tools, development workflows, and infrastructure. They suggested that future conversations might benefit from a clearer topical focus.

### Contact and Sharing

The meeting concluded with one participant reminding the other that they would clean up the transcription, remove sensitive parts, share it for approval, and then potentially publish it online.

## Action Items

- **Action item:** The meeting recorder will clean the transcript, removing any sensitive content, and share the cleaned version with the other participant for approval before publishing online.
- **Action item (unassigned):** Look into the ECS (Entity-Component-System) architectural pattern, which is used in game development as an alternative to traditional OOP inheritance.
- **Action item (unassigned):** Consider whether future technical discussions would benefit from a more focused topical structure.
