import os

class Config(object):
    SECRET_KEY = 'innovations'

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/bench_control'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
