---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimalism Wins in Tech Design
translated: false
type: note
---

Question: What are real-world cases of "less is better" in tech products, and why is removing features from software/hardware so hard compared to adding them?

Answer:

## "Less is Better" — The Philosophy and Practice of Simplification in Tech

This is a fascinating topic that touches on design philosophy, engineering, business strategy, and human psychology. Let's break it all down comprehensively.

---

## 1. The Core Idea: Why "Less" Is Valuable

Digital minimalism is the intentional practice of focusing digital products and processes on what truly matters, while stripping away the unnecessary. It rejects "feature bloat" — the temptation to add one more button, menu, or configuration — and instead prioritizes depth over breadth and purpose over novelty.

The concept "Worse is Better" (also called the New Jersey style) was coined by Richard P. Gabriel. It argues that software quality does not necessarily increase with functionality — there is a point where less functionality ("worse") is a preferable option ("better") in terms of practicality and usability. Software that is limited but simple to use may be more appealing to the user and market than the reverse.

Minimalism is implicit in the Unix philosophies of "everything is a text stream" and "do one thing and do it well," although modern Unix/Linux distributions do not hold so rigorously to this philosophy.

---

## 2. Apple — The Most Famous Simplifier

Apple is the canonical example of a company that has removed features relentlessly, sometimes controversially, often influencing the whole industry.

### The iMac G3 (1998) — Killing the Floppy Disk

The original iMac G3, released after Steve Jobs returned to Apple, was stylish and cool — until you found out that Apple decided not to include serial ports and floppy disk drives, swapping them out for USB ports and CD-ROMs. Serial ports were becoming more inconvenient compared to the emerging USB standard, which allowed plug-and-play peripherals.

### MacBook Air (2008) — Killing the Optical Drive

A decade after touting CDs as the next big thing, Apple removed the optical drive from the original MacBook Air in 2008. This was an obvious choice since Apple was positioning the MacBook Air as the thinnest laptop in the market — a CD-ROM drive made portable PCs thicker.

### MacBook Pro (2016) — The Great Port Purge

In 2016, Apple removed the MagSafe 2 charging port, stripped away the HDMI port, the SD card slot, shut down the Thunderbolt 2 ports, and most notably killed the standard USB port — replacing all of them with four Thunderbolt 3/USB-C ports.

This was extremely controversial. In 2016, Apple reached its peak "who needs ports lol" design era, offering to sell users a dongle for their MacBook's one (singular, uno) USB port and getting rid of the MacBook Pro's HDMI, USB Type-A, and SD card ports.

### iPhone 7 (2016) — Killing the Headphone Jack

In a landmark decision, Apple eliminated the 3.5mm headphone jack starting with the iPhone 7 in 2016. Apple's stated reasons included: the port served only a single function; it freed up space for other enhancements; and digital audio offers superior quality compared to analog.

Without the headphone jack, it became easier to design waterproof or water-resistant devices. Additionally, the transition aligned with the industry's shift towards wireless technology, as companies like Google and Apple introduced their own wireless earbuds (Pixel Buds Pro and AirPods).

### Apple Eventually Reversed Course

In 2021, Apple ditched its disliked OLED Touch Bar and put more ports back on the MacBook Pro. As The Verge wrote at the time, it was hard to ignore the broader context — these improvements effectively brought the 2021 MacBook Pros back in line with features already offered from 2012 to early 2016.

Apple's long-held commitment to "Less But Better" remains a central pillar to their continued success designing consumer electronics. Leveraging minimalism catapulted Apple into becoming the world's most valuable company.

---

## 3. Software and OS Examples

### Google Search

In a sea of cluttered search engines, Google's minimalist approach — a clean interface with a single search bar — revolutionized how we find information online.

### Basecamp (Project Management)

Originally launched in 2004, Basecamp's founders were determined to create project management software that avoided the endless feature bloat and complex interfaces characterizing enterprise platforms like Microsoft Project. As Jason Fried, Basecamp's founder explained, "We deliberately restrain the feature count." There are no complex Gantt charts, customized dashboards, or advanced reporting.

### WhatsApp

WhatsApp started with a simple premise — send messages over the internet. By focusing on this core functionality and ensuring reliability, they built a user base of billions.

### Windows 8 / iOS 7 — Visual Simplification

Windows 8 implemented the "simple, squared-off" Metro appearance, which was less graphics-intensive than the previous Aero interface in Windows 7 and Vista. This change was made in part because of the rise of smaller, battery-powered devices and the need to conserve power. iOS 7 made similar changes for user experience reasons.

### Microsoft and Apple Removing Features Quietly (and Controversially)

When Apple rewrote iWork applications to be fully 64-bit with unified file formats, the release notes had no notice that features were removed. Customers weren't amused. Apple said they planned to reintroduce some features in next releases. Tesla also unilaterally removed a feature from a $100,000 car via software update without notifying owners. Amazon remotely deleted books users had already downloaded and paid for on their Kindles without notifying users.

