from flask import Blueprint, render_template, redirect, url_for, request, make_response
import json

homepage = Blueprint("homepage", __name__)


@homepage.route("/")
def index():
    return render_template("index.html")


@homepage.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'))


@homepage.route('/report-csp-violations', methods=['POST'])
def report():
    content = request.get_json(force=True)
    print(json.dumps(content, indent=4, sort_keys=True))
    with open("csp.log", "a") as f:
        print(json.dumps(content, indent=4, sort_keys=True), file=f)
    response = make_response()
    response.status_code = 204
    return response
