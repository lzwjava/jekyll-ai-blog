import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
# Reuse load_posts and text_to_vec from above

def text_to_vec(text, vocab_size=5000):
    """Convert text to a simple bag-of-words vector based on character or word frequency."""
    # Simple placeholder: create a vector of fixed size with dummy values
    # In a real scenario, use TF-IDF, word embeddings, or similar
    vec = np.zeros(vocab_size)
    for i, char in enumerate(text[:vocab_size]):
        vec[i] = ord(char) if i < len(text) else 0
    return vec

def load_posts(posts_dir='original'):
    texts = []
    labels = []  # Assume manual labels: 0=ML, 1=Notes, 2=Other
    for file in os.listdir(posts_dir):
        if file.endswith('.md'):
            with open(os.path.join(posts_dir, file), 'r') as f:
                content = f.read().split('---')[2].strip()  # Skip frontmatter
                texts.append(content)
                # Placeholder: load label from a dict or CSV
                labels.append(0)  # Replace with actual labels
    return texts, labels

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