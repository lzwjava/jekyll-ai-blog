import gc

import pandas as pd

from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier

import string


from sklearn.feature_extraction.text import TfidfVectorizer

from transformers import PreTrainedTokenizerFast
from tokenizers import (
    models,
    normalizers,
    pre_tokenizers,
    trainers,
    Tokenizer,
)

from datasets import Dataset
from tqdm.auto import tqdm

# dir_name = '/kaggle/input/llm-detect-ai-generated-text/'

dir_name = "./"

test = pd.read_csv(dir_name + "test_essays.csv")
sub = pd.read_csv(dir_name + "sample_submission.csv")
org_train = pd.read_csv(dir_name + "train_essays.csv")

# train1 = pd.read_csv("/kaggle/input/daigt-v2-train-dataset/train_v2_drcat_02.csv", sep=',')
# train2 = pd.read_csv('/kaggle/input/daigt-proper-train-dataset/train_drcat_04.csv')
# train3 = pd.read_csv('/kaggle/input/argugpt/argugpt.csv')[['id', 'text', 'model']]

org_train = org_train.drop(columns=["prompt_id", "id"])
org_train = org_train.rename(columns={"generated": "label"})
# train1 = train1.drop(columns=["prompt_name", "source", "RDizzl3_seven"])
# train2 = train2.drop(columns=["essay_id", "source", "prompt", "fold"])
# train3 = train3.drop(columns=["id"])
# train3 = train3.rename(columns={'model': 'label'})
# train3["label"] = 1

train = pd.concat([org_train])

train.reset_index(drop=True, inplace=True)
train = train.drop_duplicates(subset=["text"])
train.reset_index(drop=True, inplace=True)

train.head(2)

test.head(5)

unique_words = set()
for text in train["text"]:
    words = text.lower().split()  # Convert to lowercase and split into words
    unique_words.update(words)

unique_words = {word.strip(string.punctuation) for word in unique_words}

total_unique_words = len(unique_words)
print("Total unique words:", total_unique_words)

LOWERCASE = False
VOCAB_SIZE = total_unique_words // 2

raw_tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))

raw_tokenizer.normalizer = normalizers.Sequence(
    [normalizers.NFC()] + [normalizers.Lowercase()] if LOWERCASE else []
)
raw_tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()

special_tokens = ["[UNK]", "[SEP]"]
trainer = trainers.BpeTrainer(vocab_size=VOCAB_SIZE, special_tokens=special_tokens)

dataset = Dataset.from_pandas(test[["text"]])


def train_corp_iter():
    for i in range(0, len(dataset), 1000):
        yield dataset[i : i + 1000]["text"]


raw_tokenizer.train_from_iterator(train_corp_iter(), trainer=trainer)

tokenizer = PreTrainedTokenizerFast(
    tokenizer_object=raw_tokenizer,
    unk_token="[UNK]",
    sep_token="[SEP]",
)

tokenized_texts_test = []
for text in tqdm(test["text"].tolist()):
    tokenized_texts_test.append(tokenizer.tokenize(text))

tokenized_texts_train = []
for text in tqdm(train["text"].tolist()):
    tokenized_texts_train.append(tokenizer.tokenize(text))

tokenized_texts_test[1]


def dummy(text):
    return text


vectorizer = TfidfVectorizer(
    ngram_range=(3, 5),
    lowercase=False,
    sublinear_tf=True,
    analyzer="word",
    tokenizer=dummy,
    preprocessor=dummy,
    token_pattern=None,
    strip_accents="unicode",
)

vectorizer.fit(tokenized_texts_test)
vocab = vectorizer.vocabulary_  # Extract learned vocabulary

vectorizer = TfidfVectorizer(
    ngram_range=(3, 5),
    lowercase=False,
    sublinear_tf=True,
    vocabulary=vocab,
    analyzer="word",
    tokenizer=dummy,
    preprocessor=dummy,
    token_pattern=None,
    strip_accents="unicode",
)

tf_train = vectorizer.fit_transform(tokenized_texts_train)
tf_test = vectorizer.transform(tokenized_texts_test)

del vectorizer
gc.collect()

print_bool = False

if print_bool:
    tf_demonstration_vector = tf_test.copy()
    tf_idf_array = tf_demonstration_vector.toarray()

    print("As can be seen, we do indeed have a sparse matrix:")
    print(type(tf_demonstration_vector), tf_demonstration_vector.shape)
    print("")
    print(tf_idf_array)

y_train = train["label"].values

if len(test.text.values) <= 5:
    sub.to_csv("submission.csv", index=False)

else:
    clf = MultinomialNB(alpha=0.02)
    sgd_model = SGDClassifier(max_iter=8000, tol=1e-4, loss="modified_huber")
    p6 = {
        "n_iter": 1500,
        "verbose": -1,
        "objective": "binary",
        "metric": "auc",
        "learning_rate": 0.05073909898961407,
        "colsample_bytree": 0.726023996436955,
        "colsample_bynode": 0.5803681307354022,
        "lambda_l1": 8.562963348932286,
        "lambda_l2": 4.893256185259296,
        "min_data_in_leaf": 115,
        "max_depth": 23,
        "max_bin": 898,
    }
    lgb = LGBMClassifier(**p6)
    cat = CatBoostClassifier(
        iterations=1000,
        verbose=0,
        l2_leaf_reg=6.6591278779517808,
        learning_rate=0.005689066836106983,
        allow_const_label=True,
        loss_function="CrossEntropy",
    )
    weights = [0.07, 0.31, 0.31, 0.31]

    ensemble = VotingClassifier(
        estimators=[("mnb", clf), ("sgd", sgd_model), ("lgb", lgb), ("cat", cat)],
        weights=weights,
        voting="soft",
        n_jobs=-1,
    )
    ensemble.fit(tf_train, y_train)
    gc.collect()
    final_preds = ensemble.predict_proba(tf_test)[:, 1]
    sub["generated"] = final_preds
    sub.to_csv("submission.csv", index=False)
    sub
