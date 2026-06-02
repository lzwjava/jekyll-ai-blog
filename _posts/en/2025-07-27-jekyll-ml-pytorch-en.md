---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enhancing Jekyll Blog with PyTorch
translated: false
type: note
---

### Improving Your Jekyll Blog with ML/AI Using PyTorch

Since you're running a Jekyll blog (a static site generator), integrating ML/AI features like recommendations or categorization requires some creativity. Jekyll builds static HTML, so dynamic elements (e.g., real-time recommendations) might need client-side JavaScript or precomputing during the build process via Jekyll plugins or scripts. You mentioned avoiding LLM APIs and focusing on your own neural networks with PyTorch—great, as this keeps everything local and customizable. I'll outline practical ideas, focusing on PyTorch implementations. These assume you have access to basic libraries like NumPy (for data handling) and can handle text preprocessing manually or with simple tokenization (since advanced NLP libs like Hugging Face aren't mentioned in your setup, but you can add them locally if needed).

You'll likely create Python scripts (e.g., in your `scripts/` directory) that run during Jekyll's build process (via a Makefile hook or GitHub Actions if deployed). For example, process Markdown posts in `_posts/`, generate JSON data, and inject it into your site via Liquid templates.

#### 1. Article Categorization with a PyTorch Classifier
Categorize posts automatically (e.g., into topics like "ML", "Notes", "Latex") by training a simple neural network classifier. This is supervised learning: you'll need to manually label a subset of your posts as training data. If you don't have labels, start with unsupervised clustering (see below).

**Steps:**
- **Data Preparation:** Parse your Markdown files in `_posts/`. Extract text content (skip frontmatter). Create a dataset: list of (text, label) pairs. Use a CSV or list for ~50-100 labeled examples initially.
- **Preprocessing:** Tokenize text (simple split on spaces/whitespace), build a vocabulary, convert to numerical indices. Use one-hot encoding or basic embeddings.
- **Model:** A basic feedforward neural network in PyTorch for multi-class classification.
- **Training:** Train on your local machine. Use cross-entropy loss and Adam optimizer.
- **Integration:** Run the script during build to classify all posts, generate a `categories.json` file, and use it in Jekyll to tag pages or create category indexes.

**Example PyTorch Code Snippet (in a script like `scripts/categorize_posts.py`):**
```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from collections import Counter

# Step 1: Load and preprocess data (simplified)
def load_posts(posts_dir='_posts'):
    texts = []
    labels = []  # Assume manual labels: 0=ML, 1=Notes, etc.
    for file in os.listdir(posts_dir):
        if file.endswith('.md'):
            with open(os.path.join(posts_dir, file), 'r') as f:
                content = f.read().split('---')[2].strip()  # Skip frontmatter
                texts.append(content)
                # Placeholder: load label from a dict or CSV
                labels.append(0)  # Replace with actual labels
    return texts, labels

texts, labels = load_posts()
# Build vocab (top 1000 words)
all_words = ' '.join(texts).lower().split()
vocab = {word: idx for idx, word in enumerate(Counter(all_words).most_common(1000))}
vocab_size = len(vocab)

# Convert text to vectors (bag-of-words)
def text_to_vec(text):
    vec = np.zeros(vocab_size)
    for word in text.lower().split():
        if word in vocab:
            vec[vocab[word]] += 1
    return vec

X = np.array([text_to_vec(t) for t in texts])
y = torch.tensor(labels, dtype=torch.long)

# Step 2: Define model
class Classifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = Classifier(vocab_size, num_classes=3)  # Adjust num_classes

# Step 3: Train
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()
X_tensor = torch.tensor(X, dtype=torch.float32)

for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_tensor)
    loss = loss_fn(outputs, y)
    loss.backward()
    optimizer.step()
    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')

# Step 4: Inference on new post
def classify_post(text):
    vec = torch.tensor(text_to_vec(text), dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        pred = model(vec).argmax(1).item()
    return pred  # Map back to category name

# Save model: torch.save(model.state_dict(), 'classifier.pth')
# In build script: classify all posts and write to JSON
```

**Improvements:** For better accuracy, use word embeddings (train a simple Embedding layer in PyTorch) or add more layers. If unlabeled, switch to clustering (e.g., KMeans on embeddings—see next section). Run this script in your Makefile: `jekyll build && python scripts/categorize_posts.py`.

#### 2. Recommendation System with PyTorch Embeddings
Recommend similar articles to readers (e.g., "You might also like..."). Use content-based recommendation: learn embeddings for each post, then compute similarity (cosine distance). No user data needed—just post content.

**Steps:**
- **Data:** Same as above—extract text from posts.
- **Model:** Train an autoencoder in PyTorch to compress text into low-dimensional embeddings (e.g., 64-dim vectors).
- **Training:** Minimize reconstruction loss to learn meaningful representations.
- **Recommendations:** For a given post, find nearest neighbors in embedding space.
- **Integration:** Precompute embeddings during build, store in JSON. Use JS on the site to show recommendations (or Liquid for static lists).

**Example PyTorch Code Snippet (in `scripts/recommend_posts.py`):**
```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# Reuse load_posts and text_to_vec from above

texts, _ = load_posts()  # Ignore labels
X = np.array([text_to_vec(t) for t in texts])
X_tensor = torch.tensor(X, dtype=torch.float32)

# Autoencoder model
class Autoencoder(nn.Module):
    def __init__(self, input_size, embedding_size=64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, embedding_size)
        )
        self.decoder = nn.Sequential(
            nn.Linear(embedding_size, 256),
            nn.ReLU(),
            nn.Linear(256, input_size)
        )

    def forward(self, x):
        emb = self.encoder(x)
        return self.decoder(emb)

model = Autoencoder(vocab_size)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

for epoch in range(200):
    optimizer.zero_grad()
    reconstructed = model(X_tensor)
    loss = loss_fn(reconstructed, X_tensor)
    loss.backward()
    optimizer.step()
    if epoch % 20 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')

# Get embeddings
with torch.no_grad():
    embeddings = model.encoder(X_tensor).numpy()

# Recommend: for post i, find top 3 similar
similarities = cosine_similarity(embeddings)
for i in range(len(texts)):
    rec_indices = similarities[i].argsort()[-4:-1][::-1]  # Top 3 excluding self
    print(f'Recs for post {i}: {rec_indices}')

# Save embeddings to JSON for Jekyll
import json
with open('embeddings.json', 'w') as f:
    json.dump({'embeddings': embeddings.tolist(), 'posts': [f'post_{i}' for i in range(len(texts))]}, f)
```

**Improvements:** Use a variational autoencoder for better embeddings. If you have user views (via analytics), add collaborative filtering with a matrix factorization model in PyTorch. Client-side: Load JSON in JS and compute similarities on-the-fly for personalization.

#### 3. Other Ideas with PyTorch
- **Unsupervised Clustering for Auto-Tagging:** If labeling is tedious, use embeddings (from above autoencoder) + KMeans clustering to group posts into topics. PyTorch for embeddings, NumPy/SciPy for clustering.
  ```python
  from sklearn.cluster import KMeans
  kmeans = KMeans(n_clusters=5)
  clusters = kmeans.fit_predict(embeddings)
  # Assign tags based on clusters
  ```
  Integrate: Generate tags in frontmatter via script.

- **Semantic Search Enhancement:** Embed queries and posts similarly, then use cosine similarity for a search bar. Precompute post embeddings; use JS for query embedding (but since PyTorch is Python, export model to ONNX for JS inference via ONNX.js, or keep search static).

- **Post Summarization:** Train a seq2seq model (RNN/LSTM in PyTorch) on paired (full text, manual summary) data. Challenging without large datasets, but start small with your posts. Use for generating excerpts.

**General Tips:**
- **Scalability:** For a small blog, train on CPU; PyTorch handles it fine. Save models with `torch.save` and load for inference.
- **Build Integration:** Add to Makefile: `train: python scripts/train_models.py` then `build: jekyll build && python scripts/generate_features.py`.
- **Limitations:** Without advanced NLP (e.g., transformers), results are basic—consider adding `torchtext` or manual GloVe embeddings locally. Test on your `ml/` or `notes/` dirs.
- **Deployment:** If on GitHub Pages, run scripts in CI. For dynamic stuff, consider adding a lightweight Flask backend, but that deviates from static Jekyll.

If you share more details (e.g., post count, topics), I can refine these!
