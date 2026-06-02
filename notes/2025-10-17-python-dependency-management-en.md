---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Python Dependency Management with Poetry
translated: false
type: note
---

### What is Poetry?

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on, and it handles installing, updating, and resolving them automatically while ensuring reproducible environments.

### Main Purpose

Poetry simplifies Python project workflows by managing dependencies through a single configuration file (`pyproject.toml`), creating a lockfile for consistent installations across machines, and supporting the building of projects for distribution (e.g., to PyPI). It's designed to replace fragmented tools like `pip`, `pipenv`, and `setuptools` with a unified, user-friendly approach.

### Key Features

- **Dependency Resolution**: Automatically installs and updates dependencies, resolving conflicts intelligently.
- **Lockfile**: Generates `poetry.lock` to pin exact versions for repeatable builds.
- **Virtual Environments**: Creates isolated environments per project to avoid global pollution.
- **Packaging**: Builds wheels or sdists for easy distribution.
- **Multi-Platform Support**: Works on Linux, macOS, and Windows.
- **Shell Integration**: Tab completion for Bash, Fish, and Zsh.
- **Python 3.9+ Compatible**: Requires modern Python versions.

### Installation

Install Poetry in an isolated environment using `pipx` (recommended for global access without conflicts):

1. Install `pipx` if needed (via your OS package manager or `python -m pip install --user pipx`).
2. Run: `pipx install poetry`.

For updates: `pipx upgrade poetry`.
For uninstall: `pipx uninstall poetry`.

Enable shell completions (e.g., for Bash: `poetry completions bash >> ~/.bash_completion`).

### Basic Usage

Initialize a new project: `poetry init`.
Add a dependency: `poetry add requests`.
Install from lockfile: `poetry install`.
Run scripts: `poetry run python script.py`.
Build package: `poetry build`.

For full commands, check the docs.

[Poetry Documentation](https://python-poetry.org/docs/)
