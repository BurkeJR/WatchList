"""
@author: John Burke
"""

# -------------------- INIT --------------------

# imports
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required
from flask_login.utils import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
import os, sys
from forms import LoginForm
from forms import RegisterForm
from forms import UpdatePassword
from forms import UpdateUsername
from forms import AddShow
from db import User
from db import Show
from db import Movie
from db import Text
import math

# round down function
def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

# get path
scriptdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(scriptdir)

# get db file
dbfile = os.path.join(scriptdir, 'watchList.sqlite3')

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

# -------------------- INIT --------------------

# ##################################################

# -------------------- INDEX/HOME --------------------

@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/home/")
def home():
    return render_template("home.j2", current_user=current_user)

# -------------------- INDEX/HOME --------------------

# ##################################################

# -------------------- MAIN PAGES --------------------

@app.get("/shows/")
@login_required
def get_shows():
    showForm = AddShow()
    shows = Show.query.filter(Show.user_id == current_user.id).all()
    return render_template("shows.j2", shows=shows, showForm=showForm, current_user=current_user)

@app.post("/shows/")
@login_required
def post_shows():
    form = AddShow()
    if form.validate():
        # get progress select field data
        formProgress = form.progress.data
        # check for special inputs
        if formProgress == "In Progress":
            temp = ""
            if form.season.data != None:
                temp += f"s{form.season.data} "
            if form.episode.data != None:
                temp += f"ep{form.episode.data}"
            # if season or episode field was filled out, change formProgress
            if temp != "":
                formProgress = temp
        elif formProgress == "Custom":
            formProgress = form.custom.data
        print("season: ", form.season.data, "ep: ", form.episode.data)
        db.session.add(Show(user_id= current_user.id,title=form.title.data, 
            rating=round_down(form.rating.data, 2), progress=formProgress))
        db.session.commit()
        return redirect(url_for("get_shows"))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_shows'))


@app.get("/movies/")
@login_required
def get_movies():
    pass

@app.post("/movies/")
@login_required
def post_movies():
    pass


@app.get("/texts/")
@login_required
def get_texts():
    pass

@app.post("/texts/")
@login_required
def post_texts():
    pass

# -------------------- MAIN PAGES --------------------

# ##################################################

# -------------------- ACCOUNT MANAGEMENT --------------------

@app.get("/register/")
def get_register():
    form = RegisterForm()
    return render_template("register.j2", form=form, loginLink=url_for('get_login'), 
        current_user=current_user)

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
    return render_template("login.j2", form=form, registerLink=url_for('get_register'),
        current_user=current_user)

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
                next = url_for('home')

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


@app.get("/changeUsername/")
@login_required
def get_changeUsername():
    form = UpdateUsername()
    return render_template("updateUsername.j2", current_user=current_user, form=form)

@app.post("/changeUsername/")
@login_required
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
        return redirect(url_for("get_profile"))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_changeUsername'))


@login_required
@app.route("/profile/")
def get_profile():
    return render_template("profile.j2", current_user=current_user)

# -------------------- ACCOUNT MANAGEMENT --------------------