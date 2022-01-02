import pandas as pd

from .loader import Loader

from app.store import get_sqlite3_store_connection

class PandasLoader(Loader):    

    def load_file(self, file):
        """ read format from config """
        self.data = pd.read_csv(file)

    def load_object(self, obj):
        return self.load_file(obj)

    def store(self, append = False):
        conn = get_sqlite3_store_connection()
        self.data.to_sql('default', conn, if_exists = ('append' if append == True else 'replace'))
        conn.close()



