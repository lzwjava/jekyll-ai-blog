---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Criticisms of Ansible Playbooks
translated: false
type: note
---

Question: What are unpopular opinions about Ansible playbooks?

Answer:

Ansible playbooks, while widely praised for simplifying infrastructure automation, draw some sharp criticism in niche discussions among DevOps practitioners. Here are several unpopular opinions drawn from community threads and posts, focusing on their limitations, misuse, and alternatives. These views often challenge the tool's "agentless simplicity" hype:

- **Long playbooks are a nightmare compared to simple scripts**: YAML shines as a config format but fails miserably as a programming language. Anything over 500 lines (let alone 3,400) turns into unmaintainable spaghetti with nested loops, Jinja2 templating hell, and conditional bloat. At that point, switch to a Python script or even Bash—it's faster to read, debug, and rewrite. Ansible's "declarative" promise crumbles under real complexity, making it actively worse than imperative scripting.

- **Playbooks aren't for programming—delegate logic elsewhere**: Ansible excels at side effects (e.g., installing packages or configuring services) but sucks at algorithms, conditionals, or any real computation. Offload decisions to a proper language like Python where you can unit-test logic, then feed the results into a simple playbook. Treating playbooks as codebases leads to brittle, untestable messes that "magic" away errors instead of exposing them.

- **Source of truth obsession is overrated for most use cases**: The Ansible community's fixation on a centralized "source of truth" (e.g., pulling facts from every server to verify state) is inefficient and unnecessary. For environments, just define desired packages/services in roles and apply them—don't query live systems unless you're in a hyper-complex setup like pure networking. This "pull everything" mindset wastes cycles and ignores that playbooks are better as push-based enforcers.

- **Idempotency is a myth in practice, leading to hidden failures**: Playbooks are sold as idempotent (rerunning changes nothing), but complex ones often drift due to unhandled edge cases, like partial failures in loops or OS-specific quirks. The advice to "run twice to verify" exposes this—it's not a feature, it's a hack. In reality, this encourages sloppy testing, and you're better off with tools that fail loudly (e.g., Terraform) rather than Ansible's quiet "it worked... mostly."

- **YAML's syntax and verbosity kill productivity**: Ansible's reliance on YAML makes even simple tasks feel bloated with indentation wars and verbose blocks. It's not "human-readable"—it's a config file pretending to be a DSL. For anything beyond ad-hoc commands, the boilerplate outweighs benefits, especially when async handling or error logging feels tacked-on and error-prone. Pros stick to ad-hoc mode and bail to scripts for the rest.

- **Roles vs. playbooks distinction is arbitrary and confusing**: There's no real difference between a "role" and a "playbook" beyond directory structure and variable precedence—it's all just disaggregated YAML. This leads to over-engineering: people cram everything into monolithic playbooks instead of modular roles, or vice versa, creating inflexible spaghetti. Keep it flat with many small playbooks for maintainability, not one god-playbook doing it all.

- **Ansible is outdated for modern cloud-native workflows**: In a world of Kubernetes, Terraform, and immutable infra, playbooks feel clunky for declarative orchestration. They're great for on-prem SSH pushes but add unnecessary abstraction layers in cloud environments where providers handle config natively. Skip Ansible entirely if you're all-in on AWS/GCP—focus on IaC tools that integrate better with CI/CD without the YAML tax.

These opinions highlight Ansible's strengths in quick, agentless automation but underscore frustrations with scaling it into full-fledged systems. If you're building playbooks, prioritize simplicity: use modules over shell commands, test idempotency rigorously, and know when to pivot to code.

References:
- [Ansible Playbooks with 3,400 lines aren't better than bash](https://x.com/brankopetric00/status/1997053364690211182)
- [Open Source Collection of Ansible Good and Bad Practices](https://www.reddit.com/r/ansible/comments/xw588g/open_source_collection_of_ansible_good_and_bad/)
- [Source of Truth is not important](https://www.reddit.com/r/ansible/comments/1dqtjja/source_of_truth_is_not_important/)
- [Good Practices for Ansible - The Zen of Ansible](https://redhat-cop.github.io/automation-good-practices/)
- [The ultimate guide for writing high-quality Ansible Playbooks](https://steampunk.si/spotter/blog/ultimate-guide-for-high-quality-ansible-playbooks/)
- [What is "best"? One playbook doing everything, or many?](https://www.reddit.com/r/ansible/comments/11m70hi/what_is_best_one_playbook_doing_everything_or/)
