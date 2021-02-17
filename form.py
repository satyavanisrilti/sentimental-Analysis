from flask_wtf import FlaskForm
from wtforms import SubmitField,TextField,PasswordField,StringField,FileField
from wtforms.validators import DataRequired,Length

class Login(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
   
    submit = SubmitField('Login')
    register = SubmitField('Register')

class Register(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password',validators=[DataRequired()])
    register = SubmitField('Register')
