from flask import Flask
import os


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
URL_DARASETS = '/static/datasets/'
URL_IMAGES = '/static/images/'
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(UPLOAD_FOLDER, 'datasets')

from graphics_app import routes
