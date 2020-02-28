from requeWeblio import WordMeaning
import saveToData
import time

def save_and_search(keyword):
    word = WordMeaning(keyword=keyword).exec()
    time.sleep(3)
    saveToData.save_to_csv(word_dict=word)
    time.sleep(3)
    result = saveToData.search_from_csv(keyword=keyword)
    print("--------------- end ------------------")


if __name__ == '__main__':
    wordlst = ["明かす","赤らむ","あざ笑う","焦る","誂える"]
    for k in wordlst:
        save_and_search(k)
