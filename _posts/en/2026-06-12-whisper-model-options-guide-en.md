---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whisper Model Options Guide
translated: false
type: note
---

Here's the full rundown of Whisper options:

== MODELS ==

  tiny    39M params   ~1 GB VRAM   fastest, lowest quality
  base    74M params   ~1 GB VRAM   good for prototyping
  small  244M params   ~2 GB VRAM   solid balance
  medium 769M params   ~5 GB VRAM   high quality
  large 1550M params  ~10 GB VRAM   best quality, multilingual only
  turbo  809M params   ~6 GB VRAM   best speed/quality tradeoff

Recommendation: turbo for general use, base for quick tests.

== LANGUAGES (99 total) ==

  Top-tier (WER < 10%):
    en  English        zh  Chinese        ja  Japanese
    es  Spanish        ko  Korean         fr  French
    de  German         it  Italian        pt  Portuguese
    nl  Dutch          pl  Polish         ru  Russian

  Good (WER 10-20%):
    ar  Arabic         tr  Turkish        vi  Vietnamese
    sv  Swedish        fi  Finnish        cs  Czech
    ro  Romanian       hu  Hungarian      da  Danish
    no  Norwegian      th  Thai           he  Hebrew
    el  Greek          id  Indonesian     ms  Malay

  Also supports: Afrikaans, Albanian, Amharic, Armenian, Bengali,
  Bosnian, Bulgarian, Burmese, Cantonese, Catalan, Croatian,
  Estonian, Finnish, Georgian, Gujarati, Haitian Creole, Hindi,
  Icelandic, Javanese, Kannada, Kazakh, Khmer, Lao, Latin,
  Latvian, Lithuanian, Macedonian, Mongolian, Nepali, Persian,
  Punjabi, Sanskrit, Serbian, Slovak, Slovenian, Somali,
  Sundanese, Swahili, Tagalog, Tamil, Telugu, Tibetan, Turkish,
  Ukrainian, Urdu, Uzbek, Welsh, Yiddish, Yoruba, and more.

  Language codes are ISO 639-1 (2-letter).

== KEY OPTIONS ==

  language="zh"          # Specify language (faster than auto-detect)
  task="transcribe"      # Transcribe in original language (default)
  task="translate"       # Translate any language -> English
  initial_prompt="..."   # Context hint (improves accuracy for tech terms)
  word_timestamps=True   # Word-level timing
  temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)  # Fallback temps
  device="cuda"          # Force GPU (auto-detects if not set)
  output_format="srt"    # txt, srt, vtt, json

== CLI USAGE ==

  whisper audio.mp3 --model turbo --language Chinese
  whisper audio.mp3 --task translate --output_format srt

== CHINESE-SPECIFIC TIPS ==

- Use medium or large model (small has ~15% WER, large drops to ~5%)
- Specify language="zh" explicitly
- Add initial_prompt for context:
      initial_prompt="这是一段关于技术的讨论"
- Cantonese has its own code: language="yue"
