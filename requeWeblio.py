import requests
from bs4 import BeautifulSoup
from saveToCsv import save_to_csv

class WordMeaning:
    def __init__(self,keyword):
        self.keyword = keyword
        self.meaning_html,self.sentence_html,self.jpmeaning_html = self.get_html()

        self.word = {
            "kanji" : keyword,
            "kana" : "",
            "jp_explanation" : "",
            "explanation":"",
            "phrase1_jp" : "",
            "phrase1_en" : "",
            "phrase2_jp" : "",
            "phrase2_en" : "",
            "phrase3_jp": "",
            "phrase3_en": "",
            "phrase4_jp": "",
            "phrase4_en": "",
            "phrase5_jp": "",
            "phrase5_en": "",
            "memory_times":"0",
        }
        self.user_ag = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        }



    def get_html(self):
        user_ag = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
        d = {
            "User-Agent": user_ag,
        }

        res = requests.get("https://ejje.weblio.jp/content/{}".format(self.keyword), data=d)
        meaning_html = res.text
        res = requests.get("https://ejje.weblio.jp/sentence/content/{}".format(self.keyword), data=d)
        sentence_html = res.text
        res = requests.get("https://www.weblio.jp/content/{}".format(self.keyword), data=d)
        jp_meaning = res.text
        return meaning_html,sentence_html,jp_meaning

    def get_jp_explain(self):
        try:
            print("---------------start find in 実用日本語表現辞典-----------------")
            soup = BeautifulSoup(self.jpmeaning_html, 'html.parser')
            # jp_exp = soup.find_all(class_="NetDicBody")
            # jp_exp2 = jp_exp[0].div.div
            # jp_exp = jp_exp2.find_all("div", style="text-indent:0;")
            jp_exp = soup.find_all(class_="Sgkdj")
            # jp_exp = jp_exp.p
            # print(jp_exp)
            exp_text = ""
            for exp in jp_exp:
                # print(exp)
                exp_text += exp.get_text()+ "\n"
            if not exp_text:
                jp_exp = jp_exp2.find_all("div")
                exp_text = ""
                for exp in jp_exp:
                    for string in exp.strings:
                        exp_text += string
            print(exp_text)
            self.word.update({"jp_explanation" : exp_text})
        except Exception:
            print("wrong")


    def get_kanji_kana_phrace(self):
        print("---------------start find in 研究社新和英中辞典-----------------")
        try:
            soup = BeautifulSoup(self.meaning_html, 'html.parser')
            kanji = soup.find(id="h1Query").get_text()
            print(kanji)
            kana = soup.find(class_="ruby").get_text()
            kenji = soup.find(class_="Kejje")
            explanation = soup.find(class_="content-explanation je").get_text()
            print(kanji, kana)
            self.word.update({"kanji": kanji, "kana": kana, "explanation": explanation})
        except AttributeError:
            print("Can't find 漢字　カタカナ　主な英訳in 和英中辞典")
        try:
            kejjeyrhd = kenji.find_all(class_="KejjeYrLn")
            for item in kejjeyrhd:
                jpp = item.find(class_="KejjeYrJp").get_text()
                enp = item.find(class_="KejjeYrEn").get_text()
                self.update_sentence_to_dict(jpp,enp)
        except AttributeError:
            print("can't find in 研究社新和英中辞典")
            self.get_kanji_etc_JMdict()

    def get_kanji_etc_JMdict(self):
        try:
            print("---------------start find in JMdict----------------")
            soup = BeautifulSoup(self.meaning_html, 'html.parser')
            jmdct = soup.find(class_="mainBlock hlt_JMDCT")
            explanation = soup.find(class_="content-explanation je").get_text()
            kanji = jmdct.find(class_="midashigo").get_text()
            kana = jmdct.select(".Jmdct .jmdctYm a")[1].get_text()
            self.word.update({"kanji":kanji,"kana":kana,"explanation":explanation})
        except (AttributeError,IndexError):
            print("can't find in JMdict")


    def get_sentences(self,grammar=None):
        print("--------------start find sentences--------------")
        soup = BeautifulSoup(self.sentence_html, 'html.parser')
        sentences = soup.find_all(class_="qotC")
        for sentence in sentences:
            jj = sentence.find(class_="qotCJJ")
            sent = []
            for word in jj:
                if word.string:
                    sent.append(word.string)
            jj = "".join(sent)[:"".join(sent).find("例文帳に追加")]

            je = sentence.find(class_="qotCJE")
            sent = []
            for word in je:
                if word.name == "span":
                    continue
                if word.string:
                    sent.append(word.string)
            je ="".join(sent)

            if not grammar and jj and je and "" in self.word.values():
                self.update_sentence_to_dict(jj,je)
            if grammar and jj and je and "" in self.word.values() and self.keyword in jj:
                self.update_sentence_to_dict(jj, je)


    def update_sentence_to_dict(self,jj,je):
        for k, v in self.word.items():
            if k.startswith("phrase") and k.endswith("jp") and not v and je not in self.word.values() and jj not in self.word.values():
                self.word.update({k: jj, k.replace("jp", "en"): je})
                break

    def exec(self):
        self.get_jp_explain()
        self.get_kanji_kana_phrace()
        self.get_sentences()

        print("漢字 : {}".format(self.word["kanji"]))
        print("カタカナ : {}".format(self.word["kana"]))
        print("意味 : {}".format(self.word["jp_explanation"]))
        print("例文１ : \n{}　({})".format(self.word["phrase1_jp"],self.word["phrase1_en"]))
        print("例文２ : \n{}　({})".format(self.word["phrase2_jp"],self.word["phrase2_en"]))
        print("例文３ : \n{}　({})".format(self.word["phrase3_jp"],self.word["phrase3_en"]))
        print("例文４ : \n{}　({})".format(self.word["phrase4_jp"],self.word["phrase4_en"]))
        print("例文５ : \n{}　({})".format(self.word["phrase5_jp"],self.word["phrase5_en"]))

        return self.word

    def sentences_exec(self):
        self.get_sentences(grammar=True)

        print("漢字 : {}".format(self.word["kanji"]))
        print("例文１ : \n{}　({})".format(self.word["phrase1_jp"], self.word["phrase1_en"]))
        print("例文２ : \n{}　({})".format(self.word["phrase2_jp"], self.word["phrase2_en"]))
        print("例文３ : \n{}　({})".format(self.word["phrase3_jp"], self.word["phrase3_en"]))
        print("例文４ : \n{}　({})".format(self.word["phrase4_jp"], self.word["phrase4_en"]))
        print("例文５ : \n{}　({})".format(self.word["phrase5_jp"], self.word["phrase5_en"]))

        return self.word

if __name__ == '__main__':
    WordMeaning("拗れる").exec()