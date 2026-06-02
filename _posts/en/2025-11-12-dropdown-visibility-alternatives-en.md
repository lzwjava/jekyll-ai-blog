---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Dropdown Visibility and Alternatives
translated: false
type: note
---

In the provided HTML snippet, you're using `<select>` elements, which by default render as dropdown menus. This means users can only see the currently selected option at a glance—other options are hidden until the dropdown is clicked or expanded (via keyboard/mouse interaction). This is standard behavior for `<select>` in HTML, as it's designed for compact selection from a list without cluttering the UI.

HTML doesn't have a built-in "switch" element specifically for toggling visibility of options in a `<select>`. However, there are a few ways to achieve what you're describing (making all options visible without a dropdown, or providing a toggle to show/hide them). I'll outline the pros/cons and code examples below. These approaches use native HTML/CSS where possible, with optional JavaScript for interactivity. Since your code appears to be part of a Jekyll site (based on the Liquid templating), these should integrate easily.

### 1. **Use Radio Buttons Instead of `<select>` (Always Visible Options)**

- **Why?** Radio buttons (`<input type="radio">`) display all options inline or in a list, making them fully visible without any interaction. This is great for small lists (like your type-select with 2 options) but can get crowded for longer ones (like your language-sort with 9 options).
- **Pros:** No JS needed; accessible; users see everything immediately.
- **Cons:** Takes more space; requires JS to handle the "selection" logic if you need to trigger actions (e.g., sorting/filtering posts).
- **Example Code:**
     Replace your `<select>` with a group of radio buttons. Wrap them in a `<fieldset>` for semantics/accessibility.

{% raw %}
     ```html
     <div class="sort-container">
       <!-- Type selection as radios -->
       <fieldset>
         <legend>Type</legend>
         <label>
           <input type="radio" name="type" value="posts" checked> Posts
         </label>
         <label>
           <input type="radio" name="type" value="notes"> Notes
         </label>
       </fieldset>

       <!-- Language sort as radios -->
       <fieldset>
         <legend>Sort by Language</legend>
         <label>
           <input type="radio" name="sort" value="en" checked> English
         </label>
         <label>
           <input type="radio" name="sort" value="zh"> 中文
         </label>
         <label>
           <input type="radio" name="sort" value="ja"> 日本語
         </label>
         <!-- Add more labels for es, hi, fr, de, ar, hant -->
       </fieldset>

       <div>
         <span id="post-number" class="post-number">
           {{ site[type].size }} {{ type }}
           ({{ site[type].size | divided_by: 7 | times: 6 }} Translated by <a href="https://openrouter.ai">AI</a>)
         </span>
       </div>
     </div>
     ```
{% endraw %}

     - Add CSS for styling (e.g., to make them look like buttons):
       ```css
       fieldset {
         border: none; /* Remove default border */
         display: flex;
         gap: 10px;
       }
       label {
         background: #f0f0f0;
         padding: 5px 10px;
         border-radius: 5px;
         cursor: pointer;
       }
       input[type="radio"] {
         appearance: none; /* Hide default radio circle */
       }
       input[type="radio"]:checked + span { /* If using <span> inside label for text */
         background: #007bff;
         color: white;
       }
       ```
     - For functionality: Use JS to listen for changes (e.g., `addEventListener('change')`) and update the UI or trigger a sort.

### 2. **Use Buttons or Divs for Clickable Options (Custom "Button Group")**

- **Why?** If you want a more button-like interface, use `<button>` or `<div>` elements styled as buttons. This shows all options visibly and allows custom toggling.
- **Pros:** Flexible styling; can mimic tabs or pills; easy to make responsive.
- **Cons:** Requires JS to manage active states and actions; not as semantically correct as form elements (use ARIA attributes for accessibility).
- **Example Code:**
{% raw %}

     ```html
     <div class="sort-container">
       <!-- Type as button group -->
       <div class="button-group" role="group" aria-label="Type selection">
         <button data-type="posts" class="active">Posts</button>
         <button data-type="notes">Notes</button>
       </div>

       <!-- Language as button group -->
       <div class="button-group" role="group" aria-label="Language selection">
         <button data-sort="en" class="active">English</button>
         <button data-sort="zh">中文</button>
         <button data-sort="ja">日本語</button>
         <!-- Add more buttons for other languages -->
       </div>

       <div>
         <span id="post-number" class="post-number">
           {{ site[type].size }} {{ type }}
           ({{ site[type].size | divided_by: 7 | times: 6 }} Translated by <a href="https://openrouter.ai">AI</a>)
         </span>
       </div>
     </div>
     ```

{% endraw %}

     - CSS for button styling:
       ```css
       .button-group {
         display: flex;
         gap: 5px;
         flex-wrap: wrap; /* For long lists */
       }
       button {
         padding: 5px 10px;
         border: 1px solid #ccc;
         border-radius: 5px;
         cursor: pointer;
       }
       button.active {
         background: #007bff;
         color: white;
       }
       ```
     - JS to handle clicks (add this in a `<script>` tag or external file):
       ```javascript
       document.querySelectorAll('.button-group button').forEach(button => {
         button.addEventListener('click', function() {
           // Remove active from siblings
           this.parentNode.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
           this.classList.add('active');
           // Trigger your sort logic here, e.g., update post-number or filter content
           console.log('Selected:', this.dataset.type || this.dataset.sort);
         });
       });
       ```

### 3. **Add a Toggle/Switch to Expand Options (Hybrid Approach)**

- **Why?** If you want to keep the compact `<select>` but allow users to "switch" to a view showing all options, use a checkbox styled as a toggle switch to show/hide an expanded list.
- **Pros:** Keeps default compact; native HTML for toggle.
- **Cons:** Requires CSS/JS; adds complexity.
- **Example:** Use `<input type="checkbox">` for the switch, and toggle visibility of a div with all options listed.

     ```html
     <div class="sort-container">
       <!-- Your original selects here -->

       <!-- Toggle switch -->
       <label class="switch">
         <input type="checkbox" id="show-all-toggle">
         <span>Show All Options</span>
       </label>

       <!-- Hidden expanded view -->
       <div id="expanded-options" style="display: none;">
         <!-- List all type and sort options as plain text or buttons -->
         <ul>
           <li>Posts</li>
           <li>Notes</li>
           <li>English</li>
           <li>中文</li>
           <!-- etc. -->
         </ul>
       </div>

       <!-- Your post-number span -->
     </div>
     ```

  - CSS for switch:

       ```css
       .switch input {
         opacity: 0;
         width: 0;
         height: 0;
       }
       .switch span {
         /* Style as a toggle slider */
         position: relative;
         display: inline-block;
         width: 40px;
         height: 20px;
         background: #ccc;
         border-radius: 20px;
         transition: background 0.3s;
       }
       .switch input:checked + span {
         background: #007bff;
       }
       /* Add a slider knob with ::before or ::after */
       ```

  - JS to toggle:

       ```javascript
       document.getElementById('show-all-toggle').addEventListener('change', function() {
         document.getElementById('expanded-options').style.display = this.checked ? 'block' : 'none';
       });
       ```

### Recommendations

- For your **type-select** (only 2 options), radio buttons or buttons work well and keep things simple.
- For **sort-select** (9 languages), buttons in a group are fine if space allows; otherwise, stick with `<select>` and add a tooltip or label explaining it.
- Test for accessibility (e.g., using screen readers) and mobile responsiveness.
- If this is for a dynamic site, integrate with your existing JS to update the `post-number` based on selections.

If this doesn't match what you meant by "switch," or if you share more context (e.g., what the selects do), I can refine this!
