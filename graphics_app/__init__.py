from flask import Flask
import os


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static'
IMAGES_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER + '/datasets'

from graphics_app import routes
