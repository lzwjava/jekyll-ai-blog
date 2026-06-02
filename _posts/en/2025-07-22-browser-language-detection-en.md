---
audio: false
generated: true
lang: en
layout: post
title: Detect User Language Preference
translated: false
type: note
---

### Detecting User's Country or Language Preference

Since your Jekyll blog is static (generated HTML/JS), you can't do server-side detection easily without integrating with a hosting platform that supports it (e.g., Netlify functions or GitHub Pages with limitations). The best approach is client-side JavaScript detection on page load. You have two main options:

1. **Browser Language Preference** (Recommended for your use case): This detects the user's preferred language from their browser settings (via `navigator.language` or `navigator.languages`). It's fast, doesn't require external APIs, respects user privacy (no IP sharing), and directly ties to language rather than country. Countries often have multiple languages (e.g., India uses English widely alongside Hindi), so this is more accurate for auto-setting the dropdown.

2. **IP-Based Country Detection**: This uses a free geolocation API to get the country from the user's IP address, then maps it to a language. It's useful if you specifically need country info (e.g., for analytics), but it requires an external fetch, may have privacy implications, and isn't always precise (VPNs, proxies). Mapping country to language is approximate.

Your goal seems to be auto-selecting the language in the `<select id="sort-select">` dropdown (e.g., 'date-desc|en' for English). I'll provide code for both methods, which you can add inside your `<script>` tag, right after `const sortSelect = document.getElementById('sort-select');`.

Prioritize checking `localStorage` (as your code already does), then fall back to detection if no saved preference exists.

#### Option 1: Using Browser Language (Simpler and Preferred)
Add this code snippet. It checks the primary language code from `navigator.language` (e.g., 'en-US' -> 'en', 'zh-CN' -> 'zh') and maps it to your dropdown values. Defaults to English if no match.

```javascript
// Inside window.addEventListener('load', function () { ... });

// After const sortSelect = ...;

// Restore from localStorage if available
const savedSort = localStorage.getItem('sortOption');
if (savedSort) {
  sortSelect.value = savedSort;
} else {
  // Detect browser language if no saved preference
  let lang = navigator.language.toLowerCase().split('-')[0]; // e.g., 'en-US' -> 'en'

  // Special handling for Chinese variants (zh-Hant for traditional)
  if (lang === 'zh') {
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

  sortSelect.value = langMap[lang] || 'date-desc|en'; // Default to English
}

updatePosts();
```

This runs synchronously on load, so no delays. Test it by changing your browser language settings (e.g., in Chrome: Settings > Languages).

#### Option 2: Using IP-Based Country Detection
This requires an async fetch to a free API. I recommend `country.is` as it's simple and returns just the country code (e.g., {country: 'US'}). It's free, no API key needed, and open-source.

Add this code. Note: It's async, so we use `await` and wrap in an async function to avoid blocking the UI. If the fetch fails (e.g., ad-blockers), it defaults to English.

```javascript
// Inside window.addEventListener('load', async function () { ... });  // Make the load handler async

// After const sortSelect = ...;

// Restore from localStorage if available
const savedSort = localStorage.getItem('sortOption');
if (savedSort) {
  sortSelect.value = savedSort;
  updatePosts();
} else {
  try {
    // Fetch country code
    const response = await fetch('https://country.is/');
    const data = await response.json();
    const country = data.country.toUpperCase(); // e.g., 'US'

    // Map country codes to your languages (ISO 3166-1 alpha-2 codes)
    // This is approximate; expand as needed (e.g., multiple countries per language)
    const countryLangMap = {
      'US': 'date-desc|en',  // USA -> English
      'GB': 'date-desc|en',  // UK -> English
      'CN': 'date-desc|zh',  // China -> Simplified Chinese
      'TW': 'date-desc|hant', // Taiwan -> Traditional Chinese
      'HK': 'date-desc|hant', // Hong Kong -> Traditional Chinese
      'JP': 'date-desc|ja',  // Japan -> Japanese
      'ES': 'date-desc|es',  // Spain -> Spanish
      'MX': 'date-desc|es',  // Mexico -> Spanish (example for Latin America)
      'IN': 'date-desc|hi',  // India -> Hindi
      'FR': 'date-desc|fr',  // France -> French
      'DE': 'date-desc|de',  // Germany -> German
      'SA': 'date-desc|ar',  // Saudi Arabia -> Arabic
      'AE': 'date-desc|ar'   // UAE -> Arabic
    };

    sortSelect.value = countryLangMap[country] || 'date-desc|en'; // Default to English
  } catch (error) {
    console.warn('Country detection failed:', error);
    sortSelect.value = 'date-desc|en'; // Fallback
  }

  updatePosts();
}
```

- **Notes**:
  - Update the `window.addEventListener` to `async function ()` as shown.
  - For privacy: Inform users if needed (GDPR in EU). Some browsers/APIs may block cross-origin requests; test thoroughly.
  - If you prefer a different API, alternatives include `https://ip-api.com/json/` (returns more data like `{ "countryCode": "US" }`) or `https://ipgeolocation.io/ip_location/` (sign up for free tier).
  - Rate limits: These are generous for personal blogs, but monitor if traffic grows.

#### Additional Considerations
- **Fallback and User Override**: Users can always change the dropdown, and it saves to localStorage. You could add a "Detect Language" button if auto-detection isn't always desired.
- **Testing**: Use VPNs to simulate different countries or browser extensions to spoof languages.
- **Privacy**: Browser language is low-risk. For IP methods, consider adding a consent prompt if your audience is sensitive.
- **Combining Both**: Use browser language first, then IP if it doesn't match your supported ones (but keep it simple).
- **Jekyll-Specific**: No changes to Jekyll config needed. If you host on Netlify/Vercel, you could use edge functions for server-side detection, but that's overkill here.

If this doesn't work or you can share errors, provide more details!

[Country.is API](https://country.is/)
[IP-API Geolocation](https://ip-api.com/)
[ipgeolocation.io](https://ipgeolocation.io/)
