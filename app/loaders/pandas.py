from numpy import isin
import pandas as pd
import logging
import sqlite3 as sql
import json

from app.config import settings

from .loader import Loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PandasLoader(Loader):

    def __init__(self, config):
        logger.info('[Pandas Loder] initialized')
        self.config = config

    def get_connection(self):
        return sql.connect(f'{settings.MOUNT_FOLDER}/data.db')

    def load_files(self, files, append):
        logger.info('Loading files started')
        method = self.config.get('loader_method', 'read_csv')
        config = self.config.get('load_config', {})
        self.data = [getattr(pd, method)(file.file, **config)
                     for file in files]
        self.append = append

    def load_content(self, content, format, append):
        content = content.json()        
        self.data = pd.DataFrame(content)
        self.append = append

    def default_process(self):
        if isinstance(self.data, list):
            self.data = pd.concat(self.data)        

    def count(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) from "raw_data"')
        cur_result = cur.fetchone()
        conn.close()
        return cur_result[0]

    def store(self):
        self.store_to_db()

    def store_to_db(self):
        conn = self.get_connection()
        replace = ('append' if self.append == True else 'replace')
        self.data.to_sql('raw_data', conn, index=False, if_exists=replace)
        conn.close()

    def load_from_store(self):
        conn = self.get_connection()
        df = pd.read_sql_query('SELECT * from "raw_data"', conn)
        conn.close()
        return df

    async def load_request(self, request):
        json_data = await request.json()
        return json_data

    def load_data(self, page=0, count=10, format=''):
        conn = self.get_connection()
        df = pd.read_sql_query(
            f'SELECT * from "raw_data" LIMIT {page * count},{count}', conn)
        return json.loads(df.to_json(orient="records"))

    def export_content_types(self):
        return [
            'application/json'
        ]
