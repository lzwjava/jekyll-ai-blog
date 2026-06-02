import re

# Lyrics data: (Japanese, Romaji) pairs
lyrics = [
    ("呼んでいる 胸のどこか奥で", "Yondeiru mune no dokoka oku de"),
    ("いつも心 踊る夢を見たい", "Itsumo kokoro odoru yume o mitai"),
    ("悲しみは 数えきれないけれど", "Kanashimi wa kazoekirenai keredo"),
    ("その向こうできっと あなたに会える", "Sono mukou de kitto anata ni aeru"),
    ("繰り返すあやまちの そのたび 人は", "Kurikaesu ayamachi no sono tabi hito wa"),
    ("ただ青い空の 青さを知る", "Tada aoi sora no aosa o shiru"),
    ("果てしなく道は続いて見えるけれど", "Hateshinaku michi wa tsuzuite mieru keredo"),
    ("この両手は 光を抱ける", "Kono ryoute wa hikari o dakeru"),
    ("さよならの時の 静かな胸", "Sayonara no toki no shizuka na mune"),
    ("ゼロになるからだが 耳をすませる", "Zero ni naru karada ga mimi o sumaseru"),
    ("生きている 不思議 死んでいく 不思議", "Ikiteiru fushigi shindeiku fushigi"),
    ("花も風も街も みんな同じ", "Hana mo kaze mo machi mo minna onaji"),
    ("呼んでいる 胸のどこか奥で", "Yondeiru mune no dokoka oku de"),
    ("いつも何度でも 夢を描こう", "Itsumo nando demo yume o egakou"),
    ("悲しみの数を 言い尽くすより", "Kanashimi no kazu o iitsukusu yori"),
    ("同じ唇で そっと歌おう", "Onaji kuchibiru de sotto utaou"),
    ("閉じていく 思い出の その中にいつも", "Tojiteiku omoide no sono naka ni itsumo"),
    ("忘れたくない ささやきを聞く", "Wasuretakunai sasayaki o kiku"),
    ("粉々に砕かれた 鏡の上にも", "Konagona ni kudakareta kagami no ue ni mo"),
    ("新しい景色が 映される", "Atarashii keshiki ga utsusareru"),
    ("はじまりの朝の 静かな窓", "Hajimari no asa no shizuka na mado"),
    ("ゼロになるからだ 充たされてゆけ", "Zero ni naru karada mitasarete yuke"),
    ("海の彼方には もう探さない", "Umi no kanata ni wa mou sagasanai"),
    ("輝くものは いつもここに", "Kagayaku mono wa itsumo koko ni"),
    ("わたしのなかに 見つけられたから", "Watashi no naka ni mitsukerareta kara"),
]


def split_japanese(line):
    # Split Japanese line into words/phrases based on spaces or natural breaks
    return re.split(r"\s+", line.strip())


def split_romaji(line, jap_segments):
    # Split romaji to match Japanese segments
    romaji_words = re.split(r"\s+", line.strip())
    # Ensure romaji segments match Japanese segments in number
    if len(romaji_words) != len(jap_segments):
        # Adjust romaji to match Japanese segmentation
        romaji_words = []
        romaji_index = 0
        for jap_seg in jap_segments:
            jap_len = len(jap_seg)
            temp = ""
            while romaji_index < len(line) and (not temp or len(temp) < jap_len):
                temp += line[romaji_index]
                romaji_index += 1
            romaji_words.append(temp.strip())
    return romaji_words


def align_segments(jap_segments, romaji_segments):
    aligned_pairs = []
    for jap, rom in zip(jap_segments, romaji_segments):
        # Count width: 1 Japanese char ≈ 2.5 Latin chars in monospaced font
        jap_width = len(jap) * 2.5
        rom_width = len(rom)
        # Pad romaji with spaces to match Japanese width
        padding = " " * max(0, int(jap_width - rom_width))
        aligned_pairs.append((jap, rom + padding))
    return aligned_pairs


def format_lyrics(lyrics):
    output = []
    for jap_line, rom_line in lyrics:
        jap_segments = split_japanese(jap_line)
        rom_segments = split_romaji(rom_line, jap_segments)
        aligned_pairs = align_segments(jap_segments, rom_segments)

        # Format Japanese and romaji lines
        jap_formatted = " ".join(jap for jap, _ in aligned_pairs)
        rom_formatted = " ".join(rom for _, rom in aligned_pairs)

        output.append(jap_formatted)
        output.append(rom_formatted)
        output.append("")  # Blank line for readability

    return "\n".join(output)


# Generate and print the aligned lyrics
aligned_text = format_lyrics(lyrics)
print(aligned_text)

# Optionally, save to a file
with open("aligned_lyrics.txt", "w", encoding="utf-8") as f:
    f.write(aligned_text)
