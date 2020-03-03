from requeWeblio import WordMeaning
from saveToDb import insert_data
import saveToCsv
import time
import datetime

def save_and_search(keyword):
    word = WordMeaning(keyword=keyword).exec()
    time.sleep(3)
    saveToCsv.save_to_csv(word_dict=word)
    time.sleep(3)
    saveToCsv.search_from_csv(keyword=keyword)
    print("--------------- save_and_search end ------------------")
    return word

def save_to_db(keyword):
    word = WordMeaning(keyword=k).exec()
    word.update({"save_time": str(datetime.datetime.today())})
    valuelst = [item for item in word.values()]
    trantab = str.maketrans("',()", "    ")
    for ind in range(len(valuelst)):
        valuelst[ind] = valuelst[ind].translate(trantab)
    # print("//////////////",valuelst)
    insert_data(valuelst)


if __name__ == '__main__':
    wordlst = ["明かす","赤らむ","あざ笑う","焦る","誂える","愛想","間柄","敢えて","あくどい","痣","浅ましい","欺く"]
    for k in wordlst:
        save_to_db(keyword=k)

