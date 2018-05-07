from flask import request, redirect, url_for, render_template, flash
from flaskr import app

@app.route('/')
def show_card():
    cards = [0,0,0,0,0,1,0,0,0,0,0,0]
    return render_template('show_card.html',cards=cards)
