from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    user = "zavanton"
    return render_template("home.html", user=user)


@app.route("/greet/<user>")
def greet(user):
    return render_template("greet.html", user=user)


@app.errorhandler(404)
def handle_error(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
