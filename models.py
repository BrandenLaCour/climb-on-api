from peewee import *
from flask_login import UserMixin

DATABASE  = SqliteDatabase('climbs.sqlite')


class User(UserMixin, Model):
    username=CharField(unique=True)
    password=CharField()
    email=CharField()
    city=CharField(default = '')
    picture=CharField(default = 'https://pixabay.com/vectors/blank-profile-picture-mystery-man-973460/')

    class Meta():
        database = DATABASE


class Climb(Model):
    name= CharField()
    grade=CharField()
    location=CharField()
    date=DateField()
    rating=CharField()
    thoughts=CharField()
    picture=CharField()
    user=ForeignKeyField(User, backref='climbs')

    class Meta():
        database= DATABASE


def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User, Climb], safe=True)
    print("connected to the Db and created tables if they didn't exist")

    DATABASE.close()