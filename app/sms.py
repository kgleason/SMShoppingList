from app.models import Person, ListItem
from app import db
from app import views
import os, re
from twilio.rest import Client


def process_sms(r):
    from_number = str(r.values.get('From', None))

    person = Person.find_by_mobile(from_number)

    if not person:
        return "You need to be invited to this service in order to use it."

    text = r.values.get('Body', None)

    words = text.split()

    if words[0].lower() == "#invite":
        if from_number in Person.all_admin_phones()[0]:
            return invite_new_user(inviter=person, txt=words[1:])
        else:
            return "{0} You are not an admin. You are not allowed to invite new users.".format(from_number)
    else:
        li = ListItem(list_item = text, created_by = person.id)
        db.session.add(li)
        db.session.commit()
        new_row = { 'id': li.id,
                    'checked': False,
                    'creator': li.creator,
                    'created': li.created_in_words,
                    'item': li.list_item }
        views.insert_row(new_row)
        return "Added \"{0}\" to the list. You can view the list at {1}".format(text, os.environ.get('SHOPPING_LIST_URL'))


def invite_new_user(inviter, txt):
    fname = txt[0]
    lname = txt[1]
    mbl = re.sub(r"[^\w\s]",'',txt[2])

    if list(mbl)[0] == "1":
        mbl = "+{0}".format(mbl)
    elif len(mbl) == 10 and re.match('[2-9]',list(mbl)[0]):
        mbl = "+1{0}".format(mbl)

    newb = Person.query.filter(Person.mobile == mbl).first()
    if not newb:
        newb = Person(firstname = fname, lastname = lname, mobile = mbl)
        db.session.add(newb)
        db.session.commit()

        send_sms(person=newb, msg="Please save me in your contacts as Shopping List. If you text things to me, I will add them to the shopping list.")
        send_sms(person=newb, msg="You can view the current shopping list at {0}".format(os.environ.get('SHOPPING_LIST_URL')))
        return "Successfully added {0}".format(newb.display_name)
    else:
        return "{0} already exists with mobile number {1}".format(newb.display_name, newb.mobile)


def send_sms(person, msg):

    try:
        client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
        client.messages.create(to=person.mobile, from_=os.environ.get('TWILIO_NUMBER'),body=msg)
    except Exception as exc:
        print("Unable to send SMS to {0} because {1}".format(person.mobile,exc))
