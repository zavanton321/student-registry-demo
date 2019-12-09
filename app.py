from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def home():
    user = "zavanton"
    return render_template("home.html", user=user)


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.errorhandler(404)
def handle_error(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
