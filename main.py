import saveToCsv
import time
import datetime
from requeWeblio import WordMeaning
from ope_database import sql_exec,create_table,insert_data,list_all_kanji,delete_from_db,check_review
from memorize import MemorizeVocabulary

def db_check_review():
    check_review()


def save_and_search(keyword):
    word = WordMeaning(keyword=keyword).exec()
    time.sleep(3)
    saveToCsv.save_to_csv(word_dict=word)
    time.sleep(3)
    saveToCsv.search_from_csv(keyword=keyword)
    print("--------------- save_and_search end ------------------")
    return word

def save_to_db(keyword):
    if keyword:
        word = WordMeaning(keyword=keyword).exec()
        choice = input("if save to vocabulary book? 1 yes 2 no : ")
        if choice in ["1","１"]:
            word.update({"save_time": str(datetime.datetime.today()),
                         "last_updated": str(datetime.datetime.today())})
            valuelst = [item for item in word.values()]
            trantab = str.maketrans("',()", "    ")
            for ind in range(len(valuelst)):
                valuelst[ind] = valuelst[ind].translate(trantab)
            insert_data(valuelst)
    else:
        print("Please enter the word.")

def delete_word():
    wordlst = list_all_kanji()
    print(wordlst)
    choice = int(input("choice input : "))
    for row in wordlst:
        if choice == row[0]:
            delete_from_db(row[1])

if __name__ == '__main__':
    db_check_review()
    while True:
        try:
            print("------------ search word or memory word ------------")
            print("------------ 1 search word from weblio ------------")
            print("------------ 2 memory word ------------")
            print("------------ 3 show vocabulary ------------")
            print("------------ 4 delete from vocabulary ------------")
            print("------------ 5 exit ------------")
            choice = input("1 - 5 : ")
            if choice in ["1","１"]:
                keyword = input("word : ")
                create_table()
                save_to_db(keyword=keyword)
            elif choice in ["2","２"]:
                for num in range(2):
                    MemorizeVocabulary().memory_main()
            elif choice in ["3","３"]:
                print(list_all_kanji())
            elif choice in ["4","４"]:
                delete_word()
            elif choice in ["5","５"]:
                break
        except (KeyError,IndexError):
            continue


