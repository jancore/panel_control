import os

class Config(object):
    SECRET_KEY = 'innovations'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:JanSoltec93@localhost/bench_control'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = dict(
    DEBUG = False,
    SECRET_KEY = 'innovations'
)