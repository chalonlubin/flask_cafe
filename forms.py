"""Forms for Flask Cafe."""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, URL

class AddCafeForm(FlaskForm):
    """ Form for adding/editing cafes"""

    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    url = StringField('URL', validators=[URL(), Optional()])
    address = StringField('Address',
                    validators=[InputRequired()])
    city_code = SelectField('City')
    image_url = StringField('Image', validators=[URL(), Optional()])
