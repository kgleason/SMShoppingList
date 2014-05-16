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
    return render_template('person.html', person=p)
    
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    pass
