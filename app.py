from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Admin_user, Departed, Post
from forms import User_registration
import datetime

#TODO:
# from forms import User_registration, User_login, Admin_registration, Admin_login

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///remembertogether'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='magic'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

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
    # today = utc.localize(datetime.datetime.now())

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


@app.route('/create')
def create_obituary():
    """ renders form to create a new obituary """

    return render_template('create-memorial.html')



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



