---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Jeff Dean and Noam Shazeer AI Discussion
translated: false
type: note
---

Question: What does Noam Shazeer say in the YouTube video at https://www.youtube.com/watch?v=v0gjI__RyCY&t=4s?

Answer:

The video is a 2+ hour podcast interview titled "Jeff Dean & Noam Shazeer — 25 years at Google: from PageRank to AGI," hosted by Dwarkesh Patel (uploaded February 2025). It features Google's Chief Scientist Jeff Dean and Noam Shazeer (co-inventor of the Transformer architecture, Mixture of Experts, and other key AI technologies) discussing their careers at Google, the evolution of AI systems, hardware trends, scaling laws, future of large language models, and paths toward artificial general intelligence (AGI).

Noam Shazeer speaks extensively throughout the conversation, alternating with Jeff Dean and responding to the host's questions. His contributions include personal anecdotes, technical insights, and forward-looking ideas on AI development.

Key topics and selected quotes from Noam Shazeer:

- **Joining Google and early AI interests**: He describes seeing Google at a 1999 job fair, applying because of its exponential growth in search queries, and initially planning to work there briefly to fund independent AI research. "I figured it was my favorite search engine... it looked like a bunch of smart people doing good stuff. They had this really nice crayon chart... daily number of search queries... looked very exponential."

- **Hardware and Moore's Law**: He notes the shift from general CPUs to specialized accelerators like TPUs. "More recently, the general-purpose CPU-based machine scaling has not been as good... But we're seeing much more specialized computational devices, like machine learning accelerators, TPUs... making it so that we can actually get really high performance."

- **Mixture of Experts (MoE) and modularity**: As the inventor of modern MoE techniques, he advocates for sparse models where different experts handle different tasks, enabling continual learning and better interpretability. "I've been a big fan of models that are sparse... different parts of the model to be good at different things... I think we should probably have a more organic structure."

- **Distillation and model efficiency**: "Distillation is a really useful tool... you can transform a model into a different form... at the module level... continual process where each module has a few different representations."

- **Inference scaling and longer context**: He discusses improving models at inference time and attending to massive contexts. "You want the system to be actively exploring a bunch of different potential solutions... having a dial where you can make the model give you better answers with more inference time compute." Also: "It would be really nice if the model could attend to trillions of tokens... Could it attend to the entire internet... all your personal information... with my permission."

- **Interpretability**: "Actually, in the past, I found experts to be relatively easy to understand... this expert was getting words referring to cylindrical objects. This one's super good at dates."

- **Sample efficiency and training objectives**: Comparing to human learning: "A person has seen a billion tokens... and they're pretty good at a lot of stuff." He suggests changing objectives beyond next-token prediction.

The video starts near the beginning (t=4s is essentially the intro), where the host introduces the guests, and Noam soon says: "Thank you. Super excited to be here."

For the full detailed transcript of everything Noam Shazeer says, refer to the official transcript linked in the video description.

References:

- [YouTube Video](https://www.youtube.com/watch?v=v0gjI__RyCY)
- [Full Transcript](https://www.dwarkeshpatel.com/p/jeff-dean-and-noam-shazeer)
