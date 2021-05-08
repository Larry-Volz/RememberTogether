import datetime
from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads, IMAGES, UploadSet
from forms import User_registration, Create_memorial_form, Post_form, LoginForm, ZipForm, AddFlowerToCart, FlowerOrderForm
import json 
from models import db, connect_db, User, Admin_user, Departed, Post
from os import getenv
import requests, base64
import socket
from flowershop import *
import pdb


# ****NEED TO ALSO INSTALL Flask-Reloaded in requirements TO FIX BUGS IN flask_uploads!!!


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
    session["departed_id"] = id

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
    session["departed_id"] = departed_id

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


#######################################################
#                     FLOWER SHOP                     #
#######################################################


@app.route("/api_tester")
def api_tester():

    added_form = AddFlowerToCart()

    """ Main Page for flower shop """
    departed_id = session['departed_id']
    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')

    departed=Departed.query.get_or_404(departed_id)
    session['departed_id']=departed_id
    
    all_flowers = requests.get('https://www.floristone.com/api/rest/flowershop/getproducts', params={"category": "sy", "count":10000}, auth=(flower_user, flower_pass))
    all_flowers = all_flowers.json()

    #get valid API session # -- also stored in session['cart_id']

    #SCAFFOLDING FOR TESTING PURPOSES
    # session['cart_id'] = "junkyjunkjunknotrealjunkyjunkerson"
    cart_id = flowershop_get_session(flower_user, flower_pass)
    
    #get cart contents from API
    cart_contents = get_cart_contents(cart_id, flower_user, flower_pass)

    #scaffolding
    print_test("CART CONTENTS:", cart_contents)

    return "DONE!"


@app.route("/sendflowers")
def sendflowers():

    added_form = AddFlowerToCart()

    """ Main Page for flower shop """
    departed_id = session['departed_id']
    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')

    departed=Departed.query.get_or_404(departed_id)
    session['departed_id']=departed_id
    
    all_flowers = requests.get('https://www.floristone.com/api/rest/flowershop/getproducts', params={"category": "sy", "count":10000}, auth=(flower_user, flower_pass))
    all_flowers = all_flowers.json()

    #get valid API session # -- also stored in session['cart_id']

    #SCAFFOLDING FOR TESTING PURPOSES
    # session['cart_id'] = "junkyjunkjunknotrealjunkyjunkerson"
    cart_id = flowershop_get_session(flower_user, flower_pass)
    
    #get cart contents from API
    cart_contents = get_cart_contents(cart_id, flower_user, flower_pass)

    #scaffolding
    print_test("CART CONTENTS:", cart_contents)

    return render_template("flowers.html", departed=departed, all_flowers=all_flowers, )



@app.route('/flower-cart', methods=['POST'])
def flower_cart_post():
    """ 
    GET for going directly to the cart
    POST for coming from a clicked flower
    This shows item details and options in cart with ability to purchase, suggestions for add-on products or to continue shopping.  
    (first time) creates cart in API, puts a session id in flask-session 
    (not first time) updates flask-session
    (every time) adds item in cart in API, store in db shopping history as having been carted"""

    # flower_id = request.form['flower_id']
    
    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')

    departed_id=session['departed_id']
    departed=Departed.query.get_or_404(departed_id)

    added_form = AddFlowerToCart()

    feedback=""

    #get valid API cart session # -- also stored in session['cart_id']
    cart_id = flowershop_get_session(flower_user, flower_pass)
    
    #get cart contents from API
    cart_contents = get_cart_contents(cart_id, flower_user, flower_pass)

    # get form info 
    flower_id = request.form['flower_id']
    feedback = "form submitted"

    #Get individual flower
    flower = requests.get('https://www.floristone.com/api/rest/flowershop/getproducts', params={"code": flower_id}, auth=(flower_user, flower_pass))
    flower = flower.json()
    flower = flower['PRODUCTS'][0]

    feedback += f"\r\nFlower requested: {flower['NAME']}"
    feedback += f"\r\nFlower id: {flower_id}"

    #add to cart at API
    # TODO: OUGHTA BE ABLE TO FIND IF NO SESSION AT API HERE
    # JSON atAT API responds:  {errors: {'invalid sessionid'}} - ish...
    resp = requests.put(f"https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}&action=add&productcode={flower_id}",  auth=(flower_user, flower_pass))
    # resp=resp.json()

    # if resp['errors'][0] == 'invalid sessionid'
    """ assuming the error is that the cart/session timed out at API"""
        # session['cart_id'] = None
        # #start a new cart/session
        # session['cart_id'] = create_cart(flower_user, flower_pass)
        # print('**************************************************************')
        # print('INVALID SESSION ID AT API')
        # print(f"resp")
        # print('**************************************************************')
        #     # #TRY again
        # requests.put(f"https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}&action=add&productcode={flower_id}",  auth=(flower_user, flower_pass))

    #get cart contents from API
    cart_contents = requests.get(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}', auth=(flower_user, flower_pass))
    cart_contents = cart_contents.json()
    # cart_contents = cart_contents['products']

    
    flower_urls = get_flower_urls(cart_contents)
    
    
    # zip form to retrieve list of available dates
    form=ZipForm()
    

    #scaffolding
    print("################################################")
    print("FLOWER POSTED")
    print(feedback)
    print("CART CONTENTS")
    for flower in cart_contents['products']:
        print(flower['NAME'])
    print("cart_id:")
    print(session['cart_id'])
    print("################################################")

    # flash("Added to Cart")
    return render_template("flower-cart.html", flower_urls = flower_urls, departed=departed, form=form, cart_contents=cart_contents )



