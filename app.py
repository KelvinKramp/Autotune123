from flask_app import init_app

app = init_app()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
