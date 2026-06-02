---
audio: false
generated: true
image: false
lang: en
layout: post
title: GloVe Format and Loading Guide
translated: false
type: note
---

GloVe vectors are plain-text files. Each line is one token followed by its embedding values, all space-separated. There’s **no header** (unlike many word2vec text files).

Example (300-d GloVe):

```
the 0.418 0.24968 -0.41242 0.1217 ... 0.34527   # 300 floats total
to   0.68047 -0.039263 -0.67412 0.056051 ... -0.067549
U.S. 0.3459  0.21513  -0.09982  0.25344 ... 0.024118
```

A few practical notes:

* Common releases:

  * `glove.6B.{50,100,200,300}d.txt` (Wikipedia + Gigaword; \~400k vocab, lowercase).
  * `glove.840B.300d.txt` (Common Crawl; \~2.2M vocab).
  * `glove.twitter.27B.{25,50,100,200}d.txt` (Twitter; lots of hashtags/emoticons).
* Tokens never contain spaces (phrases use underscores), so a simple `line.split()` is fine.
* Floats are ASCII; you’ll see regular decimals and sometimes scientific notation.
* There’s no special `<unk>` row; OOV handling is up to you.

Your loader

```python
def read_glove_vecs(glove_file):
    with open(glove_file, 'r', encoding='utf-8') as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
    return words, word_to_vec_map
```

matches that format. Two small upgrades you may want:

1. Use float32 to cut memory in half:

```python
vec = np.asarray(line[1:], dtype=np.float32)
```

2. Skip accidental “headers” or bad lines (some repackaged files add one):

```python
parts = line.rstrip().split(' ')
if len(parts) < 2:
    continue
if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
    # looks like a word2vec-style header: "<vocab> <dim>"
    continue
word, *vals = parts
```

### Building an embedding matrix for your vocab

After you create `dictionary: word -> id`, map GloVe rows into a weight matrix for your `nn.Embedding`:

```python
def build_embedding_matrix(dictionary, glove_path, dim=300, dtype=np.float32):
    _, glove = read_glove_vecs(glove_path)  # as above, but dtype=float32
    V = len(dictionary)
    W = np.random.uniform(-0.05, 0.05, (V, dim)).astype(dtype)
    for w, idx in dictionary.items():
        vec = glove.get(w)
        if vec is not None and vec.shape[0] == dim:
            W[idx] = vec
    return torch.tensor(W)

# usage
# emb_weight = build_embedding_matrix(dictionary, "glove.6B.300d.txt", dim=300)
# model.in_embeddings.weight.data.copy_(emb_weight)
```

### Quick contrast with word2vec text/binary

* **GloVe text**: no header, `word float float ...`
* **word2vec text**: often starts with `"<vocab> <dim>"` header.
* **word2vec binary**: header + binary floats.

If you ever need to use tooling expecting word2vec format, convert with `gensim.scripts.glove2word2vec`.