---

## 4. Why "Adding is Easy, Removing is Hard"

This is the deep and important question. There are several dimensions:

### Technical: Legacy Code and Spaghetti Dependencies

Old code is inextricably linked with new code. When you try to remove or change it, that creates a butterfly effect with a potentially devastating impact on operational continuity.

Dealing with the complexity of code within legacy systems, as well as teasing out the business processes the systems support, creates enormous challenges. The complexity of untangling thousands — or even millions — of lines of code from the business processes and rules that the code enables can be daunting.

### Human: User Resistance and Habit

Beyond IT teams, the biggest hurdle is often end-user adoption. It doesn't matter how advanced the new system is — if employees refuse to use it, the whole project is dead on arrival. People resist change, especially when it disrupts their workflow.

### Business: Fear of Losing Customers

If you remove a feature that even 2% of your users rely on, those users may leave. Product teams tend to be risk-averse about removal because the downside (losing real users) feels more immediate than the upside (cleaner product). Adding features has a clear success story; removing features has no ribbon-cutting moment.

### Organizational: Feature Ownership and Internal Politics

Inside a company, every feature was built by a team. That team has ownership, pride, and business justification. Removing their feature is politically difficult — it implies their work was wasteful. Minimalist codebases are easier to onboard new team members, less prone to bugs, and more adaptable to changing requirements — but achieving them requires practicing "You Aren't Gonna Need It" (YAGNI), resisting the urge to implement features "just in case."

### Cognitive: Feature Bloat Feels Like Value

Humans often equate "more features" with "better product." In a world where "more features" often equates to "better product" in people's minds, convincing stakeholders to embrace minimalism requires sharing case studies of successful minimalist products and using data to demonstrate how focused features lead to higher user engagement.

---

## 5. The Business Case for Removal

Less code and fewer features mean fewer bugs, reduced support load, and easier upgrades. Small, focused releases can be shipped quickly, validated with real users, and iterated upon. Simpler software is also easier to audit for security, privacy, and regulatory requirements.

Reducing the number of functions offered can optimize the user's decision-making. Too many options might cause a user to become overwhelmed and ultimately quit the task they are attempting to accomplish.

---

## 6. Engineering Principles That Codify "Less is Better"

| Principle | Meaning |
|---|---|
| **KISS** | Keep It Simple, Stupid — favor simple solutions |
| **YAGNI** | You Aren't Gonna Need It — don't build features speculatively |
| **DRY** | Don't Repeat Yourself — reduce code duplication |
| **Unix Philosophy** | Do one thing and do it well |
| **MVP** | Minimum Viable Product — ship the smallest useful thing |

---

## Summary

The "less is better" insight is counterintuitive but proven repeatedly in tech history. Adding is easy because it's additive — no breakage, no political fight, and it feels like progress. Removing is hard because it breaks dependencies, angers users, destroys internal ownership, and requires courage to admit that past work was unnecessary. Apple's repeated port and feature removals — some brilliant (floppy disk, optical drive), some overcorrected (MacBook Pro ports in 2016) — are the clearest real-world laboratory of this tension.

References:

- [Beyond the Backlog — Less is More in Product Design](https://beyondthebacklog.com/2024/01/20/less-is-more/)
- [Minimalism (computing) — Wikipedia](https://en.wikipedia.org/wiki/Minimalism_(computing))
- [Gitready — Digital Minimalism in Software Engineering](https://gitready.com/the-rise-of-digital-minimalism-in-software-engineering/)
- [The National — When Apple Removed Key Hardware Components](https://www.thenationalnews.com/business/technology/2023/09/12/when-apple-removed-key-hardware-components-on-its-devices-and-turned-out-to-be-right/)
- [PC Gamer — Apple Ports and the Courage Narrative](https://www.pcgamer.com/hardware/7-years-after-declaring-it-took-courage-to-remove-the-iphones-headphone-jack-apple-has-finally-decided-buttons-and-ports-are-cool-again/)
- [TechCrunch — MacBook Pro Kills Off Ports](https://techcrunch.com/2016/10/27/apples-new-macbook-pro-just-killed-off-most-of-the-ports-you-probably-need/)
- [Steve Blank — When Product Features Disappear](https://steveblank.com/2013/11/21/when-product-features-disappear-amazon-apple-and-tesla-and-troubled-future-of-21st-century-consumers/)
- [TechTarget — 6 Reasons Legacy Systems Are Still In Use](https://www.techtarget.com/searchcio/feature/6-reasons-legacy-systems-are-still-in-use)
- [Generaite Labs — Art of Minimalism in Software Engineering](https://generaitelabs.com/the-art-of-minimalism-in-software-engineering-focusing-on-core-features-for-maximum-impact/)
