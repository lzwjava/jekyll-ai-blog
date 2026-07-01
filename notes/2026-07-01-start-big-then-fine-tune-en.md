---
audio: false
generated: true
image: false
lang: en
layout: post
title: Start Big, Then Fine-Tune
translated: false
type: note
---

Question: When comparing a general-purpose speech/ASR model trained on a massive generic dataset versus a finance-specific model trained on a smaller-but-more-relevant financial dataset (same parameter count), does the general model still win? Isn't scale-of-data usually the deciding factor?

Answer:

Your intuition is directionally right, but the framing ("general model vs finance model, same size, which wins") is actually a false dichotomy — the empirical literature says the answer isn't "pick one," it's "start from the big general model and fine-tune it on a comparatively tiny amount of financial data." That combination beats either pure strategy.

## Why pure domain-specific training loses

If you train a finance-only ASR model from scratch at the same parameter count as Whisper (680K hours, weakly supervised, multilingual) or NVIDIA's Parakeet/Nemotron, you lose on **acoustic generalization** — different speakers, mic conditions, noise, code-switching, accents. Financial call center data alone, even at hundreds of hours, doesn't give you that acoustic diversity. A finance-only paper explicitly frames this as a **distribution shift problem across three axes**, not just vocabulary: off-the-shelf models often falter when deployed in specialized, or out-of-domain (OOD), scenarios like medical transcription, legal dictation, or financial calls. This performance drop is primarily due to distribution shifts in acoustic conditions, speaker characteristics, and, most critically, domain-specific terminology.

## Why pure general-model deployment also loses

Conversely, deploying vanilla Whisper/Parakeet on financial audio underperforms on the thing that actually matters for your product: **entity/jargon accuracy**. AWS's writeup on fine-tuning Nemotron/Parakeet for domain use is blunt about this: While pre-trained models offer strong capabilities for general speech, fine-tuning for specific domains and use cases can enhance accuracy and performance... Domain-specific terminology – Enhanced recognition of specialized vocabulary and jargon that can be rare in general training datasets. Ticker symbols, fund names, basis points, derivatives terminology — these are exactly the tokens a general model will misrecognize, and they're also exactly the tokens that matter most for downstream correctness (a transcription error on "50 bps" vs "50 basis points" vs mishearing a company name is catastrophic in a finance pipeline, unlike a generic ASR WER point).

## The evidence for "big model isn't the fix, fine-tuning is"

A police-radio ASR study (a good analog — also jargon-heavy, high-noise, out-of-domain audio) directly tested "does scaling the base model close the domain gap" and found no: the larger models sometimes but not always improve WER, suggesting that scaling up the model does not necessarily address domain differences. But fine-tuning did: After fine-tuning the NeMo Fast-Conformer CTC model on BPC data, we see a dramatic improvement in WER, suggesting that fine-tuning can bridge much of the domain difference between the pre-trained model and the police radio domain.

A German ASR continual-learning paper generalizes this into the actual rule you should operate on: it is beneficial to combine unsupervised pre-training with language- or domain-specific supervised fine-tuning — i.e., large-scale pretraining gives you the acoustic/language prior, small-scale domain fine-tuning gives you the terminology.

## Practical implication for your finance-voice-model bet

Don't train a finance ASR from scratch, and don't just ship raw Whisper/Parakeet either. The move that actually wins:

1. Take the best open general checkpoint (Whisper-large-v3-turbo, Parakeet-TDT-0.6B-v2, or Qwen2-Audio if you want the LLM-decoder route).
2. Fine-tune with **LoRA on the decoder + a financial text/vocabulary bias**, not full retraining — a Meta paper shows this is where the leverage is: high-quality domain-specific text data can still significantly enhance ASR performance on domain adaptation tasks, and they specifically target this via **soft-prompt fine-tuning** rather than full fine-tuning to preserve the general capability while injecting entity accuracy.
3. You don't need a huge financial audio corpus — hundreds of hours, even synthetic TTS-augmented financial audio, gets most of the gain, per the NVIDIA/AWS writeup on synthetic-data domain adaptation.

Minimal LoRA fine-tuning skeleton for Whisper on financial audio (runs fine on your RTX 4070, 12GB is enough for whisper-large-v3-turbo LoRA):

```python
# pip install transformers peft datasets accelerate soundfile
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model_id = "openai/whisper-large-v3-turbo"
processor = WhisperProcessor.from_pretrained(model_id)
model = WhisperForConditionalGeneration.from_pretrained(model_id, load_in_8bit=True, device_map="auto")

lora_config = LoraConfig(
    r=32, lora_alpha=64,
    target_modules=["q_proj", "v_proj"],  # attention only, cheap + effective
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # ~0.5-1% of params — this is the whole point

# then: standard Seq2SeqTrainer on (financial_audio, financial_transcript) pairs
# key move: build a custom vocab/prompt bias list of financial terms
# (ticker symbols, fund names, jargon) and inject as decoder prompt tokens
# or contextual biasing list — this is where your labeled data ROI is highest,
# not raw hours of audio.
```

Your "blue ocean" read is correct, but the actual moat isn't a bigger finance-only model — it's **entity-level accuracy + evaluation harness for financial terminology WER**, which nobody's built well yet. That's a much smaller, faster thing to ship than training a competing foundation ASR model, and it's where the DeepSeek/Kimi-Audio-class labs aren't focused (they're optimizing general benchmarks, not financial entity WER).

References:

- [Marco-ASR: Fine-Tuning Large-Scale ASR Models for Domain Adaptation (financial calls)](https://arxiv.org/html/2512.22165)
- [Effective Text Adaptation for LLM-based ASR through Soft Prompt Fine-Tuning (Meta AI)](https://arxiv.org/pdf/2412.06967)
- [Fine-tuning NVIDIA Nemotron/Parakeet Speech ASR for domain adaptation (AWS)](https://aws.amazon.com/blogs/machine-learning/fine-tuning-nvidia-nemotron-speech-asr-on-amazon-ec2-for-domain-adaptation/)
- [Speech Recognition for Analysis of Police Radio Communication (scaling vs fine-tuning)](https://arxiv.org/pdf/2409.10858)
- [Replay to Remember: Continual Layer-Specific Fine-tuning for German Speech Recognition](https://arxiv.org/pdf/2307.07280)
