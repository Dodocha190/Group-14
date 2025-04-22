from flask import Flask, render_template

application = Flask(__name__)

import app.routes

if __name__ == '__main__':
    application.run(debug=True)
