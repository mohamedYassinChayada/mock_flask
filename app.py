from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! yoooooo'

if __name__ == '__main__':
    app.run(debug=True)
    ##comment: This is a simple Flask application that returns 'Hello, World! yoooooo' when accessed at the root URL.