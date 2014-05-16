import os
from flask import render_template, request
from app import app
from models import *

@app.route('/')
def index():
    return render_template('index.html', my_list=ListItem.all_open())
    
@app.route('/people')
def people():
    return render_template('people.html', people=Person.all())
    
@app.route('/help')
def help():
    return render_template('help.html')
    
@app.route('/person/<int:id>')
def person(id):
    p = Person.query.filter(Person.id == id).first()
    h = None
    if p:
        h = ListItem.query.filter(ListItem.created_by == p.id).order_by(desc(ListItem.id)).limit(50)
    return render_template('person.html', person=p, history=h)
    
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    pass
