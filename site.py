from flask import Flask, render_template, request, redirect
from main import create_web_page

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/map", methods=["GET", "POST"])
def map():
    name = request.form['name']
    count = request.form['count']
    create_web_page(name, count)
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)
