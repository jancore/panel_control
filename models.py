from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(66))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repre__(self):
        return '<User %r>' % self.username
