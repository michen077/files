import random
import time


class testSet:
    def __init__(self,set_txt):
        self.setxt = set_txt
        self.questions = {1:{}}
        pass

        self._exec()

    def _exec(self):
        # load file to dict
        self.load_question_set()
        # start random test
        self.test_question()

    def load_question_set(self):
        qnum = 1
        kw = ["問題","選択1","選択2","選択3","正解","解説"]
        with open(self.setxt,encoding="utf8") as f:
            qsetline = f.readlines()
        for item in qsetline:
            for k in kw:
                if item and item.startswith(k):
                    value = item[item.index(k)+len(k)+1:]
                    if value:
                        self.questions[qnum][k] = value
                    break
            if item.startswith("解説"):
                qnum += 1
                self.questions[qnum] = {}

    def test_question(self):
        numlist = random.sample(range(1,len(self.questions.keys())+1),len(self.questions.keys()))
        for num in numlist:
            if self.questions[num]:
                print(num,self.questions[num]["問題"])
                ques = self.questions[num]
                answer = [ques["選択1"],ques["選択2"],ques["選択3"],ques["正解"]]
                anlst = random.sample(range(0,4),4)
                random_answer = []
                ch = 1
                for choice in anlst:
                    print(ch,answer[choice])
                    random_answer.append(answer[choice])
                    ch += 1

                # choose
                u_choice = int(input("Please input your answer : "))
                if random_answer[u_choice-1] == ques["正解"]:
                    print("Right")
                else:
                    print("Wrong")
                    print("正解は　：",ques["正解"],ques["解説"])
                    time.sleep(5)


if __name__ == '__main__':
    file = "chapter3.txt"
    testSet(file)