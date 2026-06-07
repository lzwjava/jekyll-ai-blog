---
audio: false
generated: true
image: false
lang: en
layout: post
title: Large Language Model Training Complete
translated: false
type: note
---

Training complete!

  Status:    DONE — step 130,000/130,000
  Total time: 2,549.86 minutes (~42.5 hours)
  Val bpb:   0.780026 (minimum)
  Peak VRAM: 9,443.99 MiB
  Checkpoint: /home/lzw/.cache/nanochat/base_checkpoints/d12/model_130000.pt

Eval results (CORE metric: 0.1916):

  hellaswag (10-shot):        0.43
  winograd (0-shot):          0.62
  winogrande (0-shot):        0.54
  boolq (10-shot):            0.585
  bigbench_cs_algorithms:     0.34
  squad (10-shot):            0.27
  coqa (0-shot):              0.26
  agi_eval_lsat_ar (3-shot):  0.21
  bigbench_dyck_languages:    0.17
  bigbench_operators:         0.14
  bigbench_repeat_copy_logic: 0.00
  bigbench_language_id:       0.195

Sample generations look coherent but repetitive (typical for a 286M model). The checkpoint is saved and ready for chat or further eval.
