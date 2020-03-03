from requeWeblio import WordMeaning
from saveToDb import create_table,insert_data
from memorize import MemorizeVocabulary
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
    word = WordMeaning(keyword=keyword).exec()
    word.update({"save_time": str(datetime.datetime.today())})
    valuelst = [item for item in word.values()]
    trantab = str.maketrans("',()", "    ")
    for ind in range(len(valuelst)):
        valuelst[ind] = valuelst[ind].translate(trantab)
    # print("//////////////",valuelst)
    insert_data(valuelst)


if __name__ == '__main__':
    print("------------ search word or memory word ------------")
    print("------------ 1 search word ------------")
    print("------------ 2 memory word ------------")
    print("------------ 3 exist ------------")
    while True:
        choice = input("1 - 3 : ")
        if choice == "1":
            keyword = input("word : ")
            create_table()
            save_to_db(keyword=keyword)
        elif choice == "2":
            MemorizeVocabulary().memory_main()
        elif choice == "3":
            break


