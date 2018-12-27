# SMS Shopping List

This app is to allow my family, who seem to prefer to send text messages with shopping items, to text them to a place where they will be stored and displayed in a sensible format. Try going to the grocery store sometime with a shopping list split across 3 different text conversations. Not fun.

## Getting started.

In order to use this app, you'll need a Twilio account and a Heroku account. You don't technically need to use Heroku, but this document will assume that you are. Heroku has documentation to help you get this app deployed. You can connect Heroku into git, but before you deploy it, you'll need to set the following config variables:

  * TWILIO_ACCOUNT_SID: You can find this on your Twilio account page.
  * TWILIO_AUTH_TOKEN: You'll also find this on your Twilio account page.
  * TWILIO_NUMBER: Also from Twilio. You'll have to provision a number.
  * SHOPPING_LIST_URL: This is the URL for the site where the app lives. You can use the herokuapp.com address if you want. This will be texted back to you when add something to the list.
  * DISABLE_COLLECTSTATIC: Set this to 1. For some reason the app hangs on some deployments without this.

With those out of the way, you'll need to provision a database: 

 `heroku addons:create heroku-postgresql:hobby-dev`

That will get you a free postgresql database. As of the writing of this, it will hold up to 10,000 rows. Once the database is provisioning, Heroku will have created the last config variable that you need: DATABASE_URL.

Now you can deploy the app with `git push heroku master`.

## Setting up the database

Now the app the is deployed, the last thing to do is to get the database set up. The first thing is to actually build the database structures: `heroku run python manage.py db upgrade`.

Lastly, we need to manually create a single user, who is an admin:


    heroku run python manage.py shell
    >>> import app
    >>> from app.models import *
    >>> p = Person(firstname='Your First Name',lastname='Your Last Name',mobile='+18885551212',isAdmin=True)
    >>> db.session.add(p)
    >>> db.session.commit()


With some obvious substitutions, that should create a new user. Don't forgot to format the phone number properly. It needs to start with a + sign, followed by a 1, then your area code, and your phone number.

With that out of the way, you can ctrl D, and you should be up and running.