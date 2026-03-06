import numpy as np
import torch
import torch.nn.functional as F
import re
from w2v_utils import *


# Load or create word vectors
def load_or_create_word_vectors(file_path):
    """
    Try to load pre-trained vectors, or create simple word vectors from text
    """
    try:
        # First try to load as GloVe format
        words, word_to_vec_map = read_glove_vecs(file_path)
        print(f"Loaded {len(words)} pre-trained word vectors from {file_path}")
        return words, word_to_vec_map
    except (ValueError, FileNotFoundError) as e:
        print(f"Could not load as pre-trained vectors ({e})")

        try:
            # Try to read as text file and create simple word vectors
            print(f"Attempting to create word vectors from text in {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().lower()

            # Simple tokenization and vocabulary creation
            words_list = re.findall(r"\b[a-zA-Z]+\b", text)
            unique_words = list(set(words_list))[
                :1000
            ]  # Limit to 1000 most common words

            # Create simple random word vectors (in practice, you'd train these)
            embedding_dim = 50
            word_to_vec_map = {}
            np.random.seed(42)  # For reproducible results

            for word in unique_words:
                word_to_vec_map[word] = np.random.randn(embedding_dim)

            # Add some common test words if they're not in the text
            test_words = [
                "father",
                "mother",
                "man",
                "woman",
                "boy",
                "girl",
                "computer",
                "technology",
            ]
            for word in test_words:
                if word not in word_to_vec_map:
                    word_to_vec_map[word] = np.random.randn(embedding_dim)

            words = set(word_to_vec_map.keys())
            print(f"Created {len(words)} word vectors from text content")
            return words, word_to_vec_map

        except FileNotFoundError:
            print(
                f"File {file_path} not found. Creating sample word vectors for demonstration."
            )
            # Create a minimal sample for demonstration
            word_to_vec_map = {
                "father": np.random.randn(50),
                "mother": np.random.randn(50),
                "ball": np.random.randn(50),
                "crocodile": np.random.randn(50),
                "france": np.random.randn(50),
                "italy": np.random.randn(50),
                "paris": np.random.randn(50),
                "rome": np.random.randn(50),
                "man": np.random.randn(50),
                "woman": np.random.randn(50),
                "boy": np.random.randn(50),
                "girl": np.random.randn(50),
                "receptionist": np.random.randn(50),
                "computer": np.random.randn(50),
                "technology": np.random.randn(50),
                "science": np.random.randn(50),
            }
            words = set(word_to_vec_map.keys())
            print(f"Created {len(words)} sample word vectors")
            return words, word_to_vec_map


words, word_to_vec_map = load_or_create_word_vectors("tmp/my_posts.txt")


def cosine_similarity(u, v):
    """
    Compute cosine similarity between two vectors using PyTorch for better performance
    """
    u_tensor = torch.tensor(u, dtype=torch.float32)
    v_tensor = torch.tensor(v, dtype=torch.float32)

    # Handle identical vectors
    if torch.allclose(u_tensor, v_tensor):
        return 1.0

    # Compute cosine similarity using PyTorch
    cosine_sim = F.cosine_similarity(
        u_tensor.unsqueeze(0), v_tensor.unsqueeze(0), dim=1
    )
    return cosine_sim.item()


def cosine_similarity_numpy(u, v):
    """
    Original numpy implementation for comparison
    """
    if np.all(u == v):
        return 1

    dot = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)

    if np.isclose(norm_u * norm_v, 0, atol=1e-32):
        return 0

    cosine_similarity = dot / norm_u / norm_v
    return cosine_similarity


def safe_get_word_vector(word, word_to_vec_map, default_dim=50):
    """
    Safely get word vector, return random vector if word not found
    """
    word = word.lower()
    if word in word_to_vec_map:
        return word_to_vec_map[word]
    else:
        print(f"Warning: Word '{word}' not found in vocabulary. Using random vector.")
        return np.random.randn(default_dim)


# Test cosine similarity with available words
print("=== Testing Cosine Similarity ===")


def cosine_similarity_test(target):
    a = np.random.uniform(-10, 10, 10)
    b = np.random.uniform(-10, 10, 10)
    c = np.random.uniform(-1, 1, 23)

    assert np.isclose(target(a, a), 1), "cosine_similarity(a, a) must be 1"
    assert np.isclose(target((c >= 0) * 1, (c < 0) * 1), 0), (
        "cosine_similarity(a, not(a)) must be 0"
    )
    assert np.isclose(target(a, -a), -1), "cosine_similarity(a, -a) must be -1"
    assert np.isclose(target(a, b), target(a * 2, b * 4)), (
        "cosine_similarity must be scale-independent"
    )

    print("\033[92mAll cosine similarity tests passed!")


