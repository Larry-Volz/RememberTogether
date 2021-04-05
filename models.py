from flask_sqlalchemy import SQLAlchemy
import datetime
"""Models for RememberTogether"""

db=SQLAlchemy()
def connect_db(app):
    db.app = app 
    db.init_app(app)

'''NOTE: view departed as plural and deceased as singular for sqlalchemy relationship referencing'''


class Departed(db.Model):
    """ Sign-in/contact information for end user """
    __tablename__ = 'departed'

    def __repr__(self):
           return f"departed id={self.id} fname={self.fname} lname={self.lname}"  #for better referencing

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    fname = db.Column(db.Text, nullable = False)
    lname = db.Column(db.Text, nullable = False)
    city_born = db.Column(db.Text, nullable = True)
    state_born = db.Column(db.Text, nullable = True)

    #TODO:  FIX!
    born = db.Column(db.Date, nullable = False)
    died = db.Column(db.Date, nullable = False)

    # born = datetime.datetime.now()
    # died = datetime.datetime.now()

    headshot = db.Column(db.Text, nullable = True) #url for face picture
    hero1 = db.Column(db.Text, nullable = True) #url for large picture 1
    hero2 = db.Column(db.Text, nullable = True) #url for large picture 2
    biography = db.Column(db.Text, nullable = False) #obituary
    headline = db.Column(db.Text, nullable = True)
    text_color = db.Column(db.Text, nullable = True, default = "white")

    booked_yet = db.Column(db.Boolean, nullable=True, default=False)
    funeral_home_name = db.Column(db.Text, nullable = True)

    #TODO: FIX!
    event_start = db.Column(db.DateTime(timezone=True), nullable=True)
    event_end = db.Column(db.DateTime(timezone=True), nullable=True)



    room = db.Column(db.String(30), nullable=True)
    event_address = db.Column(db.String(100), nullable = True)
    event_city = db.Column(db.String(60), nullable = True)
    event_state = db.Column(db.String(2), nullable = True, default = 'VA')
    event_zip = db.Column(db.String(10), nullable = True)
    event_phone = db.Column(db.String(14), nullable = True)
    event_url = db.Column(db.Text, nullable = True)
    
    #TODO: re-factor into additional table(s)
    # event_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    def serialize(self):
        """turn model into a dictionary/JSON format"""
        return {
        'id':self.id,
        'fname':self.fname,
        'lname':self.lname,
        'city_born':self.city_born,
        'state_born':self.state_born,
        'born':self.born,
        'died':self.died,
        'headshot':self.headshot,
        'hero1':self.hero1,
        'hero2':self.hero2,
        'biography':self.biography
    }



class User(db.Model):
    """ Sign-in/contact information for end user """ 
    __tablename__ = 'users'

    def __repr__(self):
           return f"loved one id={self.id} fname={self.fname} lname={self.lname}"  #for better referencing

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    fname = db.Column(db.Text, nullable = False)
    lname = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)

    password = db.Column(db.Text, nullable = False)
    # salt = db.Column(db.Text, nullable = True)

    # accept_tos = db.Column(db.Boolean, nullable = False)

    # post = db.relationship('Post', backref="user")


class Post(db.Model):
    """posts by users about specific departed 
    newpost = Post(text='', file_url='', user_id = '', departed_id = '')
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    text = db.Column(db.Text, nullable = True)

    file_url = db.Column(db.Text, nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))

    departed_id = db.Column(db.Integer, db.ForeignKey(
        'departed.id'), primary_key=True)

    departed = db.relationship('Departed')
    user = db.relationship('User')


    

class Admin_user(db.Model):
    """ Sign-in/contact information for end user """
    __tablename__ = 'admins'

    def __repr__(self):
           return f"admin user id={self.id} fname={self.fname} lname={self.lname}"  #for better referencing

    id = db.Column(db.Integer,
    primary_key = True,
    autoincrement = True)

    fname = db.Column(db.Text, nullable = False)
    lname = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    phone = db.Column(db.Text, nullable = False)


    username = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)
    # salt = db.Column(db.Text, nullable = True)
    
    admin_type = db.Column(db.Text, nullable = False)

    biz_name = db.Column(db.Text, nullable = True)
    street_address = db.Column(db.Text, nullable = True)
    street_address2 = db.Column(db.Text, nullable = True)
    city = db.Column(db.Text, nullable = True)
    state = db.Column(db.Text, nullable = True)
    zip = db.Column(db.Text, nullable = True)
    website = db.Column(db.Text, nullable = True)



# class Event(db.Model):
#     '''table for individual events - connected to 1 or more departed through event-departed mapping table, also foreign key for admin (funeral home) '''
#     __tablename__ = 'events'

#     def __repr__(self):
#            return f"event id={self.id} fname={self.fname} lname={self.lname}"  #for better referencing
    
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     when_start = db.Column(db.DateTime(timezone=True), nullable=False)
#     when_end = db.Column(db.DateTime(timezone=True), nullable=False)
#     admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
#     room = db.Column(db.String(30), nullable=True)
     
    # facility = db.relationship('Admin_user', backref="event")


# class Departed_event(db.Model):
#     '''mapping table for when there is more than one departed being memorialized'''
#     __tablename__ = 'departed_events'

    # id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # departed_id = db.Column(db.Integer, db.ForeignKey('departed.id'))
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # event = db.relationship('Event', backref="departed_event")
    # deceased = db.relationship('Departed', backref="departed_event")



