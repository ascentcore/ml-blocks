import pandas as pd

from .loader import Loader
from app.store import get_sqlite3_store_connection


class RawLoader(Loader):

    def load_file(self, file):
        output = []
        for line in file.readlines():
            output.append({'raw': line})

        self.data = output

    def load_object(self, obj):
        output = []
        for line in obj:
            output.append({'raw': line})

        self.data = output

    def store(self, append=False):
        df = pd.DataFrame(self.data)
        conn = get_sqlite3_store_connection()
        df.to_sql('default', conn, if_exists=(
            'append' if append == True else 'replace'))
        conn.close()
