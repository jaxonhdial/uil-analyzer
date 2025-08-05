from flask import Flask

app = Flask(__name__)

@app.route("/")
def foo():
    return "<p>API Called</p>"

if __name__ == "__main__":
    app.run(debug=True)
