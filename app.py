from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Admin_user, Departed, Post
from forms import User_registration, Create_memorial_form, Post_form, LoginForm
from flask_uploads import configure_uploads, IMAGES, UploadSet
import datetime
from os import getenv
import requests, base64

# ****NEED TO ALSO INSTALL Flask-Reloaded TO FIX BUGS IN flask_uploads!!!


#TODO:
# from forms import User_registration, User_login, Admin_registration, Admin_login

app=Flask(__name__)

# original local postgresql db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///remembertogether'

#secure variables
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQL_CONNECTION_STRING')
app.config['SECRET_KEY']= getenv('API_SECRET_KEY')

app.config['FLORIST_ONE_KEY']= getenv('FLORIST_ONE_KEY')
app.config['FLORIST_ONE_PASSWORD']= getenv('FLORIST_ONE_PASSWORD')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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


#ADMINISTRATE FACILITY & SUBDOMAIN
#create_facility
#edit_facility
#delete_facility

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

    if departed.event_start:
        event_times = departed.event_start.strftime("%B %d, %Y from %I:%M %p")
        if departed.event_end:
            event_times += departed.event_end.strftime(" to %I:%M %p")
    else:
        event_times = ''
    

    # event_room = departed.event.room
    return render_template('obituary.html', departed=departed, posts=posts, event_times=event_times) 


@app.route('/reg_login')
def reg_login(): 
    login_form = LoginForm()
    registration_form=User_registration()
    '''registers or logs in a person to create a new obituary'''
    return render_template('reg_login.html', login_form=login_form, registration_form=registration_form)

#TODO: FIX GREYED-OUT 'LOGIN FIRST'
@app.route('/create', methods=["GET","POST"])
def create_obituary():
    """ renders form to create a new obituary """
    form = Create_memorial_form()
    # user = User.query.get(user_id)

    if "user_id" not in session:
        flash("You must login or register to create a memorial.")
        return redirect("/")

    if form.validate_on_submit(): #csrf & is POST
        
        fname = form.fname.data   
        lname = form.lname.data

        born= form.born.data
        died=form.died.data

        city_born = form.city_born.data
        state_born = form.state_born.data

        headshot = images.save(form.headshot.data)
        hero1 = images.save(form.hero1.data)
        hero2 = images.save(form.hero2.data)

        biography = form.biography.data
        text_color = form.text_color.data
        headline = form.headline.data
        booked_yet = form.booked_yet.data
        funeral_home_name = form.funeral_home_name.data
        

        event_start_date = form.event_start_date.data  #date field
        event_start_time = form.event_start_time.data  #time field
        event_end = form.event_end.data  #time field


        #convert timestamp to time
        #logic for case = not entered
        if event_start_date and event_start_time:
            event_start = merge_into_DateTime(event_start_date, event_start_time)
        elif event_start_date and (not event_start_time):
            event_start = event_start_date
        else:
            event_start = None

        if  event_start_date and event_end:
            event_end = merge_into_DateTime(event_start_date, event_end)
        else:
            event_end = None


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

        flash(f"Successfully created {fname} {lname}.")
        flash("You can enter their name in search bar to view their memorial,")
        flash("edit it and share memories.")
        return redirect('/')

    else:
        return render_template("create-memorial.html", form=form)


@app.route('/edit/<int:departed_id>',methods=["GET","POST"])
def edit_obituary(departed_id):
    """form and functionality to edit an obituary/memorial"""
    departed = Departed.query.get_or_404(departed_id)
    form = Create_memorial_form(obj=departed)

    if form.validate_on_submit(): #csrf & is POST

        departed.fname = form.fname.data   
        departed.lname = form.lname.data

        departed.born= form.born.data
        departed.died=form.died.data

        departed.city_born = form.city_born.data
        departed.state_born = form.state_born.data

        departed.headshot = form.headshot.data
        departed.hero1 = form.hero1.data
        departed.hero2 = form.hero2.data


        departed.biography = form.biography.data
        departed.text_color = form.text_color.data
        departed.headline = form.headline.data
        departed.booked_yet = form.booked_yet.data
        departed.funeral_home_name = form.funeral_home_name.data
        
        #convert back to 
        departed.event_start_date = form.event_start_date.data  #date field
        departed.event_start_time = form.event_start_time.data  #time field
        departed.event_end = form.event_end.data  #time field

        #convert timestamp to time
        # departed.event_start = merge_into_DateTime(event_start_date, event_start_time)
        # departed.event_end = merge_into_DateTime(event_start_date, event_end)


        departed.room = form.room.data
        departed.event_address = form.event_address.data
        departed.event_city = form.event_city.data
        departed.event_state = form.event_state.data
        departed.event_zip = form.event_zip.data
        departed.event_phone = form.event_phone.data
        departed.event_url = form.event_url.data


        db.session.commit()

        flash(f"Successfully edited {departed.fname} {departed.lname}")
        return redirect(f'/memorial/{departed_id}')

    else:
        return render_template("edit-memorial.html", form=form, departed=departed)