@app.route('/flower-cart', methods=['GET'])
def flower_cart1_get():
    """ 
    GET for going directly to the cart
    POST for coming from a clicked flower
    This shows item details and options in cart with ability to purchase, suggestions for add-on products or to continue shopping.  
    (first time) creates cart in API, puts a session id in flask-session 
    (not first time) updates flask-session
    (every time) adds item in cart in API, store in db shopping history as having been carted"""

    session['page_current']=0
    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')

    departed_id=session['departed_id']
    departed=Departed.query.get_or_404(departed_id)

    added_form = AddFlowerToCart()

    feedback=""

    #get valid API session # -- also stored in session['cart_id']
    cart_id = flowershop_get_session(flower_user, flower_pass)
    
    #get cart contents from API
    cart_contents = get_cart_contents(cart_id, flower_user, flower_pass)

    flower_urls = get_flower_urls(cart_contents)

    # zip form to retrieve list of available dates
    form=ZipForm()
    #scaffolding
    print("################################################")
    print("CART CONTENTS")
    for flower in cart_contents['products']:
        print(flower['NAME'])
    print("cart_id:")
    print(session['cart_id'])
    print("################################################")

    # flash("Added to Cart")
    return render_template("flower-cart.html", flower_urls = flower_urls, departed=departed, cart_contents=cart_contents, form=form)


@app.route('/flower-cart2', methods=['GET', 'POST'])
def flowercart2():
    """ """

    session['page_current']=2

    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')
    departed_id=session['departed_id']
    departed=Departed.query.get_or_404(departed_id)
    cart_id = session['cart_id']
    # zip = session['zip'] 
    form = FlowerOrderForm()

    if session.get('zip') is None: 
        zip = request.form['zip']
        session['zip'] = zip
    else:
        zip = session['zip']

    #TODO: put in next flower-cart with order-processing
    # if session.get('delivery-date') is None:
    #     date = request.form['delivery-date']
    #     session['delivery-date']=date
    # else:
    #     date = session['delivery-date']

    dates = requests.get('https://www.floristone.com/api/rest/flowershop/checkdeliverydate', params={"zipcode": zip}, auth=(flower_user, flower_pass))
    dates = dates.json()

    try:
        dates = dates['DATES']
        session['dates'] = dates
        #SCAFFOLDING - TEMPORARY - PUT BACK
        #dynamically populate delivery_date field
        form.delivery_date.choices = [(date,date) for date in dates]


    except:
        flash("Must enter a valid zip code")
        return redirect (f"/sendflowers")
    

    cart_contents = requests.get(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}', auth=(flower_user, flower_pass))
    cart_contents = cart_contents.json()

    flower_urls = get_flower_urls(cart_contents)



    #TODO: FORWARD INTO NEXT FLOWER-CART:  cost=total_cost, date = date, date2=date2,
    return render_template("flower-cart2.html", flower_urls=flower_urls,departed=departed, cart_contents=cart_contents, zip=zip, form=form, dates=dates)


