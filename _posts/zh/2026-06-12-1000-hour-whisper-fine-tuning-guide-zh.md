---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1000小时Whisper微调指南
translated: true
type: note
---

网络搜索已关闭，但我对这个领域非常熟悉。以下是完整路线图：


== 策略：达成1000小时的三种方法 ==

  1. 使用现有公开数据集（最快、免费）
  2. 自行抓取/收集音频（自定义领域）
  3. 结合以上两种方法（最佳实际效果）


== 1. 公开数据集（获取1000+小时的最简单途径） ==

  英语：
    LibriSpeech          960小时   有声书，纯净+其他
    Common Voice 17.0   ~2500小时  众包，100+种语言
    GigaSpeech          10,000小时 有声书/播客/YouTube
    VoxPopuli           1,800小时  欧洲议会演讲
    SPGISpeech          5,000小时  金融财报电话会议

  中文：
    AISHELL-1           178小时    普通话朗读语音
    AISHELL-2           1000小时   普通话朗读语音（免费）
    WenetSpeech         10,000小时 普通话，多领域
    MagicData-RAMC      180小时    普通话对话

  多语言：
    Common Voice        2500小时+  100+种语言
    MLS (Meta)          50,000小时 来自LibriVox的8种语言
    VoxPopuli           1,800小时  23种欧洲语言

  通过HuggingFace下载：
    pip install datasets
    from datasets import load_dataset

    # Common Voice 中文
    ds = load_dataset("mozilla-foundation/common_voice_17_0", "zh-CN", split="train")

    # LibriSpeech
    ds = load_dataset("librispeech_asr", "clean", split="train.100")

    # AISHELL-1
    ds = load_dataset("aishell", split="train")


== 2. 收集自己的音频 ==

  A) YouTube/播客抓取：
     - yt-dlp 下载音频 + 自动生成字幕
     - 字幕 = 你的转录标签

       yt-dlp -x --audio-format wav \
         --write-auto-sub --sub-lang en \
         "https://youtube.com/playlist?list=..."

     - 工具：yt-whisper pipeline, tube-audio-scraper

  B) 文本转语音增强：
     - 使用TTS（edge-tts, coqui-tts）从文本语料库合成语音
     - 添加噪声/混响以增强鲁棒性
     - 快速生成数千小时数据的方法

       pip install edge-tts
       edge-tts --voice zh-CN-XiaoxiaoNeural \
         --text "你好世界" --write-media output.mp3

  C) 有声书 + 电子书对齐：
     - LibriVox有声书（公共领域）
     - 与Project Gutenberg文本对齐
     - 工具：aeneas, gentle, Montreal Forced Aligner

  D) 会议录音：
     - 录制自己的会议/通话
     - 先用Whisper large转录，然后手动修正
     - 创建特定领域的训练数据


== 3. 数据格式（Whisper期望的格式） ==

  每个样本需要：
    {
      "audio": {"path": "file.wav", "array": [...], "sampling_rate": 16000},
      "text": "hello world this is a transcription",
      "language": "en"
    }

  预处理：
    - 重采样为16kHz单声道
    - 分割成30秒片段
    - 标准化音频电平

  准备数据集的脚本：

    import json, os, whisper
    from whisper.audio import load_audio

    samples = []
    for audio_file in audio_files:
        audio = load_audio(audio_file)  # 16kHz单声道
        with open(audio_file.replace(".wav", ".txt")) as f:
            text = f.read().strip()
        samples.append({
            "audio": audio_file,
            "text": text,
            "language": "zh"  # 或 "en" 等
        })

    with open("metadata.jsonl", "w") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")


== 4. 训练流程 ==

  选项A：HuggingFace Transformers（推荐）

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

    # 强制解码器使用中文 + 转录
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

  选项B：LoRA微调（节省显存）

    pip install peft
    from peft import LoraConfig, get_peft_model

    config = LoraConfig(
        r=32, lora_alpha=64,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05, bias="none"
    )
    model = get_peft_model(model, config)
    # 现在只有约5%的参数可训练


== 5. 硬件需求 ==

  模型    Batch 16  LoRA     全量微调
  tiny     2 GB      1 GB     4 GB
  base     4 GB      2 GB     8 GB
  small    8 GB      4 GB     16 GB
  medium   16 GB     8 GB     32 GB
  large    32 GB     12 GB    64 GB

  你的RTX 4070（12 GB）：
    - 全量微调：base或small
    - LoRA：medium或turbo
    - 1000小时数据集：base模型训练约2-4天


== 6. 达成1000小时的最快路径 ==

  中文：
    1. 下载WenetSpeech（10,000小时，OpenSLR免费）
    2. 筛选到你的领域
    3. 在RTX 4070上用LoRA微调whisper-base
    4. 约12-24小时训练

  英语：
    1. 下载GigaSpeech（10,000小时，免费）
    2. 或LibriSpeech（960小时）+ Common Voice（约2500小时）
    3. 微调whisper-base

  混合：
    1. 结合Common Voice（多语言）+ 特定领域音频
    2. 使用语言标签进行微调


== 7. 评估 ==

    pip install jiwer
    from jiwer import wer

    # 生成预测
    predictions = []
    references = []
    for batch in eval_dataset:
        pred = model.generate(batch["input_features"])
        predictions.append(processor.decode(pred[0]))
        references.append(batch["text"])

    error_rate = wer(references, predictions)
    print(f"WER: {error_rate:.2%}")


== 快速启动脚本 ==

  以下是一个针对中文的最小化端到端示例：

    pip install datasets transformers accelerate peft

    # 下载AISHELL-1子集
    from datasets import load_dataset
    ds = load_dataset("aishell", split="train[:10000]")

    # 微调
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    from peft import LoraConfig, get_peft_model

    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    model.generation_config.language = "zh"
    model.generation_config.task = "transcribe"

    lora_config = LoraConfig(r=32, lora_alpha=64,
        target_modules=["q_proj", "v_proj"])
    model = get_peft_model(model, lora_config)

    # ... 使用Seq2SeqTrainer的训练循环

需要我为你构建一个完整的训练脚本吗？我需要了解以下信息：
  - 目标语言（中文？英文？两者都有？）
  - 领域（通用？技术？会议？）
  - 你的GPU（RTX 4070 12GB 还是 MI300X 192GB？）