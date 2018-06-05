import os

from flask import Flask, send_file, jsonify
app = Flask(__name__)


@app.route("/")
def main():
    return jsonify({"msg": "Hello World!"})


@app.route("/test")
def test():
    return jsonify({"msg": "Test World!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8050)
