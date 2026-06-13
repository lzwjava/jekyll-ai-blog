---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA Careers Portal Explained
translated: false
type: note
---

**Question:** What is the portal at jobs.nvidia.com/careers?

**Answer:**

It's NVIDIA's official external careers portal — their job listing and application site for candidates.

Under the hood, it's built on **Eightfold AI** (eightfold.ai), an AI-powered talent intelligence platform. The config reveals a lot about how it works:

- **AI-driven job matching** — it scores your profile against positions and shows a match percentage. The config has `showMatchScore: true` and `strongMatchThreshold: 4`.
- **Skills-based search** — filterable by job category, skills, location, time type (full-time/intern), remote eligibility.
- **Talent network** — you can sign up to receive job alerts without applying. It uses the candidate's profile (resume, skills, experience) to send matched recommendations on a 7-day interval.
- **ATS backend** — applications get redirected to NVIDIA's Workday ATS (`nvidia.wd5.myworkdayjobs.com`) for the actual submission. The apply button is a link-off to Workday, not a native form.
- **Profile intelligence** — the platform ingests your resume and builds a structured profile (experience, education, skills, certs, projects) that powers match scoring across all open reqs.

**Why it matters for you specifically:** NVIDIA has heavy AI infrastructure roles — CUDA kernels, GPU architecture, inference optimization, large-scale training systems. Their roles in the Compute, Networking, and AI/ML divisions are exactly aligned with where you're heading. The match score system means a well-crafted profile with the right skills (CUDA, PyTorch, transformers, MoE, LoRA, RLHF) will surface you higher in recruiter searches. Worth building a profile there if you're serious about an NVIDIA trajectory.
