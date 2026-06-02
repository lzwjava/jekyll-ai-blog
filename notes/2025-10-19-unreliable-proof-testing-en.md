---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Science's Unreliable Proof by Testing
translated: false
type: note
---

### Why People Blindly Trust Scientific Experiments: A Programmer's Analogy

Many people fail to grasp the logical flaws inherent in scientific experiments, leading them to accept "proven" science at face value. They don't understand why a theory that's been "confirmed" through experiments can still turn out to be wrong. But if you understand the principles of software testing, you'll see the true nature of scientific experiments—like the issues I discussed in my article *The Logic of Testing*.

In short, a scientific theory is like a piece of code, and scientific experiments are like tests designed to "verify" that the code works correctly. Imagine writing a program to calculate multiplication, but you accidentally implement it as addition: `(x, y) => x + y`. If you test it with inputs (2, 2) and get 4, you might think, "Great, it's multiplying correctly!" But you'd be dead wrong. To truly confirm it's a multiplication function, you'd need to test *every possible input* and ensure it produces the right output every time. Since we can't test infinite inputs, no amount of tests can *guarantee* the program is correct. Even if thousands pass, it could still fail spectacularly on an untested case.

Science works the same way. A theory is only truly "proven" if it holds up under *all conceivable conditions*—every possible "input" from the universe. A common pitfall is running just one experiment in a narrow setup and declaring the theory validated. That's like patting yourself on the back after the (2, 2) test and calling it done. Sometimes, you run thousands of tests, and everything checks out—until a novel input comes along, and boom, the theory crumbles.

This is the essence of science's "falsifiability." Some folks tout falsifiability as the hallmark of true science, dismissing anything unfalsifiable as pseudoscience. But using the programming analogy, we can see that's not quite right. Falsifiability highlights the *limitations* of experiments—they can disprove a theory but never fully prove it. It shouldn't be the rigid *definition* of what counts as science.

The more constraints and complexity you add to your tests (or experiments), the harder it becomes to confidently claim your program (or theory) is correct. In programming, intricate test setups with tons of edge cases make validation tougher and less convincing. Science is no different: The more controlled conditions, fancy equipment, and isolated variables an experiment involves, the weaker its "persuasiveness" for proving a broad theory. It might work in that petri dish, but does it scale to the messy real world?

That's why I can't buy into Einstein's theory of relativity. The experiments used to test it are few and far between, confined to ultra-specialized conditions without much universality. Classic validation experiments for relativity only happen once a century or so, making independent replication nearly impossible for most researchers. To this day, there's no practical application that *requires* relativity— the oft-cited example of GPS satellites doesn't actually need it; basic Newtonian physics suffices with minor tweaks. Even the core premise, "the speed of light is constant regardless of the source's motion," rests on a single experiment in a contrived setup with hyper-complex gear, elevated to eternal truth without broader scrutiny.

A lot of medical theories follow the same pattern: One study gets hailed as gospel, cited endlessly, but rarely double-checked independently. Later generations just parrot it, assuming it's rock-solid.

This analogy isn't about dismissing science outright—it's a call to stay humble about what "proof" really means. Experiments are powerful tools, but they're spotlights, not floodlights. They illuminate patches of truth, but shadows lurk everywhere. If we treated theories like code under constant review—open to endless testing and refactoring—science would be even stronger.
