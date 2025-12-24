from flask import Flask, render_template, request, url_for
from school_data import find_id

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        student_id = int(request.form["student-id"])
    except ValueError:
        return render_template("index.html")
    student = find_id(student_id)
    if not student:
        return render_template("index.html")
    return render_template("result.html", name=student.name, id=student.id, age=student.age)


if __name__ == "__main__":
    app.run(debug=True)