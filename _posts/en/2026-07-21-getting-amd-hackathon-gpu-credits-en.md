---
audio: false
generated: true
image: false
lang: en
layout: post
title: Getting AMD Hackathon GPU Credits
translated: false
type: note
---

Question: When joining the AMD hackathon, do we need to ask AMD employees for Radeon Cloud credits?

Answer:

Yes, **most likely you need to get credits before using the Radeon Cloud GPU**, but it may not necessarily require directly asking an AMD employee. There are usually several paths:

1. **Hackathon-provided credits**

   For AMD-sponsored hackathons, organizers often provide participants with cloud access codes/credits. The best action is:

   * join the Luma event

   * join the event Discord/Slack (if provided)

   * ask the AMD organizer or mentor:

   > "Is there a GPU credit code or AMD Radeon Cloud access available for hackathon participants?"

   This is the normal way.

2. **AMD Developer Program credits**

   AMD also has an official developer program that provides cloud credits. Their current flow is:

   * join AMD AI Developer Program
   * request cloud credits
   * wait for approval

   AMD says developers can request credits through the developer portal, with approval based on use case. ([AMD][1])

3. **Radeon Cloud account credits**

   The Radeon Cloud page indicates login via GitHub or ModelScope and launching GPU notebooks after claiming credits. ([Radeon Cloud][2])

The "10 credits/hour" shown means:

```
GPU usage:
1 hour = 1 credit

Example:
100 credits = 10 hours GPU runtime
```

The important thing is **do not start a GPU instance before confirming the credit source**, because cloud GPUs usually consume credits while running.

For the hackathon, I would ask early:

```
Hi AMD team,

I joined the AMD hackathon and would like to use Radeon Cloud
for my project. Are there free GPU credits available for participants?
If yes, could you share the process/code to claim them?

Thanks!
```

Also check whether the hackathon has a prize or participant benefit section. Some AMD events explicitly provide cloud credits or GPU access. ([AMD][3])

References:

* AMD AI Developer Program Cloud Credits ([AMD][1])
* AMD Developer Portal Member Perks ([AMD Developer Portal][4])
* Radeon Cloud login/credit portal ([Radeon Cloud][2])

[1]: https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-claim-amd-cloud-credits.html?utm_source=chatgpt.com "How to Claim AMD Cloud Credits"
[2]: https://radeon-global.anruicloud.com/profile?utm_source=chatgpt.com "Profile - Radeon Cloud"
[3]: https://www.amd.com/en/developer/resources/technical-articles/2026/build-across-the-ai-stack--join-the-amd-x-lablab-ai-hackathon-.html?utm_source=chatgpt.com "Build Across the AI Stack: Join the AMD x LabLab.ai Hackathon"
[4]: https://developer.amd.com/member-perks/?utm_source=chatgpt.com "Member Perks - AMD Developer Portal"
