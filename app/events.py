import logging
import sqlite3 as sql

logger = logging.getLogger(__name__)

def db_cleanup():
    logger.info('Removing dependencies')
    conn = sql.connect('data/session.db')
    cur = conn.cursor()
    cur.execute("DELETE from dependency")
    conn.commit()
    conn.close()
