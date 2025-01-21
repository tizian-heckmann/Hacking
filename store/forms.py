from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[Length(min=3, max=20)])
    email = StringField("email", validators=[Length(min=3, max=20)])
    password = StringField("password", validators=[Length(min=10, max=32),
    ])
