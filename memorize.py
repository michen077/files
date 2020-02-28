import csv
import random

class MemorizeVocabulary:
    def __init__(self):
        self.wordslst = self.reader_to_list()

    def reader_to_list(self):
        vocabulary = open("vocabulary_shiftjis.csv", "r", encoding="shiftjis")
        reader = csv.DictReader(vocabulary)
        wordlst = []
        for word in reader:
            wordict = {k:v for k,v in word.items()}
            wordlst.append(wordict)
        return wordlst

    def set_ten_wordlst(self):
        tenwordlst = []
        rannum = set([item for item in range(len(self.wordslst))])
        for num in rannum:
            if len(tenwordlst) <= 10:
                tenwordlst.append(self.wordslst[num])
        return tenwordlst

    def random_selection(self):
        section = []
        while len(section) < 4:
            rint = random.randint(0,len(self.wordslst))
            if rint not in section: section.append(rint)

        print(self.wordslst)
        selection = {
            "1":self.wordslst[section[0]]["kana"],
            "2":self.wordslst[section[1]]["kana"],
            "3":self.wordslst[section[2]]["kana"],
            "4":self.wordslst[section[3]]["kana"],
        }
        return selection

    def memory_main(self):
        selection = self.random_selection()
        # for row in self.set_ten_wordlst():
        #     print("----------------------{}----------------------".format(row["kanji"]))
        #     for k,v in selection.items():
        #         print(k,v)




if __name__ == '__main__':
    MemorizeVocabulary().memory_main()

