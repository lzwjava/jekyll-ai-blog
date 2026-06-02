---
audio: false
generated: false
image: false
lang: en
layout: post
title: 'BCEmbedding: Bilingual Embedding for RAG'
translated: false
type: post
---

[https://github.com/netease-youdao/BCEmbedding](https://github.com/netease-youdao/BCEmbedding)

```bash
git clone git@github.com:netease-youdao/BCEmbedding.git
cd BCEmbedding
pip install -v -e .
```

```python
from BCEmbedding import EmbeddingModel

# list of sentences
sentences = ['sentence_0', 'sentence_1']

# init embedding model
model = EmbeddingModel(model_name_or_path="maidalun1020/bce-embedding-base_v1")

# extract embeddings
embeddings = model.encode(sentences)
```

The code runs successfully, as demonstrated by the log below.

```bash
% python scripts/bce_embedding.py

/opt/homebrew/lib/python3.13/site-packages/transformers/utils/generic.py:441: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
/opt/homebrew/lib/python3.13/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
/opt/homebrew/lib/python3.13/site-packages/transformers/utils/generic.py:309: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
/opt/homebrew/lib/python3.13/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
pytorch_model.bin:  98%|  | 1.09G/1.11G [16:15<00:11, 1.84MB/s]Error while downloading from https://cdn-lfs-us-1.hf.co/repos/c2/ec/c2ecf54f7fa0d838b0e99f7ff8b8b4776cef647a35e582c3cfc2ef6a3b35216a/ac079810acaca8a00ac1abef5c5d2e2d746a9b99fdefc98d0bf5031a2748482f?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27pytorch_model.bin%3B+filename%3D%22pytorch_model.bin%22%3B&response-content-type=application%2Foctet-stream&Expires=1738608683&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczODYwODY4M319LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmhmLmNvL3JlcG9zL2MyL2VjL2MyZWNmNTRmN2ZhMGQ4MzhiMGU5OWY3ZmY4YjhiNDc3NmNlZjY0N2EzNWU1ODJjM2NmYzJlZjZhM2IzNTIxNmEvYWMwNzk4MTBhY2FjYThhMDBhYzFhYmVmNWM1ZDJlMmQ3NDZhOWI5OWZkZWZjOThkMGJmNTAzMWEyNzQ4NDgyZj9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSomcmVzcG9uc2UtY29udGVudC10eXBlPSoifV19&Signature=cYLZWTurgzrKLbsWxcaVlKXwS5Sk-alE1rauv9AYxPWTi93eOS-Rk80lC%7EN6vaxX8dCuzQ73rbbQCoN5SDWxi7nmG5SUkELDJ4nKmIjSYMf2Pz-N6v8Rwuddb-SJLtr-Yrfs33yqJ%7Eazt-yBYo28gbJIW5cgsDKrFVapFZH26dzjl3jTDOg7X9Lfs2AFQE8FnNoMweceRr45Z1mO0ORzlWjk47dyaeAZBvVYx%7EM0VAiVBsh4x8kLl-I%7E61BCJvjSDkc7Oh2FjUUjZSvXl0Zm2ocSnfWeO-Bdjb7QPZSVGkJ2NDUfhurq1ewD1cCe2ITpjEHCSrvvXC7N2Ni3pMbThg__&Key-Pair-Id=K24J24Z295AEI9: HTTPSConnectionPool(host='cdn-lfs-us-1.hf.co', port=443): Read timed out.
Trying to resume download...
02/04/2025 02:07:45 - [WARNING] -huggingface_hub.file_download->>>    Error while downloading from https://cdn-lfs-us-1.hf.co/repos/c2/ec/c2ecf54f7fa0d838b0e99f7ff8b8b4776cef647a35e582c3cfc2ef6a3b35216a/ac079810acaca8a00ac1abef5c5d2e2d746a9b99fdefc98d0bf5031a2748482f?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27pytorch_model.bin%3B+filename%3D%22pytorch_model.bin%22%3B&response-content-type=application%2Foctet-stream&Expires=1738608683&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczODYwODY4M319LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmhmLmNvL3JlcG9zL2MyL2VjL2MyZWNmNTRmN2ZhMGQ4MzhiMGU5OWY3ZmY4YjhiNDc3NmNlZjY0N2EzNWU1ODJjM2NmYzJlZjZhM2IzNTIxNmEvYWMwNzk4MTBhY2FjYThhMDBhYzFhYmVmNWM1ZDJlMmQ3NDZhOWI5OWZkZWZjOThkMGJmNTAzMWEyNzQ4NDgyZj9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSomcmVzcG9uc2UtY29udGVudC10eXBlPSoifV19&Signature=cYLZWTurgzrKLbsWxcaVlKXwS5Sk-alE1rauv9AYxPWTi93eOS-Rk80lC%7EN6vaxX8dCuzQ73rbbQCoN5SDWxi7nmG5SUkELDJ4nKmIjSYMf2Pz-N6v8Rwuddb-SJLtr-Yrfs33yqJ%7Eazt-yBYo28gbJIW5cgsDKrFVapFZH26dzjl3jTDOg7X9Lfs2AFQE8FnNoMweceRr45Z1mO0ORzlWjk47dyaeAZBvVYx%7EM0VAiVBsh4x8kLl-I%7E61BCJvjSDkc7Oh2FjUUjZSvXl0Zm2ocSnfWeO-Bdjb7QPZSVGkJ2NDUfhurq1ewD1cCe2ITpjEHCSrvvXC7N2Ni3pMbThg__&Key-Pair-Id=K24J24Z295AEI9: HTTPSConnectionPool(host='cdn-lfs-us-1.hf.co', port=443): Read timed out.
Trying to resume download...
pytorch_model.bin: 100%|| 1.11G/1.11G [00:10<00:00, 2.06MB/s]
pytorch_model.bin:  98%|| 1.09G/1.11G [16:33<00:25, 866kB/s]
02/04/2025 02:07:57 - [INFO] -BCEmbedding.models.EmbeddingModel->>>    Loading from `maidalun1020/bce-embedding-base_v1`.
02/04/2025 02:07:57 - [INFO] -BCEmbedding.models.EmbeddingModel->>>    Execute device: cpu;  gpu num: 0;  use fp16: False;  embedding pooling type: cls;  trust remote code: False
Extract embeddings: 100%| 1/1 [00:00<00:00,  1.21it/s]
```

Let's try the reranker model.

```python
from BCEmbedding import RerankerModel

# your query and corresponding passages
query = 'input_query'
passages = ['passage_0', 'passage_1']

# construct sentence pairs
sentence_pairs = [[query, passage] for passage in passages]

# init reranker model
model = RerankerModel(model_name_or_path="maidalun1020/bce-reranker-base_v1")

# method 0: calculate scores of sentence pairs
scores = model.compute_score(sentence_pairs)

# method 1: rerank passages
rerank_results = model.rerank(query, passages)
```

```bash
% python scripts/bce_reranker.py

/opt/homebrew/lib/python3.13/site-packages/transformers/utils/generic.py:441: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
/opt/homebrew/lib/python3.13/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
tokenizer_config.json: 100%|
# ...
/opt/homebrew/lib/python3.13/site-packages/transformers/utils/generic.py:309: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
/opt/homebrew/lib/python3.13/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
pytorch_model.bin: 100%|| 1.11G/1.11G [02:11<00:00, 8.47MB/s]
02/04/2025 02:56:39 - [INFO] -BCEmbedding.models.RerankerModel->>>    Loading from `maidalun1020/bce-reranker-base_v1`.
02/04/2025 02:56:39 - [INFO] -BCEmbedding.models.RerankerModel->>>    Execute device: cpu;  gpu num: 0;  use fp16: False
Calculate scores: 100%| 1/1 [00:00<00:00,  2.37it/s]
You're using a XLMRobertaTokenizerFast tokenizer. Please note that with a fast tokenizer, using the `__call__` method is faster than using a method to encode the text followed by a call to the `pad` method to get a padded encoding.
```
