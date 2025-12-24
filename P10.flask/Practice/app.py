from flask import Flask, render_template, request, redirect, url_for
from functions import reverse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["data"]
    name = reverse(name)
    return render_template("result.html", value=name)

if __name__ == "__main__":
    app.run(debug=True)