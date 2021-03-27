from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Admin_user, Departed
from forms import User_registration

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
    #TODO = later use AJAX/Axios query for departed with JSON?
    departed = Departed.query.all()
    return render_template("index.html", departed=departed)

@app.route('/api/departed')
def list_departed():
    """return list of all departed in JSON format"""

    #should turn into [{{'':''},{'':''},{'':''}...}, {{'':''},{'':''},{'':''}...}... ]
    serialized = [friend.serialize() for friend in Departed.query.all()]

    #turns it into {cupcakes:{'':'','':''}}
    return jsonify(departed = serialized)

@app.route('/add',methods=["GET","POST"])
def user_sign_in():
    """displays app sign-in form for end users"""
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

