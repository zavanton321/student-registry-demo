from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
bootstrap = Bootstrap(app)


class LoginForm(Form):
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 16)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(1, 20)])
    login = SubmitField("Login")


@app.route("/")
def home():
    user = "zavanton"
    return render_template("home.html", user=user)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.errorhandler(404)
def handle_error(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
