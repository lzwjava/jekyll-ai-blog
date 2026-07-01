---
audio: false
generated: true
image: false
lang: en
layout: post
title: "SPGISpeech: Fully Formatted End-to-End ASR"
translated: false
type: note
---

Question: Give an introduction to the paper "SPGISpeech: 5,000 hours of transcribed financial audio for fully formatted end-to-end speech recognition" (arXiv:2104.02014).

Answer:

## The core idea

Standard ASR (speech-to-text) systems predict *unformatted* text — lowercase, no punctuation, numbers spelled out ("ninety two year history"). Getting to readable output like "92-year history" normally requires a separate post-processing pipeline: truecasing model, punctuation restoration model, inverse text normalization (ITN) model, each trained and maintained independently.

This paper's contribution is two things:

1. **A dataset**: SPGISpeech — 5,000 hours of earnings-call audio, fully orthographically transcribed (proper casing, punctuation, "92-year" not "ninety two year"), ~50,000 speakers, 100K vocabulary. It's ~10x larger than any prior corpus with this level of transcription formatting.
2. **A task framing**: train the acoustic model to emit fully-formatted text directly, end-to-end, instead of chaining formatting models after a bare transcript.

The argument for doing this end-to-end (rather than post-hoc) is an information-availability one: some orthographic decisions genuinely need acoustic signal, not just text. Their example — "the CEO retired" — whether it ends in `.` or `?` can hinge on pitch contour, which is gone once you've collapsed to unformatted text. So chaining a punctuation-restoration model onto flat ASR output throws away information the acoustic model already had.

## Architecture (this is the part relevant to your transformer/attention interests)

They train **Conformer** models — this is the key technical piece worth understanding since you're deep in transformer internals.

Conformer = Transformer encoder block + a convolution module inserted in the middle. The intuition: self-attention captures long-range/global dependencies well but is weaker at modeling fine-grained *local* patterns (which matter a lot in audio — phoneme-level transitions happen over tens of milliseconds). A depthwise conv sub-layer complements this.

A single Conformer block, roughly:

```python
class ConformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, conv_kernel=31, ff_mult=4):
        super().__init__()
        self.ff1 = FeedForward(d_model, ff_mult)          # half-step residual
        self.mhsa = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.conv = ConvModule(d_model, kernel=conv_kernel)  # depthwise conv + GLU
        self.ff2 = FeedForward(d_model, ff_mult)           # half-step residual
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, attn_mask=None):
        x = x + 0.5 * self.ff1(x)
        attn_out, _ = self.mhsa(x, x, x, attn_mask=attn_mask)
        x = x + attn_out
        x = x + self.conv(x)
        x = x + 0.5 * self.ff2(x)
        return self.norm(x)
```

The conv module is depthwise-separable with a GLU gate before it — this is the local-pattern extractor:

```python
class ConvModule(nn.Module):
    def __init__(self, d_model, kernel=31):
        super().__init__()
        self.pointwise1 = nn.Conv1d(d_model, 2 * d_model, 1)
        self.glu = nn.GLU(dim=1)
        self.depthwise = nn.Conv1d(d_model, d_model, kernel,
                                    padding=kernel // 2, groups=d_model)
        self.bn = nn.BatchNorm1d(d_model)
        self.pointwise2 = nn.Conv1d(d_model, d_model, 1)

    def forward(self, x):  # x: (B, T, C)
        x = x.transpose(1, 2)
        x = self.glu(self.pointwise1(x))
        x = self.depthwise(x)
        x = F.silu(self.bn(x))
        x = self.pointwise2(x)
        return x.transpose(1, 2)
```

Two model variants in the paper:
- **Conformer (ESPnet)**: encoder-decoder, RNN-T style (12 encoder blocks, 6 transformer decoder blocks, autoregressive at inference — slower).
- **Conformer-CTC (NeMo)**: same encoder, but a linear decoder + **CTC loss** instead of the autoregressive decoder. Non-autoregressive → much faster inference, since the whole output sequence is scored/decoded in one forward pass with a monotonic alignment assumption.

CTC loss, for context since it's doing something conceptually different from cross-entropy on tokens: it marginalizes over all possible alignments between the (longer) acoustic frame sequence and the (shorter) label sequence, using a blank token to allow repeats/no-output frames, computed efficiently via dynamic programming (forward-backward algorithm, same DP structure as HMM forward-backward). This is worth understanding if you haven't — it's the same "sum over alignments via DP" trick you'd recognize from other structured prediction settings.

Both use SentencePiece subword tokenization (~5K vocab) rather than raw characters — same tokenization philosophy as LLMs, applied to the output side of an ASR model.

## Results

CER 1.7% (ESPnet Conformer) / 1.8% (Conformer-CTC) on the orthographic (fully formatted) task. Comparing to a normalized-vocabulary version of the same output (lowercase, punctuation stripped), they find roughly half to two-thirds of total error comes specifically from orthographic decisions (casing, punctuation, denormalization) — i.e., formatting is genuinely hard, not a negligible add-on, which supports their thesis that it deserves to be learned jointly with acoustic-to-phoneme mapping rather than bolted on after.

## Why this might interest you specifically

- The CTC vs. autoregressive-decoder tradeoff here is the same throughput/latency tradeoff you deal with in LLM inference (parallel decode vs. sequential sampling) — worth connecting mentally to KV-cache/speculative-decoding tradeoffs you already think about.
- If you're doing any audio-adjacent agent work (voice interfaces, transcription pipelines for your CLI agents), this is a clean example of "make the model do the whole task end-to-end" rather than pipeline-of-specialized-models — directly aligned with your AI-native bias.
- The dataset itself (Kensho / S&P Global earnings calls) is domain-specific (financial), which is thematically close to your bank AI-engineering work if you ever touch call-transcription or voice-based fintech tooling.

References:

- [SPGISpeech: 5,000 hours of transcribed financial audio for fully formatted end-to-end speech recognition (arXiv:2104.02014)](https://arxiv.org/pdf/2104.02014)
