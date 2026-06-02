---
audio: false
generated: true
lang: en
layout: post
title: Word2Vec Script with Gensim
translated: false
type: note
---

To provide you with a Python script for Word2Vec, I need to make a couple of assumptions about what you're looking for, as "a script about Word2Vec" can be quite broad. I'll provide two common scenarios:

1. **A simple script using `gensim` for training and basic usage:** This is the most common and practical way to use Word2Vec in Python.
2. **A very basic, conceptual implementation from scratch:** This is more for understanding the core algorithms, but less practical for real-world use due to complexity and optimization.

Given your request, I'll prioritize the `gensim` approach as it's what most people would use.

-----

### Python Script for Word2Vec using `gensim`

This script will demonstrate:

* Preparing sample text data.
* Training a Word2Vec model.
* Finding most similar words.
* Performing word analogies.
* Saving and loading the model.

**Prerequisites:**

You'll need to install the `gensim` library:

```bash
pip install gensim
```

**Python Script (`word2vec_gensim_example.py`):**

```python
import gensim
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import logging

# Configure logging to see training progress
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# --- 1. Prepare Sample Text Data ---
# In a real-world scenario, you would load your text data from files.
# Here, we use a simple list of sentences.
raw_sentences = [
    "I love natural language processing.",
    "Word embeddings are a fascinating topic.",
    "Machine learning revolutionizes many industries.",
    "Deep learning is a subset of machine learning.",
    "Natural language processing uses various techniques.",
    "Computers understand human language better with word vectors.",
    "The quick brown fox jumps over the lazy dog.",
    "Dog and cat are common pets.",
    "King is to Queen as Man is to Woman."
]

# Preprocess the sentences: tokenize and convert to lowercase
# gensim's simple_preprocess is convenient for this
tokenized_sentences = [simple_preprocess(sentence) for sentence in raw_sentences]

print("\n--- Tokenized Sentences ---")
for sentence in tokenized_sentences:
    print(sentence)

# --- 2. Train the Word2Vec Model ---
# Parameters explained:
#   vector_size: Dimensionality of the word vectors.
#   window: Maximum distance between the current and predicted word within a sentence.
#   min_count: Ignores all words with total frequency lower than this.
#   sg: Training algorithm: 0 for CBOW, 1 for Skip-gram. Skip-gram is generally better for rare words.
#   workers: Use these many worker threads to train the model (=faster training).
#   epochs: Number of iterations (epochs) over the corpus.
model = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=100,      # Example: 100-dimensional vectors
    window=5,             # Context window of 5 words on either side
    min_count=1,          # Include all words (for this small example)
    sg=1,                 # Use Skip-gram (sg=1)
    workers=4,            # Use 4 CPU cores for training
    epochs=10             # Train for 10 epochs
)

print("\n--- Model Training Complete ---")

# --- 3. Explore the Model ---

# Get the vector for a specific word
try:
    word_vector = model.wv['machine']
    print(f"\nVector for 'machine' (first 10 dimensions): {word_vector[:10]}")
    print(f"Vector for 'machine' shape: {word_vector.shape}")
except KeyError:
    print("\n'machine' not found in vocabulary.")

# Find the most similar words
print("\n--- Most Similar Words to 'machine' ---")
try:
    similar_words = model.wv.most_similar('machine')
    for word, similarity in similar_words:
        print(f"{word}: {similarity:.4f}")
except KeyError:
    print("\n'machine' not found in vocabulary.")

print("\n--- Most Similar Words to 'dog' ---")
try:
    similar_words_dog = model.wv.most_similar('dog')
    for word, similarity in similar_words_dog:
        print(f"{word}: {similarity:.4f}")
except KeyError:
    print("\n'dog' not found in vocabulary.")


# Perform word analogies (e.g., King - Man + Woman = Queen)
# This may not work perfectly with very small datasets, but demonstrates the concept.
print("\n--- Word Analogies (King - Man + Woman = ?) ---")
try:
    result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)
    if result:
        print(f"King - Man + Woman is similar to: {result[0][0]} (similarity: {result[0][1]:.4f})")
    else:
        print("No result for analogy. Vocabulary might be too small.")
except KeyError as e:
    print(f"One or more words for analogy not found in vocabulary: {e}")
except Exception as e:
    print(f"An error occurred during analogy: {e}")

# Check similarity between two words
print("\n--- Similarity between 'machine' and 'learning' ---")
try:
    similarity = model.wv.similarity('machine', 'learning')
    print(f"Similarity: {similarity:.4f}")
except KeyError:
    print("One or both words not found in vocabulary.")

print("\n--- Similarity between 'dog' and 'cat' ---")
try:
    similarity_pets = model.wv.similarity('dog', 'cat')
    print(f"Similarity: {similarity_pets:.4f}")
except KeyError:
    print("One or both words not found in vocabulary.")

print("\n--- Similarity between 'dog' and 'computer' ---")
try:
    similarity_diff = model.wv.similarity('dog', 'computer')
    print(f"Similarity: {similarity_diff:.4f}")
except KeyError:
    print("One or both words not found in vocabulary.")

# --- 4. Save and Load the Model ---
model_path = "word2vec_model.bin"
model.save(model_path)
print(f"\nModel saved to {model_path}")

# Load the model back
loaded_model = Word2Vec.load(model_path)
print(f"Model loaded from {model_path}")

# Verify loaded model
print("\n--- Verify Loaded Model (Most Similar Words to 'machine' using loaded model) ---")
try:
    similar_words_loaded = loaded_model.wv.most_similar('machine')
    for word, similarity in similar_words_loaded:
        print(f"{word}: {similarity:.4f}")
except KeyError:
    print("\n'machine' not found in vocabulary in loaded model.")

print("\nScript execution complete.")
```

**How to Run the Script:**

1. Save the code above as a Python file (e.g., `word2vec_gensim_example.py`).
2. Open your terminal or command prompt.
3. Navigate to the directory where you saved the file.
4. Run the script using: `python word2vec_gensim_example.py`

-----

### Key Concepts in Word2Vec (`gensim` implementation)

* **`gensim.models.Word2Vec`**: The main class for training.
* **`sentences`**: An iterable of iterables, where the outer iterable is the corpus and the inner iterables are lists of words (tokenized sentences).
* **`vector_size`**: The number of dimensions for the word vectors. Higher dimensions can capture more nuances but require more data and computation.
* **`window`**: The maximum distance between the current word and the words around it in a sentence.
* **`min_count`**: Words that appear fewer times than `min_count` are ignored. This helps filter out very rare words that might not have meaningful embeddings.
* **`sg` (Skip-gram vs. CBOW)**:
  * `sg=0` (CBOW - Continuous Bag of Words): Predicts the current word based on its context. Faster to train.
  * `sg=1` (Skip-gram): Predicts surrounding words given the current word. Generally performs better for rare words.
* **`workers`**: Number of CPU cores to use for training, speeding up the process.
* **`epochs`**: Number of times the algorithm iterates over the entire dataset. More epochs can lead to better quality embeddings but also take longer.
* **`model.wv`**: The "word vectors" object (`KeyedVectors`) which contains the trained word embeddings and methods like `most_similar`, `similarity`, etc. You can also access vectors directly like `model.wv['word']`.

-----

This `gensim` script provides a solid foundation for working with Word2Vec. For real-world applications, you would typically use a much larger corpus (e.g., Wikipedia, Common Crawl) and tune the hyperparameters for optimal performance.
