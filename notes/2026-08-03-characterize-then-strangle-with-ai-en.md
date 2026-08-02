---
audio: false
generated: true
image: false
lang: en
layout: post
title: Characterize Then Strangle with AI
translated: false
type: note
---

Question: When internal enterprise libs (e.g. custom Spring wrappers) become unmaintainable because the original vendor devs left, should you rewrite/replace them with AI?

Answer: Yes, but the decision isn't "rewrite vs keep" — it's "characterize first, then strangle." The reason internal libs used to stay untouched for years wasn't that they were good, it was that *reading cost* > *rewrite risk*. LLMs collapsed reading cost to near zero. That changes the math, but only if you do it in the right order.

**Wrong approach**: dump the wrapper into a chat, ask for a "clean rewrite," ship it. This silently drops the tribal-knowledge edge cases — null handling for a specific downstream service, a retry hack for a CVE patch, a timeout tuned after an incident three years ago. None of that is in the "clean" version an LLM produces from first principles.

**Right pipeline** — branch-by-abstraction + characterization, AI-assisted at every step:

```bash
# 1. Inventory: find every call site of the internal lib across the monorepo
rg -l "com.yourcompany.internal.SpringWrapper" --type java > callsites.txt
wc -l callsites.txt

# 2. Dump the lib + its call sites into context, ask model to produce a
#    behavior spec, not a rewrite. This is the step people skip.
cat internal-lib/src/main/java/**/*.java > /tmp/lib_dump.txt
```

Prompt (this is the actual leverage point):
```
Here is an internal Spring wrapper library and its call sites.
Do NOT propose a rewrite. Instead:
1. List every observable behavior (inputs -> outputs, including error paths)
2. List every place behavior deviates from vanilla Spring/Boot defaults
   (these are usually the reason the wrapper exists)
3. Flag anything that looks like a CVE patch, retry/timeout tuning,
   or workaround for a specific downstream service
```

```python
# 3. Turn that spec into characterization tests against the CURRENT lib
#    (golden master testing — capture real behavior, bugs included)
def test_wrapper_matches_golden_output():
    for case in golden_cases:
        assert current_wrapper.call(case.input) == case.expected  # recorded, not derived
```

```java
// 4. Branch by abstraction: introduce an interface, current impl behind it,
//    let AI-generated new impl sit behind the SAME interface
interface HttpClientPort {
    Response execute(Request req);
}
// old: SpringWrapperAdapter implements HttpClientPort  (unchanged, just wrapped)
// new: ModernRestClientAdapter implements HttpClientPort  (AI-generated candidate)
```

```bash
# 5. Route a % of traffic or a subset of call sites to the new impl,
#    diff against golden master and prod shadow traffic, then finish
#    strangling call site by call site.
```

**When to actually delete instead of reimplement**: if the wrapper is just gluing standard Spring/Boot features that Spring itself now does natively (e.g. a homegrown `RestTemplate` retry wrapper when `RestClient` + `@Retryable`/resilience4j already covers it) — don't reimplement the wrapper at all, migrate call sites straight to the modern Spring API. AI is great here because it can mechanically diff "what does this custom code do" against "what does the current framework do out of the box" and tell you the wrapper is now dead weight.

**When NOT to touch it**: if step 2's spec surfaces business logic (fee calculation, entitlement rules) hiding inside what looks like plumbing. That's not a library problem, that's undocumented domain logic — extract it as named business rules with tests, not as part of a "Spring wrapper cleanup."

Bottom line: the AI's job isn't rewriting the code, it's collapsing the archaeology cost so you can safely apply the boring, decades-old strangler fig / branch-by-abstraction pattern instead of a big-bang rewrite.

References:
- [Strangler Fig Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
- [Branch by Abstraction variant for library/framework migrations](https://layrs.me/course/hld/11-cloud-design-patterns/strangler-fig)
- [Strangler Fig Pattern - CTO's Guide](https://www.wireapps.co.uk/blog/strangler-fig-pattern-guide)