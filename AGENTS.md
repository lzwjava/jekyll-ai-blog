# Repository Guidelines

Contributors should read this guide before touching the repository. It highlights how the Jekyll site, automation scripts, and tests fit together so you can ship changes confidently and keep the tooling working.

## Project Structure & Module Organization

Jekyll sources live under `_posts/<lang>/`, `_layouts/`, `_includes/`, `_sass/`, `_plugins/`, and `assets/`. Language landing pages such as `index-zh.html` sit in the project root. Python automation is grouped in `scripts/` with domain folders like `scripts/audio/`, `scripts/pdf/`, and `scripts/translation/`. Draft content resides in `original/` and `notes/`, while LaTeX resumes and their Makefile targets live in `latex/`. Tests are under `tests/` with LLM-specific pytest suites in `tests/llm/`.

## Build, Test, and Development Commands

- `bundle install` then `bundle exec jekyll serve --draft --incremental`: install Ruby gems and run a live preview.
- `bundle exec jekyll build`: produce the static site output.
- `python scripts/audio/audio_pipeline.py --task posts --n 10`: refresh a batch of audio assets.
- `python scripts/pdf/pdf_pipeline.py --task posts --n 10`: regenerate PDFs for recent posts.
- `make easy-resume`: compile the primary LaTeX resume (alternate: `make latex && make copy`).

## Coding Style & Naming Conventions

Use 4-space indentation for Python and prefer type hints. Run `black .` for formatting and `ruff .` for linting before opening a PR. Post files follow the `YYYY-MM-DD-slug.md` pattern under the correct language folder. Tests and fixtures use `test_*.py`, `Test*` classes, and `test_*` functions.

## Testing Guidelines

Default to the Python `unittest` suite via `python -m unittest discover -s tests -p 'test_*.py'`. Pytest-based LLM checks sit in `tests/llm/` and can be run with `python -m pytest tests/llm -v -m "not slow and not network"`. Integration tests depend on API keys via environment variables; document any new requirements in the PR.

## Commit & Pull Request Guidelines

Follow Conventional Commits (`feat(scope):`, `fix(scope):`, `docs:`, etc.) to match the existing history. PRs should describe the change, link related issues, and include screenshots or GIFs for UI or CSS updates. Confirm `black`, `ruff`, and the relevant tests pass locally before requesting review.

## Security & Configuration Tips

Never commit secrets; use environment variables for API tokens such as Azure or GCP credentials. Core configuration lives in `_config.yml`, while Ruby gems are tracked in `Gemfile` and Python dependencies in `requirements/`. For containerized workflows, build with `docker build -t blog .` and invoke your preferred serve or build command inside the container.
