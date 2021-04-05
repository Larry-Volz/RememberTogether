from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Admin_user, Departed, Post
from forms import User_registration, Create_memorial_form
import datetime

#for uploading files
import os 
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



#TODO:
# from forms import User_registration, User_login, Admin_registration, Admin_login

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///remembertogether'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='magic'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# debug = DebugToolbarExtension(app)

# WTF_CSRF_SECRET_KEY = 'magic'


connect_db(app)
db.create_all()



@app.route('/')
def home():
    """ home page - should give login option and information about app"""
    
    departed = Departed.query.all()
    return render_template("index.html", departed=departed)

@app.route('/api/departed')
def list_departed():
    """return list of all departed in JSON format for use in jQuery-ui autocomplete"""

    #should turn into [{{'':''},{'':''},{'':''}...}, {{'':''},{'':''},{'':''}...}... ]
    serialized = [friend.serialize() for friend in Departed.query.all()]

    #turns it into {cupcakes:{'':'','':''}}
    return jsonify(departed = serialized)


@app.route('/memorial/<int:id>')
def memorial_page(id):
    """render MEMORIAL/OBITUARY for chosen departed
    TODO:  make it the zoom version if memorial service is currently going on or will be starting within ___ minutes (as set by Admin)"""
    # if (live):
    #     render_template("zoom_memorial.html")
    # else:
    
    # utc = pytc.UTC
    # today = datetime.datetime.now()

    departed = Departed.query.get_or_404(id)
    posts = Post.query.filter_by(departed_id=id).all()

    event_times = departed.event_start.strftime("%B %d, %Y from %I:%M %p to ")
    event_times += departed.event_end.strftime("%I:%M %p")

    
    #TODO: scaffolding - remove
    print('*****************POSTS:')
    print("id:",id)
    for ea in posts:
        print('TEXT:',ea.text)
    print('***********************')
    

    # event_room = departed.event.room
    return render_template('obituary.html', departed=departed, posts=posts, event_times=event_times) 


@app.route('/create', methods=["GET","POST"])
def create_obituary():
    """ renders form to create a new obituary """
    form = Create_memorial_form()

    if form.validate_on_submit(): #csrf & is POST
        
        fname = form.fname.data   
        lname = form.lname.data

        #TODO: FIX!
        # born = form.born.data
        # died = form.died.data

        born= datetime.datetime.now()
        died=datetime.datetime.now()

        city_born = form.city_born.data
        state_born = form.state_born.data

        headshot = form.headshot.data  
        post_photo(headshot)

        hero1 = form.hero1.data
        post_photo(hero1)

        hero2 = form.hero2.data
        post_photo(hero2)


        biography = form.biography.data
        text_color = form.text_color.data
        headline = form.headline.data
        booked_yet = form.booked_yet.data
        funeral_home_name = form.funeral_home_name.data
        
        #TODO: FIX!
        # event_start = form.event_start.data
        # event_end = form.event_end.data  

        event_start = datetime.datetime.now()
        event_end = datetime.datetime.now()

        room = form.room.data
        event_address = form.event_address.data
        event_city = form.event_city.data
        event_state = form.event_state.data
        event_zip = form.event_zip.data
        event_phone = form.event_phone.data
        event_url = form.event_url.data


        departed =  Departed(fname=fname, lname=lname, born=born, died=died, city_born=city_born, state_born=state_born, headshot=headshot, hero1=hero1, hero2=hero2, biography=biography, text_color=text_color, headline=headline, booked_yet=booked_yet , funeral_home_name=funeral_home_name, event_start=event_start, event_end=event_end, room=room, event_address=event_address, event_city=event_city, event_state=event_state, event_zip=event_zip, event_phone=event_phone, event_url=event_url)

        db.session.add(departed)
        db.session.commit()

        flash(f"Successfully created a memorial page for {fname} {lname}.  You can visit their page by typing their name in the search box in the menu")
        return redirect('/')

    else:
        return render_template("create-memorial.html", form=form)




@app.route('/add',methods=["GET","POST"])
def user_sign_in():
    """displays app sign-in form for USERS"""
    form = User_registration()

    if form.validate_on_submit(): #csrf & is POST
        
        fname = form.fname.data  
        lname = form.lname.data 

        email = form.email.data 
        password = form.password.data
        accept_tos = form.accept_tos.data

        #TODO - departed lookup/id 

        user = User(fname=fname, lname=lname, email=email, password=password, accept_tos=accept_tos)

        db.session.add(user)
        db.session.commit()

        flash(f"Successfully created {fname} {lname}")
        #TODO - route to departed-specific page - every post needs to go to that specific person's file
        return redirect('/')

    else:
        return render_template("add_user.html", form=form)

# @app.route('/admin')
# def admin_sign_in():
#     """displays app sign-in form for admin users"""
#     return render_template('admin_sign_in.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def post_photo(photo):
    filename = secure_filename(photo.filename)
    photo.save(os.path.join(app.instance_path, '/static/images', filename))