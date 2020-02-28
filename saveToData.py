import csv

with open("vocabulary_book.csv","a+",encoding="utf8") as VOCABULARYBOOK:
    pass

def save_to_csv(word_dict):
    fieldnames = ["kanji","kana","phrase1_jp","phrase1_en","phrase2_jp","phrase2_en","phrase3_jp","phrase3_en","phrase4_jp","phrase4_en","phrase5_jp","phrase5_en",]
    writer = csv.DictWriter(VOCABULARYBOOK, fieldnames=fieldnames)
    writer.writerow(word_dict)

def load_fromt_csv():
    pass
