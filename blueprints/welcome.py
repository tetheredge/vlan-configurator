from blueprints.base_blueprint import *

bp = create_blueprint(__file__)

@bp.route("/v1")
def index():
    return ('Welcome to v1 of vlan configurator!')