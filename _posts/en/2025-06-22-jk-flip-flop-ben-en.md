---
audio: false
generated: true
lang: en
layout: post
title: SR Latch and Flip-Flop Modifications by Ben Eater
translated: false
type: note
---

Below is a coherent and organized version of the provided text, preserving the original content as much as possible while improving clarity, structure, and flow. The text has been edited for grammatical accuracy, logical progression, and readability without altering the technical details or core explanations.

---

In a previous video, I discussed the SR Latch, and I encourage you to review that video if you're unfamiliar with it. To summarize, the SR Latch has two inputs: **R** (Reset) and **S** (Set). When the Reset input goes high, the output **Q** goes low (off), resetting the latch. When the Set input goes high, the output **Q** goes high (on), setting the latch. There’s also a complementary output, **Q̅** (Q-bar), which is always the opposite of **Q**, except in one case: when both **R** and **S** inputs are high simultaneously. In this scenario, both **Q** and **Q̅** go low, which is considered an invalid state, as you shouldn’t set and reset the latch at the same time. If both inputs are released, the latch’s state becomes unpredictable, as it depends on which input is released first. Generally, the SR Latch will remain latched in one of its two stable states.

In this video, I’ll discuss modifications to the basic SR Latch circuit. The first modification is the **SR Latch with Enable**. This version adds **AND gates** to both the **R** and **S** inputs, controlled by an **Enable** signal. When the Enable signal is high (1), the AND gates pass the **R** and **S** inputs through unchanged. For example, if **Enable** is 1 and **Reset** is 1, the AND gate outputs a 1; if **Reset** is 0, it outputs a 0. However, if the **Enable** signal is low (0), the AND gate outputs are always 0, regardless of the **R** and **S** inputs. This causes the latch to remain in its last state, effectively ignoring the inputs. Thus, the Enable signal allows you to either enable the latch to respond to its **R** and **S** inputs or disable it to hold its current state.

Next, we can extend this concept to create an **SR Flip-Flop**. The key difference between a latch and a flip-flop is that a latch’s outputs change whenever its inputs change, while a flip-flop’s outputs only change on a specific trigger, typically a clock pulse. In an SR Flip-Flop, a **Clock** input (indicated by a triangle symbol in diagrams) controls when the outputs update. Specifically, the outputs **Q** and **Q̅** change only when the clock transitions from low to high (a rising edge). At all other times, the inputs **R** and **S** are ignored, and the flip-flop retains its previous state.

The SR Flip-Flop achieves this using a capacitor in the clock circuit. When the clock transitions from low to high, a brief current flows through the capacitor as it charges, creating a short voltage pulse at the inputs of the AND gates. This pulse effectively enables the SR Latch with Enable for just that moment, allowing the **R** and **S** inputs to affect the outputs **Q** and **Q̅**. Once the capacitor is fully charged, the pulse stops, and the flip-flop ignores further input changes until the next rising edge.

Here’s how the SR Flip-Flop behaves during a clock rising edge:

- If **R** is high and **S** is low, **Q** goes low (reset), and **Q̅** goes high.
- If **S** is high and **R** is low, **Q** goes high (set), and **Q̅** goes low.
- If both **R** and **S** are low, the flip-flop remains in its previous state.
- If both **R** and **S** are high (the invalid state from the SR Latch), the behavior is unpredictable. Similar to the SR Latch, both **Q** and **Q̅** may go low during the pulse, but when the inputs are released, the flip-flop settles into one state or the other based on which input drops first. This makes the output uncertain, as it depends on timing differences (e.g., a few nanoseconds), rendering this an invalid and unpredictable state.

To address this unpredictability, we can use a **JK Flip-Flop**, which is similar to the SR Flip-Flop but includes feedback from the outputs **Q** and **Q̅** to the inputs. The JK Flip-Flop uses three-input AND gates that incorporate **J** (analogous to **S**), **K** (analogous to **R**), and the feedback signals **Q** and **Q̅**. The letters **J** and **K** are arbitrary and don’t stand for specific terms, but they distinguish this circuit from the SR Flip-Flop.

The JK Flip-Flop operates as follows:

- If **J** and **K** are both 0, the AND gate outputs are 0, so the flip-flop remains in its previous state, even during a clock pulse.
- If the latch is currently set (**Q** = 1, **Q̅** = 0) and you want to reset it (**K** = 1, **J** = 0), the AND gate connected to **K** outputs a 1 during the clock pulse (since **Q** = 1), resetting the flip-flop (**Q** = 0, **Q̅** = 1).
- If the latch is already reset (**Q** = 0, **Q̅** = 1) and **K** = 1, **J** = 0, the AND gate outputs remain 0, so the flip-flop stays reset, which is the desired behavior.
- Similarly, if the latch is reset (**Q** = 0, **Q̅** = 1) and you want to set it (**J** = 1, **K** = 0), the AND gate connected to **J** outputs a 1 during the clock pulse (since **Q̅** = 1), setting the flip-flop (**Q** = 1, **Q̅** = 0).
- If the latch is already set and **J** = 1, **K** = 0, it stays set, as expected.

The JK Flip-Flop’s unique feature arises when both **J** and **K** are 1. Because of the feedback, only one AND gate can be active at a time (since **Q** and **Q̅** cannot both be 1). If **Q** is 1, the AND gate for **K** is active, and the flip-flop resets on the next clock pulse (**Q** = 0, **Q̅** = 1). If **Q** is 0, the AND gate for **J** is active, and the flip-flop sets on the next clock pulse (**Q** = 1, **Q̅** = 0). This creates a **toggle** behavior: if **J** = **K** = 1, the flip-flop switches its state on each clock pulse (**Q** flips from 0 to 1 or 1 to 0). This predictable toggling eliminates the invalid, unpredictable state of the SR Flip-Flop, making the JK Flip-Flop more robust and versatile.

---

This version organizes the content into clear sections, corrects grammatical errors, and ensures technical accuracy while maintaining the original explanations and terminology. Let me know if you need further refinements or additional details!
