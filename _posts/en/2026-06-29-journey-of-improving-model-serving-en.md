---
audio: false
generated: true
image: false
lang: en
layout: post
title: Journey of Improving Model Serving
translated: false
type: note
---

Here's the full journey of improving the model serving:

== PROBLEM ==

The server on RunPod was producing degenerate, repetitive, incoherent output —
mixing "oil and natural gas industry" with "healthcare industry", repeating phrases,
and generating garbage like "ivableivable...".

== ROOT CAUSES FOUND ==

1. WRONG MODEL CONVERSION (nanoGPT → HuggingFace)
   - nanoGPT stores Linear weights as [out_features, in_features]
   - HF GPT2Conv1D expects [in_features, out_features]
   - Conversion script transposed weights, which was correct for non-square matrices
   - BUT the model was also loaded with wrong vocab (50304 padded → 50257 trimmed),
     zero biases added, and transformers generate() has different internal logit processing
   - Result: transformers version produced noticeably worse output than native nanoGPT

2. BAD SAMPLING PARAMETERS
   - Server used top_p=0.9 (nucleus sampling)
   - nanoGPT uses top_k=200
   - top_p on a small 124M model leaks probability to unlikely tokens → incoherent text

3. SEC_SYSTEM PREFIX POISONING
   - Every prompt was prepended with:
     "The following are excerpts from SEC EDGAR filings filed with the
      U.S. Securities and Exchange Commission by publicly traded companies."
   - The model was NOT trained with this prefix → confused context → repetitive garbage

4. NEWLINE TRIMMER CUT OUTPUT SHORT
   - Chat endpoint had: `if "\n" in text[20:]: text = text[:text.index("\n", 20)]`
   - SEC filing text naturally has newlines early → output truncated to ~134 chars

== FIXES APPLIED ==

| Fix | Before | After |
| ----- | -------- | ------- |
| Model loading | HF transformers GPT2LMHeadModel + converted safetensors | Native nanoGPT model.py + original ckpt.pt (1.4GB) |
| Tokenizer | transformers AutoTokenizer | tiktoken GPT-2 BPE |
| Sampling | top_p=0.9 | top_k=200 |
| Temperature | 0.7 | 0.8 |
| Default max_tokens | 100 | 1000 |
| SEC_SYSTEM prefix | prepended to every prompt | removed |
| Newline trimmer | cut chat output at first \n | removed |
| Dependencies | torch + transformers + accelerate + fastapi | torch + tiktoken + fastapi |

== RESULT ==

Before:
  "Our principal business is our principal executive office in San Francisco,
   California and is located in The San Francisco, California..."

After:
  "$2.0 million during the year ended December 31, 2016, the Company recognized
   non-cash impairment charges of $0.1 million... bad debt expense. See Note 9
   for further details."

== FILES ON RUNPOD (/workspace/model/) ==

  ckpt.pt       1.4GB   Original nanoGPT checkpoint (47k steps, val loss 2.2778)
  model.py      8.6KB   nanoGPT model definition (native, not HF)
  server.py     4.5KB   FastAPI server using native model
  index.html    Chat UI
  hf-model/     622MB   Old HF model (backup, not used)
