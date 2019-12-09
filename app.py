from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = "SOME_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class StudentEntity(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)


class StudentForm(Form):
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 16)])
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(1, 16)])
    last_name = StringField("Last Name: ", validators=[DataRequired(), Length(1, 16)])
    register = SubmitField("Register")


class LoginForm(Form):
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 16)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(1, 20)])
    login = SubmitField("Login")


@app.before_first_request
def setup_data():
    db.create_all()
    student_entity = StudentEntity.query.filter_by(username="zavanton").first()
    if student_entity is None:
        student_entity = StudentEntity(username="zavanton", first_name="Anton", last_name="Zaviyalov")
        db.session.add(student_entity)
        db.session.commit()


@app.route("/")
def home():
    user = "zavanton"
    return render_template("home.html", user=user)


@app.route("/student", methods=["GET", "POST"])
def student():
    username = None
    first_name = None
    last_name = None
    student_form = StudentForm()
    if student_form.validate_on_submit():
        username = student_form.username.data
        student_form.username.data = ""
        first_name = student_form.first_name.data
        student_form.first_name.data = ""
        last_name = student_form.last_name.data
        student_form.last_name.data = ""

        result = StudentEntity.query.filter_by(username=username).first()
        if result is not None:
            flash("The student with this username already exists!")
        else:
            save_student(first_name, last_name, username)

    return render_template(
        "student.html",
        student_form=student_form,
        username=username,
        first_name=first_name,
        last_name=last_name)


def save_student(first_name, last_name, username):
    student_entity = StudentEntity(
        username=username,
        first_name=first_name,
        last_name=last_name)
    db.session.add(student_entity)
    db.session.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    username = None
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
    return render_template("login.html", login_form=login_form, username=username)


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.errorhandler(404)
def handle_error(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
