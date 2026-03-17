def word_frequency(text):
    text = text.lower()
    for ch in [".", ",", "!", "?", ":", ";", "'", "\"", "(", ")", "-", "\n"]:
        text = text.replace(ch, " ")
    words = text.split()

    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


paragraph = (
    "Python is simple, but it is powerful. "
    "Python is used in web development, data analysis, and automation. "
    "If you practice a little every day, Python becomes easier and easier!"
)

freq = word_frequency(paragraph)
top_5 = sorted(freq.items(), key=lambda item: item[1], reverse=True)[:5]

for word, count in top_5:
    print(word, "->", count)

