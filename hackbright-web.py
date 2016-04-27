from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student_search")
def get_student_form():
	return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
     #call the get_grade_function
    grades = hackbright.get_grades_by_github(github)
    #send it with the render template
    html = render_template("student_info.html",
    						first=first,
    						last=last,
    						github=github,
    						grades=grades)
    return html

@app.route("/student-add")
def student_add():
    """Collect input for student to add."""
    return render_template("student_add.html")


@app.route("/student-added", methods=["POST"])
def student_added():
	"""Add student to database and display confirmation of action."""
	# first_name = request.form.get('first_name')
	# last_name = request.form.get('last_name')
	# github = request.form.get('github')
	first_name, last_name, github = request.form.values()
	# Add student to db, assign returned row to identifier
	hackbright.make_new_student(first_name, last_name, github)
	return render_template("student_added.html", github=github)

@app.route("/project")
def project_info():
    """Displays the project info."""
    title = request.args.get('title')
    project_info = hackbright.get_project_by_title(title)

    return render_template("project.html", 
                            title=project_info[0], 
                            description=project_info[1],
                            max_grade=project_info[2])


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
