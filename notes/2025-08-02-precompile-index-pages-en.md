---
audio: false
generated: true
image: false
lang: en
layout: post
title: Precompile Language-Specific Index Pages
translated: false
type: note
---

Yes, you can precompile separate index pages for different languages (e.g., `index-zh.html`, `index-en.html`) to improve performance and user experience, especially if your site has a large number of posts or if you want to reduce client-side JavaScript processing. This approach would involve generating static HTML files for each language during the build process, rather than relying on JavaScript to filter and sort posts dynamically on the client side.

Below, I’ll outline how you can achieve this with Jekyll, focusing on creating separate index pages for each language (`index-zh.html`, `index-en.html`, etc.) while maintaining the functionality of your current setup. This will leverage Jekyll’s build system to precompute the filtered post lists for each language, reducing the need for complex client-side JavaScript.

---

### Approach to Precompile `index-zh.html`, `index-en.html`, etc.

To precompile language-specific index pages, you can create separate Jekyll page templates for each language and use Liquid to filter posts by language during the build process. This way, each page (`index-en.html`, `index-zh.html`, etc.) will contain only the relevant posts, and the sorting/filtering logic will be handled at build time rather than in the browser.

Here’s how you can do it:

---

#### 1. Create Language-Specific Page Templates

Create separate page files in your Jekyll project’s root directory for each language, such as:

- `index-en.html`
- `index-zh.html`
- `index-ja.html`
- ...and so on for other languages (`es`, `hi`, `fr`, `de`, `ar`, `hant`, etc.).

Each file will use a similar structure to your provided code but will filter posts for a specific language using Liquid. Here’s an example for `index-en.html`:

{% raw %}
```html
---
layout: page
lang: en
permalink: /en/
---

<div class="sort-container">
  <span id="post-number" class="post-number">
    {% assign en_posts = site.posts | where: "lang", "en" %}
    {{ en_posts.size }} posts
    ({{ en_posts | where: "translated", true | size }} by <a href="https://mistral.ai">AI</a>)
  </span>

  <select id="sort-select">
    <option value="author-picks|en">Picks</option>
    <option value="date-desc|all">All</option>
    <option value="date-desc|original">Original</option>
    <option value="date-desc|en" selected>English</option>
    <option value="date-desc|zh">中文</option>
    <option value="date-desc|ja">日本語</option>
    <option value="date-desc|es">Español</option>
    <option value="date-desc|hi">हिंदी</option>
    <option value="date-desc|fr">Français</option>
    <option value="date-desc|de">Deutsch</option>
    <option value="date-desc|ar">العربية</option>
    <option value="date-desc|hant">繁體中文</option>
  </select>
</div>

<ul class="post-list">
  {% if en_posts.size > 0 %}
    {% for post in en_posts %}
      <li class="list-group-item post-item lang-en" data-top="{{ post.top | default: 0 }}" data-translated="{{ post.translated | default: false }}" data-generated="{{ post.generated | default: false }}">
        <a href="{{ post.url }}">
          <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
          <span class="type">{% if post.image %}image{% else %}text{% endif %}</span>
          <span class="title">{{ post.title }}</span>
        </a>
      </li>
    {% endfor %}
  {% else %}
    <li class="list-group-item post-item">No posts available.</li>
  {% endif %}
</ul>

<footer class="site-footer">
  <span class="site-footer-credits">
    Powered by <a href="https://jekyllrb.com/">Jekyll</a><br>
    Ignited by <a href="https://mistral.ai">Mistral</a><br>
    Updated at <a href="https://github.com/lzwjava/lzwjava.github.io/commit/{{ site.release }}">{{ site.release | slice: 0, 6 }}</a><br>
    Copyright©{{ site.starting_year }}–{{ site.time | date: "%Y" }}
  </span>
</footer>
```
{% endraw %}

For `index-zh.html`, you would replace the `lang` and `where` filter:

{% raw %}
```html
---
layout: page
lang: zh
permalink: /zh/
---
<div class="sort-container">
  <span id="post-number" class="post-number">
    {% assign zh_posts = site.posts | where: "lang", "zh" %}
    {{ zh_posts.size }} posts
    ({{ zh_posts | where: "translated", true | size }} by <a href="https://mistral.ai">AI</a>)
  </span>
  <!-- Same sort-select as above -->
</div>

<ul class="post-list">
  {% if zh_posts.size > 0 %}
    {% for post in zh_posts %}
      <li class="list-group-item post-item lang-zh" data-top="{{ post.top | default: 0 }}" data-translated="{{ post.translated | default: false }}" data-generated="{{ post.generated | default: false }}">
        <a href="{{ post.url }}">
          <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
          <span class="type">{% if post.image %}image{% else %}text{% endif %}</span>
          <span class="title">{{ post.title }}</span>
        </a>
      </li>
    {% endfor %}
  {% else %}
    <li class="list-group-item post-item">No posts available.</li>
  {% endif %}
</ul>

<!-- Same footer as above -->
```
{% endraw %}

