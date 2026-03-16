---
audio: false
generated: true
image: false
lang: en
layout: post
title: OASIS Social Media Simulation Framework
translated: false
type: note
---

I'll fetch the GitHub repository to give you an introduction to OASIS.## Introduction to OASIS

OASIS is an open-source social media simulator that uses large language model agents to realistically mimic the behavior of up to one million users on platforms like Twitter and Reddit. It's designed to facilitate the study of complex social phenomena such as information spread, group polarization, and herd behavior.

### Key Features

**Scalability**: OASIS supports simulations of up to one million agents, enabling studies of social media dynamics at a scale comparable to real-world platforms.

**Dynamic Environments**: The system adapts to real-time changes in social networks and content, mirroring the fluid dynamics of platforms like Twitter and Reddit for authentic simulation experiences.

**Rich Interactions**: Agents can perform 23 actions, such as following, commenting, and reposting, allowing for multi-faceted interactions.

**Smart Recommendations**: It features interest-based and hot-score-based recommendation algorithms, simulating how users discover content and interact within social media platforms.

### Use Cases

The platform supports diverse research and industry applications including:
- Research simulations studying social phenomena
- Content interaction analysis
- User behavior prediction
- Social dynamics experimentation

### Getting Started

The framework is available via PyPI (`pip install camel-oasis`) and uses OpenAI's API for agent intelligence. You define agent profiles, specify available actions, create an environment, and then run simulations with either manual or LLM-driven agent actions.

### Technical Details

- Built on Python with documentation available at docs.oasis.camel-ai.org/
- Licensed under Apache 2.0
- Part of the CAMEL-AI ecosystem
- Includes visualization and analysis tools for simulation data

This is particularly valuable for researchers studying social dynamics at unprecedented scale without the ethical constraints of experimenting with real platforms.