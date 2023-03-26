import sqlite3


class Database:

    def __init__(self, db_file):
        self.db = self.load_db(db_file)

    def load_db(self, db_file):
        pass


class QueryRunner:

    def __init__(self):
        pass

    def execute(self):
        pass
