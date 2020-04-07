import time
import random
from ope_database import select_less_times_data_to_dict,alter_memory_times_data

class MemorizeVocabulary:
    def __init__(self):
        self.db_wordlst = select_less_times_data_to_dict()
        self.wordslst = self.set_ten_wordlst()


    def set_ten_wordlst(self):

        tenwordlst = []
        rannum = set([item for item in range(len(self.db_wordlst))])
        for num in rannum:
            if len(tenwordlst) <= 10:
                tenwordlst.append(self.db_wordlst[num])
        return tenwordlst


    def random_selection(self,question_item,answer_item):
        wordlst = self.wordslst
        section = []
        selection = {}
        time1 = time.time()
        while len(section) < 4:
            time2 = time.time()
            if time2 - time1 > 3:
                self.test_prase()
                break
            elif time2 - time1 > 5:
                print("\nYou haven't anything to review.\n")
                break
            try:
                rint = random.randint(0,len(wordlst))
                if rint not in section and wordlst[rint][answer_item] and wordlst[rint][question_item]:
                    section.append(rint)
            except IndexError:
                continue

        num = 0
        while num < 4:
            if self.wordslst[section[num]][answer_item]:
                selection[str(num + 1)] = wordlst[section[num]][answer_item]
            num += 1
        try:
            rint = random.randint(0,3)
            selection[question_item] = wordlst[section[rint]][question_item]
        except IndexError:
            selection[question_item] = wordlst[section[rint]]["kanji"]
        word = wordlst[section[rint]]
        answer = wordlst[section[rint]][answer_item]

        return word,selection,answer




    def get_word(self,word):
        # Explanation
        kana = word["kana"] if word["kana"] else ""
        jp_explanation = word["jp_explanation"] if word["jp_explanation"] else ""
        explanation = word["explanation"] if word["explanation"] else ""
        print("\n----------------------{}----------------------".format(word["kanji"]))
        print("カタカナ : {}".format(kana))
        print("意味 : {}".format(jp_explanation))
        print("主な英訳 : {}".format(explanation))
        print("例文 : \n{}\n\n".format("    "+word["phrase1_jp"]+" "+word["phrase1_en"]))


    def get_question(self,**word):
        print("----------------------{}----------------------".format(word["selection"][word["question_item"]]))
        for k, v in word["selection"].items():
            if k != word["question_item"]: print(k, v,"\n")

        # checkAnswer
        while True:
            my_answer = input("\nMy choice is(1-4) : ")
            if my_answer in ["1","2","3","4"]:
                break
            else:
                my_answer = None
                continue

        if word["selection"][my_answer] == word["answer"]:
            print("\nTrue")
            self.get_word(word["word"])
            return self.modify_memorize_times(word["word"],"add")
        else:
            print("\nFalse The answer is : {}".format(word["answer"]))
            self.get_word(word["word"])
            input("enter any key to continue: ")
            return self.modify_memorize_times(word["word"],"minus")


    def word_study_and_question(self, question_item, answer_item, study=None):
        word, selection, answer = self.random_selection(question_item, answer_item)
        word_items = {
            "word" : word,
            "selection" : selection,
            "answer" : answer,
            "question_item" : question_item,
            "answer_item" : answer_item
        }

        if study:
            self.get_word((word))

        # Question
        self.get_question(**word_items)


    def test_kanji_kana_explanation(self):
        question_items = ["kanji", "kana", "explanation","jp_explanation"]
        for i in range(5):
            rint = random.randint(0, len(question_items) - 1)
            item1 = question_items[random.randint(0,1)]
            try:
                item2 = question_items[rint + 1]
            except IndexError:
                item2 = question_items[rint - 1]
            self.word_study_and_question(question_item=item1, answer_item=item2)
            self.word_study_and_question(question_item=item1, answer_item=item2)
        return self.test_prase()

    def test_prase(self):
        prase_items = ["phrase1_jp", "phrase1_en", "phrase2_jp", "phrase2_en", "phrase3_jp", "phrase3_en", "phrase4_jp",
                       "phrase4_en", "phrase5_jp", "phrase5_en"]
        for c in range(2):
            rint = random.randint(1,5)
            item1 = "phrase{}_jp".format(rint)
            item2 = "phrase{}_en".format(rint)
            self.word_study_and_question(question_item=item1, answer_item=item2)
        return alter_memory_times_data(self.wordslst)



    def get_memorize_times(self,word):
        # get memorize times
        print("----------get memory times----------")
        for item in self.wordslst:
            if item["kanji"] == word["kanji"]:
                return item["kanji"]

    def modify_memorize_times(self, word,result=None):
        if result == "add":
            #memorize times plus one
            for item in self.wordslst:
                if item["kanji"] == word["kanji"]:
                    item["memory_times"] = int(item["memory_times"])+1
        elif result != "add":
            for item in self.wordslst:
                if item["kanji"] == word["kanji"]:
                    item["memory_times"] = int(item["memory_times"])-1


    def memory_main(self):
        self.test_kanji_kana_explanation()
        # # alter memorize times to db
        # alter_memory_times_data(self.wordslst)


