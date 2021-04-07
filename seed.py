from models import Departed, db, User, Post, Admin_user
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
Departed.query.delete()
User.query.delete()
Post.query.delete()

#Add departed

# example = Departed(fname='', lname='', born='', died='', city_born='', state_born='', headshot='', hero1='', hero2='', biography='', text_color='', headline='', booked_yet=  , funeral_home_name='', event_start='', event_end='', room='', event_address='', event_city='', event_state='', event_zip='', event_phone='', event_url='')

ruth = Departed(fname='Ruth', lname='Bader Ginsburg', born='1933-03-15', died='2020-09-18', city_born='Brooklyn', state_born='NY', 
headshot='RBG_headshot.jpg', 
hero1='RBG_hero2.jpg', 
hero2='RBG_hero1.jpg', 
biography='Joan Ruth Bader Ginsburg (/ˈbeɪdər ˈɡɪnzbɜːrɡ/ BAY-dər GINZ-burg; née Bader; March 15, 1933 – September 18, 2020) was an American lawyer and jurist who served as an associate justice of the Supreme Court of the United States from 1993 until her death in September 2020.[1] She was nominated by President Bill Clinton, replacing retiring justice Byron White,[2] and at the time was generally viewed as a moderate consensus-builder. She eventually became part of the liberal wing of the Court as the Court shifted to the right over time. Ginsburg was the first Jewish woman and the second woman to serve on the Court, after Sandra Day O''Connor. During her tenure, Ginsburg wrote notable majority opinions, including United States v. Virginia (1996), Olmstead v. L.C. (1999), Friends of the Earth, Inc. v. Laidlaw Environmental Services, Inc. (2000), and City of Sherrill v. Oneida Indian Nation of New York (2005).<br>Here is some more text.  <br> But this time I am including HTML so people can format their biographies better.  <bold> I hope it works!</bold>', 
text_color='white', 
headline='Fight for the things you care about.  But do it in a way that will lead others to join you.', 
booked_yet= True, 
funeral_home_name='Resting Hearts Funeral Home', 
event_start='2020-09-23 14:00:00.0', 
event_end='2020-09-23 15:00:00.0', 
room='Memorial room C', 
event_address='365 Downing St.', 
event_city='Washington', 
event_state='DC', 
event_zip='23999', 
event_phone='804-227-1111', 
event_url='testingurl.com')



leonard = Departed(fname='Leonard', lname='Nimoy',born='1931-03-26', died='2015-02-17', city_born='Boston', state_born='MA', headshot='nimoy_headshot.jpg', hero1='nimoy_hero1.jpg', hero2='nimoy_hero3.jpg',biography='"I''m touched by the idea that when we do things that are useful and helpful - collecting these shards of spirituality - that we may be helping to bring about a healing"Despite a career that also embraced directing, writing and photography, he never managed to escape the character that came to define him.  At times it seemed the actor and character were becoming one and the same person and Nimoy battled with alcohol abuse as a result.  But he eventually derived great satisfaction from the role that dominated his life.', text_color="white", headline='Live long and prosper', 
booked_yet= True , 
funeral_home_name='Shady Pines Funeral Home', 
event_start='2015-03-02 18:00:00.0', 
event_end='2015-03-02 19:00:00.0', 
room='Memorial room 2', 
event_address='2 Main street.', 
event_city='Boston', 
event_state='MA', 
event_zip='32185', 
event_phone='800-299-1991', 
event_url='anotherfuneralhome.com')


harry = Departed(fname='Harry',lname="Anderson", 
born='1952-10-14',died='2018-04-16',
city_born='Newport',state_born='RI', 
headshot='harry-anderson_face.jpg', 
hero1='harry_anderson_hero1.jpeg',
hero2='harry_anderson_hero2.jpg',
biography='Harry Anderson, the actor best known for playing an off-the-wall judge working the night shift of a Manhattan court room in the television comedy series "Night Court," was found dead in his North Carolina home Monday.Anderson was 65.A statement from the Asheville Police Department said officers responded to a call from Anderson''s home early Monday and found him dead. The statement said foul play is not suspected.On "Night Court," Anderson played Judge Harry T. Stone, a young jurist who professed his love for singer Mel Torme, actress Jean Harlow, magic tricks and his collection of art-deco ties."I am richer than Davy Crockett," Anderson said in the story. "I can settle back and do what I want to do. And what I want to do is card tricks and magic." That includes magic shows for corporate clients ("Fifty-five minutes with applause," says Anderson) at $20,000 a pop.', 
text_color="white", 
headline='"Every fool knows you can''t touch the stars, but it doesn''t stop a wise man from trying. "', 
booked_yet= True , 
funeral_home_name='Foo Funeral home', 
event_start='2018-04-15 12:00:00.0', 
event_end='2018-04-15 13:30:00.0', 
room='Memorial room 1', 
event_address='1 Testing drive', 
event_city='Los Angeles', 
event_state='CA', 
event_zip='90210', 
event_phone='555-867-5309', 
event_url='afuneralhome.com'
)



