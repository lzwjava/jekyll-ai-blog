from gensim.corpora import WikiCorpus

# This automatically handles .bz2 and extracts text + tokenizes
wiki = WikiCorpus(
    "wiki_train/enwiki-latest-pages-articles1.xml-p1p41242.bz2", dictionary=False
)

# Iterate over articles
with open("wiki_train/output.txt", "w", encoding="utf-8") as f:
    for i, text in enumerate(wiki.get_texts()):
        f.write(" ".join(text) + "\n")
        if i % 10000 == 0:
            print(f"Processed {i} articles")
