import sqlite3

conn = sqlite3.connect("vocabulary.db")
Table_Name = "my_vocabulary"

FIELDNAME = ["kanji","kana","explanation","phrase1_jp","phrase1_en","phrase2_jp","phrase2_en","phrase3_jp","phrase3_en","phrase4_jp","phrase4_en","phrase5_jp","phrase5_en","memory_times","save_time"]

def create_table():
    try:
        cursor = conn.cursor()
        SQL = '''
              CREATE TABLE my_vocabulary (
                kanji,
                kana,
                explanation,
                phrase1_jp,
                phrase1_en,
                phrase2_jp,
                phrase2_en,
                phrase3_jp,
                phrase3_en,
                phrase4_jp,
                phrase4_en,
                phrase5_jp,
                phrase5_en,
                memory_times,
                save_time,
                UNIQUE(kanji))
                '''
        cursor.execute(SQL)
        conn.commit()
        print('创建数据库表%s成功' % (Table_Name))
    except Exception as e:
        print(e)

def insert_data(word_lst):
    try:
        value_lst = str(word_lst)
        values = value_lst.replace('[','')
        values = values.replace(']','')
        cursor =conn.cursor()
        SQL = """
        insert or ignore into my_vocabulary values(
        {}
        )
        """.format(values)
        cursor.execute(SQL)
        conn.commit()
        print("insert successful")
    except Exception as e:
        print(e)

def alter_memory_times_data(word_lst):
    try:
        for word_dict in word_lst:
            cursor =conn.cursor()
            SQL = """
            update my_vocabulary set memory_times = {} where kanji = {}
            """.format(word_dict["memory_times"],'"'+word_dict["kanji"]+'"')
            cursor.execute(SQL)
            conn.commit()
        print("alter successful")
    except Exception as e:
        print(e)

def select_data_to_dict():
    try:
        cursor =conn.cursor()
        wordlst = []

        SQL = """
        select * from my_vocabulary
        """
        cursor.execute(SQL)

        for row in cursor.fetchall():
            itemdict = {}
            rowlst = [item for item in row]
            for ind in range(len(rowlst)):
                itemdict[FIELDNAME[ind]] = rowlst[ind]
                print(itemdict)
            wordlst.append(itemdict)

        print("search successful")
        return wordlst
    except Exception as e:
        print(e)

if __name__ == '__main__':
    create_table()
    select_data_to_dict()

