---
audio: false
generated: true
image: false
lang: en
layout: post
title: Overcoming Censorship and Myopia
translated: false
type: note
---

### Lessons Learned from This Experience

This personal journey highlights the ongoing struggle against internet censorship in China, drawing parallels to personal health challenges like reversing myopia. It's a story of adaptation, trial-and-error, and optimization over 15+ years. Here are key takeaways that can be applied more broadly, whether to tech problem-solving, personal development, or overcoming systemic barriers:

1. **Persistence and Adaptation Are Key to Long-Term Challenges**: The author evolved from basic tools like Goagent (2010–2013) to sophisticated setups like automated Python scripts for proxy selection (2025). This shows that solutions to entrenched problems (e.g., censorship or health issues) require continuous iteration. Lesson: Don't stick with outdated methods; experiment with new technologies and providers (e.g., switching from Digital Ocean to Aliyun or zhs.cloud) as barriers evolve.

2. **Measurement Drives Improvement**: The author regrets not using tools like Speedtest earlier to quantify proxy performance (e.g., discovering 5G networks often exceed 100 Mbps). Similarly, for myopia, they emphasize using eye charts. Lesson: Without metrics, progress is guesswork. In any field—tech, health, or business—regular testing (e.g., speed tests, benchmarks, or health trackers) helps identify inefficiencies and validate changes. "No measuring, no improvement" is a core principle here.

3. **Deep Understanding Reduces Frustration**: Early regrets stem from shallow thinking, like simply replacing banned IPs without investigating causes (e.g., checking cellular vs. broadband blocks, or 4G vs. 5G). Now, they have recovery methods that take just 1 minute. Lesson: Invest time in root-cause analysis. For censorship, this means learning how systems like the GFW detect proxies; for personal goals, it means nuanced checks (e.g., eye strain differences). This prevents repeated failures and builds expertise.

4. **Resource Efficiency Matters**: The author optimized costs and data (e.g., 150–200 CNY/month for 20–35GB via Macao SIM) while achieving high speeds (80 Mbps down, 50 Mbps up). They also automated processes to prioritize servers (Singapore over Hong Kong for AI tools). Lesson: Balance effectiveness with sustainability. In tech, this could mean scripting automation; in life, it's about scalable habits that don't drain resources.

5. **Regrets Highlight the Value of Early Education and Foresight**: Wasting time on unreliable protocols or not learning from providers like zhs.cloud sooner is a common theme. The author notes it's "still early" for broader awareness, comparing it to myopia reversal methods shared by Todd Becker in 2014, which remain niche despite millions of views. Lesson: Seek knowledge proactively—read docs, follow experts (e.g., the Qujing author on Twitter), and avoid reinventing the wheel. Fundamental issues like censorship or health myths persist because awareness spreads slowly.

6. **Analogies Between Technical and Personal Challenges**: Both GFW bypassing and myopia reversal involve "hacking" a system—understanding principles (e.g., how GFW blocks IPs or eye muscles adapt) leads to straightforward solutions. But one is measurable quickly (proxy speeds), while the other takes months/years (eyeball changes). Lesson: Apply problem-solving frameworks across domains. If a solution "works well" (e.g., stable proxies or reduced-prescription glasses), refine it iteratively, but be patient with delayed-feedback problems.

Overall, this experience teaches resilience in the face of authoritarian controls or biological limitations. It underscores that freedom—digital or physical—often requires DIY ingenuity, but sharing stories (like this post) accelerates collective learning.

### Are All Points Reasonable?

Most points in the post are reasonable based on the author's personal context and common experiences with internet censorship in China. They reflect practical, evolving strategies that align with how many users bypass the GFW. However, some claims warrant nuance or caveats for accuracy, potential risks, or scientific backing. I'll evaluate key sections:

