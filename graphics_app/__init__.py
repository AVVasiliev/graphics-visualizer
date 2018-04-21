from flask import Flask

app = Flask(__name__)

from graphics_app import routes
