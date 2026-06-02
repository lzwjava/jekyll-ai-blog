---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Automated Jekyll Build and Deploy Workflow
translated: false
type: note
---

You can do this entirely in GitHub Actions: build the site on the runner, then check out the destination repo into a subfolder and push the contents of `_site/` there.

Below is a drop-in workflow you can add to your **source** repo (where your Python scripts and Jekyll content live):

{% raw %}
```yaml
# .github/workflows/build-and-deploy.yml
name: Build & Deploy Jekyll to External Repo

on:
  push:
    branches: [ main ]
  workflow_dispatch:

# We’ll use a PAT for the destination repo push
permissions:
  contents: read

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Check out source repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: Install Jekyll deps
        run: |
          bundle install --jobs 4 --retry 3

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python deps
        if: hashFiles('requirements.txt') != ''
        run: pip install -r requirements.txt

      - name: Run your local workflow pipeline (CI mode)
        env:
          # add any keys your scripts need here
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        run: |
          # Run exactly the same steps your script orchestrates.
          # If you want, you can call your script directly:
          python scripts/workflow_local.py
          # Or, if you prefer explicit steps:
          # python scripts/generate/update_notes_link.py
          # python scripts/translation/update_lang.py --max_files 9 --model gemini-flash --commits 1000
          # python -m unittest discover -s tests/workflow
          # python scripts/release/update_release.py

      - name: Build Jekyll (to _site)
        run: |
          # If your Python module sets DEFAULT_DESTINATION elsewhere, you can still override here.
          bundle exec jekyll build --destination _site

      - name: Check out destination repo
        uses: actions/checkout@v4
        with:
          repository: lzwjava/lzwjava.github.io   # <-- your DESTINATION_REPO_URL target
          token: ${{ secrets.WORKFLOW_ACCESS_TOKEN }}      # <-- PAT with "repo" scope
          path: destination
          fetch-depth: 0

      - name: Sync built site to destination repo
        run: |
          mkdir -p destination/_site
          rsync -av --delete _site/ destination/_site/
          cd destination
          # Optional: ensure Pages doesn’t process Jekyll again
          touch _site/.nojekyll

          git config user.name  "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          if [ -n "$(git status --porcelain)" ]; then
            git add -A
            git commit --amend --no-edit
            # adjust branch if your destination uses something else (e.g., gh-pages)
            git push --force-with-lease origin HEAD:main
          else
            echo "No changes to deploy."
          fi

      - name: (Optional) Upload built site artifact
        uses: actions/upload-artifact@v4
        with:
          name: site
          path: _site
```
{% endraw %}

### What you need to set up

* **PAT for the destination push**: create a classic Personal Access Token with `repo` scope on your GitHub account (or use a fine-grained token that grants write access to the destination repo). Save it in the source repo settings as `WORKFLOW_ACCESS_TOKEN` (i.e., `Settings → Secrets and variables → Actions → New repository secret`).
* **Branch and repo names**: in the `Check out destination repo` step, set `repository:` to the external repo (it can be public or private). In the push command, set the branch you want to deploy to (often `main` or `gh-pages`).
* **GitHub Pages settings** (if you’re serving from the destination repo): in that repo’s **Settings → Pages**, choose the correct **Branch** (e.g., `main` / root), and keep `CNAME`/custom domain as you like.
* **History expectations**: the deploy step amends the latest commit and uses `--force-with-lease`; make sure this branch is dedicated to deploy artifacts so rewriting history is acceptable.

### Notes about your Python script

* You don’t need `open_destination_repo_in_browser()` in CI, so it’s fine to leave it as-is; it simply won’t be called here. The workflow pushes directly from the runner.
* You also don’t need `push_destination_repo()` in CI. The workflow handles the second checkout and push, so you can keep your script unchanged for local runs.
* If your `build_site()` writes to a different `DEFAULT_DESTINATION`, you can still override by running the explicit Jekyll build step shown above, which writes to `_site/`. The deploy step syncs from `_site/`.

### Private destination repo?

* That’s fine. GitHub Pages only serves public repos (or public branches in orgs with Pages enabled), but if your goal is just to push artifacts to a private repo for any reason, the above still works. If you do want Pages hosting, make sure that destination repo/branch is configured to serve Pages (public where required) or use an alternative host (e.g., Cloudflare Pages, Netlify) and deploy there instead.

That’s it—you’ll now build on GitHub’s runners and push `_site/` to another repo in the cloud.
