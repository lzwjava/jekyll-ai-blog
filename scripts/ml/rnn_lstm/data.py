from collections import defaultdict

import numpy as np
from torch.utils import data

np.random.seed(42)


def generate_dataset(num_sequences=100):
    samples = []

    for _ in range(num_sequences):
        num_tokens = np.random.randint(1, 10)
        sample = ["a"] * num_tokens + ["b"] * num_tokens + ["EOS"]
        samples.append(sample)

    return samples


sequences = generate_dataset()

print("A single sample from the generated dataset:")
print(sequences[0])


def sequences_to_dicts(sequences):
    flatten = lambda l: [item for sublist in l for item in sublist]

    all_words = flatten(sequences)

    word_count = defaultdict(int)
    for word in flatten(sequences):
        word_count[word] += 1

    word_count = sorted(list(word_count.items()), key=lambda l: -l[1])

    unique_words = [item[0] for item in word_count]

    unique_words.append("UNK")

    num_sentences, vocab_size = len(sequences), len(unique_words)

    word_to_idx = defaultdict(lambda: num_words)
    idx_to_word = defaultdict(lambda: "UNK")

    for idx, word in enumerate(unique_words):
        word_to_idx[word] = idx
        idx_to_word[idx] = word

    return word_to_idx, idx_to_word, num_sentences, vocab_size


word_to_idx, idx_to_word, num_sequences, vocab_size = sequences_to_dicts(sequences)

print(
    f"We have {num_sequences} sentences and {len(word_to_idx)} unique tokens in our dataset (including UNK).\n"
)
print("The index of 'b' is", word_to_idx["b"])
print(f"The word corresponding to index 1 is '{idx_to_word[1]}'")


class Dataset(data.Dataset):
    def __init__(self, inputs, targets):
        self.inputs = inputs
        self.targets = targets

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, index):
        X = self.inputs[index]
        y = self.targets[index]

        return X, y


def create_datasets(sequences, dataset_class, p_train=0.8, p_val=0.1, p_test=0.1):
    num_train = int(len(sequences) * p_train)
    num_val = int(len(sequences) * p_val)
    num_test = int(len(sequences) * p_test)

    sequences_train = sequences[:num_train]
    sequences_val = sequences[num_train : num_train + num_val]
    sequences_test = sequences[-num_test:]

    def get_inputs_targets_from_sequences(sequences):
        inputs, targets = [], []

        for sequence in sequences:
            inputs.append(sequence[:-1])
            targets.append(sequence[1:])

        return inputs, targets

    inputs_train, targets_train = get_inputs_targets_from_sequences(sequences_train)
    inputs_val, targets_val = get_inputs_targets_from_sequences(sequences_val)
    inputs_test, targets_test = get_inputs_targets_from_sequences(sequences_test)

    training_set = dataset_class(inputs_train, targets_train)
    validation_set = dataset_class(inputs_val, targets_val)
    test_set = dataset_class(inputs_test, targets_test)

    return training_set, validation_set, test_set


training_set, validation_set, test_set = create_datasets(sequences, Dataset)

print(f"We have {len(training_set)} samples in the training set.")
print(f"We have {len(validation_set)} samples in the validation set.")
print(f"We have {len(test_set)} samples in the test set.")


def one_hot_encode(idx, vocab_size):
    one_hot = np.zeros(vocab_size)

    one_hot[idx] = 1.0

    return one_hot


def one_hot_encode_sequence(sequence, vocab_size):
    encoding = np.array(
        [one_hot_encode(word_to_idx[word], vocab_size) for word in sequence]
    )

    encoding = encoding.reshape(encoding.shape[0], encoding.shape[1], 1)

    return encoding


test_word = one_hot_encode(word_to_idx["a"], vocab_size)
print(f"Our one-hot encoding of 'a' has shape {test_word.shape}.")

test_sentence = one_hot_encode_sequence(["a", "b"], vocab_size)
print(f"Our one-hot encoding of 'a b' has shape {test_sentence.shape}.")

hidden_size = 50
vocab_size = len(word_to_idx)