# eddie = Departed(fname='Eddie',lname="VanHalen", born='1955-01-26', died='2020-10-06')
# roy = Departed(fname='Roy',lname='Horn', born='1944-10-3', died='2020-04-08')
# terry = Departed(fname='Terry',lname='Jones', born='1942-02-01', died='2020-01-21', city_born='Colwyn Bay', state_born='North Wales')
# carl = Departed(fname='Carl',lname='Reiner', born='1922-03-20', died='2020-06-29', city_born='the Bronx', state_born='NY')

# david = Departed(fname='David',lname='Lander')
# neil = Departed(fname='Neil',lname='Pert')
# prince = Departed(fname='Prince',lname="!")
# alex = Departed(fname='Alex',lname='Trebek')


db.session.add(harry)
db.session.add(leonard)
db.session.add(ruth)
# db.session.add(eddie)
# db.session.add(roy)
# db.session.add(terry)
# db.session.add(carl)

db.session.commit()


# db.session.add(prince)
# db.session.add(david)
# db.session.add(neil)
# db.session.add(alex)


#ADD ADMINS
larry_admin = Admin_user(fname='Larry', lname='Volz', email='imaginologist@gmail.com', phone='804-882-1951', username='larryvolz', password='magic', admin_type='1')

db.session.add(larry_admin)
db.session.commit()

#ADD EVENTS
# harry_event = Event(when_start = '2018-04-15 12:00:00.0', when_end = '2018-04-15 12:00:00.0', admin_id=1, room="Memorial room 1")

# leonard_event = Event(when_start = '2015-03-02 18:00:00.0', when_end = '2015-03-02 19:00:00.0', admin_id=1, room="Memorial room 2")

# ruth_event = Event(when_start = '2020-09-23 14:00:00.0', when_end = '2020-09-23 15:00:00.0', admin_id=1, room="Memorial room 1")

# db.session.add(ruth_event)
# db.session.add(leonard_event)
# db.session.add(harry_event)

# db.session.commit()

#ADD Departed-events mappings
# ruth_event_mapper = Departed_event(departed_id=1, event_id=1)
# leonard_event_mapper = Departed_event(departed_id=2, event_id=1)
# harry_event_mapper = Departed_event(departed_id=2, event_id=1)

# db.session.add(ruth_event_mapper)
# db.session.add(leonard_event_mapper)
# db.session.add(harry_event_mapper)

# db.session.commit()

#ADD USERS
larry = User(fname='Larry', lname='Volz', email='imaginologist@gmail.com', password='magic')
zach = User(fname='Zachary', lname='Volz', email='zach@gmail.com', password='nascar')
faniel = User(fname='Nathaniel', lname='Volz', email='faniel@gmail.com', password='chess')

db.session.add(faniel)
db.session.add(larry)
db.session.add(zach)

db.session.commit()


#ADD POSTS - HARRY ANDERSON
newpost1 = Post(text='Harry Anderson died much too young.  At just 65 he not only made us all laugh in Cheers, Night Court, Saturday Night Live and on stages around the world.  He also was a teacher and mentor to magicians and comedians everywhere.  ', 
file_url='harry-anderson1.jpg', 
user_id = 1, 
departed_id = 1)


newpost2 = Post(text='Harry Anderson was also a family man - survived by his wife and son.  Both of whom are adorable.', file_url='harry-anderson2.jpg', user_id = 2, departed_id = 1)

newpost3 = Post(text='“Night Court,” which ran from 1984 to 1992, more than held its own against juggernauts like “Cheers,” “The Cosby Show” and “The Golden Girls” during a storied period for sitcoms.  It was nominated for 31 Emmys and won seven. John Larroquette, Markie Post, Richard Moll, Charles Robinson and Marsha Warfield starred alongside Mr. Anderson. -- The New York TImes', file_url='harry-anderson3.jpg', user_id = 3, departed_id = 1)

newpost4 = Post(text='“Mr. Anderson is survived by his wife, the former Elizabeth Morgan, and two children from his first marriage, to Leslie Pollack: Eva Fay Anderson, a writer and producer in Los Angeles; and Dashiell Anderson, a teacher. -- The New York TImes', file_url='harry-anderson4.jpg', user_id = 1, departed_id = 1)


db.session.add(newpost1)
db.session.add(newpost2)
db.session.add(newpost3)
db.session.add(newpost4)

db.session.commit()

