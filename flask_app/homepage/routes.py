from flask import Blueprint, render_template, redirect, url_for

homepage = Blueprint("homepage", __name__)


@homepage.route("/")
def index():
    return render_template("index.html")


@homepage.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'))
