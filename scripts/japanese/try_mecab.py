import MeCab

t = MeCab.Tagger("-r /opt/homebrew/etc/mecabrc")
sentence = "太郎はこの本を女性に渡した。"
result = t.parse(sentence)

print("MeCab format explanation:")
print(
    "Surface\tPOS1,POS2,POS3,POS4,Inflection Type,Inflection Form,Base Form,Reading,Pronunciation"
)
print("\nDetailed analysis:")
for line in result.split("\n"):
    if line == "EOS" or not line.strip():
        continue
    parts = line.split("\t")
    if len(parts) == 2:
        surface = parts[0]
        features = parts[1].split(",")
        print(f"\nWord: {surface}")
        print(f"POS1 (品詞): {features[0]}")  # Part of Speech
        print(f"POS2 (品詞細分類1): {features[1]}")  # Subcategory 1
        print(f"POS3 (品詞細分類2): {features[2]}")  # Subcategory 2
        print(f"POS4 (品詞細分類3): {features[3]}")  # Subcategory 3
        print(f"Inflection Type (活用型): {features[4]}")  # Conjugation type
        print(f"Inflection Form (活用形): {features[5]}")  # Conjugation form
        print(f"Base Form (原形): {features[6]}")  # Dictionary form
        print(f"Reading (読み): {features[7]}")  # Reading in kana
        if len(features) > 8:
            print(f"Pronunciation (発音): {features[8]}")  # Pronunciation
