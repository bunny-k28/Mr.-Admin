import os
import flask
import dotenv
from termcolor import cprint
from datetime import timedelta
from flask import session, request
from werkzeug.utils import secure_filename
from flask import render_template as render, url_for as to, redirect, send_from_directory

from __init__ import *


# web app dev configuration(s)
app = flask.Flask(__name__)

app.secret_key = app.secret_key = "3d9efc4wa651728"
app.permanent_session_lifetime = timedelta(days=1)

app.config["PORT"] = dotenv.get_key("./.env", "SITE_PORT")
app.config["HOST"] = dotenv.get_key("./.env", "SITE_HOST")
app.config["CACHE_FOLDER"] = dotenv.get_key("./.env", "UPLOAD_CACHE_FOLDER_PATH")
app.config["STORAGE_FOLDER"] = dotenv.get_key("./.env", "UPLOAD_STORAGE_FOLDER_PATH")


# web app route(s) or endpoint(s)
@app.route("/")
def redirectToIndex():
    return redirect(to("index"))


@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render('index.html')

    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["CACHE_FOLDER"], filename))
            return redirect(to('viewTables', filename=filename))


@app.route('/viewer/tables?file:<filename>', methods=['GET', 'POST'])
def viewTables(filename):
    DBObject = MrAdmin(filename)

    if request.method == "GET":
        tables = DBObject.get_tables(); del DBObject
        return render('view_table.html', 
                filename=filename, tables=tables)
    
    if request.method == "POST":
        return redirect(to('tableContentViewer', 
        tablename=request.form.get('table-name'), 
        filename=filename))


@app.route('/viewer/content?file:<filename>&table:<tablename>', methods=['GET', 'POST'])
def tableContentViewer(filename, tablename):
    if request.method == "GET":
        DBObject = MrAdmin(filename)
        content_table = DBObject.get_content(tablename)

        del DBObject

        return render('view_table_content.html', 
                      filename=filename, 
                      table=content_table, 
                      tablename=tablename)

    if request.method == "POST":
        pass




################################################################
if __name__ == "__main__":

    app.run(debug=True, port=app.config["PORT"], host=app.config["HOST"])
