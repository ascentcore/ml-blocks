import sqlite3 as sql
import pandas

def get_sqlite3_store_connection():
    conn = sql.connect(f'database/data.db')
    return conn



class Storage:
    
    def save(self, item):
        pass

    def load(self):
        pass

    def store_json(self, data):
        pass
    

class SQLStorage(Storage):

    def get_connection(self):
        conn = sql.connect(f'database/data.db')
        return conn

    def store_json(self, data):
        df = pandas.DataFrame(data)
        conn = self.get_connection()
        df.to_sql('default', conn, if_exists = 'replace')
        conn.close()

    def store_pandas(self, df):
        conn = self.get_connection()
        df.to_sql('default', conn, if_exists = 'replace')
        conn.close()

    def load(self):
        conn = self.get_connection()
        conn.row_factory = sql.Row

        crs = conn.cursor()

        query = f'SELECT * FROM "default"'
        print(query)
        crs.execute(query)

        rows = crs.fetchall()

        conn.close()
        return rows
