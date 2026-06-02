---
audio: false
generated: true
lang: en
layout: post
title: 'Speeding Up Jekyll Builds: Exploring Multithreading Approaches'
translated: false
type: note
---

Jekyll's build process is single-threaded by default, which can be slow for large sites. While there’s no built-in configuration option in Jekyll to enable multithreaded builds, you can explore some approaches to achieve parallelism. Below, I outline the possibilities, challenges, and practical steps based on available information and technical considerations.

### Why Jekyll Builds Are Single-Threaded
Jekyll processes pages sequentially to ensure dependencies (like `site.related_posts` or Liquid templates) are handled correctly. Some components, such as Liquid and certain plugins, may not be thread-safe, which complicates multithreading (). This design prioritizes correctness over speed, but for large sites, this can lead to build times of several minutes (,).[](https://github.com/jekyll/jekyll/issues/9485)[](https://github.com/jekyll/jekyll/issues/1855)[](https://github.com/jekyll/jekyll/issues/4297)

### Approaches to Multithreaded Jekyll Builds
Here are potential ways to introduce parallelism to Jekyll builds, particularly in the context of a GitHub Actions workflow like the one you provided:

#### 1. **Use a Custom Plugin for Multithreaded Rendering**
A proof-of-concept plugin for multithreaded rendering has been proposed (). It reduced build time from 45 seconds to 10 seconds in a test case but had issues with thread safety, leading to incorrect page content. The plugin also conflicted with plugins like `jekyll-feed`, which rely on sequential rendering.[](https://github.com/jekyll/jekyll/issues/9485)

**Steps to Try a Custom Plugin:**
- **Create a Plugin**: Implement a Ruby plugin that extends Jekyll’s `Site` class to parallelize page rendering. For example, you could modify the `render_pages` method to use Ruby’s `Thread` class or a thread pool ().[](https://github.com/jekyll/jekyll/issues/9485)
  ```ruby
  module Jekyll
    module UlyssesZhan::MultithreadRendering
      def render_pages(*args)
        @rendering_threads = []
        super # Call original method
        @rendering_threads.each(&:join) # Wait for threads to complete
      end
    end
  end
  Jekyll::Site.prepend(Jekyll::UlyssesZhan::MultithreadRendering)
  ```
- **Add to Gemfile**: Place the plugin in your `_plugins` directory and ensure it’s loaded by Jekyll.
- **Test for Thread Safety**: Since Liquid and some plugins (e.g., `jekyll-feed`) may break, test thoroughly. You may need to patch Liquid or avoid multithreading for certain features ().[](https://github.com/jekyll/jekyll/issues/9485)
- **Integrate with GitHub Actions**: Update your workflow to include the plugin in your repository. Ensure the `jekyll-build-pages` action uses your custom Jekyll setup:
  ```yaml
  - name: Build with Jekyll
    uses: actions/jekyll-build-pages@v1
    with:
      source: ./
      destination: ./_site
    env:
      BUNDLE_GEMFILE: ./Gemfile # Ensure your custom Gemfile with the plugin is used
  ```

**Challenges**:
- Thread safety issues with Liquid and plugins like `jekyll-feed` ().[](https://github.com/jekyll/jekyll/issues/9485)
- Potential for incorrect page rendering (e.g., one page’s content appearing in another).
- Requires Ruby expertise to debug and maintain.

#### 2. **Parallelize Builds with Multiple Configurations**
Instead of multithreading a single build, you can split your site into smaller parts (e.g., by collection or directory) and build them in parallel using multiple Jekyll processes. This approach avoids thread-safety issues but requires more setup.

**Steps**:
- **Split the Site**: Organize your site into collections (e.g., `posts`, `pages`, `docs`) or directories and create separate `_config.yml` files for each (,).[](https://amcrouch.medium.com/configuring-environments-when-building-sites-with-jekyll-dd6eb2603c39)[](https://coderwall.com/p/tfcj2g/using-different-build-configuration-in-jekyll-site)
  ```yaml
  # _config_posts.yml
  collections:
    posts:
      output: true
  destination: ./_site/posts

  # _config_pages.yml
  collections:
    pages:
      output: true
  destination: ./_site/pages
  ```
- **Update GitHub Actions Workflow**: Modify your workflow to run multiple Jekyll builds in parallel, each with a different configuration file.
  ```yaml
  name: Build Jekyll Site
  on:
    push:
      branches: [main]
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Setup Ruby
          uses: ruby/setup-ruby@v1
          with:
            ruby-version: '3.1'
            bundler-cache: true
        - name: Build Posts
          run: bundle exec jekyll build --config _config_posts.yml
        - name: Build Pages
          run: bundle exec jekyll build --config _config_pages.yml
        - name: Combine Outputs
          run: |
            mkdir -p ./_site
            cp -r ./_site/posts/* ./_site/
            cp -r ./_site/pages/* ./_site/
        - name: Deploy
          uses: actions/upload-artifact@v4
          with:
            name: site
            path: ./_site
  ```
- **Combine Outputs**: After parallel builds, merge the output directories into a single `_site` folder for deployment.

**Challenges**:
- Managing interdependencies between collections (e.g., `site.related_posts`).
- Increased complexity in configuration and deployment.
- May not scale well for sites with tightly coupled content.

#### 3. **Use a Thread Pool for Large Sites**
A pull request for the `amp-jekyll` plugin suggested using a thread pool to process pages, with a configurable number of threads to avoid overwhelming the system (). This approach balances performance and resource usage.[](https://github.com/juusaw/amp-jekyll/pull/26)

**Steps**:
- **Implement a Thread Pool**: Modify or create a plugin to use Ruby’s `Thread::Queue` to manage a fixed number of worker threads (e.g., 4 or 8, depending on your system).
  ```ruby
  require 'thread'

  module Jekyll
    module ThreadPoolRendering
      def render_pages(*args)
        queue = Queue.new
        site.pages.each { |page| queue << page }
        threads = (1..4).map do # 4 threads
          Thread.new do
            until queue.empty?
              page = queue.pop(true) rescue nil
              page&.render_with_liquid(site)
            end
          end
        end
        threads.each(&:join)
        super
      end
    end
  end
  Jekyll::Site.prepend(Jekyll::ThreadPoolRendering)
  ```
- **Add Configuration Option**: Allow users to toggle multithreading or set the number of threads in `_config.yml`:
  ```yaml
  multithreading:
    enabled: true
    thread_count: 4
  ```
- **Integrate with Workflow**: Ensure the plugin is included in your repository and loaded during the GitHub Actions build.

**Challenges**:
- Similar thread-safety issues as the first approach.
- Context-switching overhead for large sites with many short tasks ().[](https://github.com/juusaw/amp-jekyll/pull/26)
- Requires testing to ensure compatibility with all plugins.

#### 4. **Optimize Without Multithreading**
If multithreading proves too complex or risky, you can optimize the single-threaded build process:
- **Enable Incremental Builds**: Use `jekyll build --incremental` to rebuild only changed files (,). Add to your workflow:[](https://github.com/jekyll/jekyll/blob/master/lib/jekyll/commands/build.rb)[](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)
  ```yaml
  - name: Build with Jekyll
    uses: actions/jekyll-build-pages@v1
    with:
      source: ./
      destination: ./_site
      incremental: true
  ```
- **Reduce Plugin Usage**: Custom plugins can significantly slow builds (). Audit and remove unnecessary plugins.[](https://github.com/jekyll/jekyll/issues/4297)
- **Use Faster Converters**: Switch from Kramdown to a faster markdown processor like CommonMark, or test Pandoc for specific use cases ().[](https://github.com/jekyll/jekyll/issues/9485)
- **Cache Dependencies**: Ensure `bundler-cache: true` in your GitHub Actions workflow to avoid reinstalling gems ().[](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)

### Recommendations
- **Start with Incremental Builds**: This is the simplest way to speed up builds without risking thread-safety issues. Add `--incremental` to your workflow and test its impact.
- **Experiment with a Thread Pool Plugin**: If you have Ruby expertise, try implementing a thread pool plugin with a configurable number of threads (Option 3). Start with a small site to test thread safety.
- **Avoid Full Multithreading for Now**: Given the thread-safety concerns with Liquid and plugins (), full multithreading may require significant refactoring or a custom Liquid fork, which may not be practical unless you’re contributing to Jekyll’s core development.[](https://github.com/jekyll/jekyll/issues/9485)
- **Monitor Build Times**: Use GitHub Actions logs to measure build times and identify bottlenecks. For example, a site taking 6 minutes to build () suggests plugins or large asset processing may be the issue.[](https://github.com/jekyll/jekyll/issues/1855)

### GitHub Actions Example with Incremental Builds
Here’s an updated version of your workflow with incremental builds enabled:
```yaml
name: Build Jekyll Site
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site
          incremental: true
      - name: Deploy
        uses: actions/upload-artifact@v4
        with:
          name: site
          path: ./_site
```

### Caveats
- **Thread Safety**: Multithreading in Jekyll is experimental and may break plugins or produce incorrect output (). Test thoroughly on a small site first.[](https://github.com/jekyll/jekyll/issues/9485)
- **GitHub Actions Limits**: Parallel builds (Option 2) increase resource usage, so ensure your workflow stays within GitHub’s free-tier limits.
- **Jekyll 5 Potential**: Future versions of Jekyll may address multithreading natively, as it’s been discussed (). For now, custom solutions are needed.[](https://github.com/jekyll/jekyll/issues/9485)

If you need help implementing a specific approach (e.g., writing a plugin or splitting builds), let me know, and I can provide more detailed guidance or code!
