import hanlp

HanLP = hanlp.load(
    hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH
)

import os  # noqa: E402

directory_path = "./_posts"

files = sorted(os.listdir(directory_path))

for file in files:
    file_path = os.path.join(directory_path, file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        # print(f'content length: {len(content)}')

        print(f"{f.name}")

        paragraphs = content.split("\n\n")

        for paragraph in paragraphs:
            # print(f'paragraph length: {len(paragraph)}')

            result = HanLP(paragraph)
            # print(result)

            pku = result["ner/pku"]

            for i in range(len(pku)):
                item = pku[i]
                if item[1] == "nr":
                    print(item)
