from flask import Flask, render_template, request, url_for, redirect, session
from school_data import find_id

app = Flask(__name__)

app.secret_key = "secret-key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/student", methods=["POST", "GET"])
def submit():
    print("1")
    if request.method == "POST":
        print("2")
        try:
            student_id = request.form.get("student-id")
        except ValueError:
            return render_template("index.html")
        student = find_id(student_id)
        if not student:
            return render_template("index.html")
        session["id"] = student_id
        return render_template("result.html", name=student.name, id=student.id, age=student.age, grades=student.grades)
    
    print("4")
    stud = find_id(session['id'])
    # print(stud.grades)
    # print(session["data"])
    return render_template("result.html", name=stud.name, id=stud.id, age=stud.age, grades=stud.grades)




@app.route("/course", methods=["POST"])
def add_course():
    course_code = request.form.get("course-code")
    st_id = session["id"]
    st = find_id(st_id)
    st.enroll_class(course_code)
    # print(session["data"])
    # session["data"][3] = st.grades
    # print(session["data"])
    # print("3")
    return redirect(url_for("submit"))




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)