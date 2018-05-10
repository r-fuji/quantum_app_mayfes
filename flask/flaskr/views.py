from flask import request, redirect, url_for, render_template, flash
from flaskr import app

@app.route('/')
@app.route('/card')
def show_card():
    cards = [0,0,0,0,0,1,0,0,0,0,0,0]
    return render_template('show_card.html',cards=cards)


@app.route('/quantum')
def show_card_quantum():
    cards = [0,0,0,0,0,1,0,0,0,0,0,0]
    return render_template('show_card_quantum.html',cards=cards)


@app.route('/mahojin')
def show_mahojin():
    cards = [0,0,0,0,0,1,0,0,0,0,0,0]
    return render_template('show_mahojin.html',cards=cards)
