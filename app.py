from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return "<p>Hong</p>"

@app.route('/user/<name>')
def hello_user(name):
    return f"<h1> Hello {name}!</h1>"


if __name__ == "__main__":
    app.run()


