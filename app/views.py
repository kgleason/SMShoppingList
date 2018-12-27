import os
from flask import render_template, request
from app import app, socketio
from app.models import ListItem, Person, desc, db
from sms import process_sms
import twilio.twiml
from flask.ext.socketio import emit
import json, re


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
    if request.method == "POST":
        message = process_sms(r=request)
    else:
        message = "Sorry, but HTTP {0} is not currently allowed.".format(request.method)

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)


@socketio.on('value changed')
def value_changed(message):
    print(message)
    #values[message['who']] = message['data']
    emit('update value', message, broadcast=True)


@socketio.on('checkbox changed')
def checkbox_changed(message):
    print(message)
    update_item_status(message)
    emit('update checkbox', message, broadcast=True)


def insert_row(message):
    print(json.dumps(message))
    socketio.emit('insert row', json.dumps(message))


def update_item_status(data):
    id = re.match('.*?([0-9]+)$', data['who']).group(1)
    print('Changing closed status of {0} to {1}'.format(id, data['data']))
    li = ListItem.query.filter(ListItem.id == id).first()
    if li:
        li.closed = data['data']
        db.session.add(li)
        db.session.commit()
