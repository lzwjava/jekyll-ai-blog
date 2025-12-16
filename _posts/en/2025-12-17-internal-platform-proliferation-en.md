---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Internal Platform Proliferation in Corporations
translated: false
type: note
---

Question: In large corporations and banks, is it common for teams to build internal platforms and tools that essentially wrap existing open-source solutions like Ansible playbooks, Jenkins for building packages, and custom deployment platforms—when much of this could be done directly in Jenkins—primarily to create internal projects for career advancement, resulting in lower-quality tools with small user bases (10k–50k users), small maintenance teams, high long-term costs, and eventual obsolescence?

Answer: 

Yes, this is very normal—and unfortunately quite common—in large corporations, especially in highly regulated industries like banking and finance.

Several factors drive this behavior:

- **Career incentives and politics**: In big organizations, promotions and visibility often depend on "delivering impact" through new projects, leading teams, or owning platforms. Building an internal tool or platform demonstrates leadership and creates a "kingdom" that justifies headcount and budget. Simply improving existing open-source tools or pipelines rarely gets the same recognition.

- **Regulatory and compliance requirements**: Banks face strict audit, security, and compliance rules (e.g., SOX, PCI-DSS, GDPR, or local financial regulations). Off-the-shelf tools like Jenkins or Ansible may not meet all requirements out of the box (e.g., fine-grained access controls, audit trails, approval workflows). So teams build wrappers or platforms to add enterprise features, even if it partially duplicates functionality.

- **Integration with legacy systems**: Large banks often have decades-old mainframes, custom middleware, and proprietary systems. Generic tools struggle to integrate seamlessly, so internal platforms emerge to bridge those gaps.

- **Vendor lock-in avoidance and customization**: Companies prefer not to depend too heavily on one open-source project in case it changes direction or becomes unmaintained. They also want branding, unified UI/UX, and support contracts—hence internal solutions.

- **Not-Invented-Here (NIH) syndrome**: Engineers and architects sometimes believe they can build something better tailored to their needs, underestimating the effort required to match the quality and ecosystem of mature tools like Jenkins, GitHub Actions, or Docker.

The downsides you mentioned are real and well-known:

- Lower initial and long-term quality compared to battle-tested open-source projects.
- High maintenance costs over 10+ years with small teams (often 5–20 people).
- Technical debt accumulation, leading to outdated stacks that are hard to modernize.
- Fragmentation: multiple overlapping internal tools across different departments.

Many organizations eventually recognize this and shift toward "inner sourcing" (treating internal tools like open-source projects), adopting cloud-native platforms (GitHub Actions, GitLab CI, ArgoCD, Harness, etc.), or consolidating onto fewer standardized tools. But the transition is slow because of sunk costs, politics, and risk aversion.

In summary, yes—it's normal, widespread, and often inefficient, but deeply rooted in organizational incentives and constraints typical of large enterprises. Progressive companies try to fight it by rewarding contributions to shared platforms rather than new inventions, but it's an ongoing battle.