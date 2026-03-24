const translations = {
  'en': 'Translated',
  'zh': '翻译'
};

window.addEventListener('load', function () {
  const postNumber = document.getElementById('post-number');
  if (!postNumber) return;

  const currentPath = window.location.pathname;
  let currentLang = 'en';

  const langMatch = currentPath.match(/-(zh|ja|es|hi|fr|de|ar|hant)\.html$/);
  if (langMatch) {
    currentLang = langMatch[1];
  }

  const posts = document.querySelectorAll('.post-list li.post-item');
  const translatedCount = Array.from(posts).filter(post => post.dataset.translated === 'true').length;
  const translatedText = translations[currentLang] || translations['en'];
  const type = postNumber.dataset.type || (currentPath.includes('/notes') ? 'notes' : 'posts');
  postNumber.innerHTML = `${posts.length} ${type} (${translatedCount} ${translatedText} by <a href="https://openrouter.ai">AI</a>)`;
});
