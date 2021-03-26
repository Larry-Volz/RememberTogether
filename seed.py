from models import Pet, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Pet.query.delete()

#Add pets
griffin = Pet(name='Griffin', species='dog', photo_url= "http://127.0.0.1:5000/static/images/shih-tzu.png", age=15, notes='Griffin is an adorable little guy who, despite only being 12 lbs, is a true guardian.  He''ll let you know if the kids are misbehaving and sleep beside you to keep you safe.  Good natured, friendly and affectionate you can''t find a more adorable and loving pet.  He''s great with families and the perfect size for an apartment companion.', available = False)

starlight = Pet(name='Starlight', species='cat', photo_url="http://127.0.0.1:5000/static/images/cockatoo.jpg", age= 20, notes="Starlight is a 20 year old umbrella cockatoo and a brilliant and affectionate pet.  She is full flight and has been trained to come when called, wave 'hello' and even do the 'hokey pokey.'  A playful charmer she needs LOTS of attention and affection and will only be given to a good home to owners that have references and experience with parrots.", available = False)

yoda = Pet(name='Yoda', species='cat', photo_url="http://127.0.0.1:5000/static/images/calico.jpg", age=8,notes = "Yoda is an 8 year old playful and fun calico kitty.  Her full name is Yoda-dora the Jedi explorer (named by a four and an 8 year old) and loves laser pointers, cat-nip and shrimp.", available = True)

fred = Pet(name='Fred', species='dog', photo_url= "http://127.0.0.1:5000/static/images/yorkie.png", age=15, notes='Fred is an adorable little guy with a ton of personality.  He has a TON of energy and loves to chase and be chased.  Being a little guy, he''s great with families and the perfect size for an apartment companion.', available = False)

db.session.add(yoda)
db.session.add(starlight)
db.session.add(griffin)
db.session.add(fred)

db.session. commit()

