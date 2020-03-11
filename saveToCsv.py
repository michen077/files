import csv
import datetime


FIELDNAME = ["kanji","kana","jp_explanation","explanation","phrase1_jp","phrase1_en","phrase2_jp","phrase2_en","phrase3_jp","phrase3_en","phrase4_jp","phrase4_en","phrase5_jp","phrase5_en","memory_times","save_time","last_updated"]

VOCABULARY = open("vocabulary_shiftjis.csv","a+",encoding="shiftjis",newline="\n")

def save_to_csv(word_dict):
    writer = csv.DictWriter(VOCABULARY, fieldnames=FIELDNAME)
    word_dict.update({"save_time": get_save_time()})
    if not search_from_csv(word_dict["kanji"]):
        writer.writerow(word_dict)


def search_from_csv(keyword=None):
    vocabulary = open("vocabulary_shiftjis.csv", "r", encoding="shiftjis")
    reader = csv.DictReader(vocabulary)
    wordlst = []
    for dict in reader:
        wordlst.append(dict)
        for k,v in dict.items():
            if keyword and v == keyword:
                    return dict
            else:
                return None
    return wordlst


def get_save_time():
    current_time = datetime.datetime.today()
    return current_time

if __name__ == '__main__':
    search_from_csv()