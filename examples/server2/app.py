from flask import Flask, render_template
from cartoons import Cartoons

app = Flask(__name__)


@app.route('/')
def hello_world():
    cartoon = Cartoons.get_random_cartoon()
    return render_template("cartoon.html", **cartoon)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
