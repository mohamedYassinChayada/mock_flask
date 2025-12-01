from flask import Flask

app = Flask(__name__)

@app.route('/')
    return 'Hello, World! yoooooo'

if __name__ == '__main__':  
    app.run(debug=True)
    ##comment: This is a simple Flask application that returns 'Hello, World! yoooooo' when accessed at the root URL.
    ##comment: The application is set to run in debug mode for easier development and troubleshooting.
    ##comment: To run the application, execute this script and navigate to http://
    ##"localhost:5000/" in your web browser.
    ## new message
    ## another new message
    