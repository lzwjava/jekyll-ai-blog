---
audio: false
generated: true
lang: en
layout: post
title: Rich Sutton's Bitter Lesson
translated: false
type: note
---

Rich Sutton's "bitter lesson" is a thought-provoking observation about the history of Artificial Intelligence research. In essence, it states that **AI researchers who try to build in human-like knowledge and handcrafted features into their systems eventually hit a wall and are surpassed by approaches that rely more on general-purpose learning algorithms given enough computation.**

The "bitter" part comes from the fact that researchers often have strong intuitions about how intelligence works and what kinds of knowledge or architecture should be beneficial. However, history has repeatedly shown that these intuitions often lead down blind alleys compared to letting algorithms learn directly from data through methods like search and learning.

Here's a breakdown of the key aspects of the bitter lesson:

* **Human Knowledge is Often a Short-Term Crutch:** While incorporating human knowledge can lead to initial progress or better performance on small datasets, it often limits the system's ability to scale and adapt to more complex problems or larger amounts of data. The handcrafted features become brittle and fail to generalize.
* **General-Purpose Methods Triumph with Scale:** Sutton argues that the most significant breakthroughs in AI have come from general-purpose methods like search (e.g., in game playing) and learning (e.g., in machine learning and deep learning). These methods, when given enough data and computational power, can discover their own representations and strategies, often surpassing human-engineered solutions.
* **The Importance of Computation:** A central theme is the increasing availability and importance of computation. As computing power grows, the advantage shifts towards methods that can effectively leverage this power to learn from vast amounts of data.
* **Examples Sutton Often Cites:**
    * **Game Playing (Chess, Go):** Early attempts to build chess-playing programs relied heavily on hand-coded rules and evaluation functions based on expert human knowledge. These were eventually surpassed by systems like Deep Blue (which used massive search) and AlphaGo (which used deep reinforcement learning), which learned their strategies through computation and data.
    * **Speech Recognition:** Early speech recognition systems incorporated a lot of linguistic knowledge and handcrafted features. Modern systems based on deep learning, trained on massive amounts of audio data, have achieved much better performance without explicitly encoding such knowledge.
    * **Computer Vision:** Similar to speech recognition, early computer vision relied on hand-engineered features like edge detectors and texture descriptors. Deep learning models, trained end-to-end on large image datasets, have revolutionized the field.

**Implications for AI Research:**

Sutton's bitter lesson suggests that AI research should focus more on developing scalable, general-purpose learning algorithms and providing them with as much data and computation as possible, rather than trying to hardcode human-like intelligence or rely heavily on handcrafted features. It's a call to trust in the power of learning and the relentless increase in computational resources.

While the bitter lesson doesn't completely dismiss the value of human insight in designing the learning algorithms themselves, it emphasizes that the knowledge about the *problem domain* is often best learned directly from the data rather than being explicitly programmed in.

In summary, the bitter lesson is a reminder that while human intuition can be a starting point, the long-term success of AI often lies in the ability of general-purpose learning methods to discover solutions through computation and data, even if those solutions are not immediately intuitive to humans.