Repeat this for each language (`ja`, `es`, `hi`, `fr`, `de`, `ar`, `hant`, etc.), adjusting the `lang` front matter and the `where` filter accordingly.

---

#### 2. Update Post Front Matter

Ensure that each post in your `_posts` directory has a `lang` front matter variable that corresponds to its language (e.g., `en`, `zh`, `ja`, etc.). For example:

```yaml
---
title: My English Post
lang: en
date: 2025-08-01
translated: true
generated: false
top: 1
---
```

This allows the `where` filter to correctly identify posts by language.

If your posts are organized in subdirectories like `_posts/en/`, `_posts/zh/`, etc., you can infer the language from the path instead of using a `lang` variable. For example, in `index-en.html`:

{% raw %}
```liquid
{% assign en_posts = site.posts | where_exp: "post", "post.path contains '_posts/en/'" %}
```
{% endraw %}

---

#### 3. Simplify the JavaScript

Since the language filtering is now handled at build time, you can simplify the JavaScript to only handle sorting (e.g., by date or author picks) and navigation between language pages. Here’s an updated version of the JavaScript:

{% raw %}
```javascript
window.addEventListener('load', function () {
  const sortSelect = document.getElementById('sort-select');
  const postNumber = document.getElementById('post-number');
  const postList = document.querySelector('.post-list');

  function updatePosts() {
    const selectedValue = sortSelect.value;
    const [sortOption, langFilter] = selectedValue.split('|');

    // If the selected language doesn't match the current page, redirect
    const currentLang = '{{ page.lang }}';
    if (langFilter !== currentLang && langFilter !== 'all' && langFilter !== 'original' && sortOption !== 'author-picks') {
      window.location.href = `/${langFilter}/?sort=${selectedValue}`;
      return;
    }

    // Grab all posts
    const posts = document.querySelectorAll('.post-list li.post-item');
    let processedPosts = [];

    if (sortOption === 'author-picks') {
      // Filter posts with 'data-top' > 0
      processedPosts = Array.from(posts)
        .filter(post => parseInt(post.dataset.top || 0, 10) > 0)
        .map(post => ({ element: post }));
    } else if (sortOption === 'date-desc' && langFilter === 'original') {
      // Filter original (non-translated, non-generated) posts
      processedPosts = Array.from(posts)
        .filter(post => post.dataset.translated === 'false' && post.dataset.generated === 'false')
        .map(post => {
          const dateElement = post.querySelector('.date');
          const dateStr = dateElement ? dateElement.textContent.trim().replace(/\./g, '-') : null;
          return { element: post, date: dateStr ? new Date(dateStr) : null };
        })
        .filter(item => item.date)
        .sort((a, b) => b.date - a.date);
    } else {
      // Sort by date descending
      processedPosts = Array.from(posts)
        .map(post => {
          const dateElement = post.querySelector('.date');
          const dateStr = dateElement ? dateElement.textContent.trim().replace(/\./g, '-') : null;
          const aElement = post.querySelector('a');
          const href = aElement ? aElement.getAttribute('href') : '';
          const fileName = href ? href.split('/').pop() : '';
          return { element: post, date: dateStr ? new Date(dateStr) : null, fileName };
        })
        .filter(item => item.date)
        .sort((a, b) => {
          const dateComparison = b.date - a.date;
          return dateComparison !== 0 ? dateComparison : a.fileName.localeCompare(b.fileName);
        });
    }

    // Clear existing list
    postList.innerHTML = '';

    // Append processed posts or show a message
    if (processedPosts.length > 0) {
      processedPosts.forEach(item => {
        if (item.element) {
          postList.appendChild(item.element);
        }
      });
    } else {
      const noPostsMessage = document.createElement('li');
      noPostsMessage.className = 'list-group-item post-item';
      noPostsMessage.textContent = 'No posts available. Please refresh the page.';
      postList.appendChild(noPostsMessage);
    }

    // Update the post count
    const translatedCount = processedPosts.filter(item => item.element && item.element.dataset.translated === 'true').length;
    postNumber.innerHTML = `${processedPosts.length} posts (${translatedCount} by <a href="https://mistral.ai">AI</a>)`;

    // Show the list
    postList.style.display = 'block';
  }

  // Restore from localStorage or set default
  const savedSort = localStorage.getItem('sortOption');
  if (savedSort) {
    sortSelect.value = savedSort;
  } else {
    sortSelect.value = 'date-desc|{{ page.lang }}';
  }

  updatePosts();

  // Event listener for dropdown changes
  sortSelect.addEventListener('change', function () {
    localStorage.setItem('sortOption', sortSelect.value);
    updatePosts();
  });
});
```
{% endraw %}

