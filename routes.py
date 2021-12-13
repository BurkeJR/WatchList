"""
@author: John Burke
"""

# imports
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_required
from flask_login.utils import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from hasher import UpdatedHasher
import os
import sys
from forms import LoginForm
from forms import RegisterForm
from forms import UpdatePassword
from forms import UpdateUsername
from forms import AddShow

# get path
scriptdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptdir)

# get db and pepper file
dbfile = os.path.join(scriptdir, 'watchList.sqlite3')
pepfile = os.path.join(scriptdir, "pepper.bin")

# get pepper key
with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()

pwd_hasher = UpdatedHasher(pepper_key)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'umaimelorinestrawberrymilkster'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# get db object
db = SQLAlchemy(app)

# LoginManager
app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'


@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# """

class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.LargeBinary)
    username = db.Column(db.Unicode)

    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")

    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)

    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)

class Show(db.Model):
    __tablename__ = "Shows"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    title = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    progress = db.Column(db.Unicode, nullable=False)

# db.drop_all()
# db.create_all()

# """


@app.route("/")
def index():
    return redirect(url_for("get_home"))

@app.get("/home/")
def get_home():
    return render_template("home.j2", current_user=current_user)

@app.get("/shows/")
@login_required
def get_shows():
    shows = Show.query.filter(Show.user_id == current_user.id).all()
    return render_template("shows.j2", shows=shows)

@app.get("/shows/add/")
@login_required
def get_add_show():
    form = AddShow()
    return render_template("addShow.j2", form=form)

@app.post("/shows/add/")
@login_required
def post_add_show():
    form = AddShow()
    if form.validate():
        db.session.add(Show(user_id= current_user.id,title=form.title.data, 
            rating=form.rating.data, progress=form.progress.data))
        db.session.commit()
        return redirect(url_for("get_shows"))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_add_show'))

@app.get("/register/")
def get_register():
    form = RegisterForm()
    return render_template("register.j2", form=form, loginLink=url_for('get_login'))

@app.post("/register/")
def post_register():
    form = RegisterForm()
    if form.validate():
        # check if existing account has this username
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("This username is already in use")
            return redirect(url_for('get_register'))
        # username not already being used, create new user
        db.session.add(
            User(password=form.password.data, username=form.username.data))
        db.session.commit()
        return redirect(url_for('get_login'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))


@app.get("/login/")
def get_login():
    form = LoginForm()
    return render_template("login.j2", form=form, registerLink=url_for('get_register'))


@app.post("/login/")
def post_login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        # if user with this username exists and password matches
        if user is not None and user.verify_password(form.password.data):
            # log in user using login_manager
            login_user(user)
            # redirect to page they wanted or to home page
            next = request.args.get("next")
            if next is None or not next.startswith('/'):
                next = url_for('get_home')

            return redirect(next)
        # if user doesn't exist or password is wrong
        else:
            flash("Invalid username or password")
            return redirect(url_for('get_login'))

    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))

@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    return redirect(url_for('index'))

@ app.get("/changeUsername/")
def get_changeUsername():
    form = UpdateUsername()
    return render_template("updateUsername.j2", current_user=current_user, form=form)


@ app.post("/changeUsername/")
def post_changeUsername():
    form = UpdateUsername()
    if form.validate():
        # check if existing account has this email
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash("The old username that was submitted does not match your account")
            return redirect(url_for('get_changeUsername'))
        # username are both not already being used, create new user
        user.username = form.newUsername.data
        db.session.commit()
        return render_template("profile.j2", current_user=current_user, form=form)
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_changeUsername'))