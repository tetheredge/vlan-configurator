from flask import Blueprint
import os

def create_blueprint(filename):
    bp = Blueprint(os.path.basename(filename).split('.')[0], __name__)
    return bp
