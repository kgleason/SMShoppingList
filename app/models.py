from app import db
from sqlalchemy import desc
import datetime
from webhelpers.date import time_ago_in_words

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    mobile = db.Column(db.String(12), unique=True)
    
    @classmethod
    def all(cls):
        return Person.query.order_by(Person.lastname, Person.firstname).all()

    @classmethod
    def find_by_mobile(cls, mobile):
        return Person.query.filter(Person.mobile == mobile).first()
        
    @property
    def display_name(self):
        if self.firstname:
            return "{0} {1}".format(self.firstname, self.lastname)
        else:
            return self.mobile
            
class ListItem(db.Model):
    __tablename__ = 'list_item'
    id = db.Column(db.Integer, primary_key=True)
    list_item = db.Column(db.String(200))
    created = db.Column(db.DateTime, default = datetime.datetime.now)
    closed = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('person.id'))
    
    @property
    def creator(self):
        p = Person.query.filter(Person.id == self.created_by)
        return p.display_name
        
    @property
    def created_in_words(self):
        return time_ago_in_words(created)
        
    @classmethod
    def all(cls):
        return ListItem.query.order_by(desc(id)).all()
        
    @classmethod
    def all_open(cls):
        return ListItem.query.filter(ListItem.closed == False).order_by(desc(id)).all()
        
        