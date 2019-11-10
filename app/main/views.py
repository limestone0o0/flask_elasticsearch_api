from flask import render_template
from manage import app


@app.route('/', endpoint='index')
def index():

    return render_template('test.html')
