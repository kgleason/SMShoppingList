from models import *
from app import db
import re
from twilio.rest import TwilioRestClient
from config import CONFIG

def process_sms(r):
    from_number = str(r.values.get('From', None))
    
    person = Person.find_by_mobile(from_number)
    
    if not person:
        return "You need to be invited to this service in order to use it."
        
    text = r.values.get('Body', None)
    
    words = text.split()
    
    if words[0].lower() == "#invite":
        if from_number in CONFIG['ADMIN_MOBILE_NUMBERS']:
            return invite_new_user(person=person, txt=words[1:])
        else:
            return "You are not an admin. You are not allowed to invite new users."
    else:
        li = ListItem(list_item = text, created_by = person.id)
        db.session.add(li)
        db.session.commit()
        return "Added \"{0}\" to the list".format(text)
        
def invite_new_user(person, txt):
    fname = txt[0]
    lname = txt[1]
    mbl = "+1{0}".format(txt[2])
    p = Person.query.filter(Person.mobile == mbl).first()
    if not p:
        p = Person(firstname = fname, lastname = lname, mobile = mbl)
        db.session.add(p)
        db.session.commit()
    
        send_sms(person=p, msg="Please save me in your contacts as Shopping List. If you text things to me, I will add them to the shopping list.")
        send_sms(person=p, msg="You can view the current shopping list at {0}".format(CONFIG['SHOPPING_LIST_URL']))
        return "Successfully added {0}.".format(p.display_name)
    else:
        return "{0} already exists with mobile number {1}".format(p.display_name, p.mobile)
    
def send_sms(person, msg):
    
    try:
        client = TwilioRestClient(CONFIG['TWILIO_ACCOUNT_SID'], CONFIG['TWILIO_AUTH_TOKEN']) 
        output = client.messages.create(to=person.mobile, from_='TWILIO_NUMBER',body=msg)  
    except Exception, e:
        print "Unable to send SMS to {0}".format(person.mobile)  