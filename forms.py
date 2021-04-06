from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import DateField, DateTimeField, TimeField
from wtforms import StringField, FloatField,IntegerField, StringField, TextAreaField, BooleanField, SubmitField, validators
from wtforms.validators import InputRequired, Optional, Email, NumberRange, AnyOf, URL,  EqualTo, DataRequired
#TODO: add PasswordField?


class Create_memorial_form(FlaskForm):
    """To create a memorial wall for a dearly departed"""
    fname = StringField("First name", 
    validators = [InputRequired(message = "cannot be blank")])
    lname = StringField("Last name", 
    validators = [InputRequired(message = "cannot be blank")])
    city_born  = StringField("City")
    state_born = StringField("State")

    #TODO:  FIX!
    # born = DateField("Date of birth", 
    # validators = [InputRequired(message = "cannot be blank (if you aren't sure you can change it later)")])
    # died = DateField("Date this person passed away", 
    # validators = [InputRequired(message = "cannot be blank (if you aren't sure you can change it later)")])

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

    #TODO: MAKE DATETIME AGAIN WITH CORRECT INPUT BOXES
    # event_start = DateTimeField("Date & time services will begin")
    # event_end = DateTimeField("Date & time services will end (an estimate is okay)")

    event_start_date = DateField("Date of the memorial service")
    event_start_time = TimeField("Time service will begin")
    event_end = TimeField("Date & time services will end (an estimate is okay)")

    room = StringField("In what room at the facility will the services be held (ok to leave blank if unknown)")
    event_address = StringField("Street address of the funeral home")
    event_city = StringField("City")
    event_state =StringField("State")
    event_zip = StringField("Zip")
    event_phone = StringField("Phone number of the funeral home")
    #TODO: figure out how to use URL field/validations
    event_url = StringField("Website of the funeral home")

class User_registration(FlaskForm):
    """For loved ones to sign up to use the service"""

    fname = StringField("First name", 
    validators = [InputRequired(message = "cannot be blank")])

    lname = StringField("Last name", 
    validators = [InputRequired(message = "cannot be blank")])

    email = StringField("Email Address",
    validators=[InputRequired("required field"), Email()])

    password = TextAreaField("Password", 
    validators = [DataRequired(message = "required field"), EqualTo('confirm', message="passwords must match") ])

    confirm = TextAreaField('Repeat Password')
    
    accept_tos = BooleanField('I accept the TOS', 
    validators = [DataRequired("required to register")])

# class User_login(Flaskform):
#     """For loved ones to login"""

#     username = StringField("Username", 
#     validators = [InputRequired(message = "cannot be blank")])

#     password = PasswordField("Password", 
#     validators = [DataRequired(message = "required field")])


# class Admin_registration(Flaskform):
    #TODO

# class Admin_login(Flaskform):
    #TODO