@app.route('/flower-cart3', methods= ['GET', 'POST'])
def flowercart3():
    """ processing the customer order form"""

    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')
    departed_id=session['departed_id']
    departed=Departed.query.get_or_404(departed_id)
    cart_id = session['cart_id']
    zip = session['zip'] 
    date = session['delivery-date']

    cart_contents = requests.get(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={cart_id}', auth=(flower_user, flower_pass))
    cart_contents = cart_contents.json()

    flower_urls = get_flower_urls(cart_contents)

    #TODO: PUT IN NEXT FLOWER-CART to get quote
    complete_order = [ {"PRICE":item['PRICE'], "RECIPIENT":{"ZIPCODE":zip}, "CODE":item['CODE']} for item in cart_contents['products']]

    #TODO: PUT IN NEXT FLOWER-CART to get quote
    #attempting to stringify it to work in API call
    complete_order = json.dumps(complete_order)

    #TODO: 
    #TYPES APPEAR TO BE CORRECT
    print("ZIP is type:", type(zip))
    for ea in cart_contents['products']:
        print("---------------------------------------")
        print("IN flowercart3()")
        print("ea['PRICE'] is type:", type(ea['PRICE']))
        print("ea['NAME'] is type:", type(ea['NAME']))
        print("ea['CODE'] is type:", type(ea['CODE']))
        print("---------------------------------------")

    #TODO: PUT IN NEXT FLOWER-CART to get quote
    total_cost = requests.get('https://www.floristone.com/api/rest/flowershop/gettotal', params={"products":complete_order}, auth=(flower_user, flower_pass))
    total_cost = total_cost.json()
    

    # TESTED IT SUCCESSFULLY IN INSOMNIA WITH: [{"PRICE":84.95,"RECIPIENT":{"ZIPCODE":"23111"},"CODE":"FA302"}]

    #NOTE: ALWAYS PRINT OUT THE OUTPUT WITHOUT KEYS TO CHECK FOR ERRORS
    # GOT THIS: total_cost {'errors': ['at least one product is required']}
    # helped me realize that it needed to be json.dump(x) 'd (stringified) into text for API to be able to read it

    #DONE(?): format json as needed to get cost back
    complete_order = [ {"PRICE":item['PRICE'], "RECIPIENT":{"ZIPCODE":zip}, "CODE":item['CODE']} for item in cart_contents['products']]

    #attempting to stringify it to work in API call
    complete_order = json.dumps(complete_order)

    total_cost = requests.get('https://www.floristone.com/api/rest/flowershop/gettotal', params={"products":complete_order}, auth=(flower_user, flower_pass))
    total_cost = total_cost.json()
    

    # TESTED IT SUCCESSFULLY IN INSOMNIA WITH: [{"PRICE":84.95,"RECIPIENT":{"ZIPCODE":"23111"},"CODE":"FA302"}]

    #NOTE: ALWAYS PRINT OUT THE OUTPUT WITHOUT KEYS TO CHECK FOR ERRORS
    # GOT THIS: total_cost {'errors': ['at least one product is required']}
    # helped me realize that it needed to be json.dump(x) 'd (stringified) into text for API to be able to read it
    

    form = FlowerOrderForm()
    ############################################### customer form ##################
    ## getting ip address for floristone API
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    #will get name separately as anyone can buy flowers, - using mom's card, etc.
    # user_id = session["user_id"]
    # user = User.query.get_or_404(user_id)
    # name = f"{user.fname} {user.lname}"
    if form.is_submitted():
        print( "____________________________submitted______________")

    if form.validate():
        print("_______________________________valid_________________")

    print("_________________________FORM ERRORS:",form.errors)


    if form.validate_on_submit(): #csrf & is POST
        date = request.form['delivery_date']

        cardmessage = form.cardmessage.data

        to_name = form.to_name.data 
        to_institution = form.to_institution.data  
        to_address1 = form.to_address1.data   
        to_address2 = form.to_address2.data
        to_city = form.to_city.data   
        to_state = form.to_state.data
        to_zipcode = form.to_zipcode.data
        to_country = form.to_country.data   
        to_phone = form.to_phone.data

        delivery_date = form.delivery_date.data
        cardmessage = form.cardmessage.data
        from_name = form.from_name.data 
        from_address1 = form.from_address1.data   
        from_address2 = form.from_address2.data
        from_city = form.from_city.data   
        from_state = form.from_state.data
        from_zipcode = form.from_zipcode.data
        from_country = form.from_country.data   
        from_phone = form.from_phone.data

        specialinstructions = form.specialinstructions.data

        # print("---------------------------------------")
        # print("name", name)
        # print("address1", address1)
        # print("address2",address2)
        # print("city", city)
        # print("state", state)
        # print("zip", zip_cust)
        # print("country", country)
        # print("phone", phone)
        # print("---------------------------------------")

        return render_template("flower-cart3.html", flower_urls=flower_urls,departed=departed, cart_contents=cart_contents, date=date, zip=to_zipcode, cost=total_cost, form=form, name=to_name, institution=to_institution, address=to_address1, address2=to_address2, city=to_city,state=to_state, cardmessage=cardmessage)

    else:
        return redirect('/flower-cart2')
        


    # return render_template('flower-cart2.html')

@app.route('/flower-cart4', methods= ['GET','POST'])
def flower_cart4():
    """ Credit card form & purchase w/API"""

    return render_template('flower-cart4.html')



@app.route('/deletefromcart/<product_code>')
def delete_from_cart(product_code):
    page_num = session['page_current']
    print("************PAGE_NUM:", page_num)

    flower_user = getenv('FLORIST_ONE_KEY')
    flower_pass = getenv('FLORIST_ONE_PASSWORD')

    SESSIONID = session['cart_id']

    requests.put(f'https://www.floristone.com/api/rest/shoppingcart?sessionid={SESSIONID}&action=remove&productcode={product_code}', auth=(flower_user, flower_pass))
    
    if page_num == 0:
        return redirect(f'/flower-cart')
    else:
        return redirect(f'/flower-cart{page_num}')


#------------------------------------ FUNCTIONS -------------------------------------





#---------------------------------------------------------
# TODO: ROUTES TO MAKE
#---------------------------------------------------------

""" purchase(cart_id)  give form to fill in personal and credit card information.  Put cc info in flask-session(?) """



""" confirm_info(cart_info)  get auth key and price from api's, get order confirmation click"""

""" place_order(cart_info) place_order_api, getorderinfo_api, destroy cart, destroy auth token, store order in order history table in db, create post for memorial wall, send receipt, return Order Confirmation page """


""" Tracking form page """

""" Tracking info return page """