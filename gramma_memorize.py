import time
import random
import datetime
from ope_grammmar_db import sql_exec,select_data_to_dict,alter_db_item,create_table,GrammayTextToDb

def get_rnlst(range,length=4):
    ranlst = []
    while len(ranlst) < length:
        rint = random.randint(0, range)
        if rint not in ranlst:
            ranlst.append(rint)
    return ranlst

class GrammaMemorize:
    def __init__(self):
        self.wodlst,count = select_data_to_dict()
        self.four_selectionlst = []

    def get_grlst_fromdb(self):
        # random select four item
        ranlst = get_rnlst(range=len(self.wodlst)-1,length=4)
        self.four_selectionlst = []
        for ind in ranlst:
            self.four_selectionlst.append(self.wodlst[ind])

    def convert_phrase_toquestion(self,selectionlst=None):
        if not selectionlst : selectionlst = self.four_selectionlst
        for item in selectionlst:
            for key in item.keys():
                if str(key).startswith("phrase"):
                    item[key] = item[key].replace(item["kanji"].replace("～",""),"_______")

    def get_question_and_answer(self,selectionlst = None):
        if not selectionlst : selectionlst = self.four_selectionlst
        a = random.randint(0,3)
        anwlst = []
        one_question = {
            "question" : "",
            "selection" : [],
            "answer" : a
        }
        q = selectionlst[a]
        one_question["question"] = q["kanji"]
        selector = ["en_explanation","phrase1_jp","phrase2_jp","phrase3_jp","phrase4_jp","phrase5_jp","phrase6_jp","phrase7_jp","phrase8_jp"]
        while len(anwlst) < 4:
            anwlst = []
            rint = random.randint(0,len(selector)-1)
            for item in selectionlst:
                if item[selector[rint]]:
                    anwlst.append(item[selector[rint]])
        one_question["selection"] = anwlst
        return one_question

    def get_the_question_and_review(self):
        one_question = self.get_question_and_answer()
        print("---------------------{}---------------------".format(one_question["question"]))
        for itin in range(len(one_question["selection"])):
            print("{} {}".format(itin+1,one_question["selection"][itin]))
        while True:
            choice = int(input("1 ~ 4 : "))
            if choice-1 == int(one_question["answer"]):
                print("Right")
                # modify memorize times
                self.modify_memorize_times(word=one_question["question"],result="add")
                break
            elif choice-1 != int(one_question["answer"]):
                print("Wrong")
                print("The answer is : "+one_question["selection"][one_question["answer"]])
                # modify memorize times
                self.modify_memorize_times(word=one_question["question"], result="minus")
                input("Press any key to continue :")
                break
            elif choice not in ["1","2","3","4","１","２","３","４"]:
                continue


    def modify_memorize_times(self,word,result):
        for item in self.wodlst:
            if item["kanji"] == word:
                if result == "add":
                    item["memory_times"] += 1
                elif result == "minus":
                    item["memory_times"] -= 1
                self.get_word(word=item)
                time.sleep(5)
                item["last_updated"] = str(datetime.datetime.today())
                alter_db_item(item="memory_times", word_dict=item)
                alter_db_item(item="last_updated", word_dict=item)

    def get_word(self,word):
        # Explanation
        jp_explanation = word["explanation"] if word["explanation"] else ""
        explanation = word["en_explanation"] if word["en_explanation"] else ""
        print("\n----------------------{}----------------------".format(word["kanji"]))
        print("意味 : {}".format(jp_explanation))
        print("英訳 : {}".format(explanation))
        print("例文 : \n{}\n".format("    "+word["phrase1_jp"]))


    def gra_memo_exec(self):
        # create_table()
        # GrammayTextToDb().grammar_text_to_db()
        for count in range(5):
            self.get_grlst_fromdb()
            self.convert_phrase_toquestion()
            self.get_the_question_and_review()



if __name__ == '__main__':
    GrammaMemorize().gra_memo_exec()