---
audio: false
generated: true
lang: en
layout: post
title: 'Meta''s Smart Glasses: Features and APIs'
translated: false
type: note
---

Let's break down Meta's smart glasses offerings, including Ray-Ban and Oakley, their user base, and what their APIs offer to developers.

**What are Meta VR Glass, Ray-Ban, and Oakley smart glasses?**

It's important to clarify the terminology here. "Meta VR Glass" isn't a specific product name that Meta widely uses. Instead, Meta's primary VR/MR offering is the **Meta Quest** line of headsets (e.g., Meta Quest 3).

When people refer to "Meta glasses" in a more general, glasses-like form factor, they're typically talking about:

* **Ray-Ban Meta Smart Glasses:** These are consumer-focused smart glasses developed in partnership with EssilorLuxottica (the company behind Ray-Ban). They are designed to look like conventional Ray-Ban sunglasses and focus on features like:
    * Hands-free photo and video capture (with a visible LED indicator for privacy).
    * Open-ear speakers for audio (music, podcasts, calls).
    * Integrated microphones for calls and voice commands (including "Hey Meta" for Meta AI).
    * Livestreaming capabilities to Facebook and Instagram.
    * Integration with Meta AI for various tasks (e.g., getting information, sending messages, describing surroundings for accessibility).
    * No integrated display or AR head-mounted display (they are "smart glasses," not AR glasses in the typical sense).

* **Oakley Meta Glasses (e.g., Oakley Meta HSTN):** This is a newer line of "Performance AI Glasses" developed in collaboration with Oakley, also part of EssilorLuxottica. They share many of the features of the Ray-Ban Meta glasses but are specifically designed with athletes and performance in mind. Key aspects include:
    * Bold, sporty aesthetics typical of Oakley.
    * Enhanced durability and water resistance (IPX4).
    * Longer battery life.
    * Higher resolution camera (3K video).
    * Integration with Meta AI, offering features tailored for athletes (e.g., asking about wind conditions for golf).

**How many users?**

As of February 2025, the **Ray-Ban Meta Smart Glasses** have sold over **2 million units** since their launch in September 2023. EssilorLuxottica plans to increase annual production capacity to 10 million units by the end of 2026, indicating strong demand and Meta's belief in the product's future.

The **Oakley Meta Glasses** are a newer product line, with pre-orders starting in July 2025. Therefore, specific user numbers for Oakley Meta glasses are not yet available, but they are aiming for a significant market presence.

**What does its API provide to developers?**

It's important to distinguish between APIs for VR/MR headsets (like Meta Quest) and smart glasses (like Ray-Ban Meta and Oakley Meta).

**For Meta Quest (VR/MR headsets):**

Meta provides a robust developer platform for its Meta Horizon OS (formerly Quest OS), offering various APIs and SDKs for creating immersive VR and mixed reality experiences. Key areas for developers include:

* **OpenXR:** A standard for creating high-performance XR experiences, allowing developers to build cross-platform VR/MR apps.
* **Meta Horizon Worlds:** Tools for creating and shaping experiences within Meta's social VR platform.
* **Android Apps:** Developers can make existing Android apps compatible with Meta Horizon OS and leverage its unique spatial features.
* **Web Development:** Design and deploy 2D web apps that utilize Quest's multitasking capabilities.
* **Meta Spatial SDK:** Designed for mixed reality, enabling developers to transform 2D apps with innovative spatial elements.
* **Passthrough Camera API:** Allows developers to seamlessly blend virtual and real worlds, creating mixed reality applications.
* **Interaction APIs:** For hand tracking, controller input, locomotion, and more.
* **Voice Command & Text-to-Speech (TTS) APIs:** To integrate voice control and spoken output into applications.
* **Scene Understanding APIs:** To access and utilize data about the user's physical environment (e.g., scene mesh, anchors).
* **Social Features APIs:** For leaderboards, challenges, user notifications, etc.

**For Ray-Ban Meta and Oakley Meta Smart Glasses:**

Currently, there isn't a publicly released, comprehensive, official SDK or API specifically for third-party developers to build custom applications that run *directly on* the Ray-Ban Meta or Oakley Meta smart glasses.

However, developers have been creative in finding ways to interact with these devices:

* **Meta AI Integration:** The primary way developers can interact with these glasses is through their integration with **Meta AI**. This means developers can potentially leverage Meta AI's capabilities for various tasks by using existing APIs for large language models (LLMs) and other AI services. For example, some community-driven projects have demonstrated "hacky" integrations using Messenger as a bridge to send commands or receive data from the glasses, then processing that data with services like ChatGPT or Google Gemini via their respective APIs. This relies on the glasses' built-in ability to interact with Meta AI and send/receive messages.
* **Content Sharing:** The glasses primarily function as a capture and sharing device. Developers can interact with the **Meta View app** (the companion app for the glasses) by providing ways to share content captured on the glasses to their platforms, similar to how content is shared to Instagram, Facebook, WhatsApp, etc.
* **Accessibility Features:** The built-in Meta AI provides accessibility features like describing surroundings or reading text aloud. While not a direct API for developers to build new apps *on* the glasses, it highlights the potential for AI-driven assistance that could eventually be exposed through more open development tools.

While Meta has stated its long-term vision for more open development on future smart glasses (potentially with heads-up displays, like the rumored "Orion" project), for the current Ray-Ban Meta and Oakley Meta smart glasses, developer access is primarily indirect, leveraging their integration with Meta AI and content sharing functionalities. The community is actively exploring workarounds and unofficial integrations in the absence of a dedicated public SDK for on-device app development.
