import sqlite3
import json
import datetime
import time
import os


# key must be str type
class sqlite_dict():
    def __init__(self, dbfilename):
        self.dbfilename = dbfilename
        self.table_name = "test"
        self.is_connect = False
        self.con = None

    def drop_db_file(self):
        if os.path.isfile(self.dbfilename):
            os.remove(self.dbfilename)
        self.is_connect = False

    def connect(self):
        self.con = sqlite3.connect(self.dbfilename)
        self.is_connect = True

    def close(self):
        if self.is_connect:
            self.con.close()
            self.is_connect = False
            self.con = None

    def set_table_name(self, table_name):
        self.table_name = table_name

    def create_table(self):
        cur = self.con.cursor()
        cur.execute(f"CREATE TABLE {self.table_name} (timestamp REAL,"
                    f"dict_key text primary key,json_dump text)")
        self.con.commit()

    # dict를 하나 또는 여러개를 DB에 저장합니다.
    # dupkey_process
    # "ignore":에러가 안나는 것만 부분 업데이트
    # "forced":기존값 모두 업데이트
    # "error":하나가 에러나면 모두 업데이트 중지함
    # return 0 : 에러없음, -1:에러
    def save_dict(self, dict_data, dupkey_process="error"):
        nowtime = datetime.datetime.now().timestamp()
        cur = self.con.cursor()
        for key in dict_data:
            value = dict_data[key]
            json_dump = json.dumps(value)
            json_dump = str(json_dump)
            json_dump = json_dump.replace("'", "''")
            print(f"{key}//{json_dump}")
            try:
                cur.execute(f"INSERT INTO '{self.table_name}' VALUES ('{nowtime}','{key}','{json_dump}')")
            except sqlite3.OperationalError as ex:
                if str(ex).startswith("no such table:"):
                    self.create_table()
                    cur.execute(f"INSERT INTO '{self.table_name}' VALUES ('{nowtime}','{key}','{json_dump}')")
            except sqlite3.IntegrityError as ex:
                if str(ex).startswith("UNIQUE constraint failed:"):
                    if dupkey_process == "ignore":
                        pass
                    if dupkey_process == "error":
                        self.con.rollback()
                        return -1
                    if dupkey_process == "forced":
                        cur.execute(f"UPDATE '{self.table_name}' SET json_dump='{json_dump}' WHERE dict_key='{key}'")
                        cur.execute(f"UPDATE '{self.table_name}' SET timestamp='{nowtime}' WHERE dict_key='{key}'")
        self.con.commit()
        return 0

    # dect , timestamp
    def get_data(self, find_key):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()

        try:
            cursor.execute(f"SELECT json_dump,timestamp FROM '{self.table_name}' WHERE dict_key='{find_key}'")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return None, None
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None, None
        # print("debug:",row)
        dict_data = json.loads(row[0])
        timestamp = row[1]
        return dict_data, timestamp

    def get_all_data(self):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT * FROM '{self.table_name}'")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return None, None
        rows = cursor.fetchall()
        cursor.close()
        if rows is None:
            return None, None
        ret = {}
        ret_tp = {}
        # print("debug:",rows)
        for row in rows:
            ret[row[1]] = json.loads(row[2])
            ret_tp[row[1]] = row[0]
        return ret, ret_tp

    def get_all_keys(self):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT dict_key FROM '{self.table_name}'")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return None, None
        rows = cursor.fetchall()
        cursor.close()
        if rows is None:
            return None, None
        ret = []
        #print("debug:",rows)
        for row in rows:
            ret.append(row[0])
        return ret

    # 삭제한 레코드 갯수
    def del_key(self, find_key):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        del_count = 0
        try:
            r_del = cursor.execute(f"DELETE FROM '{self.table_name}' WHERE dict_key='{find_key}'")
            del_count = r_del.rowcount
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return -1
        cursor.close()
        self.con.commit()
        return del_count

    # 전체 카운트 리턴
    def get_count_all(self):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        result = 0
        try:
            cursor.execute(f"SELECT COUNT(*) FROM '{self.table_name}'")
            result = cursor.fetchone()[0]
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return -1
        cursor.close()
        return result

    # 가장 오래된 레코드 가져오기
    # dict, timestamp
    def get_old_record_one(self):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT * FROM '{self.table_name}' ORDER BY timestamp ASC LIMIT 1")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return None, None
        row = cursor.fetchone()
        print(row)
        cursor.close()
        if row is None:
            return None, None
        ret = {row[1]: json.loads(row[2])}
        return ret, row[0]

    # 시간차 구하기 초단위
    def diff_timestamp_sec(self, last_time, now_time):
        return now_time - last_time

    # 특정 시간 이전 레코드 삭제하기
    # -60 : -60 초 이전 레코드 삭제
    def del_old_record(self, time_old_sec):
        nowtime = datetime.datetime.now().timestamp()
        print(nowtime+time_old_sec)
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT * FROM '{self.table_name}' WHERE timestamp < {nowtime+time_old_sec}")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return -1
        rows = cursor.fetchall()
        #print(rows)
        cursor.close()
        count = 0
        if rows is not None:
            for row in rows:
                self.del_key(row[1])
                count = count + 1
        return count

