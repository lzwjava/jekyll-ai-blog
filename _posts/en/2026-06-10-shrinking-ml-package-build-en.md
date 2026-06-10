---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shrinking ML Package Build
translated: false
type: note
---

Done! Here's what happened:

RELEASE LIVE: https://github.com/lzwjava/ww/releases/tag/v0.1.0

What was done:

1. Excluded ww/ml/ from build artifacts
   - ww/ml/ had 133MB of ML datasets/models (.h5, .pkl.gz, .csv, .wav)
   - Added hatch build config in pyproject.toml to exclude it
   - Wheel: 87MB → 713KB, sdist: 87MB → 687KB

2. Created GitHub Actions release workflow
   - File: .github/workflows/release.yml
   - Triggers on tag push (v*)
   - Builds wheel + sdist with uv build
   - Creates GitHub release with auto-generated release notes
   - Attaches .whl and .tar.gz as downloadable assets

3. Published v0.1.0 release
   - Tag v0.1.0 created and pushed
   - Release created by github-actions[bot] with both artifacts

How users install:

  # From GitHub release (download .whl)
  pip install ww-0.1.0-py3-none-any.whl

  # Or directly from the repo
  pip install git+https://github.com/lzwjava/ww.git@v0.1.0

Future releases — just bump version in pyproject.toml and tag:

  # bump version in pyproject.toml to 0.2.0, commit, then:
  git tag v0.2.0
  git push origin main --tags

The workflow auto-builds and publishes the release.
