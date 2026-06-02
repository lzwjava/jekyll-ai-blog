---
audio: false
generated: true
image: false
lang: en
layout: post
title: Double-Blind Review in AI Conferences
translated: false
type: note
---

**Question:** How is double-blind review used in AI conferences, and what are its rules, benefits, challenges, and current controversies?

**Answer:**

## What is Double-Blind Review?

Double-blind review means both sides stay anonymous during peer review: reviewers cannot see the authors' names or affiliations, and authors cannot see who the reviewers are. The purpose is simple — the conference wants the paper to be assessed on its academic merit rather than on the author's reputation, institution, or career stage.

This contrasts with:

- **Single-blind**: reviewers know who the authors are, but authors don't know the reviewers.
- **Open review**: both parties know each other (used by some venues like ICLR in post-acceptance phases).

---

## Which Major AI Conferences Use Double-Blind Review?

Top AI conferences such as ICML, ICLR, NeurIPS, and CVPR have adopted double-blind peer review as the standard, with their papers carrying impact comparable to many prestigious journals.

Specific policies:

- **ICLR 2026**: Submissions will be double blind — reviewers cannot see author names when conducting reviews, and authors cannot see reviewer names. Any paper where author identity is revealed in either the main text or the supplementary material will be desk rejected.
- **ICML 2026**: All papers will be reviewed in a double-blind process.
- **AAAI**: Reviews are double blind — neither reviewers nor authors should be able to identify each other. The first page should include the title, abstract, content areas, and ID number, but not names or affiliations of the authors.
- **IJCAI-ECAI 2026**: Authors are responsible for anonymizing their submission. They should not include author names or affiliations and should avoid providing any other identifying information, even in the supplementary material.

---

## Rules Authors Must Follow

**1. Remove identifying information:**
Authors must remove all author and affiliation information from their submission for review, and may replace it with other information such as paper number and keywords. Acknowledgements should also be omitted.

**2. Write self-citations in third person:**
When referring to one's own prior work, authors should use the third person rather than the first person. For example, say "Previously, Hinton et al. (2006) showed that…" rather than "In our previous work (Hinton et al., 2006) we showed that…"

**3. Handle arXiv carefully:**
It is acceptable for submitted work to appear in a preliminary version as an unrefereed preprint (e.g., on arXiv, social media, or personal websites). However, the conference submission should not include citations or pointers to the non-anonymous material, and the non-anonymous online material should not reference the fact that the work was submitted to the conference.

**4. Anonymize supplementary materials:**
Supplementary material and code should also be anonymized, including hardcoded paths or URLs that may give away login identifiers or institutions.

---

## Rules Reviewers Must Follow

Reviewers should not attempt to find out the identities of the authors for any assigned submissions (e.g., by searching on arXiv). This would constitute an active violation of the double-blind reviewing policy.

The goal of the double-blind reviewing process is to help members make a judgment about the paper without bias, not to make it impossible for them to discover the authors if they were to try. Nothing should be done for the sake of anonymity that potentially weakens the submission or makes reviewing more difficult — for example, important background references should not be omitted or anonymized.

---

## Benefits of Double-Blind Review

Because both authors and reviewers are "blind," this guards against reviewers being influenced by an author's prestige. Even submissions from stars in a field are considered on individual merit rather than on the author's reputation. Another benefit is that it reduces the possibility of reviewer bias.

Research evidence supports its effectiveness:
When the Conference on Learning Representations (ICLR) moved from single-anonymous to double-anonymous review, scores given to the most prestigious authors decreased significantly. Double-anonymous review was also found to be more effective at accepting high-quality papers (those cited most often) and rejecting low-quality papers.

Studies also found that newcomers are around twice as common in conferences that use double-anonymous review than single, indicating that single-anonymous review tends to bias against researchers who are not already well-known in the community.

---

## Challenges and Limitations

**1. De-anonymization is still possible:**
In small research communities, reviewers may still guess who wrote a paper from the topic, citations, or writing style.

