from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import DateField, DateTimeField, TimeField
from wtforms import StringField, FloatField,IntegerField, StringField, TextAreaField, BooleanField, SubmitField, validators, HiddenField, PasswordField, SelectField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, AnyOf, URL,  EqualTo, DataRequired, Length
from wtforms.fields.html5 import EmailField

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class Create_memorial_form(FlaskForm):
    """To create a memorial wall for a dearly departed"""
    fname = StringField("First name", 
    validators = [InputRequired(message = "cannot be blank")])
    lname = StringField("Last name", 
    validators = [InputRequired(message = "cannot be blank")])
    city_born  = StringField("City")
    state_born = StringField("State")

    
    born = DateField('Date of birth', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    died = DateField('Date passed away', format='%Y-%m-%d', validators=(validators.DataRequired(),))

    headshot = FileField("Face picture", validators =[FileRequired()])
    hero1 = FileField("Big picture for top of screen",validators =[FileRequired()])
    hero2 = FileField("Another big picture for top of screen",validators =[FileRequired()])



    biography = StringField("Biography/Life Story", 
    validators = [InputRequired(message = "cannot be blank")])
    headline = StringField("Headline about the dearly departed", 
    validators = [InputRequired(message = "cannot be blank")])
    text_color = StringField("Color text to go over picture (black or white recommended)")

    booked_yet = BooleanField("Have you made funeral arrangements yet?")
    funeral_home_name = StringField("Name of funeral home where services will be held")

    #TODO: MAKE DATETIME AGAIN WITH CORRECT INPUT BOXES LOOK AT TIME ZONES!
    # event_start = DateTimeField("Date & time services will begin")
    # event_end = DateTimeField("Date & time services will end (an estimate is okay)")

    event_start_date = DateField("Date of the memorial service", validators=(validators.Optional(),))
    event_start_time = TimeField("Time service will begin", validators=(validators.Optional(),))
    event_end = TimeField("Date & time services will end (an estimate is okay)", validators=(validators.Optional(),))

    room = StringField("In what room at the facility will the services be held (ok to leave blank if unknown)")
    event_address = StringField("Street address of the funeral home")
    event_city = StringField("City")
    event_state =StringField("State")
    event_zip = StringField("Zip")
    event_phone = StringField("Phone number of the funeral home")
    #TODO: figure out how to use URL field/validations
    event_url = StringField("Website of the funeral home")

class Post_form(FlaskForm):
    """For making a memorial post"""


    text = StringField("Share a memory or tell us about a picture you are contributing", 
    validators = [InputRequired(message = "cannot be blank")])
    file_url = FileField("Share a picture if you like")
    #TODO: remember to cast this to integer in app.py
    # user_id = HiddenField()  <- actually just get both of these in app.py
    # departed_id = HiddenField()


class User_registration(FlaskForm):
    """For loved ones to sign up to use the service"""

    fname = StringField("First name", 
    validators = [InputRequired(message = "cannot be blank")])

    lname = StringField("Last name", 
    validators = [InputRequired(message = "cannot be blank")])

    email = StringField("Email Address",
    validators=[InputRequired("required field"), Email()])

    password = PasswordField("Password", 
    validators = [InputRequired(message = "required field"), EqualTo('confirm', message="passwords must match") ])

    # password = PasswordField("Password", validators=[InputRequired()])

    confirm = PasswordField('Repeat Password')
    
    # accept_tos = BooleanField('I accept the TOS', 
    # validators = [DataRequired("required to register")])

# class User_login(Flaskform):
#     """For loved ones to login"""

#     username = StringField("Username", 
#     validators = [InputRequired(message = "cannot be blank")])

#     password = PasswordField("Password", 
#     validators = [DataRequired(message = "required field")])

class LoginForm(FlaskForm):
    """Form for registering a user."""

    email = StringField("email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])



# class Admin_registration(Flaskform):
    #TODO

# class Admin_login(Flaskform):
    #TODO

################################ FLOWER SHOP FORMS ##################################

class AddFlowerToCart(FlaskForm):
    flower_id = HiddenField("")

class ZipForm(FlaskForm):
    zip = StringField("Enter zip code where flowers are GOING", validators=[InputRequired(),  Length(min=5, message="must be at least 5 digits")])
    

class FlowerOrderForm(FlaskForm):
    """
        To Create data to make a JSON request in the following format:
        {  
   "customer": "{  
      \"ZIPCODE\":11779,
      \"PHONE\":1234567890,
      \"ADDRESS2\":\" \",
      \"STATE\":\"DE\",
      \"ADDRESS1\":\"123 Big St\",
      \"NAME\":\"John Doe\",
      \"COUNTRY\":\"US\",
      \"IP\":\"1.1.1.1\",
      \"EMAIL\":\"phil@floristone.com\",
      \"CITY\":\"Wilmington\"
   }",
   "products": "[  
      {  
         \"PRICE\":39.95,
         \"CARDMESSAGE\":\"This is a card message\",
         \"RECIPIENT\":{  
            \"ZIPCODE\":11779,
            \"PHONE\":1234567890,
            \"ADDRESS2\":\" \",
            \"STATE\":\"DE\",
            \"ADDRESS1\":\"123 Big St\",
            \"NAME\":\"Phil FloristOne\",
            \"COUNTRY\":\"US\",
            \"INSTITUTION\":\" \",
            \"CITY\":\"Wilmington\"
         },
         \"DELIVERYDATE\":\"2016-02-29\",
         \"CODE\":\"F1-509\"
      }
   ]",
   "ccinfo": "{  
      \"AUTHORIZENET_TOKEN\":\"****\"
   }",
   "ordertotal":58.79
}
    """
    cardmessage = StringField("Write a message for your gift card")

    #RECIPIENT
    to_name = StringField("First & last name", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])
    
    to_institution = StringField("Institution", 
    validators = [Length(max=100)])
    
    to_address1 = StringField("Street address", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])
    
    to_address2 = StringField("PO Box or Apt. number")
    
    to_city = StringField("City", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])
    
    to_state = SelectField("state", choices = [(st, st) for st in states])  
    
    to_zipcode = StringField("Zip code", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=5)])
    
    to_country = StringField("Country", validators = [Length(max=2)], default="US")
    
    to_phone = StringField("Phone", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=10)])

    #CUSTOMER
    from_name = StringField("First & last name", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])

    from_email = EmailField('Email address', [validators.DataRequired("Please enter your email address."), Length(max=100), validators.Email()])
    
    from_address1 = StringField("Street address", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])
    
    from_address2 = StringField("PO Box or Apt. number")
    
    from_city = StringField("City", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])
    
    from_state = SelectField("state", choices = [(st, st) for st in states])  
    
    from_zipcode = StringField("Zip code", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=5)])
    
    from_country = StringField("Country",validators = [Length(max=2)], default="US")
    
    from_phone = StringField("Phone", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=10)])

    specialinstructions = StringField("Any special instructions?", 
    validators = [InputRequired(message = "cannot be blank"), Length(max=100)])

    #PRODUCTS (AN ARRAY)
    #code - get from cart
    #prices - get from inquiry





