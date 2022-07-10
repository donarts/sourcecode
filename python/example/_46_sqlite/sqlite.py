import os
import sqlite3
import json

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
        cur.execute(f"CREATE TABLE {self.table_name} ( dict_key text primary key, json_dump text)")
        self.con.commit()

    # dict를 하나 또는 여러개를 DB에 저장합니다.
    # dupkey_process
    # "ignore":에러가 안나는 것만 부분 업데이트
    # "forced":기존값 모두 업데이트
    # "error":하나가 에러나면 모두 업데이트 중지함
    # return 0 : 에러없음, -1:에러
    def save_dict(self,dict_data,dupkey_process="error"):
        cur = self.con.cursor()
        for key in dict_data:
            value = dict_data[key]
            json_dump = json.dumps(value)
            print(f"{key}//{json_dump}")
            try:
                cur.execute(f"INSERT INTO '{self.table_name}' VALUES ('{key}','{json_dump}')")
            except sqlite3.OperationalError as ex:
                if str(ex).startswith("no such table:"):
                    self.create_table()
                    cur.execute(f"INSERT INTO '{self.table_name}' VALUES ('{key}','{json_dump}')")
            except sqlite3.IntegrityError as ex:
                if str(ex).startswith("UNIQUE constraint failed:"):
                    if dupkey_process == "ignore":
                        pass
                    if dupkey_process == "error":
                        self.con.rollback()
                        return -1
                    if dupkey_process == "forced":
                        cur.execute(f"UPDATE '{self.table_name}' SET json_dump='{json_dump}' WHERE dict_key='{key}'")
        self.con.commit()
        return 0

    def get_data(self, find_key):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT json_dump FROM '{self.table_name}' WHERE dict_key='{find_key}'")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return None
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        dict_data = json.loads(row[0])
        return dict_data

    def get_all_data(self):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT * FROM '{self.table_name}'")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return None
        rows = cursor.fetchall()
        cursor.close()
        if rows is None:
            return None
        ret = {}
        for row in rows:
            ret[row[0]] = json.loads(row[1])
        return ret

    def del_key(self, find_key):
        if not self.is_connect:
            self.connect()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"DELETE FROM '{self.table_name}' WHERE dict_key='{find_key}'")
        except sqlite3.OperationalError as ex:
            if str(ex).startswith("no such table:"):
                cursor.close()
                return False
        cursor.close()
        self.con.commit()
        return True

if __name__ == "__main__":
    sd = sqlite_dict("test.db")
    sd.connect()
    sd.set_table_name("test_table")
    print("** add item")
    sd.save_dict({"abc" : [1, 2, 3, 4, 5,"abc"]})
    print("** add items 2")
    sd.save_dict({"abc" : [1, 2, "한글"], "kbz" : 2} , dupkey_process="forced")
    print("** alldata")
    print(sd.get_all_data())
    print("** read item")
    print(sd.get_data("abc"))
    print(sd.get_data("kbz"))
    print(sd.get_data("kcc"))
    print("** del item")
    print(sd.del_key("kca"))
    print(sd.del_key("kbz"))
    print("** alldata")
    print(sd.get_all_data())
    sd.close()
