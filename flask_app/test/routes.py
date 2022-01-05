from flask import Blueprint, Flask, request, render_template, make_response
import simplejson


test = Blueprint("test", __name__, 
            static_folder="./static",# TODO: the directory of static files
            static_url_path="/",    # `url` proxy for static files
            template_folder="./templates"   # TODO: the directory of templates
            )

import os


@test.route("/", methods=["POST", "GET"])
def index():
    print(os.getcwd())
    # return r"<h1>Hello, CitiThrive!<h1/>"
    return render_template("hello.html")
