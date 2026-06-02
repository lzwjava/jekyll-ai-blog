---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Frege on Functions and Unsaturation
translated: false
type: note
---

### What Does Frege's 1904 Essay "What is a Function?" Say?

Gottlob Frege's short essay, originally titled *Was ist eine Funktion?* and published in a Festschrift for physicist Ludwig Boltzmann, is a concise clarification of the logical nature of functions in mathematics. Written late in Frege's career (after his major works like *Grundlagen der Arithmetik* and *Grundgesetze der Arithmetik*), it responds to ongoing confusions in mathematical practice and pedagogy—much like the issues you described with students mixing up graphical equations (y = x² + 3x) and functional notation (f(x) = x² + 3x). Frege doesn't rewrite math textbooks here, but he dissects why these notations mislead and offers a precise logical foundation for what functions *really* are. The paper is only about 8 pages in German, and its English translation (by Peter Geach) appears in collections like *Collected Papers on Mathematics, Logic, and Philosophy*.

#### Key Arguments and Structure
Frege starts by acknowledging the intuitive success of function notation in math (e.g., sin x, log x, or x²) but argues that sloppy usage hides deeper logical problems. He builds on his earlier ideas from "Function and Concept" (1891), where he first treated functions as building blocks of logic, not just arithmetic tools. The essay has three main threads:

1. **The Unsaturated Nature of Functions**:
   - Frege insists that a function isn't a complete "thing" like a number or object—it's *unsaturated* (or "incomplete"). Think of it as a gap waiting to be filled: the expression ξ² + 3ξ (using ξ as a placeholder) denotes the function itself, but it can't stand alone as a meaningful entity. Only when you insert an argument (e.g., replace ξ with 2) does it "saturate" and yield a value (like 2² + 3·2 = 10).
   - This contrasts with everyday math teaching, where y = x² + 3x is presented as "the function" equated to y (a complete value). Frege says this blurs lines: the left side (y) is saturated (an object), but the right side is unsaturated until x is specified. The notation tricks us into treating the function like a static formula, ignoring its dynamic, logical role.

2. **Critique of Traditional Mathematical Usage**:
   - Frege targets the historical shift you mentioned—from graphical y = f(x) to abstract f(x)—as symptomatic of deeper errors. Early math (e.g., Euler's era) saw functions as curves or rules, but by Frege's time, Dirichlet's definition (a function as an arbitrary correspondence between domain and range) had taken hold. Frege agrees with the extensional idea (functions defined by input-output behavior) but faults how variables are mishandled.
   - Variables aren't "variable quantities" (a common pedagogical myth); they're placeholders in expressions. Removing a variable from 2x³ + x to "get the function" (like 2( )³ + ( )) fails for multi-argument cases, where slots might need the *same* argument (as in x³ + x) or *different* ones (x³ + y). This leads to confusion in binding variables and representing complex functions.
   - He also nods to the "concept horse" paradox (from his 1892 essay): just as you can't form a proper name like "the concept horse" (treating a predicative concept as an object), you can't directly name functions as complete entities. Trying to do so collapses logical structure.

3. **Implications for Logic and Math**:
   - Functions are primitive in Frege's logicism (reducing math to logic): they're the glue for building propositions, concepts (special first-level functions returning truth-values), and even numbers (as value-courses of functions). This ties into his broader philosophy—functions enable precise inference without ambiguity.
   - Frege ends optimistically: clear function analysis will refine math, avoiding paradoxes (foreshadowing Russell's 1902 letter on his own paradox, which derailed *Grundgesetze* Vol. 2 around this time).

The essay isn't a polemic; it's diagnostic, like a philosopher-logician debugging math's language. It influenced analytic philosophy (e.g., Wittgenstein, Russell) and modern type theory in logic/computing, where functions are indeed "unsaturated" operations.

#### What Is a Function, According to Frege?
In Frege's view, a function is **an unsaturated logical entity (or expression) that maps arguments to values by completing its incomplete structure**. Formally:
- It's not the equation (y = f(x)), the graph, or even the set of outputs—those are derivative.
- It's the "gap" in an expression, like f(ξ) = ξ² + 3ξ, where ξ signals incompleteness.
- Properties: Extensional (same inputs → same outputs define identity); hierarchical (first-level functions take objects as arguments, return objects; second-level take functions); and predicative (concepts/relations as special cases).
- Example: For f(x) = x² + 3x, the function is the rule/expression with a hole; f(2) = 10 is the saturated value.

This resolves your students' confusion: The "function" isn't the whole y = x² + 3x (which mixes complete and incomplete parts) or just f(x) = x² + 3x (which still has a variable-gap). It's the pure, unsaturated mapping mechanism underneath. Teaching it this way—from logic, not just algebra—avoids the interference you noted.

If you'd like, I can suggest ways to explain this in a beginner class or dive into related Frege essays.

**References**
- [Russell and Frege on the Logic of Functions (PDF summary/discussion)](https://newprairiepress.org/cgi/viewcontent.cgi?article=1023&context=biyclc)
- [The Philosophy of Gottlob Frege (excerpt on functions)](https://assets.cambridge.org/052183/6697/excerpt/0521836697_excerpt.htm)
- [Stanford Encyclopedia of Philosophy: Gottlob Frege](https://plato.stanford.edu/entries/frege/)
- [Collected Papers on Mathematics, Logic, and Philosophy (contains English translation)](https://www.oxfordbibliographies.com/display/document/obo-9780195396577/obo-9780195396577-0065.xml)
