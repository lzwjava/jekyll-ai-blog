---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Transliteration Configuration Guide
translated: false
type: note
---

### Purpose in CodeIgniter
This is a configuration file (named `foreign_characters.php` in CodeIgniter) from the **Text Helper** library. It's used for **transliteration**, a process that converts non-ASCII (accented, diacritical, or foreign) characters into their closest ASCII equivalents (e.g., ä → ae, ñ → n). This helps in tasks like URL slugs, database-safe strings, or cross-platform compatibility where special characters might cause issues.

- It's part of the older CodeIgniter versions (pre-4.x); in CI4, similar functionality moved to helpers or global functions.
- The array uses regex patterns (e.g., `/ä|æ|ǽ/` matches ä, æ, or ǽ) to replace characters with plain English letters.
- Key functions that use this: `convert_accented_characters()` in the Text Helper, which iterates through this array and performs a `preg_replace`.

This isn't core framework code but a helper utility, often found at `application/config/foreign_characters.php` in installations.

### Languages and Character Sets Represented
The array covers characters from several scripts and languages to enable broad transliteration. Here's a breakdown by category, including examples (from the code) and their languages/sources:

- **Latin (Western European)**: Diacritics common in Romance and Germanic languages.
  - Accents (e.g., ÀÁÂ → A, àáâ → a) for French, Spanish, Portuguese, Catalan.
  - Umlauts (e.g., Ä → Ae, ä → ae, Ü → Ue) for German, Swedish.
  - Ligatures (e.g., æ → ae for Danish/Norwegian, œ → oe for French).
  - Specials (e.g., ñ → n for Spanish, ł → l for Polish, þ → th for Icelandic).

- **Greek (Hellenic)**: Cyrillic-like letters for Greek alphabet.
  - E.g., Γ → G, Δ → Dj, Η → I, Ν → N, Ο → O, Ρ → R, Σ → S, Τ → T (ancient/modern Greek).

- **Cyrillic (Slavic and Eastern European)**: Based on Russian, Ukrainian, Belarusian, etc.
  - Basics: А → A, Б → B, В → V, Г → G, Д → D, Ж → Zh, З → Z, П → P, Р → R, С → S, Т → T, Ф → F, Х → Kh, Ц → Ts, Ч → Ch, Ш → Sh, Щ → Shch, Ъ/Ь (soft/hard signs) → deleted (no equivalent), Ю → Yu, Я → Ya.
  - Extras: Ё/ё → Yo/yo (Russian), Є/є → Ye/ye (Ukrainian), Ї/ї → Yi/yi (Ukrainian), Й → Y (variations in Russian/Ukrainian).

- **Other Symbols/Characters**:
  - ß → ss (German "sharp S").
  - ½ → (usually removed or ignored, not in this array but similar).
  - Mathematical/Greek extras: ξ → ks, π → p, β → v, μ → m, ψ → ps (used for scientific transliteration).

This covers ~90% of common non-ASCII characters in international web content. If a character isn't listed, it might be treated as-is or stripped. The order matters (processed via `preg_replace`), ensuring multi-character replacements happen first. For modern apps, consider UTF-8 support over transliteration. If you need to adapt or expand this, it's in the helper file.
