import os
from flask import render_template, request
from app import app
from models import *
from sms import process_sms
import twilio.twiml

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

@app.route('/listitem/<int:id>', methods=['GET', 'POST'])
def completeListItem(id):
  if request.method == 'POST':
    li = ListItem.query.filter(ListItem.id == id).first()
    if li:
      li.closed = True
      db.session.add(li)
      db.session.commit()

  return render_template('index.html', my_list=ListItem.all_open())

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    if request.method == "POST":
        message = process_sms(r=request)
    else:
        message = "Sorry, but HTTP {0} is not currently allowed.".format(request.method)

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)
