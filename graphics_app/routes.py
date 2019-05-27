from graphics_app import app, URL_DARASETS, URL_IMAGES, MAX_FILE_SIZE
from flask import abort

import uuid
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import os
from graphics_app.graphics import create_3d_graphic, COLORMAP


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
            args["method"] = "POST"
            args["data_name"] = ""
            if file.tell() > MAX_FILE_SIZE:
                args["big"] = True
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


@app.route("/graphic/", methods=["POST", "GET"])
def construct_graphic():
    args = {"method": "POST"}
    if request.method == "POST":
        filename = request.form['filename']
        colormap = request.form.get('colormap', 'hot')
        args["colorlist"] = [{"color": cm, "flag": cm == colormap} for cm in list(COLORMAP.keys())]
        args["filename"] = filename
        file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')
        table = []
        for line in file:
            x, y, z = line.split()
            table.append(dict(x=x, y=y, z=z))
        file.close()
        table_min = table[:16] if len(table) > 16 else table
        image_name, image_path = create_3d_graphic(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                                   colormap=COLORMAP[colormap])
        args["method"] = "GET"
        args["image"] = image_name
        args["image_path"] = URL_IMAGES
        args["table"] = table_min

    return render_template("graphic_plotter.html", args=args)

