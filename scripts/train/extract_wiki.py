from mediawiki_dump.tokenizer import WikiTokenizer

with open(
    "wiki_train/wikipedia_test_5files_parallel/enwiki-latest-pages-articles1.xml-p1p41242.bz2",
    "rb",
) as dump:
    tokenizer = WikiTokenizer(dump)
    for token in tokenizer:
        if token.type == "text":
            print(token.value)
