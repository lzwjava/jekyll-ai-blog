---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1000-Hour Whisper Fine-Tuning Guide
translated: false
type: note
---

Web search is down, but I know this space well. Here's the full roadmap:


== STRATEGY: 3 APPROACHES TO 1000 HOURS ==

  1. Use existing public datasets (fastest, free)
  2. Scrape/collect your own audio (custom domain)
  3. Combine both (best real-world result)


== 1. PUBLIC DATASETS (easiest path to 1000+ hours) ==

  English:
    LibriSpeech          960h   audiobooks, clean + other
    Common Voice 17.0   ~2500h  crowdsourced, 100+ languages
    GigaSpeech          10,000h audiobooks/podcasts/YouTube
    VoxPopuli           1,800h  European Parliament speeches
    SPGISpeech          5,000h  financial earnings calls

  Chinese:
    AISHELL-1           178h    Mandarin read speech
    AISHELL-2           1000h   Mandarin read speech (free)
    WenetSpeech         10,000h Mandarin, multi-domain
    MagicData-RAMC      180h    Mandarin conversational

  Multilingual:
    Common Voice        2500h+  100+ languages
    MLS (Meta)          50,000h 8 languages from LibriVox
    VoxPopuli           1,800h  23 European languages

  Download via HuggingFace:
    pip install datasets
    from datasets import load_dataset

    # Common Voice Chinese
    ds = load_dataset("mozilla-foundation/common_voice_17_0", "zh-CN", split="train")

    # LibriSpeech
    ds = load_dataset("librispeech_asr", "clean", split="train.100")

    # AISHELL-1
    ds = load_dataset("aishell", split="train")


== 2. COLLECTING YOUR OWN AUDIO ==

  A) YouTube/Podcast scraping:
     - yt-dlp downloads audio + auto-generated subtitles
     - Subtitles = your transcription labels

       yt-dlp -x --audio-format wav \
         --write-auto-sub --sub-lang en \
         "https://youtube.com/playlist?list=..."

     - Tools: yt-whisper pipeline, tube-audio-scraper

  B) Text-to-Speech augmentation:
     - Use TTS (edge-tts, coqui-tts) to synthesize speech from text corpora
     - Add noise/reverb for robustness
     - Fast way to generate thousands of hours

       pip install edge-tts
       edge-tts --voice zh-CN-XiaoxiaoNeural \
         --text "你好世界" --write-media output.mp3

  C) Audiobook + e-book alignment:
     - LibriVox audiobooks (public domain)
     - Align with Project Gutenberg text
     - Tools: aeneas, gentle, Montreal Forced Aligner

  D) Meeting recording:
     - Record your own meetings/calls
     - Transcribe with Whisper large first, then manually correct
     - Creates domain-specific training data


== 3. DATA FORMAT (what Whisper expects) ==

  Each sample needs:
    {
      "audio": {"path": "file.wav", "array": [...], "sampling_rate": 16000},
      "text": "hello world this is a transcription",
      "language": "en"
    }

  Preprocessing:
    - Resample to 16kHz mono
    - Segment into 30-second chunks
    - Normalize audio levels

  Script to prepare dataset:

    import json, os, whisper
    from whisper.audio import load_audio

    samples = []
    for audio_file in audio_files:
        audio = load_audio(audio_file)  # 16kHz mono
        with open(audio_file.replace(".wav", ".txt")) as f:
            text = f.read().strip()
        samples.append({
            "audio": audio_file,
            "text": text,
            "language": "zh"  # or "en", etc.
        })

    with open("metadata.jsonl", "w") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")


== 4. TRAINING PIPELINE ==

  Option A: HuggingFace Transformers (recommended)

    pip install transformers datasets accelerate

    from transformers import (
        WhisperForConditionalGeneration,
        WhisperProcessor,
        WhisperTokenizer,
        Seq2SeqTrainer,
        Seq2SeqTrainingArguments
    )

    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")

    # Force decoder to Chinese + transcription
    model.generation_config.language = "zh"
    model.generation_config.task = "transcribe"

    training_args = Seq2SeqTrainingArguments(
        output_dir="./whisper-finetuned",
        per_device_train_batch_size=16,
        gradient_accumulation_steps=2,
        learning_rate=1e-5,
        warmup_steps=500,
        max_steps=5000,
        fp16=True,
        evaluation_strategy="steps",
        save_steps=500,
        logging_steps=25,
        predict_with_generate=True,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=processor.feature_extractor,
    )
    trainer.train()

  Option B: LoRA fine-tuning (saves VRAM)

    pip install peft
    from peft import LoraConfig, get_peft_model

    config = LoraConfig(
        r=32, lora_alpha=64,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05, bias="none"
    )
    model = get_peft_model(model, config)
    # Now only ~5% of params are trainable


== 5. HARDWARE REQUIREMENTS ==

  Model    Batch 16  LoRA     Full fine-tune
  tiny     2 GB      1 GB     4 GB
  base     4 GB      2 GB     8 GB
  small    8 GB      4 GB     16 GB
  medium   16 GB     8 GB     32 GB
  large    32 GB     12 GB    64 GB

  Your RTX 4070 (12 GB):
    - Full fine-tune: base or small
    - LoRA: medium or turbo
    - 1000h dataset: ~2-4 days training on base


== 6. FASTEST PATH TO 1000 HOURS ==

  For Chinese:
    1. Download WenetSpeech (10,000h, free on OpenSLR)
    2. Filter to your domain
    3. Fine-tune whisper-base with LoRA on RTX 4070
    4. ~12-24 hours training

  For English:
    1. Download GigaSpeech (10,000h, free)
    2. Or LibriSpeech (960h) + Common Voice (~2500h)
    3. Fine-tune whisper-base

  Mixed:
    1. Combine Common Voice (multilingual) + domain-specific audio
    2. Fine-tune with language tags


== 7. EVALUATION ==

    pip install jiwer
    from jiwer import wer

    # Generate predictions
    predictions = []
    references = []
    for batch in eval_dataset:
        pred = model.generate(batch["input_features"])
        predictions.append(processor.decode(pred[0]))
        references.append(batch["text"])

    error_rate = wer(references, predictions)
    print(f"WER: {error_rate:.2%}")


== QUICK START SCRIPT ==

  Here's a minimal end-to-end for Chinese:

    pip install datasets transformers accelerate peft

    # Download AISHELL-1 subset
    from datasets import load_dataset
    ds = load_dataset("aishell", split="train[:10000]")

    # Fine-tune
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    from peft import LoraConfig, get_peft_model

    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    model.generation_config.language = "zh"
    model.generation_config.task = "transcribe"

    lora_config = LoraConfig(r=32, lora_alpha=64,
        target_modules=["q_proj", "v_proj"])
    model = get_peft_model(model, lora_config)

    # ... train loop with Seq2SeqTrainer

Want me to build a complete training script for your specific use case? I'd need to know:
  - Target language (Chinese? English? Both?)
  - Domain (general? technical? meetings?)
  - Your GPU (RTX 4070 12GB or MI300X 192GB?)
