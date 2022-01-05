from flask import Blueprint

test = Blueprint("test", __name__)


@test.route("/", methods=["POST", "GET"])
def index():
    return r"<h1>Hello, CitiThrive!<h1/>"
