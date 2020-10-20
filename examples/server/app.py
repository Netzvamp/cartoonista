from flask import Flask, render_template, jsonify, request
import cartoonista

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("cartoon.html")


@app.route('/cartoonists')
def cartoonists():
    return jsonify(cartoonista.get_all_cartoonists())


@app.route('/cartoon', methods=['POST', 'GET'])
def cartoon():
    return cartoonista.get_random_cartoon(exclude=request.json["excluded_cartoonists"])


if __name__ == '__main__':
    app.run(port=5001, debug=True)
