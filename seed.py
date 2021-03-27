from models import Departed, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Departed.query.delete()

#Add departed
deane = Departed(fname='David', lname='Dean')
johnny = Departed(fname='Johnny', lname='Moser')
brookelyn = Departed(fname='Brookelyn', lname='Latham')
jeannette = Departed(fname='Jeannette', lname='Cox')
jim = Departed(fname='Jim', lname='Richmond, Sr.')


db.session.add(deane)
db.session.add(johnny)
db.session.add(jeannette)
db.session.add(jim)

db.session. commit()