@app.route('/createpost/<int:departed_id>', methods = ["GET","POST"])
def create_post(departed_id):
    '''Create a post linked to a specific departed person'''
    #TODO: only allow signed-in person to do it
    #TODO: send notice to moderator to approve if wanted

    form = Post_form()
    departed = Departed.query.get_or_404(departed_id)

    if "user_id" not in session:
        flash(f"Please register or login first to share a memory")
        return redirect(f'/memorial/{departed_id}')

    if form.validate_on_submit(): #csrf & is POST
        text = form.text.data   

        file_url=""
        picture = form.file_url.data
        #IMPORTANT: SYNTAX FOR PHOTO FILE DOWNLOAD
        try:
            file_url = images.save(picture)
        except:
            print("****PICTURE NOT INCLUDED IN POST****")

        #TODO: FIX THIS - from SIGN-IN GET USER INFO from SESSION
        user_id = 1

        post =  Post(text=text, departed_id=departed_id, file_url=file_url, user_id=user_id)
        

        db.session.add(post)
        db.session.commit()

        flash(f"Thanks for sharing your memory!")
        return redirect(f'/memorial/{departed_id}')

    else:
        return render_template("create_post.html", form=form,departed=departed)


@app.route('/editpost/<int:post_id>',methods=["GET","POST"])
def edit_post(post_id):
    """form and functionality to edit an memory/post"""
    post = Post.query.get_or_404(post_id)
    departed = Departed.query.get_or_404(post.departed_id)

    form = Post_form(obj=post)

    if form.validate_on_submit(): #csrf & is POST

        post.id = post_id
        post.departed_id = departed_id 
        post.text = form.text.data   
        post.file_url = form.file_url.data

        db.session.commit()

        flash(f"Successfully edited your shared memory")
        return redirect(f'/memorial/{post.departed_id}')

    else:
        return render_template(f"edit-post.html", form=form, departed=departed, post=post)



@app.route('/register',methods=["GET","POST"])
def user_register():
    """registration for new users (family members)"""
    form = User_registration()

    if form.validate_on_submit(): #csrf & is POST
        
        fname = form.fname.data  
        lname = form.lname.data 

        email = form.email.data 
        pwd = form.password.data
        # accept_tos = form.accept_tos.data

        #TODO - departed lookup/id 

        user = User.register(fname, lname, email, pwd)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        flash(f"Welcome {fname}, you have successfully registered.")
        flash("You can create a memorial or post memories of someone you love now.")
        #TODO - route to departed-specific page - every post needs to go to that specific person's file
        return redirect('/')

    else:
        return render_template("add_user.html", form=form)

@app.route('/register/<int:departed_id>',methods=["GET","POST"])
def user_register_from_departed(departed_id):
    """registration for new users (family members)"""
    form = User_registration()

    if form.validate_on_submit(): #csrf & is POST
        
        fname = form.fname.data  
        lname = form.lname.data 

        email = form.email.data 
        pwd = form.password.data
        # accept_tos = form.accept_tos.data

        #TODO - departed lookup/id 

        user = User.register(fname, lname, email, pwd)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        flash(f"Welcome {fname}, you have successfully registered.")
        flash("You can create a memorial or post memories of someone you love now.")
        #TODO - route to departed-specific page - every post needs to go to that specific person's file
        return redirect(f'/memorial/{departed_id}')

    else:
        return render_template("add_user.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(email, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            flash("You are logged in successfully.")
            return redirect("/")

        else:
            form.email.errors = ["Bad email/password"]

    return render_template("login.html", form=form)
# end-login


@app.route("/login/<int:departed_id>", methods=["GET", "POST"])
def login_from_departed(departed_id):
    """Produce login form or handle login."""

    form = LoginForm()
    departed = Departed.query.get(departed_id)

    if form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(email, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            flash("You are logged in and can share memories and more now.")
            return redirect(f"/memorial/{departed_id}")

        else:
            form.email.errors = ["Bad email/password"]

    return render_template("login.html", form=form, departed=departed)
# end-login



@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")



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

    merged_datetime = datetime.datetime.combine(date_var,time_var)
    #remove timezone info (do on client-side)
    merged_datetime = merged_datetime.replace(tzinfo=None)

    return merged_datetime



################################################################################
@app.route("/sendflowers/<int:departed_id>")
def send_flowers(departed_id):
    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')

    departed=Departed.query.get_or_404(departed_id)


    resp = requests.get('https://www.floristone.com/api/rest/flowershop/getproducts', auth=(flower_user, flower_pass))



    print("##################################")
    print(resp.json())
    print("##################################")
    # print(resp.json())  #converts the json string into python dictionary

    return render_template("flowers.html", departed=departed)