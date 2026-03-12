import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= '4D9E2B1A8C73F056'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab5_user:password@localhost/lab5'

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from . import views
    app.register_blueprint(views.bp)

    return app