from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, unique=False)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, admin, username, password):
        self.admin = admin
        self.username = username
        self.password = self.__create_password(password)

    def __repre__(self):
        return '<User %r>' % self.username

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