if __name__ == "__main__":
    try:
        os.remove("test.db")
    except:
        pass
    sd = sqlite_dict("test.db")
    sd.connect()
    sd.set_table_name("test_table")
    print(sd.get_count_all())
    print("** add item")
    sd.save_dict({"abc": [1, 2, 3, 4, 5, "abc"]})
    print("** add items 2")
    sd.save_dict({"abc": [1, 2, "한글", {"test": "t1"}], "kbz": 2}, dupkey_process="forced")
    time.sleep(1)
    sd.save_dict({"kbz": 2}, dupkey_process="forced")
    time.sleep(1)
    sd.save_dict({"def": ["def", 2, "한글", {"test": "t1"}]}, dupkey_process="forced")
    time.sleep(1)
    sd.save_dict({"ccc": 4}, dupkey_process="forced")
    print("** alldata")
    print(sd.get_count_all())
    print(sd.get_all_data())
    print("old:", sd.get_old_record_one())
    print("** read item")
    print("get_data abc", sd.get_data("abc"))
    print("get_data kbz", sd.get_data("kbz"))
    print("get_data kcc", sd.get_data("kcc"))
    print("** del item")
    print("del kca", sd.del_key("kca"))
    print("del kbz", sd.del_key("kbz"))
    print("** alldata")
    print(sd.get_all_data())
    print(sd.get_count_all())
    nowtime = datetime.datetime.now().timestamp()
    time.sleep(3)
    print(sd.diff_timestamp_sec(nowtime, datetime.datetime.now().timestamp()))

    print("del_old_record", sd.del_old_record(-5))
    print("alldata", sd.get_all_data())
    print("get_count_all", sd.get_count_all())
    print("get_all_keys", sd.get_all_keys())
    sd.close()

'''
3
** add item
abc//[1, 2, 3, 4, 5, "abc"]
** add items 2
abc//[1, 2, "\ud55c\uae00", {"test": "t1"}]
kbz//2
kbz//2
def//["def", 2, "\ud55c\uae00", {"test": "t1"}]
ccc//4
** alldata
4
({'abc': [1, 2, '한글', {'test': 't1'}], 'def': ['def', 2, '한글', {'test': 't1'}], 'ccc': 4, 'kbz': 2}, {'abc': 1663198449.961539, 'def': 1663198451.982047, 'ccc': 1663198453.002805, 'kbz': 1663198450.974377})
(1663198449.961539, 'abc', '[1, 2, "\\ud55c\\uae00", {"test": "t1"}]')
old: ({'abc': [1, 2, '한글', {'test': 't1'}]}, 1663198449.961539)
** read item
get_data abc ([1, 2, '한글', {'test': 't1'}], 1663198449.961539)
get_data kbz (2, 1663198450.974377)
get_data kcc None
** del item
del kca 0
del kbz 1
** alldata
({'abc': [1, 2, '한글', {'test': 't1'}], 'def': ['def', 2, '한글', {'test': 't1'}], 'ccc': 4}, {'abc': 1663198449.961539, 'def': 1663198451.982047, 'ccc': 1663198453.002805})
3
3.0130131244659424
1663198451.032397
del_old_record 1
alldata ({'def': ['def', 2, '한글', {'test': 't1'}], 'ccc': 4}, {'def': 1663198451.982047, 'ccc': 1663198453.002805})
get_count_all 2
get_all_keys ['ccc', 'def']
'''