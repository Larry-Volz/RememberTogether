from models import Departed, db, User
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Departed.query.delete()

#Add departed

leonard = Departed(fname='Leonard', lname='Nimoy',born='1931-03-26', died='2015-02-17')
harry = Departed(fname='Harry',lname="Anderson", born='1952-10-14',died='2018-04-16',city_born='Newport',state_born='RI')
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

larry = User(fname='Larry', lname='Volz', email='imaginologist@gmail.com', password='magic')
zach = User(fname='Zachary', lname='Volz', email='zach@gmail.com', password='nascar')
faniel = User(fname='Nathaniel', lname='Volz', email='faniel@gmail.com', password='chess')

db.session.add(faniel)
db.session.add(larry)
db.session.add(zach)




db.session. commit()

