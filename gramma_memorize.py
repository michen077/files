import time
import random
from ope_grammmar_db import sql_exec,select_data_to_dict

def get_rnlst(range,length=4):
    ranlst = []
    while len(ranlst) < length:
        rint = random.randint(0, range)
        if rint not in ranlst:
            ranlst.append(rint)
    return ranlst

class GrammaMemorize:
    def __init__(self):
        self.wodlst = select_data_to_dict()
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
        a = random.randint(0, 3)
        anwlst = []
        one_question = {
            "question" : "",
            "selection" : [],
            "answer" : a
        }
        q = selectionlst[a]
        one_question["question"] = q["kanji"]
        selector = ["explanation","en_explanation","phrase1_jp","phrase2_jp","phrase3_jp","phrase4_jp","phrase5_jp","phrase6_jp","phrase7_jp","phrase8_jp"]
        while len(anwlst) < 4:
            anwlst = []
            rint = random.randint(0,len(selector)-1)
            for item in selectionlst:
                if item[selector[rint]]:
                    anwlst.append(item[selector[rint]])
        one_question["selection"] = anwlst
        print(one_question)
        return one_question

    def get_the_question_and_review(self):
        one_question = self.get_question_and_answer()
        print("---------------------{}---------------------").format(one_question["question"])

        while True:
            choice = input("1 ~ 4 : ")
            if choice-1 == one_question["answer"]:
                print("Right")
                # modify memorize times
                self.modify_memorize_times(one_question["question"],"add")
                break
            elif choice not in ["1","2","3","4","１","２","３","４"]:
                continue
            else:
                print("Wrong")
                # modify memorize times
                self.modify_memorize_times(one_question["question"], "minus")
                break

    def modify_memorize_times(self,word,result):


    def gra_memo_exec(self):
        selectionlst = self.get_grlst_fromdb()
        self.convert_phrase_toquestion()



if __name__ == '__main__':
    GrammaMemorize().gra_memo_exec()