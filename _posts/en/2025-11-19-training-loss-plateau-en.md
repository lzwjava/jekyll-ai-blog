---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Training Loss Plateau After Initial Drop
translated: false
type: note
---

The training log shows the loss decreasing steadily from ~10.87 at step 0 to around 3.6-3.7 by step 10000, after which progress slows significantly, with train and val losses fluctuating in a narrow range (e.g., train around 3.64-3.71, val around 3.57-3.65 from step 10000 to 14500). This isn't a hard plateau yet—there's still a slight downward trend—but the rate of improvement has diminished, and occasional small increases in loss (e.g., val at step 9500 vs. 9000) suggest instability. Since you're using nanoGPT (based on the script and config), I'll break down the likely causes step by step, focusing on the config, log patterns, and common issues in transformer training like this. I'll also suggest fixes.

### 1. **Overfitting Due to Small/Limited Dataset**
   - **Why this is likely the primary cause**: Your config notes "small data" and "single-parquet-4070", with prepare.py adapted for a single file. FineWeb (or FineWeb-Edu) parquets are chunks of a massive dataset (~15T tokens total for FineWeb), but a single parquet might only contain 100M-1B tokens (depending on which one—e.g., some FineWeb shards are ~10-50GB, translating to ~50M-250M tokens after tokenization). With your setup:
     - Tokens per iter: ~524K (16 batch_size * 32 grad_acc * 1024 block_size).
     - By iter 14500: ~7.6B tokens seen (14500 * 524K).
     - If the dataset is <<7.6B tokens (e.g., 500M-1B), the model has looped over it multiple times (nanoGPT's DataLoader will cycle if needed). This leads to memorization rather than generalization, causing the loss to plateau as the model fits noise instead of patterns.
   - **Evidence from log**: Train and val losses track very closely (difference often <0.1), which is a classic sign of overfitting to a homogeneous/small dataset. If the data were diverse and large (like full FineWeb), you'd expect more separation if overfitting, or continued steady drops. Val loss fluctuations (e.g., up at steps 6000, 9500, 13000) also hint at this—overfit models become sensitive to batch variance.
   - **Why no further improvement**: The model (~40M params, not 125M—your comment has a calc error; it's closer to a tiny GPT-2) has likely extracted most learnable signal from the limited data. NanoGPT on small data often hits this wall faster than on Chinchilla-optimal scales.

### 2. **Learning Rate and Scheduler Issues**
   - **Analysis**: LR=1e-3 with cosine decay to min_lr=1e-4 over 20K iters, warmup=500. This is aggressive for a small model/dataset:
     - High initial LR can cause early oscillations (visible in individual iter losses jumping, e.g., 4.1096 at iter 10000).
     - Decay might be too slow or min_lr too high, preventing fine-grained convergence. In nanoGPT examples (e.g., Shakespeare or OpenWebText), LR is often 3e-4 to 6e-4 for ~85M params; 1e-3 could overshoot minima on small data.
     - Warmup=500 is short (~260M tokens), which might not stabilize gradients enough before full LR kicks in.
   - **Evidence**: Loss drops quickly early (good for high LR), but slows/fluctuates later, suggesting the optimizer is bouncing around a minimum instead of descending. Beta2=0.99 (vs. standard 0.999) adds momentum damping, which helps stability but can slow convergence if not tuned.
   - **Why plateau**: Optimizer can't escape the flat region; further training just adds noise.

### 3. **Model Capacity and Regularization Mismatch**
   - **Details**: 40M params (12 layers, 384 embd, 12 heads) is tiny for language modeling, even on "small data." If your single parquet has decent diversity, the model might underfit (can't capture complex patterns), but the close train/val suggests the opposite—overfit due to capacity exceeding data scale.
     - Dropout=0.1 is added "if overfitting," which is appropriate, but might not be enough. Weight_decay=0.1 is standard, but on small data, higher (0.2-0.5) or techniques like label smoothing could help.
     - No bias terms (bias=False, like Llama/Mistral) is fine, but combined with dropout, it might regularize too much, capping loss reduction.
   - **Evidence**: Losses stabilize around 3.5-3.7 perplexity (exp(3.6)≈36), which is okay for a tiny model on web text but higher than nanoGPT's Shakespeare benchmark (~1.5-2.0 loss on tiny models). If data is noisy/low-quality (FineWeb can be), the model hits an irreducible error floor.

### 4. **Other Potential Factors (Less Likely but Worth Checking)**
   - **Data Quality/Preparation**: Single file might have duplicates, noise, or imbalance (e.g., mostly short docs). If prepare.py wasn't adapted perfectly, tokenization issues (vocab=50304 is fine) or improper splitting could make val too similar to train, masking problems.
   - **Hardware/Implementation**: Training on 4070 (12GB VRAM) with compile=True is efficient, but if VRAM is maxed (effective batch 512 seqs *1024=524K tokens/iter), subtle instabilities like mixed precision errors (float16 with GradScaler) could arise. Log shows no NaNs, but FutureWarning is harmless.
   - **Evaluation Setup**: eval_iters=200 might be too few for stable val loss on small data—variance could make it seem plateaued. Always_save_checkpoint is on, so you can load earlier ones to compare.
   - **Not a bug in nanoGPT**: The script is standard; fused AdamW and compile are working (MFU ~10-12% is decent for 4070).

### How to Fix and Improve
To break the plateau, prioritize more data if possible—that's the biggest lever. Otherwise:
- **Add more data**: Switch to multiple parquets or full FineWeb shards. Update prepare.py to load a larger subset (e.g., 10-50B tokens). This should resume loss drops.
- **Tune hyperparameters**:
  - Lower initial LR to 5e-4 or 3e-4; set min_lr=5e-5. Extend warmup to 1000-2000 iters.
  - Increase dropout to 0.2 if overfitting persists.
  - Try longer training (up to 50K iters) but monitor for val increases.
  - Add --gradient_clip=1.0 if oscillations are from exploding gradients.
- **Regularization tweaks**: Increase weight_decay to 0.2. Experiment with --init_from='resume' from a checkpoint and lower LR for fine-tuning.
- **Model adjustments**: If data is truly small, shrink the model (e.g., n_embd=256, n_layer=6) to reduce overfitting. Or scale up if VRAM allows.
- **Diagnostics**: Plot losses (use wandb_log=True for visuals). Check perplexity (exp(loss))—if ~30-40, it's reasonable for tiny model/web data; aim for <10 with improvements.
- **Rerun experiments**: Start with a fresh run using these tweaks. If val starts diverging, it's confirmed overfitting.

If you share more details (e.g., exact dataset size from prepare.py, full log, or tensorboard plots), I can refine this further.
