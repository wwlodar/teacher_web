from flask import render_template, request
from app import app

@app.route('/blah')
def hello():
    return render_template("main.html")
