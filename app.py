from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = "SOME_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
loginManager = LoginManager(app)
loginManager.login_view = "login"
db = SQLAlchemy(app)


class StudentEntity(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)


class StudentForm(Form):
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 16)])
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(1, 16)])
    last_name = StringField("Last Name: ", validators=[DataRequired(), Length(1, 16)])
    register = SubmitField("Register")


class UserEntity(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = UserEntity(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(Form):
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 16)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(1, 20)])
    remember_me = BooleanField("Remember me")
    login = SubmitField("Login")


@loginManager.user_loader
def load_user(id):
    return UserEntity.query.get(int(id))


@app.before_first_request
def setup_data():
    db.create_all()
    student_entity = StudentEntity.query.filter_by(username="zavanton").first()
    if student_entity is None:
        student_entity = StudentEntity(username="zavanton", first_name="Anton", last_name="Zaviyalov")
        db.session.add(student_entity)
        db.session.commit()
    user_entity = UserEntity.query.filter_by(username="zavanton").first()
    if user_entity is None:
        UserEntity.register("zavanton", "1234")


@app.route("/")
def home():
    user = "zavanton"
    return render_template("home.html", user=user)


@app.route("/student", methods=["GET", "POST"])
@login_required
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
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = UserEntity.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.check_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(request.args.get("next") or url_for("home"))
        else:
            return redirect(url_for("login", **request.args))
    return render_template("login.html", login_form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.errorhandler(404)
def handle_error(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
