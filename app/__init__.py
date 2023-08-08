from flask import Flask

def create_app():
    app = Flask(__name__)

    from blueprints import welcome

    app.register_blueprint(welcome.bp)

    return app