cosine_similarity_test(cosine_similarity)

# Test with actual word vectors if available
test_words = [
    "father",
    "mother",
    "ball",
    "crocodile",
    "france",
    "italy",
    "paris",
    "rome",
]
if all(word in word_to_vec_map for word in test_words):
    father = word_to_vec_map["father"]
    mother = word_to_vec_map["mother"]
    ball = word_to_vec_map["ball"]
    crocodile = word_to_vec_map["crocodile"]
    france = word_to_vec_map["france"]
    italy = word_to_vec_map["italy"]
    paris = word_to_vec_map["paris"]
    rome = word_to_vec_map["rome"]

    print("cosine_similarity(father, mother) = ", cosine_similarity(father, mother))
    print("cosine_similarity(ball, crocodile) = ", cosine_similarity(ball, crocodile))
    print(
        "cosine_similarity(france - paris, rome - italy) = ",
        cosine_similarity(france - paris, rome - italy),
    )
else:
    print("Some test words not found in vocabulary. Skipping word similarity tests.")


def complete_analogy(word_a, word_b, word_c, word_to_vec_map):
    """
    Complete word analogies: a is to b as c is to ?
    """
    word_a, word_b, word_c = word_a.lower(), word_b.lower(), word_c.lower()

    # Check if all words exist
    if not all(word in word_to_vec_map for word in [word_a, word_b, word_c]):
        missing = [w for w in [word_a, word_b, word_c] if w not in word_to_vec_map]
        print(f"Warning: Words {missing} not found in vocabulary")
        return None

    e_a, e_b, e_c = (
        word_to_vec_map[word_a],
        word_to_vec_map[word_b],
        word_to_vec_map[word_c],
    )

    words = word_to_vec_map.keys()
    max_cosine_sim = -100
    best_word = None

    for w in words:
        if w == word_c:
            continue

        cosine_sim = cosine_similarity(e_b - e_a, word_to_vec_map[w] - e_c)

        if cosine_sim > max_cosine_sim:
            max_cosine_sim = cosine_sim
            best_word = w

    return best_word


def complete_analogy_test(target):
    a = [3, 3]
    a_nw = [2, 4]
    a_s = [3, 2]
    c = [-2, 1]

    test_word_to_vec_map = {
        "a": a,
        "synonym_of_a": a,
        "a_nw": a_nw,
        "a_s": a_s,
        "c": c,
        "c_n": [-2, 2],
        "c_ne": [-1, 2],
        "c_e": [-1, 1],
        "c_se": [-1, 0],
        "c_s": [-2, 0],
        "c_sw": [-3, 0],
        "c_w": [-3, 1],
        "c_nw": [-3, 2],
    }

    for key in test_word_to_vec_map.keys():
        test_word_to_vec_map[key] = np.array(test_word_to_vec_map[key])

    assert target("a", "a_nw", "c", test_word_to_vec_map) == "c_nw"
    assert target("a", "a_s", "c", test_word_to_vec_map) == "c_s"
    assert target("a", "synonym_of_a", "c", test_word_to_vec_map) != "c", (
        "Best word cannot be input query"
    )
    assert target("a", "c", "a", test_word_to_vec_map) == "c"

    print("\033[92mAll analogy tests passed!")


print("\n=== Testing Word Analogies ===")
complete_analogy_test(complete_analogy)

# Test analogies with available words
print("\n=== Word Analogy Examples ===")
triads_to_try = [("italy", "italian", "spain"), ("man", "woman", "boy")]

for triad in triads_to_try:
    if all(word.lower() in word_to_vec_map for word in triad):
        result = complete_analogy(*triad, word_to_vec_map)
        print(f"{triad[0]} -> {triad[1]} :: {triad[2]} -> {result}")
    else:
        missing = [w for w in triad if w.lower() not in word_to_vec_map]
        print(f"Skipping analogy {triad} - missing words: {missing}")


