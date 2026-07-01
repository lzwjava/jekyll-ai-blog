---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Smiley Helper Configuration
translated: false
type: note
---

### Overview

This is a PHP configuration file from the CodeIgniter web framework, specifically for its **emoticons/smileys helper**. CodeIgniter is a PHP MVC framework for building web apps. This file defines a set of smiley/emoticon mappings used by the framework's `smiley_helper` to automatically replace text-based emoticons (like `:-)`) with HTML `<img>` tags that display corresponding GIF images.

The file ensures direct access is blocked via `defined('BASEPATH') OR exit('No direct script access allowed');`, a security measure in CodeIgniter to prevent unauthorized direct script execution.

### Key Components

- **Purpose**: Converts plain text emoticons in user-generated content (e.g., forum posts or comments) into visual images for a better user experience.
- **Data Structure**: `$smileys` is a PHP associative array with formal structure:

  ```
  $smileys = array(
      'smiley_code' => array('image_file', 'width', 'height', 'alt_text'),
      // ...
  );
  ```

  - **smiley_code**: The text pattern to match (e.g., `:-)`, `:lol:`, `>:(`).
  - **image_file**: Name of the GIF image in the smiley directory (defaults to `application/views/smileys/` in CodeIgniter).
  - **width/height**: Dimensions in pixels for the `<img>` tag (all are `'19'` here, indicating 19x19px GIFs).
  - **alt_text**: Alternative text for accessibility/screen readers, describing the emotion.

- **Usage in CodeIgniter**: Load the helper with `$this->load->helper('smiley');`, then call functions like `parse_smileys($text)` on strings containing emoticon codes. This replaces codes with `<img>` tags, e.g.:
  - Input: `I'm happy :)`
    Output: `I'm happy <img src="http://example.com/smileys/smile.gif" width="19" height="19" alt="smile">`

### Breakdown of Entries

The array includes 40+ mappings grouped by emotion type. Most images are 19x19px GIFs. Here's a summarized view (with examples):

| Smiley Code(s) | Image | Alt Text | Notes |
| --------------- | ------- | ---------- | ------- |
| `:-)`, `:)` | grin.gif, smile.gif | grin, smile | Positive grins and smiles. |
| `:lol:`, `:cheese:` | lol.gif, cheese.gif | LOL, cheese | Laughing/thumbs up, cheesy grin. |
| `;-)`, `;)` | wink.gif | wink | Winking. |
| `:smirk:`, `:roll:` | smirk.gif, rolleyes.gif | smirk, rolleyes | Sarcasm/sage nodding. |
| `:-S`, `:wow:`, `:bug:` | confused.gif, surprise.gif, bigsurprise.gif | confused, surprised, big surprise | Confusion/surprise. |
| `:-P`, `%-P`, `;-P`, `:P` | tongue_laugh.gif, etc. | tongue laugh, etc. | Tongue-out variants (laughing, wink, raspberry). |
| `:blank:`, `:long:`, `:ohh:`, `:grrr:`, `:gulp:`, `8-/` | Various | blank stare, long face, ohh, grrr, gulp, oh oh | Neutral or annoyed faces. |
| `:down:`, `:red:`, `:sick:`, `:shut:` | Various | downer, red face, sick, shut eye | Sad, embarrassed, sick. |
| `:-/`, `>:(` (`:mad:`), `>:-(` (`:angry:`) | hmm.gif, mad.gif, angry.gif | hmmm, mad, angry | Confused, mad, angry. |
| `:zip:`, `:kiss:` | zip.gif, kiss.gif | zipper, kiss | Zip mouth kiss. |
| `:ahhh:`, `:coolsmile:`, `-:coolsmirk:`, `:coolgrin:`, `:coolhmm:`, `:coolmad:`, `:coolcheese:` | shock.gif, shade_smile.gif, etc. | shock, cool smile, cool smirk, cool grin, cool hmm, cool mad, cool cheese | Shocked or "cool"/sunglass variants. |
| `:vampire:`, `:snake:` | vampire.gif, snake.gif | vampire, snake | Themed emoticons. |
| `:exclaim:`, `:question:` | exclaim.gif, question.gif | exclaim, question | Punctuation equivalents (!, ?). |

### Extension and Customization

- **Adding Smileys**: Append new entries, e.g., `':fire:' => array('fire.gif', '19', '19', 'fire');`.
- **Changing Images**: Update file names if replacing GIFs with PNGs/JPGs (adjust width/height accordingly).
- **Directory**: Ensure images exist in CodeIgniter's smiley path.
- **Limitations**: All images here are the same size; real implementations might vary. This array only defines mappings—replacement logic is in the helper itself.

If you have a specific question about customizing or using this in CodeIgniter, provide more details!
