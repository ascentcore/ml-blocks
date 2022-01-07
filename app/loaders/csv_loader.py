import pandas as pd

from .loader import Loader

from app.store import get_sqlite3_store_connection

class CSVLoader(Loader):    

    def load_files(self, files):
        """ read format from config """
        self.data = [pd.read_csv(file.file) for file in files]

    def load_object(self, obj):
        return self.load_file(obj)

    def store(self, data, append = False):
        conn = get_sqlite3_store_connection()
        data.to_sql('default', conn, if_exists = ('append' if append == True else 'replace'))
        conn.close()



