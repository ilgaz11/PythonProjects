from flask import Flask, render_template, request, url_for, redirect, session
from school_data import find_id, verify_staff, course_list

app = Flask(__name__)

app.secret_key = "secret-key"

@app.route("/")
def home():
    return render_template("index.html")

#check if webpage is running
@app.route("/ping")
def ping():
    return "pong"

@app.route("/student", methods=["POST", "GET"])
def submit():
    #print("1")
    if request.method == "POST":
        #print("2")
        student_id = request.form.get("student-id")
        student = find_id(student_id)
        if not student:
            return render_template("index.html")
        avg_grades = student.avg_grades()
        session["id"] = student_id
        return render_template("result.html", name=student.name, id=student.id, age=student.age, grades=avg_grades, courses=course_list)
    
    #print("4")
    stud = find_id(session['id'])
    avg_grades = stud.avg_grades()
    # print(stud.grades)
    # print(session["data"])
    return render_template("result.html", name=stud.name, id=stud.id, age=stud.age, grades=avg_grades, courses=course_list)




@app.route("/course", methods=["POST"])
def add_course():
    course_code = request.form.get("course-code")
    choice = request.form.get("sub-button")
    #print(choice)
    st_id = session["id"]
    st = find_id(st_id)
    print(st.course_data)
    if choice == "add":
        st.enroll_class(course_code)
    elif choice == "delete":
        st.drop_class(course_code)
    print(st.course_data)
    # print(st.courses)
    # print(st.grades)
    # print(session["data"])
    # session["data"][3] = st.grades
    # print(session["data"])
    # print("3")
    return redirect(url_for("submit"))

@app.route("/staff", methods=["POST", "GET"])
def staff_page():
    staff_id = request.form.get("staff-id")
    staff_password = request.form.get("staff-pass")
    staff = verify_staff(staff_id, staff_password)
    if not staff:
        return render_template("index.html")
    return render_template("staff.html", name=staff.name, id=staff.id)




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)