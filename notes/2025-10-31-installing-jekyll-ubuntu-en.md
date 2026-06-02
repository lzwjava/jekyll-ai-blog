---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Installing Jekyll on Ubuntu
translated: false
type: note
---

### Setting Up and Running Jekyll on Ubuntu

Based on your error ("Command 'bundle' not found") and the commands you're trying to run, it looks like you need to install Ruby, Bundler, and Jekyll properly first. Ubuntu doesn't come with these by default, but it's straightforward using the official Jekyll guide. I'll walk you through the full setup step by step, then how to run your specific commands.

#### Step 1: Install System Dependencies

Open your terminal and run this to install Ruby and build tools (this includes Ruby 3.x via `ruby-full`):

```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
```

- This sets up Ruby (check with `ruby -v`—it should show something like 3.0+).
- If you're on a recent Ubuntu (e.g., 22.04+), this works out of the box. Avoid Snap for Ruby if possible, as it can cause path issues.

#### Step 2: Set Up a User Gem Directory (Recommended to Avoid Sudo)

To install gems without root privileges (prevents permission errors later):

```bash
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

- Verify: Run `gem env`—it should show your `GEM_HOME` as `~/gems`.

#### Step 3: Install Jekyll and Bundler

Now install the tools:

```bash
gem install jekyll bundler
```

- This adds `gem`, `jekyll`, and `bundle` commands to your path.
- If you get permission errors, double-check Step 2 or temporarily use `sudo` (but avoid it long-term).

#### Step 4: Create and Run Your Blog

Now you can run the commands from your snippet. I'll explain each:

1. **Create a new Jekyll site**:

   ```bash
   jekyll new myblog
   ```

   - This generates a basic site in a `myblog` folder.

2. **Enter the directory**:

   ```bash
   cd myblog
   ```

3. **Install dependencies** (this is where your original `bundle install` failed—now it should work):

   ```bash
   bundle install
   ```

   - Pulls in gems like Jekyll plugins.

4. **Serve the site** (starts a local server at <http://127.0.0.1:4000>):

   ```bash
   bundle exec jekyll serve
   ```

   - Open your browser to that URL to see your site.

5. **Serve with incremental rebuilds** (faster for development, only rebuilds changed files):

   ```bash
   bundle exec jekyll serve --incremental
   ```

6. **Serve including drafts** (shows unpublished posts):

   ```bash
   bundle exec jekyll serve --draft
   ```

7. **If you get a "webrick" error** (common on Ruby 3+, as it's not bundled by default):

   ```bash
   bundle add webrick
   ```

   - Then restart the serve command: `bundle exec jekyll serve`.
   - Alternatively, add `gem "webrick"` to your `Gemfile` and run `bundle install`.

8. **Quick serve without Bundler** (if you skip `bundle exec`):

   ```bash
   jekyll serve
   ```

   - But use `bundle exec` for consistency in projects.

#### Troubleshooting

- **Still "bundle not found"?** Ensure Step 2 sourced your `~/.bashrc` correctly (`source ~/.bashrc`), then restart your terminal or run `hash -r`. Check with `which bundle`.
- **Permission issues with gems?** Stick to the user directory setup in Step 2.
- **Ruby version too old?** If `ruby -v` is <3.0, consider using rbenv for a newer version (install via `curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash`, then `rbenv install 3.2.0`).
- **Firewall blocking port 4000?** Ubuntu usually doesn't, but test with `curl http://127.0.0.1:4000`.
- Your project is in `~/projects/blog-source`—run these from there or adjust paths.

Once served, edit files in `_posts/` or `_config.yml` and save—Jekyll auto-rebuilds. For production, build with `jekyll build` and deploy to GitHub Pages or Netlify.

[Jekyll Ubuntu Installation Guide](https://jekyllrb.com/docs/installation/ubuntu/)