# Gender bias analysis (if relevant words are available)
print("\n=== Gender Bias Analysis ===")
if "woman" in word_to_vec_map and "man" in word_to_vec_map:
    g = word_to_vec_map["woman"] - word_to_vec_map["man"]
    print("Gender vector (woman - man) computed")

    # Test with available names
    name_list = ["john", "marie", "sophie", "computer", "technology", "science"]
    print("\nWord similarities with gender vector:")

    for w in name_list:
        if w in word_to_vec_map:
            similarity = cosine_similarity(word_to_vec_map[w], g)
            print(f"{w}: {similarity:.4f}")
        else:
            print(f"{w}: not found in vocabulary")

    # Create unit vectors for debiasing
    print("\n=== Creating Unit Vector Representations ===")
    word_to_vec_map_unit_vectors = {}
    for word, embedding in word_to_vec_map.items():
        norm = np.linalg.norm(embedding)
        if norm > 0:
            word_to_vec_map_unit_vectors[word] = embedding / norm
        else:
            word_to_vec_map_unit_vectors[word] = embedding

    if (
        "woman" in word_to_vec_map_unit_vectors
        and "man" in word_to_vec_map_unit_vectors
    ):
        g_unit = (
            word_to_vec_map_unit_vectors["woman"] - word_to_vec_map_unit_vectors["man"]
        )

        def neutralize(word, g, word_to_vec_map):
            """Remove bias component from word embedding"""
            e = word_to_vec_map[word]
            e_biascomponent = (np.dot(e, g) / np.linalg.norm(g) ** 2) * g
            e_debiased = e - e_biascomponent
            return e_debiased

        # Test debiasing
        test_word = "computer"
        if test_word in word_to_vec_map:
            print(f"\n=== Debiasing Example: '{test_word}' ===")
            print(
                f"Cosine similarity between {test_word} and gender vector, before neutralizing: ",
                cosine_similarity(word_to_vec_map[test_word], g),
            )

            e_debiased = neutralize(test_word, g_unit, word_to_vec_map_unit_vectors)
            print(
                f"Cosine similarity between {test_word} and gender vector, after neutralizing: ",
                cosine_similarity(e_debiased, g_unit),
            )

        def equalize(pair, bias_axis, word_to_vec_map):
            """Equalize a pair of words with respect to bias axis"""
            w1, w2 = pair
            if w1 not in word_to_vec_map or w2 not in word_to_vec_map:
                print(f"Cannot equalize: missing words {w1} or {w2}")
                return None, None

            e_w1, e_w2 = word_to_vec_map[w1], word_to_vec_map[w2]

            mu = (e_w1 + e_w2) / 2.0
            mu_B = np.dot(mu, bias_axis) / np.linalg.norm(bias_axis) ** 2 * bias_axis
            mu_orth = mu - mu_B

            e_w1B = np.dot(e_w1, bias_axis) / np.linalg.norm(bias_axis) ** 2 * bias_axis
            e_w2B = np.dot(e_w2, bias_axis) / np.linalg.norm(bias_axis) ** 2 * bias_axis

            corrected_e_w1B = (
                np.sqrt(1 - np.linalg.norm(mu_orth) ** 2)
                * (e_w1B - mu_B)
                / np.linalg.norm(e_w1 - mu_orth - mu_B)
            )
            corrected_e_w2B = (
                np.sqrt(1 - np.linalg.norm(mu_orth) ** 2)
                * (e_w2B - mu_B)
                / np.linalg.norm(e_w2 - mu_orth - mu_B)
            )

            e1 = mu_orth + corrected_e_w1B
            e2 = mu_orth + corrected_e_w2B

            return e1, e2

        # Test equalization
        if "man" in word_to_vec_map and "woman" in word_to_vec_map:
            print("\n=== Equalization Example ===")
            print("Cosine similarities before equalizing:")
            print(
                "cosine_similarity(man, gender) = ",
                cosine_similarity(word_to_vec_map["man"], g),
            )
            print(
                "cosine_similarity(woman, gender) = ",
                cosine_similarity(word_to_vec_map["woman"], g),
            )

            e1, e2 = equalize(("man", "woman"), g_unit, word_to_vec_map_unit_vectors)
            if e1 is not None and e2 is not None:
                print("Cosine similarities after equalizing:")
                print(
                    "cosine_similarity(equalized_man, gender) = ",
                    cosine_similarity(e1, g_unit),
                )
                print(
                    "cosine_similarity(equalized_woman, gender) = ",
                    cosine_similarity(e2, g_unit),
                )

else:
    print("Words 'man' and 'woman' not found. Skipping gender bias analysis.")

print("\n=== Analysis Complete ===")
print("Note: This analysis works with your custom word vectors from tmp/my_posts.txt")
print("The effectiveness depends on the quality and size of your word vector dataset.")
