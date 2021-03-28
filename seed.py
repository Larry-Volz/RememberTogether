from models import Departed, db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
Departed.query.delete()
User.query.delete()
Post.query.delete()

#Add departed

leonard = Departed(fname='Leonard', lname='Nimoy',born='1931-03-26', died='2015-02-17')
harry = Departed(fname='Harry',lname="Anderson", born='1952-10-14',died='2018-04-16',city_born='Newport',state_born='RI', headshot='http://127.0.0.1:5000/static/images/harry-anderson_face.jpg')
eddie = Departed(fname='Eddie',lname="VanHalen", born='1955-01-26', died='2020-10-06')
roy = Departed(fname='Roy',lname='Horn', born='1944-10-3', died='2020-04-08')
terry = Departed(fname='Terry',lname='Jones', born='1942-02-01', died='2020-01-21', city_born='Colwyn Bay', state_born='North Wales')
carl = Departed(fname='Carl',lname='Reiner', born='1922-03-20', died='2020-06-29', city_born='the Bronx', state_born='NY')

# david = Departed(fname='David',lname='Lander')
# neil = Departed(fname='Neil',lname='Pert')
# prince = Departed(fname='Prince',lname="!")
# ruth = Departed(fname='Ruth',lname="Bader Ginsburg")
# alex = Departed(fname='Alex',lname='Trebek')


db.session.add(leonard)
db.session.add(harry)
db.session.add(eddie)
db.session.add(roy)
db.session.add(terry)
db.session.add(carl)

# db.session.add(prince)
# db.session.add(ruth)
# db.session.add(david)
# db.session.add(neil)
# db.session.add(alex)

#ADD USERS

larry = User(fname='Larry', lname='Volz', email='imaginologist@gmail.com', password='magic')
zach = User(fname='Zachary', lname='Volz', email='zach@gmail.com', password='nascar')
faniel = User(fname='Nathaniel', lname='Volz', email='faniel@gmail.com', password='chess')

db.session.add(faniel)
db.session.add(larry)
db.session.add(zach)

#ADD POSTS - HARRY ANDERSON
newpost1 = Post(text='Harry Anderson died much too young.  At just 65 he not only made us all laugh in Cheers, Night Court, Saturday Night Live and on stages around the world.  He also was a teacher and mentor to magicians and comedians everywhere.  ', file_url='http://127.0.0.1:5000/static/images/harry-anderson1.jpg', user_id = 1, departed_id = 2)

newpost2 = Post(text='Harry Anderson was also a family man - survived by his wife and son.  Both of whom are adorable.', file_url='http://127.0.0.1:5000/static/images/harry-anderson2.jpg', user_id = 2, departed_id = 2)

newpost3 = Post(text='“Night Court,” which ran from 1984 to 1992, more than held its own against juggernauts like “Cheers,” “The Cosby Show” and “The Golden Girls” during a storied period for sitcoms.  It was nominated for 31 Emmys and won seven. John Larroquette, Markie Post, Richard Moll, Charles Robinson and Marsha Warfield starred alongside Mr. Anderson. -- The New York TImes', file_url='http://127.0.0.1:5000/static/images/harry-anderson3.jpg', user_id = 3, departed_id = 2)

newpost4 = Post(text='“Mr. Anderson is survived by his wife, the former Elizabeth Morgan, and two children from his first marriage, to Leslie Pollack: Eva Fay Anderson, a writer and producer in Los Angeles; and Dashiell Anderson, a teacher. -- The New York TImes', file_url='http://127.0.0.1:5000/static/images/harry-anderson4.jpg', user_id = 1, departed_id = 2)


db.session.add(newpost1)
db.session.add(newpost2)
db.session.add(newpost3)
db.session.add(newpost4)


db.session. commit()

