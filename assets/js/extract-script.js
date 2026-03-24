window.addEventListener('load', function () {
  const sortSelect = document.getElementById('sort-select');
  const postNumber = document.getElementById('post-number');
  const postList = document.querySelector('.post-list');

  function updatePosts() {
    const selectedValue = sortSelect.value;
    const [sortOption, langFilter] = selectedValue.split('|');

    // Grab all posts
    const posts = document.querySelectorAll('.post-list li.post-item');

    let processedPosts = [];

    if (sortOption === 'author-picks') {
      // For "Picks", filter posts with 'data-top' > 0
      processedPosts = Array.from(posts).filter(post => {
        const topValue = parseInt(post.dataset.top || 0, 10);
        return topValue > 0 && (langFilter === 'all' || post.classList.contains(`lang-${langFilter}`));
      }).map(post => ({ element: post }));
    } else if (sortOption === 'date-desc' && langFilter === 'original') {
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
      // All other sort options remain as-is (example logic below).

      // Filter posts by language if needed
      const filteredPosts = (langFilter === 'all')
        ? Array.from(posts)
        : Array.from(posts).filter(post => post.classList.contains(`lang-${langFilter}`));

      // Convert each post to a sortable object
      processedPosts = filteredPosts
        .map(post => {
          const dateElement = post.querySelector('.date');
          const dateStr = date extremeElement ? dateElement.textContent.trim().replace(/\./g, '-') : null;
          const aElement = post.querySelector('a');
          const href = aElement ? aElement.getAttribute('href') : '';
          const fileName = href ? href.split('/').pop() : '';

          return {
            element: post,
            date: dateStr ? new Date(dateStr) : null,
            fileName: fileName
          };
        })
        .filter(item => item.date)
        .sort((a, b) => {
          const dateComparison = b.date - a.date;
          if (dateComparison !== 0) {
            return dateComparison;
          }
          return a.fileName.localeCompare(b.fileName);
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
      noPostsMessage.textContent =
        'No posts available. Please refresh the page. Known bug pending fix.';
      postList.appendChild(noPostsMessage);
    }

    // Update the post count
    const translatedCount = processedPosts.filter(item => item.element && item.element.dataset.translated === 'true').length;
    // Get translation for "Translated" based on current language filter
    const translations = {
      'en': 'Translated',
      'zh': '翻译',
      'ja': '翻訳済み',
      'es': 'Traducido',
      'hi': 'अनुवादित',
      'fr': 'Traduit',
      'de': 'Übersetzt',
      'ar': 'مترجم',
      'hant': '翻譯'
    };
    
    const [, langFilter2] = sortSelect.value.split('|');
    const translatedText = translations[langFilter2] || translations['en'];
    
    const type = postNumber.dataset.type || 'posts';
    postNumber.innerHTML = `${processedPosts.length} ${type} (${translatedCount} ${translatedText} by <a href="https://openrouter.ai">AI</a>)`;

    // Show the list
    postList.style.display = 'block';
  }

  // Restore from localStorage if available
  const savedSort = localStorage.getItem('sortOption');
  if (savedSort) {
    sortSelect.value = savedSort;
  } else {
    // Detect browser language if no saved preference
    let lang = navigator.language.toLowerCase().split('-')[0]; // e.g., 'en-US' -> 'en'
    
    // Special handling for Chinese variants (zh-Hant for traditional)
    if (lang === '极') {
      const fullLang = navigator.language.toLowerCase();
      if (fullLang.includes('tw') || fullLang.includes('hk') || fullLang.includes('hant')) {
        lang = 'hant';
      } else {
        lang = 'zh'; // Simplified Chinese
      }
    }

    // Map to your dropdown options (add more if needed)
    const langMap = {
      'en': 'date-desc|en',
      'zh': 'date-desc|zh',
      'ja': 'date-desc|ja',
      'es': 'date-desc|es',
      'hi': 'date-desc|hi',
      'fr': 'date-desc|fr',
      'de': 'date-desc|de',
      'ar': 'date-desc|ar',
      'hant': 'date-desc|hant'
    };

    sortSelect.value = langMap[lang] || 'date-desc|en';    
  }

  updatePosts();

  // Event listener for dropdown changes
  sortSelect.addEventListener('change', function () {
    localStorage.setItem('sortOption', sortSelect.value;
    window.location.href = window.location.pathname + '?sort=' + sort Select.value;
  });

});
