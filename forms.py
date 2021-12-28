from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.core import DecimalField, IntegerField, SelectField
from wtforms.validators import InputRequired, EqualTo, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])

    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired(), Length(min=4, max=32)])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=4, max=256)])
    confirm_password = PasswordField("Confirm Password: ", validators=[InputRequired(), EqualTo("password")])

    submit = SubmitField("Register")

class UpdateUsername(FlaskForm):
    username = StringField("Old Username: ", validators=[InputRequired()])
    newUsername = StringField("New Username: ", validators=[InputRequired(), Length(min=4, max=32)])

    submit = SubmitField("Update")

class UpdatePassword(FlaskForm):
    oldPassword = PasswordField("Old Password: ", validators=[InputRequired()])
    newPassword = PasswordField("New Password: ", validators=[InputRequired(), Length(min=4, max=256)])
    confirmNewPassword = PasswordField("Confirm New Password: ", validators=[InputRequired(), EqualTo("newPassword")])

    submit = SubmitField("Update")

class AddShow(FlaskForm):
    title = StringField("Title: ", validators=[InputRequired(), Length(max=256)])
    rating = DecimalField("Rating(_/10): ", validators=[NumberRange(min=0, max=10)])
    progress = SelectField("Progress: ", 
        choices=["Finished", "In Progress", "Waiting", "Plan to"],
        validators=[InputRequired()])

    submit = SubmitField("Add")