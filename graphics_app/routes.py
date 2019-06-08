from graphics_app import app, URL_DARASETS, URL_IMAGES, MAX_FILE_SIZE
from flask import abort

import numpy as np
import uuid
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import os
from graphics_app.file_reader import FileReader
from graphics_app.graphics import (
    create_3d_graphic, COLORMAP, PICT_TYPES, create_2d_graphic, RESOLUTION,
    create_2d_contour, COLUMN_NAMES
)


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
    return render_template("index.html", args=args)


@app.route("/graphic/", methods=["POST", "GET"])
def construct_graphic():
    args = {"method": "GET", "image": "", "image_path": ""}
    filename = request.args.get('filename')
    colormap = request.form.get('colormap', 'hot')
    dpi = request.form.get('dpi', '300 dpi')
    grid = request.form.get('grid2d', False)
    type_pict = request.form.get('type_pict', '2D')
    file_reader = FileReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_reader.open()
    column_caption = COLUMN_NAMES[:file_reader.column_count()].copy()
    # x - всегда активен
    for i in range(1, len(column_caption)):
        column_caption[i]['checked'] = bool(request.form.get(f"axe_{column_caption[i]['name']}"))
    args["colorlist"] = [{"color": cm, "flag": cm == colormap} for cm in list(COLORMAP.keys())]
    args["type_pict"] = [{"type": tp, "flag": tp == type_pict} for tp in list(PICT_TYPES.keys())]
    args["resolution"] = [{"type": tp, "flag": tp == dpi} for tp in list(RESOLUTION.keys())]

    args["grid2d"] = grid
    args["filename"] = filename

    file_reader = FileReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_reader.open()

    file_reader.set_table()
    data_table = np.array(file_reader.get_table())
    args["captions"] = column_caption
    args["table"] = data_table[:16]
    file_reader.close()
    if request.method == "POST":
        if type_pict == "2D":
            image_name, image_path = create_2d_graphic(data=data_table,
                                                       active_column=column_caption,
                                                       dpi=dpi,
                                                       grid2d=grid)
        elif type_pict == "3D":
            image_name, image_path = create_3d_graphic(data=data_table,
                                                       colormap=COLORMAP[colormap],
                                                       dpi=dpi)
        elif type_pict == "2D with colors":
            image_name, image_path = create_2d_contour(data=data_table, dpi=dpi)
        args["method"] = "POST"
        args["image"] = image_name + ".png"
        args["links"] = {"eps":  URL_IMAGES + '/eps/' + image_name + '.eps',
                         "pdf":  URL_IMAGES + '/pdf/' + image_name + '.pdf'}
        args["image_path"] = URL_IMAGES + '/png/'

    return render_template("plotter.html", args=args)