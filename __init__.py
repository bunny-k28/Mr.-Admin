import os
import dotenv
import sqlite3

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