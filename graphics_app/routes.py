from graphics_app import app


@app.route('/')
def index():
    return "Initial Flask"
