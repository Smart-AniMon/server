from flask_pymongo import PyMongo

instance = PyMongo()


def init_app(app):
    instance.init_app(app)