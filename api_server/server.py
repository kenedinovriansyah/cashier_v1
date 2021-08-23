from flask import Flask

def create_app():
    app = Flask(__name__)
    from core.extensions import ext
    ext(app)
    return app