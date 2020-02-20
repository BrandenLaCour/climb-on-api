import os
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect
 
if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))

else:
  DATABASE = SqliteDatabase('climbs.sqlite')

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
    rating=SmallIntegerField()
    thoughts=CharField(default='')
    picture=CharField(default='https://prod.wp.cdn.aws.wfu.edu/sites/202/2017/11/empty-avatar-700x480.png')
    user=ForeignKeyField(User, backref='climbs')

    class Meta():
        database= DATABASE


def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User, Climb], safe=True)
    print("connected to the Db and created tables if they didn't exist")

    DATABASE.close()