import os
import dotenv
import sqlite3
import pandas as pd


ALLOWED_EXTENSIONS = {
    'db',
    'sql', 
    'sqlite',
    'sqlite3',
    'mdb',
    'accdb',
    'mysql',
    'postgresql',
    'pg',
    'psql',
    'dbf',
    'xls',
    'xlsx',
    'csv',
    'json',
    'xml',
    'yaml',
    'txt'
}


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class MrAdmin:
    def __init__(self, filename: str):
        self.filename = filename

        self.db = sqlite3.connect(
            os.path.join(
                dotenv.get_key('./.env', 'UPLOAD_CACHE_FOLDER_PATH'), 
                self.filename
            )
        )
        self.sql = self.db.cursor()


    def get_tables(self):
        table_names = self.sql.execute(
        "SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        self.sql.close(); self.db.close()
        return [name[0] for name in table_names]


    def get_content(self, table: str, target: str='*', condition: str | None=None):
        content_map = dict()

        cols = self.sql.execute(f"PRAGMA table_info({table})").fetchall()
        columns = [col[1] for col in cols]

        if condition is None:
            content = self.sql.execute(
                F"SELECT {target} FROM {table}").fetchall()

        elif condition is not None:
            content = self.sql.execute(
                F"SELECT {target} FROM {table} WHERE {condition}").fetchall()

        self.sql.close(); self.db.close()

        data_index = 0
        for column in columns:
            content_map[column] = [x[data_index] for x in content]
            data_index += 1

        data_frame = pd.DataFrame(content_map, 
                                  columns=columns)
        content_table = data_frame.to_html(
            classes='table table-bordered table-hover')

        return content_table