**2. arXiv tension:**
ArXiv poses a major challenge to double-blind reviewing. Many studies have shown biases that result from reviewers knowing author information, and a large fraction of submitted papers end up reviewed under different conditions than the rest because of arXiv pre-prints.

**3. Exploding submission volume:**
The number of paper submissions to major AI conferences exceeded 10,000 by 2025 — for example, there was a 59.8% increase in ICLR submissions in 2025 alone — overwhelming the traditional peer review system.

**4. LLM-generated reviews:**
A report by Pangram Labs found that a staggering 21% of the 75,800 peer reviews for ICLR 2026 were fully generated by AI, with over half showing signs of AI assistance. The double-blind system, meant to ensure fairness, has become a shield for academic negligence — allowing overworked or disingenuous reviewers to outsource their critical duty to a large language model.

**5. Security breaches:**
The ICLR 2026 review process suffered a breach from an OpenReview API flaw identified as a broken access control issue, demonstrating how a single point of failure can compromise the entire double-blind system.

---

## How AI Conferences Are Adapting

- **Multi-phase reviewing**: AAAI-26 uses a two-phase reviewing process where papers that survive Phase 1 receive additional reviewers who are not given access to Phase 1 reviews until after submitting their own reviews.
- **Author rebuttal**: Most major conferences now include a dedicated rebuttal phase where authors can respond to reviewer comments.
- **LLM policy**: ICML allows authors to use generative AI tools to assist in writing or research, but authors must take full responsibility for all content, including anything that might be construed as plagiarism or scientific misconduct.
- **Reviewer qualification requirements**: At ICLR, all submissions must have at least one author registered to review at least 3 papers, and if none of the authors register as a reviewer, it will result in desk rejection.

---

## Summary Table

| Aspect | Detail |
|---|---|
| Core idea | Both authors and reviewers are anonymous to each other |
| Major conferences | ICML, ICLR, NeurIPS, AAAI, IJCAI, CVPR |
| Author obligations | Remove names, write self-cites in 3rd person, anonymize code/supplements |
| Reviewer obligations | Do not search for author identity, review independently |
| Key benefit | Reduces prestige/status bias; favors paper quality over author fame |
| Key challenge | arXiv pre-prints, LLM-generated reviews, de-anonymization in niche fields |
| Recent crisis | ICLR 2026 data breach + ~21% AI-generated reviews discovered |

**References:**

- [What Is Double-Blind Review for Conference Papers? – AiScholar](https://www.aischolar.com/news/article/what-is-double-blind-review-for-conference-papers)
- [AAAI-26 Review Process](https://aaai.org/conference/aaai/aaai-26/review-process/)
- [ICLR 2026 Author Guide](https://iclr.cc/Conferences/2026/AuthorGuide)
- [ICML 2026 Call for Papers](https://icml.cc/Conferences/2026/CallForPapers)
- [IJCAI-ECAI 2026 Call for Papers](https://2026.ijcai.org/ijcai-ecai-2026-call-for-papers-main-track/)
- [NeurIPS 2025 Reviewer Guidelines](https://neurips.cc/Conferences/2025/ReviewerGuidelines)
- [Double-Anonymous Review for Robotics – arXiv](https://arxiv.org/html/2406.10059v1)
- [The AI Conference Peer Review Crisis – arXiv](https://arxiv.org/html/2505.04966v1)
- [The Glass Wall Shatters: ICLR 2026 Breach Reflection](https://www.gensee.ai/blogs/a-professor-s-reflection-on-the-iclr-2026.html)
- [ArXiv and the Future of Double-Blind Reviewing – ACL 2017 Blog](https://acl2017.wordpress.com/2017/02/19/arxiv-and-the-future-of-double-blind-conference-reviewing/)
- [Single or Double Blind Peer Review – ExOrdo](https://www.exordo.com/blog/the-peer-review-process-single-versus-double-blind)
