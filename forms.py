"""Forms for Flask Cafe."""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, email, Length

class AddCafeForm(FlaskForm):
    """ Form for adding/editing cafes"""

    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    url = StringField('URL', validators=[URL(), Optional()])
    address = StringField('Address',
                    validators=[InputRequired()])
    city_code = SelectField('City')
    image_url = StringField('Image', validators=[URL(), Optional()])


class SignupForm(FlaskForm):
    """ Form for adding user."""

    username = StringField('Username', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    email = StringField('Email', validators=[email(), InputRequired()])
    password = PasswordField('Password',
                    validators=[Length(min=6)])
    image_url = StringField('Image', validators=[URL(), Optional()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])