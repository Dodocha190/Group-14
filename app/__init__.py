from flask import Flask, render_template

application = Flask(__name__)
application.config['SECRET_KEY'] = 'your_secret_key_here' ##TODO: Change this to a random secret key

import app.routes
import app.forms

if __name__ == '__main__':
    application.run(debug=True)
