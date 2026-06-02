---
audio: false
generated: true
lang: zh
layout: post
title: 加速Jekyll构建：探索多线程方案
translated: true
type: note
---

Jekyll 的构建过程默认采用单线程模式，对于大型站点来说可能会比较慢。虽然 Jekyll 没有内置的多线程构建配置选项，但你可以探索一些实现并行化的方法。下面我将根据现有信息和技术考量，概述可能性、挑战及实际操作步骤。

### 为什么 Jekyll 构建是单线程的
Jekyll 按顺序处理页面，以确保依赖项（如 `site.related_posts` 或 Liquid 模板）得到正确处理。某些组件（如 Liquid 和特定插件）可能不是线程安全的，这使得多线程变得复杂 ()。这种设计优先考虑正确性而非速度，但对于大型站点，这可能导致构建时间长达数分钟 (,)。[](https://github.com/jekyll/jekyll/issues/9485)[](https://github.com/jekyll/jekyll/issues/1855)[](https://github.com/jekyll/jekyll/issues/4297)

### 实现 Jekyll 多线程构建的方法
以下是在 Jekyll 构建中引入并行化的潜在方法，特别是在你提供的 GitHub Actions 工作流程的背景下：

#### 1. **使用自定义插件实现多线程渲染**
有人提出了一个多线程渲染的概念验证插件 ()。在一个测试案例中，它将构建时间从 45 秒减少到 10 秒，但存在线程安全问题，导致页面内容不正确。该插件还与依赖顺序渲染的插件（如 `jekyll-feed`）冲突。[](https://github.com/jekyll/jekyll/issues/9485)

**尝试自定义插件的步骤：**
- **创建插件**：实现一个 Ruby 插件，扩展 Jekyll 的 `Site` 类以并行化页面渲染。例如，你可以修改 `render_pages` 方法，使用 Ruby 的 `Thread` 类或线程池 ()。[](https://github.com/jekyll/jekyll/issues/9485)
  ```ruby
  module Jekyll
    module UlyssesZhan::MultithreadRendering
      def render_pages(*args)
        @rendering_threads = []
        super # 调用原始方法
        @rendering_threads.each(&:join) # 等待线程完成
      end
    end
  end
  Jekyll::Site.prepend(Jekyll::UlyssesZhan::MultithreadRendering)
  ```
- **添加到 Gemfile**：将插件放入你的 `_plugins` 目录，并确保 Jekyll 加载它。
- **测试线程安全性**：由于 Liquid 和某些插件（例如 `jekyll-feed`）可能会出现问题，请进行彻底测试。你可能需要修补 Liquid 或对某些功能避免使用多线程 ()。[](https://github.com/jekyll/jekyll/issues/9485)
- **与 GitHub Actions 集成**：更新你的工作流程，将插件包含在你的仓库中。确保 `jekyll-build-pages` 操作使用你的自定义 Jekyll 设置：
  ```yaml
  - name: Build with Jekyll
    uses: actions/jekyll-build-pages@v1
    with:
      source: ./
      destination: ./_site
    env:
      BUNDLE_GEMFILE: ./Gemfile # 确保使用包含插件的自定义 Gemfile
  ```

**挑战**：
- 与 Liquid 和插件（如 `jekyll-feed`）的线程安全问题 ()。[](https://github.com/jekyll/jekyll/issues/9485)
- 可能产生不正确的页面渲染（例如，一个页面的内容出现在另一个页面中）。
- 需要 Ruby 专业知识来调试和维护。

#### 2. **使用多个配置并行构建**
你可以将站点拆分成较小的部分（例如，按集合或目录），并使用多个 Jekyll 进程并行构建它们，而不是在单个构建中使用多线程。这种方法避免了线程安全问题，但需要更多的设置。

**步骤**：
- **拆分站点**：将站点组织成集合（例如 `posts`、`pages`、`docs`）或目录，并为每个部分创建单独的 `_config.yml` 文件 (,)。[](https://amcrouch.medium.com/configuring-environments-when-building-sites-with-jekyll-dd6eb2603c39)[](https://coderwall.com/p/tfcj2g/using-different-build-configuration-in-jekyll-site)
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
- **更新 GitHub Actions 工作流程**：修改你的工作流程，以并行运行多个 Jekyll 构建，每个构建使用不同的配置文件。
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
- **合并输出**：在并行构建之后，将输出目录合并到单个 `_site` 文件夹中以进行部署。

**挑战**：
- 管理集合之间的相互依赖关系（例如 `site.related_posts`）。
- 配置和部署的复杂性增加。
- 对于内容紧密耦合的站点，可能无法很好地扩展。

#### 3. **对大型站点使用线程池**
一个针对 `amp-jekyll` 插件的拉取请求建议使用线程池来处理页面，并配置线程数量以避免系统过载 ()。这种方法在性能和资源使用之间取得平衡。[](https://github.com/juusaw/amp-jekyll/pull/26)

**步骤**：
- **实现线程池**：修改或创建一个插件，使用 Ruby 的 `Thread::Queue` 来管理固定数量的工作线程（例如 4 或 8，取决于你的系统）。
  ```ruby
  require 'thread'

  module Jekyll
    module ThreadPoolRendering
      def render_pages(*args)
        queue = Queue.new
        site.pages.each { |page| queue << page }
        threads = (1..4).map do # 4 个线程
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
- **添加配置选项**：允许用户在 `_config.yml` 中启用多线程或设置线程数量：
  ```yaml
  multithreading:
    enabled: true
    thread_count: 4
  ```
- **与工作流程集成**：确保插件包含在你的仓库中，并在 GitHub Actions 构建期间加载。

**挑战**：
- 与第一种方法类似的线程安全问题。
- 对于具有许多短任务的大型站点，上下文切换开销较大 ()。[](https://github.com/juusaw/amp-jekyll/pull/26)
- 需要测试以确保与所有插件的兼容性。

#### 4. **在不使用多线程的情况下进行优化**
如果多线程过于复杂或风险较高，你可以优化单线程构建过程：
- **启用增量构建**：使用 `jekyll build --incremental` 仅重建已更改的文件 (,)。添加到你的工作流程中：[](https://github.com/jekyll/jekyll/blob/master/lib/jekyll/commands/build.rb)[](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)
  ```yaml
  - name: Build with Jekyll
    uses: actions/jekyll-build-pages@v1
    with:
      source: ./
      destination: ./_site
      incremental: true
  ```
- **减少插件使用**：自定义插件会显著减慢构建速度 ()。审计并移除不必要的插件。[](https://github.com/jekyll/jekyll/issues/4297)
- **使用更快的转换器**：从 Kramdown 切换到更快的 Markdown 处理器，如 CommonMark，或针对特定用例测试 Pandoc ()。[](https://github.com/jekyll/jekyll/issues/9485)
- **缓存依赖项**：在你的 GitHub Actions 工作流程中确保 `bundler-cache: true`，以避免重新安装 gem ()。[](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)

### 建议
- **从增量构建开始**：这是在不冒线程安全风险的情况下加速构建的最简单方法。将 `--incremental` 添加到你的工作流程中并测试其效果。
- **尝试线程池插件**：如果你具备 Ruby 专业知识，可以尝试实现一个可配置线程数量的线程池插件（选项 3）。首先在一个小型站点上测试线程安全性。
- **暂时避免完全多线程**：考虑到 Liquid 和插件的线程安全问题 ()，完全多线程可能需要大量重构或自定义 Liquid 分支，除非你参与 Jekyll 核心开发，否则可能不切实际。[](https://github.com/jekyll/jekyll/issues/9485)
- **监控构建时间**：使用 GitHub Actions 日志测量构建时间并识别瓶颈。例如，一个构建需要 6 分钟的站点 () 表明插件或大型资源处理可能是问题所在。[](https://github.com/jekyll/jekyll/issues/1855)

### 启用增量构建的 GitHub Actions 示例
以下是你的工作流程的更新版本，启用了增量构建：
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

### 注意事项
- **线程安全**：Jekyll 中的多线程是实验性的，可能会破坏插件或产生不正确输出 ()。首先在小型站点上彻底测试。[](https://github.com/jekyll/jekyll/issues/9485)
- **GitHub Actions 限制**：并行构建（选项 2）会增加资源使用量，因此请确保你的工作流程保持在 GitHub 免费层限制内。
- **Jekyll 5 的潜力**：Jekyll 的未来版本可能会原生支持多线程，因为已经讨论过 ()。目前，需要自定义解决方案。[](https://github.com/jekyll/jekyll/issues/9485)

如果你需要帮助实施特定方法（例如编写插件或拆分构建），请告诉我，我可以提供更详细的指导或代码！