Key changes:
- The script checks if the selected language matches the current page’s language (`{{ page.lang }}`). If not, it redirects to the appropriate language page (e.g., `/zh/` for Chinese).
- The language filtering is no longer needed since the posts are prefiltered by the Liquid template.

---

#### 4. Configure Permalinks and Navigation

Ensure that each language-specific page has a unique permalink in its front matter (e.g., `permalink: /en/` for `index-en.html`). This allows users to navigate to `/en/`, `/zh/`, etc., directly.

You may also want to update your site’s navigation to include links to these language-specific pages. For example, in your layout or header:

```html
<nav>
  <a href="/en/">English</a>
  <a href="/zh/">中文</a>
  <a href="/ja/">日本語</a>
  <!-- Add other languages -->
</nav>
```

---

#### 5. Handle the "All" and "Original" Filters

For the "All" and "Original" options in the dropdown:
- **All**: You can create an `index.html` that includes all posts (similar to your original setup) or redirect to one of the language-specific pages.
- **Original**: You can create an `index-original.html` that filters posts with `translated: false` and `generated: false`:

{% raw %}
```html
---
layout: page
lang: original
permalink: /original/
---
<div class="sort-container">
  <span id="post-number" class="post-number">
    {% assign original_posts = site.posts | where: "translated", false | where: "generated", false %}
    {{ original_posts.size }} posts
    (0 by <a href="https://mistral.ai">AI</a>)
  </span>
  <!-- Same sort-select -->
</div>

<ul class="post-list">
  {% if original_posts.size > 0 %}
    {% for post in original_posts %}
      <li class="list-group-item post-item lang-{{ post.lang }}" data-top="{{ post.top | default: 0 }}" data-translated="false" data-generated="false">
        <a href="{{ post.url }}">
          <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
          <span class="type">{% if post.image %}image{% else %}text{% endif %}</span>
          <span class="title">{{ post.title }}</span>
        </a>
      </li>
    {% endfor %}
  {% else %}
    <li class="list-group-item post-item">No posts available.</li>
  {% endif %}
</ul>

<!-- Same footer -->
```
{% endraw %}

---

#### 6. Benefits of Precompiling

- **Performance**: Filtering posts at build time reduces client-side JavaScript processing, making the site faster, especially for users with slower devices or connections.
- **SEO**: Search engines can better index language-specific pages (`/en/`, `/zh/`, etc.), improving discoverability.
- **Simpler JavaScript**: The JavaScript only needs to handle sorting and navigation, not language filtering.
- **Reliability**: Precompiled pages avoid client-side bugs (e.g., the "Known bug pending fix" message in your original code).

---

#### 7. Considerations

- **Build Time**: Precompiling multiple index pages increases build time, especially if you have many posts or languages. However, this is usually negligible unless you have thousands of posts.
- **Maintenance**: You’ll need to maintain multiple index files (`index-en.html`, `index-zh.html`, etc.). To reduce duplication, you can use Jekyll includes or layouts to share common code.
- **Dynamic Sorting**: The JavaScript still handles sorting (e.g., author picks, date-desc), but you could precompute sorted versions of each page if you want fully static output (though this would create more files, e.g., `index-en-picks.html`).

---

#### 8. Example Directory Structure

Your Jekyll project might look like this:

```
├── _posts/
│   ├── en/
│   │   ├── 2025-08-01-post1.md
│   │   ├── 2025-08-02-post2.md
│   ├── zh/
│   │   ├── 2025-08-01-post1-zh.md
│   ├── ja/
│   └── ...
├── _layouts/
│   ├── page.html
├── index-en.html
├── index-zh.html
├── index-ja.html
├── index-original.html
├── _includes/
│   ├── header.html
│   ├── footer.html
├── assets/
│   ├── js/
│   │   ├── sort.js
```

---

#### 9. Testing and Deployment

- Test locally with `jekyll serve` to ensure each language page (`/en/`, `/zh/`, etc.) displays the correct posts.
- Verify that the dropdown navigation redirects correctly between language pages.
- Deploy to your hosting platform (e.g., GitHub Pages) and check that permalinks work as expected.

---

### References
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Mistral AI](https://mistral.ai)

If you have further questions or need help with specific parts of the implementation, let me know!
