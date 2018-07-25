"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def display_homepage():
	"""Display list of students and projects"""

	students = hackbright.return_students()
	projects = hackbright.return_projects()

	return render_template("homepage.html", students=students, projects=projects)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    # return "{} is the GitHub account for {} {}".format(github, first, last)
    return render_template("student_info.html", first=first,
    											last=last,
    											github=github,
    											grades=grades)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add-a-student")
def get_student_info():
	"""Show form to add a student name."""

	return render_template("student_add.html")

@app.route("/add-a-project")
def get_project_info():
    """Show form to add a project."""

    return render_template("project_add.html")

@app.route("/add-a-grade")
def assign_grade():
    """Show form to add a project."""

    students = hackbright.return_students()
    projects = hackbright.return_projects()

    return render_template("grade_add.html", students=students, projects=projects)


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_added.html", first=first_name,
    											 last=last_name,
    											 git=github)

@app.route("/project-add", methods=['POST'])
def project_add():
    """Add a project."""

    title = request.form.get('title')
    description = request.form.get('descrip')
    max_grade = request.form.get('maxgrade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("project_added.html", title=title,
                                                  description=description,
                                                  max_grade=max_grade)


@app.route("/grade-add", methods=["POST"])
def grade_add():
    """Add grade to database and display confirmation"""

    github = request.form.get('student')
    title = request.form.get('project')
    grade = request.form.get('grade')


    hackbright.assign_grade(github, title, grade)

    return render_template("grade_added.html", github=github,
                                                title=title,
                                                grade=grade)

@app.route("/project")
def show_project_info():
	""""""

	title = request.args.get('title')
	
	title, description, max_grade  = hackbright.get_project_by_title(title)
	grades = hackbright.get_grades_by_title(title)

	return render_template("project_info.html",
							title=title,
							description=description,
							max_grade=max_grade,
							grades=grades)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
