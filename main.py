from flask import Flask, request, render_template, make_response
import simplejson
import os


""" 1. Initialize the application. """
app = Flask(__name__,
            static_folder="../views/statics",# TODO: the directory of static files
            static_url_path="/static",    # `url` proxy for static files
            template_folder="../templates"   # TODO: the directory of templates
            )


@app.route("/", methods=["POST", "GET"])
def index():
    return simplejson.dumps(r"<h1>Hello, CitiThrive!<h1/>")
    # return render_template("hello.html")


if __name__ == "__main__":
    # app.run(debug=True, )
    app.run(host='0.0.0.0',port=80)
