from flask import Flask
from .views import app

from . import models
from .models import *
models.db.init_app(app)
from .models import db


from flask_login import LoginManager, UserMixin, current_user
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.login_message = u"Please log in or sign up to access this page!!"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(adresseMail):
    return Utilisateur.query.get(adresseMail)
