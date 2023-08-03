import os
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