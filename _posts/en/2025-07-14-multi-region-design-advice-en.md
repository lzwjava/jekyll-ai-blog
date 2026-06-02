---
audio: false
generated: true
lang: en
layout: post
title: Navigating Feedback on Multi-Region Design
translated: false
type: note
---

Your essay is thoughtful and well-structured, drawing on real-world examples to make a case for better multi-region software design. It highlights common pitfalls (like duplicated efforts in separate apps/backends) and advocates for scalable, shared approaches (e.g., unified codebases with configurations). Overall, it's a solid piece that demonstrates your expertise and forward-thinking mindset—qualities that good managers value in engineers. However, whether sharing it would make your manager or team lead unhappy depends on a few factors, like your team dynamics, company culture, and how you present it. I'll break this down step by step, with advice on mitigating risks.

### Potential Reasons It Could Upset Them

1. **Perceived Criticism of Current Practices**: If your team's current projects follow the "separate apps per region" model (like the bank or fast-food examples you mention), this could read as an indirect critique of decisions they've made or inherited. Phrases like "This is probably wrong to do that" or "after a decade, they will know it is very painful" might feel accusatory, especially if timelines or budgets forced those choices. Managers often defend past trade-offs, even if they're suboptimal long-term.

2. **Timing and Context**: If your team is under pressure with deadlines, compliance issues, or resource constraints, a deep dive into refactoring or redesign might seem like you're prioritizing ideals over immediate delivery. For instance, suggesting AI for fixing "big mistakes" could imply the existing setup is flawed, which might frustrate leads focused on stability rather than innovation right now.

3. **Tone and Length**: The essay is opinionated and lengthy, which is great for a blog post but might overwhelm in a work setting. References to external essays (like Yin Wang's) or big tech examples could come across as "lecturing" if your manager sees it as unrelated to your specific projects. In hierarchical cultures, unsolicited advice can sometimes be interpreted as overstepping, especially if it questions scalability without acknowledging short-term wins.

4. **Company-Specific Sensitivities**: In finance or regulated industries (e.g., banking like Standard Chartered), compliance isn't just about data storage—it's layers of legal, security, and operational hurdles. Dismissing it as "not true" that compliance drives separation might rub experts the wrong way if they've dealt with those realities firsthand.

### Reasons It Might Not Upset Them (or Even Impress)

1. **Shows Initiative and Expertise**: Many managers appreciate engineers who think strategically about architecture, extensibility, and cost savings. Your points on reducing duplicate efforts, using Spring Boot configs, and minimizing branch hell align with modern best practices (e.g., monorepos in big tech). Highlighting AI for refactoring positions you as proactive in a hot area.

2. **Aligns with Business Goals**: Arguments about easier expansion to new regions, lower maintenance costs, and better testing could resonate if your company is international or planning growth. Examples like Apple Pay or Google Cloud demonstrate you've researched this, which shows dedication.

3. **Constructive Mindset**: You end on a positive note—emphasizing getting it right from the start and using resources wisely—which frames it as helpful advice rather than complaint.

### Advice on Sharing It (To Minimize Unhappiness)

- **Frame It Positively and Collaboratively**: Don't send the essay as-is; summarize key points in a shorter memo or Slack/email thread titled something like "Ideas for Improving Multi-Region Scalability in Our Projects." Start with praise for what's working well, then suggest improvements as "opportunities" rather than fixes for "mistakes." For example: "Building on our current setup, here's how we could reduce sync efforts using shared configs..."

- **Tie It to Specific Projects**: Make it relevant by linking to your team's work. Ask questions like, "For our upcoming feature, could we explore region-based modules to avoid branch cherry-picking?" This shows it's not abstract philosophizing.

- **Test the Waters First**: Float a lighter version in a 1:1 meeting or team discussion. Gauge their reaction to one idea (e.g., "What do you think about using YAML configs for region differences instead of separate branches?") before sharing the full essay.

- **Consider Your Relationship**: If your manager is open-minded and encourages input, they're likely to appreciate it. If they're more top-down or stressed, it might land better after a win (e.g., post-release) or as part of a retro/review process.

- **Edit for Diplomacy**: Soften strong statements—change "This is probably wrong" to "While it works initially, I've seen long-term challenges in..." Add qualifiers like "In my experience" to make it personal rather than absolute.

In summary, it's unlikely to make them outright unhappy if presented thoughtfully, as it positions you as a valuable contributor. But if your team is already doing things the "painful" way, it could spark defensiveness unless you emphasize collaboration. If you're unsure, start small and build from there. This kind of insight can lead to promotions if handled well!
