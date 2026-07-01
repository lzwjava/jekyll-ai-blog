---
audio: false
generated: true
image: false
lang: en
layout: post
title: Financial Audio Datasets for ASR
translated: false
type: note
---

Question: Are there financial audio datasets available for training/fine-tuning ASR models like Whisper?

Answer:

Yes — the financial domain (mostly earnings calls) is actually one of the better-covered niches for domain-specific ASR data, because S&P Global (Kensho) and academic groups have released large, freely-licensed corpora specifically to push Whisper-class models. Here's the landscape, ranked by what you'd actually reach for:

**1. SPGISpeech — best for fine-tuning (5,000 hrs)**
Professionally transcribed earnings calls, fully formatted (punctuation, capitalization, ITN applied), which matches Whisper's normalized-output training objective. SPGISpeech is an English speech recognition corpus composed of company earnings calls that have been manually transcribed by S&P Global, Inc., with training splits ranging from 200 hours to 5,000 hours, plus canonical validation and test splits.

```python
from datasets import load_dataset
spgi = load_dataset("kensho/spgispeech", "s", use_auth_token=True)  # "s"=small/200h, "m", "l"=5000h
```

There's now also a v2 extension aimed at speaker-tagged/multi-talker ASR: SPGISpeech 2.0 consists of 3,780 additional hours of professionally transcribed earnings calls, containing call and speaker information for each audio snippet, released free for non-commercial use.

**2. Earnings-21 / Earnings-22 — best for long-form eval, not training**
These are your held-out benchmark sets, not training corpora — small and deliberately diverse in accent/region.
- Earnings-21 is a 39-hour corpus of company earnings calls over various financial sections.
- Earnings-22 contains 125 files totalling roughly 119 hours of English-language earnings calls from global countries, spanning speakers from seven different language regions and 27 unique countries, providing full audio, transcripts, and metadata such as ticker symbol and headquarters country. It's intended as a test-only split — good for measuring WER under accent stress, exactly the kind of long-form/noisy-domain case where Whisper-v3 still leads: Whisper-v3 consistently achieves the lowest WER, in the range of approximately 12%-16% on long financial audio ASR, with GPT-4o-audio as second-best.

```python
earnings22 = load_dataset("distil-whisper/earnings22", split="test")
```

There's a newer variant worth knowing about too: Contextual Earnings-22 pairs each audio segment with realistic custom-vocabulary contexts, manually reviewing and correcting transcripts to reduce artifacts, and evaluates keyword-boosting/prompting baselines against STT APIs including Whisper. Useful if you're testing biasing/contextual-vocab tricks (ticker names, exec names) rather than raw fine-tuning.

**3. MAEC — multimodal (text+audio), good if you want alignment beyond ASR**
MAEC is a large-scale multimodal, text-audio paired earnings-call dataset based on S&P 1500 companies, more than six times larger than previously available datasets, with attention paid to the text-audio alignment process. This is more useful if your downstream goal is stock-movement prediction from prosody/audio features rather than pure transcription — closer to your interest in agent pipelines over raw ASR.

**4. Not public: proprietary industrial-scale sets**
If you want a sense of scale used in production streaming-Whisper fine-tunes: one paper used randomly sampled earnings call data from before 2023 as training, yielding 5,800 hours of audio with transcriptions segmented into 5-20 second clips, holding out 83 calls from after 2023 (10 hours) as the leak-free test set — noting Earnings-22 alone was too small for their training needs. That's the realistic bar if you want to actually move WER meaningfully below SPGISpeech-trained baselines — SPGISpeech's 5,000 hrs is close but you'd want to combine it with your own scraped/aligned earnings-call audio (Seeking Alpha, Motley Fool transcripts + YouTube/investor-relations audio) to hit that scale.

**5. Benchmark to sanity-check against**
If you fine-tune, don't just eyeball WER — use FinAudio as your eval harness since it already normalizes multiple financial ASR/summarization tasks: FINAUDIO establishes over 430 hours of purposefully organized financial audio addressing domain-specific evaluation needs, constructing MDRM-test and SPGISpeech-test for short ASR, and Earnings-21/Earnings-22 test sets for long ASR, plus a new summarization task.

**Practical fine-tuning path for your setup (RTX 4070 / MI300X):**

```python
# 1. Pull SPGISpeech small split (~200h) — fits comfortably for LoRA fine-tune on 4070
from datasets import load_dataset, Audio
ds = load_dataset("kensho/spgispeech", "s", use_auth_token=True)
ds = ds.cast_column("audio", Audio(sampling_rate=16000))

# 2. Whisper fine-tune scaffold (standard HF recipe, swap in PEFT/LoRA for 4070 memory budget)
from transformers import WhisperForConditionalGeneration, WhisperProcessor
processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en")
# apply LoRA via peft.get_peft_model(...) before Trainer, given your 12GB VRAM constraint

# 3. Eval on Earnings-22 (held out, real-world accented) for honest WER, not train-set overlap
eval_ds = load_dataset("distil-whisper/earnings22", split="test")
```

Given your MI300X access (192GB HBM3), full fine-tuning (not LoRA) on the full 5,000-hour SPGISpeech "l" split is actually feasible in one long run — that's a more interesting experiment than the small-scale nanoGPT work if you want a project that's directly relevant to your bank's domain (financial NLP/ASR) while compounding toward your AI-native tooling thesis. Worth noting for your notes-en KB — I don't see an existing entry there on ASR fine-tuning or Whisper internals; this could be a good one to start.

References:

- [FinAudio: A Benchmark for Audio Large Language Models in Financial Applications](https://arxiv.org/html/2503.20990v2)
- [Adapting Whisper for Streaming Speech Recognition via Two-Pass Decoding](https://arxiv.org/pdf/2506.12154)
- [SPGISpeech 2.0: Transcribed multi-speaker financial audio](https://arxiv.org/html/2508.05554v1)
- [distil-whisper/earnings22 · Datasets at Hugging Face](https://huggingface.co/datasets/distil-whisper/earnings22)
- [A Complete Guide to Audio Datasets](https://huggingface.co/blog/audio-datasets)
- [Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling](https://arxiv.org/pdf/2311.00430)
- [MAEC: A Multimodal Aligned Earnings Conference Call Dataset](https://dl.acm.org/doi/10.1145/3340531.3412879)
- [ESB: A Benchmark For Multi-Domain End-to-End Speech Recognition](https://arxiv.org/pdf/2210.13352)
- [Contextual Earnings-22: A Speech Recognition Benchmark with Custom Vocabulary in the Wild](https://arxiv.org/html/2604.07354)
