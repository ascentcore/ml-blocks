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

def cleanup():
    try:
        conn = sql.connect('database/session.db')
        cur = conn.cursor()
        cur.execute("DELETE from dependency")
        conn.commit()
        conn.close()
    except:
        print('ERROR')
        pass



class SQLStorage(Storage):

    def get_connection(self):
        conn = sql.connect(f'database/data.db')
        return conn

    def store_json(self, data):
        df = pandas.DataFrame(data)
        conn = self.get_connection()
        df.to_sql('default', conn, if_exists='replace')
        conn.close()

    def store_pandas(self, df):
        conn = self.get_connection()
        df.to_sql('default', conn, if_exists='replace')
        conn.close()

    def row_to_dict(self, cursor: sql.Cursor, row: sql.Row) -> dict:
        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data

    def load(self):
        conn = self.get_connection()
        # conn.row_factory = sql.Row
        conn.row_factory = self.row_to_dict

        crs = conn.cursor()

        query = f'SELECT * FROM "default"'
        crs.execute(query)

        rows = crs.fetchall()

        conn.close()
        return rows

    def load_pandas(self):
        conn = self.get_connection()
        df = pandas.read_sql_query('SELECT * FROM "default"', conn)
        conn.close()
        return df
