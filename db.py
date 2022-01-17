from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from hasher import UpdatedHasher
import os, sys

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
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# get db object
db = SQLAlchemy(app)

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
    imdbID = db.Column(db.Unicode, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    title = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    progress = db.Column(db.Unicode, nullable=False)

class Movie(db.Model):
    __tablename__ = "Movies"
    id = db.Column(db.Integer, primary_key=True)
    imdbID = db.Column(db.Unicode, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    title = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    progress = db.Column(db.Unicode, nullable=False)

class Text(db.Model):
    __tablename__ = "Texts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    title = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    progress = db.Column(db.Unicode, nullable=False)
    type = db.Column(db.Unicode, nullable=False)

# db.drop_all()
# db.create_all()

