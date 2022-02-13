from flask import Blueprint, render_template

homepage = Blueprint("homepage", __name__)


@homepage.route("/")
def index():
    return render_template("index.html")
