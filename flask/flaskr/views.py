from flask import request, redirect, url_for, render_template, flash
from flaskr import app

@app.route('/')
def show_card():
    return render_template('show_card.html')
