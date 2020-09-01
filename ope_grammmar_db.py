import datetime
import sqlite3

conn = sqlite3.connect("vocabulary.db")
Table_Name = "grammar"

FIELDNAME = ["kanji","explanation","en_explanation","phrase1_jp","phrase2_jp","phrase3_jp","phrase4_jp","phrase5_jp","phrase6_jp","phrase7_jp","phrase8_jp","memory_times","save_time","last_updated"]

WORD_DICT = {
            "kanji":"",
            "explanation":"",
            "en_explanation":"",
            "phrase1_jp":"",
            "phrase2_jp":"",
            "phrase3_jp":"",
            "phrase4_jp":"",
            "phrase5_jp":"",
            "phrase6_jp":"",
            "phrase7_jp":"",
            "phrase8_jp":"",
            "memory_times":"",
            "save_time":"",
            "last_updated":""
}

def create_table():
    try:
        cursor = conn.cursor()
        SQL = '''
              CREATE TABLE {} (
                kanji,explanation,en_explanation,phrase1_jp,phrase2_jp,phrase3_jp,phrase4_jp,phrase5_jp,phrase6_jp,phrase7_jp,phrase8_jp,memory_times int,save_time,last_updated,
                UNIQUE(kanji))
                '''.format(Table_Name)
        cursor.execute(SQL)
        conn.commit()
        print('创建数据库表%s成功' % (Table_Name))
    except Exception as e:
        print(e)

def sql_exec(sql):
    try:
        cursor =conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("exec successful")
        return cursor
    except Exception as e:
        print(e)

class GrammayTextToDb:

    def txt_to_dict(self):
        with open("try_grammar.txt",encoding="utf8") as f:
            gra_text = f.read()

        gralst = gra_text.split("\n\n")
        gralst2 = []
        for item in gralst:
            itemlst = item.split("\n")
            itemdict = {}
            for ind in range(len(itemlst)):
                itemdict[FIELDNAME[ind]] = itemlst[ind]
            gralst2.append(itemdict)
        return gralst2

    def match_word_dict(self,gralst):
        # match dict
        worddiclst = []
        for gra in gralst:
            if gra["kanji"]:
                word_dict = {k: v for k, v in WORD_DICT.items()}
                for k in word_dict.keys():
                    if gra.__contains__(k):
                        word_dict[k] = gra[k]
                    word_dict.update({
                        "memory_times": 1,
                        "save_time": str(datetime.datetime.today())
                    })
                worddiclst.append(word_dict)
        return worddiclst

    def insert_gralst_int_db(self,txtworddiclst):
        for item in txtworddiclst:
            keys = str([item for item in item.keys()]).replace("[","")
            keys = keys.replace("]","")
            values = str([item for item in item.values()]).replace("[","")
            values = values.replace("]","")
            sql = """
            insert or ignore into grammar({}) values ({})
            """.format(keys.replace('\'',''),values.replace("\\'",""))
            sql_exec(sql)

    def grammar_text_to_db(self):
        # save try_grammar.txt to db
        gralst = self.txt_to_dict()
        txtworddiclst = self.match_word_dict(gralst)
        self.insert_gralst_int_db(txtworddiclst)

def select_data_to_dict():
    try:
        cursor =conn.cursor()
        wordlst = []d

        SQL = """
        select * from {} where memory_times<2 order by memory_times,save_time
        """.format(Table_Name)
        cursor.execute(SQL)

        count = 0
        for row in cursor.fetchall():
            count += 1
            itemdict = {}
            rowlst = [item for item in row]
            for ind in range(len(rowlst)):
                itemdict[FIELDNAME[ind]] = rowlst[ind]
            wordlst.append(itemdict)

        print("search successful")
        return wordlst,count
    except Exception as e:
        print(e)

def alter_db_item(word_dict,item):
    SQL = """
        update grammar set {} = {} where kanji = {}
        """.format(item,word_dict[item], '"' + word_dict["kanji"] + '"')
    sql_exec(SQL)


def check_review():
    wordlst =[]
    sql = """
    select kanji,last_updated from grammar;
    """
    cursor = sql_exec(sql)
    for row in cursor.fetchall():
        wordlst.append(row)

    today = datetime.datetime.today()
    for wd in wordlst:
        kanji = wd[0]
        updated_time = wd[1]
        if not updated_time:
            sql = """
                update grammar set last_updated={} where kanji={};
                """.format('"' + str(today) + '"', '"' + str(kanji) + '"')
            sql_exec(sql)
        if updated_time:
            ut = datetime.datetime.fromisoformat(updated_time)
            td = (today - ut).days
            sql = """
                select memory_times from grammar where kanji={}
                """.format('"' + kanji + '"')
            cursor = sql_exec(sql)
            mt = cursor.fetchone()[0]
            if mt < 0:
                sql = """
                   update grammar set memory_times={},last_updated={} where kanji={};
                   """.format('"' + str(0) + '"', '"' + str(today) + '"',
                              '"' + str(kanji) + '"')
                sql_exec(sql)
            if td >= 1:
                if mt > 0:
                    mt = mt - td
                    sql = """
                        update grammar set memory_times={},last_updated={} where kanji={};
                        """.format('"' + str(mt) + '"', '"' + str(today) + '"', '"' + str(kanji) + '"')
                    sql_exec(sql)

if __name__ == '__main__':
    create_table()
    GrammayTextToDb().grammar_text_to_db()

















