---
audio: false
generated: true
image: false
lang: en
layout: post
title: OOP Critique by Yin Wang
translated: false
type: note
---

Question: What does the blog post at https://yinwang0.wordpress.com/2013/12/24/oop/ say?

Answer:

This is a critical essay by **Yin Wang**, a programming language researcher, titled **"On Object-Oriented Programming"** (written in late 2013). It is a comprehensive critique of OOP as a paradigm. Here is a breakdown of the key arguments:

---

## 1. OOP Is Treated as a Religion

The author opens by calling OOP a "religion" — claiming it promised to save the world from the "software crisis," but instead brought more confusion and harm than benefit. He argues its dogmas have become deeply entrenched despite being fundamentally flawed.

---

## 2. "Everything Is an Object" Is a False Dogma

The OOP definition of an object is "a combination of data fields and associated procedures known as methods." The author argues that not everything can fit this model. For example, concepts like velocity, time, or change don't naturally contain methods — that would be like saying "the bullets contain the gun."

He also points out the operator problem: in `1 + 2`, does `+` belong to `1` or `2`? The arbitrary choice reveals that operations are inherently *outside* objects, not inside them.

He compares "everything is an object" to similar failed dogmas: "everything is a function" (lambda calculus / Church numerals) and "everything is a set" (set theory) — both intellectually interesting, but impractical when taken to extremes.

---

## 3. Functions Are Not Objects

The original motivation for putting functions inside objects was narrowly practical — GUI button callbacks. But this limited use case cannot justify a universal "everything is an object" principle.

He argues that most methods are just functions that *happen* to take an object as an argument. They use the object as a namespace, not as their logical owner. Languages like Scala or Python wrap functions into objects with an `apply` or `__call__` method, but this is just wrapping — it doesn't make functions objects in any meaningful sense.

---

## 4. Excessive Abstraction Is Harmful

OOP encourages a level of abstraction that makes programs hard to understand and analyze. He describes Java programs with multiple levels of inheritance, overloading, and design patterns that do very little actual work, comparing navigating such code to going through a maze.

He also critiques Smalltalk's "extremely late binding" — where even `if` and `+` can be redefined — arguing that this makes it impossible to know what any piece of code actually means, and makes compiler optimization and static analysis very difficult.

---

## 5. Design Patterns Are a Symptom of OOP's Weakness

The author argues that design patterns emerged mostly due to the dogma of "everything is an object" and the lack of proper higher-order functions in OO languages. He references Peter Norvig's 1998 talk showing that almost all design patterns become "transparent" once you have first-class functions.

He describes design patterns as a workaround for problems that wouldn't exist in a well-designed language. He compares their marketing to weight-loss products — promising easy solutions without understanding fundamentals — and argues they "eat programmers' brains," causing them to think in over-complicated ways.

---

## 6. "OO Language" Is a Meaningless Marketing Term

There is no clear definition of what makes a language "object-oriented." OOP borrowed (or "stole") most of its ideas from procedural programming, renamed the terminologies, and marketed them as original. The "OO" label was historically used mainly for marketing advantages.

---

## 7. Harm to Education and Industry

Many universities replaced introductory languages like Pascal (procedural) or Scheme (functional) with Java, causing students to miss the most essential programming concepts. The author, having been a TA for Java introductory courses at Cornell and Indiana, observed that students were deeply confused by OOP concepts like `this`, private fields, getters/setters, and the distinction between methods and static methods.

In industry, he argues that good systems built in OO languages succeed *despite* OOP, not because of it — because skilled programmers avoid pure OO style and write in a more procedural/functional hybrid.

---

## 8. Conclusion: Don't Buy Into OOP's Way of Thinking

The author's final advice is not to declare war on OO languages, but to avoid the extra "true OO techniques" that OOP adds on top of procedural programming. By eschewing those problematic features, you can still write acceptable programs in an OO language — because you are essentially using it as a non-OO procedural language.

---

**Summary in one sentence:** Yin Wang argues that OOP's core dogmas — "everything is an object," design patterns, extreme abstraction, and late binding — are fundamentally misguided, harmful to both learning and practice, and that good programmers succeed by largely ignoring these OOP-specific features.

References:

- [https://yinwang0.wordpress.com/2013/12/24/oop/](https://yinwang0.wordpress.com/2013/12/24/oop/)