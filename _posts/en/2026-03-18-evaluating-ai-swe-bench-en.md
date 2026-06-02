---
audio: false
generated: true
image: false
lang: en
layout: post
title: Evaluating AI With SWE-bench Benchmark
translated: false
type: note
---

Question: What is SWE-bench, how does it evaluate AI models, and is it trustworthy?

Answer:

## SWE-bench: A Comprehensive Introduction

### What is SWE-bench?

SWE-bench (Software Engineering Benchmark) is a benchmark designed to measure the ability of AI language models to solve **real-world GitHub issues**. It collects 2,294 task instances by crawling Pull Requests and Issues from 12 popular Python repositories. Each instance is based on a pull request that (1) is associated with an issue, and (2) modified one or more testing-related files.

It was introduced in a 2024 paper at ICLR: *"SWE-bench: Can Language Models Resolve Real-world GitHub Issues?"* by researchers from Princeton.

---

### The Benchmark Variants

SWE-bench has grown into a family of related benchmarks:

- **SWE-bench Full** — The original dataset of 2,294 tasks from 12 Python repositories.
- **SWE-bench Lite** — A smaller curated subset for less costly evaluation (300 tasks).
- **SWE-bench Verified** — A human-validated subset of SWE-bench released in collaboration with OpenAI in August 2024, aiming to more reliably evaluate AI models' ability to solve real-world software issues.
- **SWE-bench Multimodal** — Features issues with visual elements (517 tasks).
- **SWE-bench Multilingual** — Features 300 tasks across 9 programming languages beyond Python.

---

### How Does SWE-bench Evaluate AI Models?

The evaluation process follows a clear, structured pipeline:

**1. Task Setup**

Per instance, an execution environment (Docker image) is constructed with the repository successfully installed at the commit that the Pull Request is based on. Without the Pull Request's changes, a number of tests fail. After the Pull Request is merged, the same set of tests pass. These "Fail-to-Pass" tests are the primary signal for evaluation.

**2. Model Input**

The model is given access to a code repository and a description of an issue that needs to be fixed. The model must then investigate and modify the repository to resolve the issue.

**3. Patch Generation**

The AI system (agent) autonomously navigates the codebase, generates code changes, and produces a "patch" — a diff that modifies the repository to address the issue.

**4. Test-Based Grading**

A proposed edit is evaluated by running both the FAIL_TO_PASS and PASS_TO_PASS tests. If the FAIL_TO_PASS tests pass, this means the edit solves the issue. If the PASS_TO_PASS tests pass, then the edit has not inadvertently broken unrelated sections of the codebase. Both sets of tests are required to pass for the edit to fully resolve the original GitHub issue.

**5. Containerized Execution**

SWE-bench evaluates models by applying their generated patches to real-world repositories and running the repository's tests to verify if the issue is resolved. The evaluation is performed in a containerized Docker environment.

**6. Score Reporting**

The key metric is **% Resolved** — the percentage of task instances where the AI successfully generated a passing patch. As of early 2026, top agents score above 70% on SWE-bench Verified.

---

### The SWE-bench Verified Human Validation Process

The dataset was curated through a rigorous human annotation process involving 93 software developers. Each sample was reviewed by three separate annotators to ensure the issue description is well-specified, the unit tests are appropriate, and the sample is free of other major issues that could make evaluation unreliable.

---

### Is SWE-bench Trustworthy?

SWE-bench is widely respected and extensively used, but has several known limitations and criticisms that affect how much one should trust its scores at face value.

#### ✅ Strengths

- **Real-world grounding**: Tasks come from actual GitHub issues in production codebases, not synthetic puzzles.
- **Automated, reproducible scoring**: Docker-based execution ensures consistent evaluation.
- **Human validation** (Verified variant): Annotators filter out unsolvable or ambiguous tasks.
- **Public leaderboard and open tooling**: Community transparency is high.

#### ⚠️ Known Weaknesses and Criticisms

**1. Data Contamination**

Over 94% of SWE-bench Verified issues and their ground-truth pull requests predate the knowledge cutoff dates of leading LLMs. This raises the possibility that many models had access to the underlying data during training, further inflating reported scores via memorization rather than genuine reasoning.

**2. Weak Test Oracles**

The test suite used for validating each submission typically runs only those test files modified in the PR, not all available tests, leading to an estimated overstatement of passing rates by 4–7% (absolute) due to missed regression cases. In other words, a patch can pass tests while still being semantically incorrect.

**3. Benchmark Overfitting / Overestimation**

Benchmarks such as SWE-bench Verified systematically overestimate agent capabilities by up to ~20%, due to a combination of their heavy reliance on formal GitHub issue descriptions, language parity, and overfitting.

**4. Limited Scope of Tasks**

SWE-bench Verified predicts whether an AI can fix simple issues (taking at most a couple hours for a software engineer to solve) in a codebase. Furthermore, the low diversity of codebases limits external validity. Notably, Django comprises nearly half of all issues, and five repositories account for over 80% of the benchmark.

**5. Residual Error Rate**

Some samples may remain ambiguous — with a previously estimated error rate of 5–10%.

**6. Harness Dependency**

A notable complexity of SWE-bench lies in its dual evaluation of both the agentic harness and the underlying foundation model. This leads to different methodologies adopted by foundation model labs when they report their results. In other words, scores can vary significantly depending on *how* the model is scaffolded, not just the model itself.

---

### The Emerging Response: SWE-bench Pro

To address the above limitations, newer benchmarks like **SWE-bench Pro** have emerged. SWE-Bench Pro was developed to address data contamination, limited task diversity, oversimplified problems, and unreliable testing. It contains 1,865 tasks across 41 professional repositories, including private proprietary codebases. While most top models score over 70% on SWE-bench Verified, the best-performing models score only around 23% on SWE-bench Pro, highlighting the increased difficulty and realism of the new benchmark.

---

### Summary Verdict

SWE-bench is **the most widely adopted and credible benchmark** for evaluating AI software engineering agents today. Its scores are meaningful and directionally reliable for comparing models. However, due to data contamination risks, limited codebase diversity, weak test coverage, and harness variability, **raw numbers should not be taken as absolute truth**. It is best used as a *relative* signal, not an exact measure of real-world capability.

References:

- [SWE-bench Official Site](https://www.swebench.com)
- [SWE-bench Original Paper (ICLR 2024)](https://openreview.net/forum?id=VTF8yNQM66)
- [OpenAI: Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)
- [Epoch AI: SWE-bench Verified Review](https://epoch.ai/benchmarks/swe-bench-verified)
- [Epoch AI Substack: What does SWE-bench Verified actually measure?](https://epochai.substack.com/p/what-skills-does-swe-bench-verified-evaluate)
- [SWE-bench Evaluation Docs](https://www.swebench.com/SWE-bench/guides/evaluation/)
- [Scale Labs: SWE-bench Pro Leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro_public)
- [Vals.ai SWE-bench Analysis](https://www.vals.ai/benchmarks/swebench)
