from graphics_app import app, URL_DARASETS
from flask import abort

import uuid
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import os


@app.route('/index/')
def index():
    return "Initial Flask"


@app.route("/", methods=["POST", "GET"])
@app.route("/downloads/", methods=["POST", "GET"])
def load_file():
    args = {"method": "GET", "data_path": URL_DARASETS}
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            file.seek(0, os.SEEK_END)
            args["size"] = round(file.tell()/(2**20), 2)
            args["too_big"] = False
            args["method"] = "POST"
            args["data_name"] = ""
            if file.tell() > 1024*1024:
                # 1 MB limit
                args["too_big"] = True
                return render_template("file_download.html", args=args)
            file.seek(0, 0)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            args["data_name"] = filename
        else:
            abort(404)
    list_files = list()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        list_files.append(filename)
    args["files"] = list_files
    return render_template("file_download.html", args=args)
