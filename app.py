from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Admin_user, Departed, Post
from forms import User_registration, Create_memorial_form
from flask_uploads import configure_uploads, IMAGES, UploadSet
import datetime

# ****NEED TO ALSO INSTALL Flask-Reloaded TO FIX BUGS IN flask_uploads!!!



#TODO:
# from forms import User_registration, User_login, Admin_registration, Admin_login

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///remembertogether'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='magic'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['UPLOADED_IMAGES_DEST'] = 'static/images'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

        born= form.born.data
        died=form.died.data

        city_born = form.city_born.data
        state_born = form.state_born.data

        headshot = images.save(form.headshot.data)
        hero1 = images.save(form.hero1.data)
        hero2 = images.save(form.hero2.data)


         #TODO: scaffolding - remove
        print('*****************POSTS:')
        print("HEADSHOT:",headshot)
        print("hero1:",hero1)
        print("hero2:",hero2)
        print('***********************')

        # post_photo(headshot)
        # post_photo(hero1)
        # post_photo(hero2)


        biography = form.biography.data
        text_color = form.text_color.data
        headline = form.headline.data
        booked_yet = form.booked_yet.data
        funeral_home_name = form.funeral_home_name.data
        
        #TODO: event start date & time from form combine to -> event_start -> into model & db
        #TODO: A method to take event_start and break into a date and time
        event_start_date = form.event_start_date.data
        event_start_time = form.event_start_time.data
        event_end = form.event_end.data
        #convert timestamp to time
        # event_end = datetime.datetime.fromtimestamp(event_end).isoformat()
        # event_end = event_end.replace(tzinfo=None)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        print(f'event_end: {event_end}')
        print("+++++++++++++++++++++++++++++++++++++++++++++++")

        event_start = merge_into_DateTime(event_start_date, event_start_time)
        event_end = merge_into_DateTime(event_start_date, event_end)

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


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def post_photo(photo):
    # filename = secure_filename(photo.filename)
    # photo.save(os.path.join(app.instance_path, '/static/images', filename))

def merge_into_DateTime(date_var, time_var):
    """take a date_time object andextract the date and a time object from a form and add the time to the date to make a new, complete date_time object that can be passed into sqlalchemy"""
    # (year, month, day)
    # start_date = date_var.date()
    # (hours, minutes)
    # start_time = time_var.time()
    # Create a datetime object
    # merged_datetime = datetime.datetime.combine(
    #     date_var, time_var)
    merged_datetime = datetime.datetime.combine(date_var,time_var)
    merged_datetime = merged_datetime.replace(tzinfo=None)
    print(f'************************************************************************')
    print(f'date_var: {date_var}, time_var: {time_var}')
    print(f'Merged_datetime: {merged_datetime}')
    print(f'************************************************************************')
    return merged_datetime
