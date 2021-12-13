from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])

    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", validators=[InputRequired(), EqualTo("password")])

    submit = SubmitField("Register")

class UpdateUsername(FlaskForm):
    username = StringField("Old Username: ", validators=[InputRequired()])
    newUsername = StringField("New Username: ", validators=[InputRequired()])
    submit = SubmitField("Update")

class UpdatePassword(FlaskForm):
    oldPassword = PasswordField("Old Password: ", validators=[InputRequired()])
    newPassword = PasswordField("New Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    confirmNewPassword = PasswordField("Confirm New Password: ", validators=[InputRequired(), EqualTo("newPassword")])

    submit = SubmitField("Update")
