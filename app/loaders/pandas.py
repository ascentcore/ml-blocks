import pandas as pd
import logging
import sqlite3 as sql

from app.config import settings

from .loader import Loader


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PandasLoader(Loader):

    def __init__(self):
        logger.info('[Pandas Loder] initialized')

    def get_connection(self):
        return sql.connect(f'{settings.MOUNT_FOLDER}/data.db')

    def load_files(self, files, append):        
        logger.info('Loading files started')
        self.data = [pd.read_csv(file.file) for file in files]
        self.append = append

    def default_process(self):
        self.data = self.data[0]

    def count(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) from "raw_data"')
        cur_result = cur.fetchone()
        conn.close()
        return cur_result

    def store(self):
        self.store_to_db()

    def store_to_db(self):
        conn = self.get_connection()
        self.data.to_sql('raw_data', conn, if_exists='replace')
        conn.close()

    def load_data(self, page = 0, count = 10):
        conn = self.get_connection()
        cur = conn.cursor()
        # page_str = f',{page}' if page != 0 else ''
        cur.execute(f'SELECT * from "raw_data" LIMIT {page * count},{count}')
        cur_result = cur.fetchall()
        conn.close()
        return cur_result

    def store_to_file(self):
        self.data.to_json(f'{settings.MOUNT_FOLDER}/data.json')