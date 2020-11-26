import sqlite3
import datetime

conn = sqlite3.connect("vocabulary.db")
Table_Name = "my_vocabulary"

FIELDNAME = ["kanji","kana","jp_explanation","explanation","phrase1_jp","phrase1_en","phrase2_jp","phrase2_en","phrase3_jp","phrase3_en","phrase4_jp","phrase4_en","phrase5_jp","phrase5_en","memory_times","save_time","last_updated"]

def create_table():
    try:
        cursor = conn.cursor()
        SQL = '''
              CREATE TABLE my_vocabulary (
                kanji,
                kana,
                explanation,
                jp_explanation,
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
                memory_times int,
                save_time,
                last_updated,
                UNIQUE(kanji))
                '''
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
        print("insert successful")
        return cursor
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
            updated = str(datetime.datetime.today())
            SQL = """
            update my_vocabulary set last_updated = {} where kanji = {}
            """.format('"'+updated+'"','"'+word_dict["kanji"]+'"')
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
            wordlst.append(itemdict)

        print("search successful")
        return wordlst
    except Exception as e:
        print(e)

def select_kanji_updated_to_dict():
    try:
        cursor =conn.cursor()
        wordlst = []

        SQL = """
        select kanji,last_updated from my_vocabulary
        """
        cursor.execute(SQL)

        for row in cursor.fetchall():
            wordlst.append(row)
        print("search successful")
        return wordlst
    except Exception as e:
        print(e)

def select_less_times_data_to_dict():
    try:
        cursor =conn.cursor()
        wordlst = []

        SQL = """
        select * from my_vocabulary where memory_times<2 order by memory_times,save_time DESC
        """
        cursor.execute(SQL)

        for row in cursor.fetchall():
            itemdict = {}
            rowlst = [item for item in row]
            for ind in range(len(rowlst)):
                itemdict[FIELDNAME[ind]] = rowlst[ind]
            wordlst.append(itemdict)

        print("search successful")
        return wordlst
    except Exception as e:
        print(e)

def select_memory_times(kanji):
    sql = """
    select memory_times from my_vocabulary where kanji={}
    """.format('"'+kanji+'"')
    cursor = sql_exec(sql)
    mt = cursor.fetchone()
    return mt

def list_all_kanji():
    wordlst = select_data_to_dict()
    kanji_list = []
    for row in wordlst:
        kanji_list.append(row["kanji"])
    return list(enumerate(kanji_list))

def delete_from_db(keyword):
    try:
        cursor =conn.cursor()
        SQL = """
        delete from my_vocabulary where kanji={}
        """.format('"'+keyword+'"')
        cursor.execute(SQL)
        conn.commit()
        print("delete {} successful".format(keyword))
    except Exception as e:
        print(e)

def check_review():
    wordlst = select_kanji_updated_to_dict()
    today = datetime.datetime.today()
    for wd in wordlst:
        kanji = wd[0]
        updated_time = wd[1]
        if not updated_time:
            sql = """
                update my_vocabulary set last_updated={} where kanji={};
                """.format('"' + str(today) + '"', '"' + str(kanji) + '"')
            sql_exec(sql)
        if updated_time:
            ut = datetime.datetime.fromisoformat(updated_time)
            td = (today - ut).days
            mt = select_memory_times(kanji)[0]
            if mt < 0:
                sql = """
                   update my_vocabulary set memory_times={},last_updated={} where kanji={};
                   """.format('"' + str(0) + '"', '"' + str(today) + '"',
                              '"' + str(kanji) + '"')
                sql_exec(sql)
            if td >= 1:
                if mt > 0:
                    mt = mt - td
                    sql = """
                        update my_vocabulary set memory_times={},last_updated={} where kanji={};
                        """.format('"' + str(mt) + '"', '"' + str(today) + '"', '"' + str(kanji) + '"')
                    sql_exec(sql)

def check_review_number():
    """check number of words to review"""
    sql = """
    select kanji from my_vocabulary where memory_times < 2;
    """
    cursor = sql_exec(sql)
    word_count = 0
    grammar_count = 0
    for row in cursor:
        word_count += 1

    sql = """
       select kanji from grammar where memory_times < 2;
       """
    cursor = sql_exec(sql)
    for row in cursor:
        grammar_count += 1
    return word_count,grammar_count


if __name__ == '__main__':
    create_table()
    select_data_to_dict()

