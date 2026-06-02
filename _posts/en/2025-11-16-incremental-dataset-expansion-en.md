---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Incremental Dataset Expansion Strategy
translated: false
type: note
---

Yes, incrementally increasing the dataset size step by step (e.g., starting with articles1, then adding articles2 and articles3, and so on) can be a smart approach, especially if you're experimenting with NanoGPT on limited hardware like an RTX 4070. However, whether to stick with that or jump to downloading articles1 through articles10 depends on your goals, time, and resources. I'll break it down below to help you decide.

### Pros of Step-by-Step Increase (What You're Considering)

- **Controlled Experimentation**: You can monitor how adding more data affects model performance (e.g., loss curves, perplexity, or generated text quality). From your logs, training on just articles1 (a small slice of Wikipedia) got you down to ~3.9 train/val loss after 20k iterations, which is a good start for a tiny model. Adding articles2 and articles3 (bringing you to ~3 parts) lets you see if the model generalizes better or overfits less without committing to a massive run.
- **Resource Management**:
  - Disk: Your 391GB available is more than enough for now. The two new bz2 files are ~5GB compressed total. Using wikiextractor (as suggested in the echo), the extracted clean text might be ~10-15GB uncompressed for these two (Wikipedia XML compresses well, but clean text is denser). Combined with articles1's extracted data (~5GB?), you'd be at ~15-20GB total—plenty of headroom.
  - RAM/GPU: 62GB system RAM handles tokenization and data loading fine. RTX 4070 (12GB VRAM) is solid for NanoGPT's default tiny/shakespeare configs or even small GPT-2-like models (e.g., 124M params). If you're using bf16 or mixed precision, you can batch larger. Step-by-step avoids overwhelming VRAM with huge datasets upfront.
  - Time: Extraction with `--processes 8` on your setup should take 1-2 hours per file. Training increments (e.g., continuing from your articles1 checkpoint) could be done in days per step, letting you iterate quickly.
- **Curriculum Learning Angle**: Wikipedia articles are somewhat ordered by ID, so adding sequentially might act like a loose curriculum (early articles might be more "foundational"). But shuffle your dataset well in NanoGPT's prep script to avoid biases.
- **When to Do This**: If you're prototyping, testing hyperparameters (e.g., lr, batch size), or just learning, this is efficient. You can fine-tune your existing checkpoint on the new data (append extracted text from articles2/3 to your existing dataset, retokenize, and resume training with `--init_from resume` in NanoGPT).

### Cons of Step-by-Step and When to Jump to More (e.g., Articles1-10)

- **Efficiency Issues**: Retraining or fine-tuning multiple times on growing subsets wastes compute if your end goal is a model on a large chunk of Wikipedia. Language models benefit from diverse, shuffled data from the start—sequential additions might lead to catastrophic forgetting if not handled carefully (though NanoGPT's simple setup minimizes this).
- **Data Scale for Better Results**: Articles1-3 is still a tiny fraction of English Wikipedia (~20GB total clean text for the full dump). Your losses plateaued around 3.9-4.0, which is okay for small data but won't yield coherent generations. To see real improvements (e.g., sub-3.0 loss), you'd want 10+ parts (~50-100GB extracted text). Full enwiki has ~27 parts in recent dumps, but articles1-10 would cover a solid ~30-40% of the corpus—enough for a decent toy model without downloading everything.
- **Practical Downsides**:
  - Download Time: Articles1-10 bz2 files total ~20-25GB compressed (based on typical dump sizes). On a good connection, that's 1-2 hours, but mirrors like ftp.acc.umu.se can be slow.
  - Extraction Overhead: Running wikiextractor on 10 files could take 10-20 hours total, even parallelized. Output dir would balloon to ~50-100GB, still fine on your 391GB disk.
  - Training Time: On RTX 4070, full run on articles1-10 might take weeks at 20k+ iters, depending on model size. But you could downsample or use a smaller context_length to speed up.
- **When to Jump**: If your goal is a stronger model quickly (e.g., for downstream tasks like Q&A or generation), download articles1-10 now. Combine all extracted text into one big file, tokenize once, and train from scratch. This avoids repeated setups and gives better generalization. Wikipedia data is high-quality and consistent, so more is almost always better up to your hardware limits.

### Recommendation

Go step-by-step for now with articles1+2+3—it's low-risk and builds on what you have. Extract the new files, concatenate the clean text (e.g., `cat extracted/*/* > all_text.txt`), retokenize, and resume training from your last checkpoint. Watch if val loss drops below 3.5-4.0; if it does and generations improve, keep adding. If not, or if you're impatient, grab articles4-10 next (use similar wget from the same mirror, incrementing the part numbers like enwiki-20251101-pages-articles4.xml-p311330pXYZ.bz2—check the dump index for exact ranges).

Tips for Next Steps:

- **Prep Data**: After extraction, clean further if needed (e.g., remove short articles with `awk` or Python). Use NanoGPT's `prepare.py` with your tokenizer (e.g., GPT-2's).
- **Training Tweaks**: Lower learning rate (e.g., 3e-4) when resuming. Monitor MFU (your logs show ~9-10%, which is decent; aim for 15%+ with optimizations). If VRAM maxes, reduce batch_size or gradient_accumulation_steps.
- **Space Check**: Before downloading more, run `df -h` after extracting 2+3 to confirm usage.
- **Alternatives**: If Wikipedia feels too big, consider finer datasets like BookCorpus or C4 subsets for variety.

If you share more details (e.g., your NanoGPT config, model size, or specific goals), I can refine this advice.
