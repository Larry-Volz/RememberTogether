from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, DateTimeField, IntegerField, StringField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, AnyOf, URL, PasswordField, EqualTo, DataRequired

class User_registration(FlaskForm):
    """For loved ones to sign up to use the service"""

    fname = StringField("First name", 
    validators = [InputRequired(message = "cannot be blank")])

    lname = StringField("Last name", 
    validators = [InputRequired(message = "cannot be blank")])

    email = StringField("Email Address",
                        validators=[InputRequired("required field"), Email()])

    username = StringField("Username", 
    validators = [InputRequired(message = "cannot be blank")])

    password = PasswordField("Password", 
    validators = [DataRequired(message = "required field"), EqualTo('confirm', message="passwords must match") ])

    confirm = PasswordField('Repeat Password')
    
    accept_tos = BooleanField('I accept the TOS', 
    validators = [DataRequired("required to register")])

class User_login(Flaskform):
    """For loved ones to login"""

    username = StringField("Username", 
    validators = [InputRequired(message = "cannot be blank")])

    password = PasswordField("Password", 
    validators = [DataRequired(message = "required field")])


class Admin_registration(Flaskform):
    #TODO

class Admin_login(Flaskform):
    #TODO




