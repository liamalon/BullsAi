import sqlite3
import os

class CodesDB():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor
        self.table_name = "codes_table"
        self.open_DB()
        self.init_db()
        self.close_DB()
        
    def open_DB(self) -> None:
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('DataBase\\codes_table.db')
        self.current = self.conn.cursor()

    def init_db(self) -> None:
        """
        Initalize the database
        """
        self.current.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        if self.current.fetchone()[0] < 1:
            # Create codes database
            self.current.execute(f"""CREATE TABLE {self.table_name }(
                salt text,
                hashed_code text PRIMARY KEY)""")

    def close_DB(self):
        """
        Closes databse
        """
        self.conn.close()

    def commit(self):
        """
        Commits action
        """
        self.conn.commit()

    def get_hashed_codes(self) -> list:
        """
        Gets a list of all hashed codes
        Returns:
            hashed_codes: (list[tuple]) - a list of tuples (hashed_code, salt)
        """
        self.open_DB()

        sql =  f"SELECT * FROM {self.table_name };"

        res = self.current.execute(sql)
        hashed_codes = self.current.fetchall()

        self.close_DB()
        return hashed_codes

    def insert_code(self, hashed_code: str, salt: str) -> None:
        """
        Insert a hashed_code and salt
        Args:
            hashed_code: (str) - a hased code
            salt: (str) - a salt
        """
        self.open_DB()
        sql=f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE hashed_code='{hashed_code}')"
        check = self.current.execute(sql) 
        if check.fetchone()[0] == 0:
            sql = f"INSERT INTO {self.table_name} VALUES ('{salt}', '{hashed_code}');"
            res=self.current.execute(sql)
            self.commit()
            self.close_DB()
        else:
            print("File Already exits!")
            self.close_DB()

    def delete_code(self, hashed_code: str) -> None:
        """
        Deletes a code
        Args:
            hashed_code: (str) - the hashed code we want to delete
        """
        self.open_DB()
        sql= f"DELETE FROM {self.table_name} WHERE hashed_code == '{hashed_code}'"
        res =self.current.execute(sql)
        self.commit()
        self.close_DB()
        
        