- **Journey Timeline and Tools**: Highly reasonable. Tools like Goagent, Shadowsocks, Outline Manager, and providers like Digital Ocean or Aliyun are standard for GFW bypassing. The Macao SIM card method (150 CNY/month for 20GB) is a known workaround, as Macao's telecoms (e.g., CTM) often route traffic outside mainland China's censorship when roaming. Users report it provides uncensored access in border areas or with specific plans, though it's not foolproof—it can be throttled, detected, or costly with add-ons (e.g., extra 5GB for 20 MOP). The automated Python script for proxy selection (prioritizing Singapore for AI) is a smart, modern optimization, and maintaining consistent rules across devices (e.g., Shadowrocket, Clash) is best practice.

- **Differences and Similarities to Myopia Reversal**: The analogies are thoughtful but mixed in reasonableness. Differences (GFW as "human-made" vs. eye biology; quick proxy metrics vs. slow myopia changes) are valid—censorship is adversarial and testable, while vision adaptation is physiological and subjective. Similarities (both needing understanding of underlying principles for "straightforward" solutions) hold metaphorically, emphasizing problem-solving. However, myopia reversal via reduced-prescription glasses (e.g., 200 degrees less) is controversial. Mainstream ophthalmology views myopia as largely irreversible in adults (due to elongated eyeballs), with methods like those from Todd Becker (inspired by hormesis and "print pushing") lacking strong clinical evidence. Becker's 2014 talks promote it anecdotally, but studies show it may slow progression in kids, not reverse it reliably. If it "works well" for the author, that's personal success, but it's not universally reasonable without medical consultation—risks include eye strain or accidents from under-correction.

- **Reasoning and Nuance**: Reasonable emphasis on investigation (e.g., checking network types for blocks, or eye differences for myopia). It shows maturity from experience. The GFW's mechanics (IP blocking, protocol detection) are accurately portrayed—deeper analysis (e.g., via logs or tests) is indeed key, not just IP swaps.

- **Current Status and Recovery**: Practical and reasonable. High speeds (80/50 Mbps) on Hong Kong servers are achievable with optimized setups. Quick recovery (changing elastic IPs in 1 minute) via scripts is efficient for cloud users. Using non-HK servers for AI tools makes sense, as some services (e.g., ChatGPT) block or throttle certain regions.

- **Regrets**: Valid self-reflection. Experimenting with detectable protocols wastes time, and not learning provider "secrets" (e.g., zhs.cloud's obfuscation techniques) earlier is a common pitfall. Deeper thinking beyond "new IP fixes everything" is spot-on—GFW uses DPI (deep packet inspection), so protocols matter. Router setups (e.g., OpenWrt) do require stable upstream proxies.

- **Metrics**: Excellent point, fully reasonable. Speedtest is essential for networking; analogous to eye charts for vision. The observation about 5G (>100 Mbps) vs. broadband (<100 Mbps) aligns with real-world data in China, where mobile networks often outperform fixed lines in urban areas.

- **It Is Still Early**: Optimistic but reasonable in context. Predicting GFW's fall is speculative—it's strengthened over years, but global pressures (e.g., trade, tech) could change it. The myopia comparison highlights slow adoption of ideas; Becker's videos have ~1M+ views cumulatively, but awareness is niche (likely <10,000 active practitioners worldwide, based on community sizes). "It's still early" encourages patience for foundational changes.

In summary, ~90% of the points are reasonable as experiential advice, especially for tech-savvy users in censored environments. The myopia parallels add inspirational value but should be taken with skepticism—consult professionals for health claims. Risks like legal issues with VPNs in China (technically illegal without approval) aren't mentioned, so users should proceed cautiously.

References:

- [Using Macau SIM cards for uncensored internet in China](https://www.reddit.com/r/China/comments/10zq0z8/macau_sim_card_for_uncensored_internet/)
- [Todd Becker on Reversing Myopia](https://gettingstronger.org/2014/05/reverse-myopia/)
- [zhs.cloud (VPN Provider Summary)](https://zhs.cloud) – A Chinese-language site offering cloud-based VPN/proxy services with servers in Hong Kong, Singapore, etc., focused on bypassing censorship.
