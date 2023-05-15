from flask import Flask
from os import environ

from src.database import db, ma , migrate, jwt

from src.endpoints.products import products
from src.endpoints.providers import providers
from src.endpoints.users import users
from src.endpoints.accounts import accounts
from src.endpoints.auth import auth
from src.endpoints.movements import movement


# def create_app(test_config=None):
#     app = Flask(__name__,
#                 instance_relative_config=True)
    
#     if test_config is None:
#         app.config.from_mapping(
#             SECRET_KEY=os.environ.get("SECRET_KEY"),
#         )
#     else:
#         app.config.from_mapping(test_config)
        
#     app.register_blueprint(products) 
#     app.register_blueprint(providers)       

#     return app

def create_app():
    app = Flask(__name__,
    instance_relative_config=True)

    app.config['ENVIRONMENT'] = environ.get("ENVIRONMENT")
    config_class = 'config.DevelopmentConfig'

    match app.config['ENVIRONMENT']:
        case "development":
            config_class = 'config.DevelopmentConfig'
        case "production":
            config_class = 'config.ProductionConfig'
        case _:
            print(f"ERROR: environment unknown: {app.config.get('ENVIRONMENT')}")
    app.config['ENVIRONMENT'] = "development"
    app.config.from_object(config_class)

    app.register_blueprint(products)
    app.register_blueprint(providers)
    app.register_blueprint(users)
    app.register_blueprint(accounts)
    app.register_blueprint(auth)
    app.register_blueprint(movement)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    with app.app_context():
        #db.drop_all()
        db.create_all()
    
    return app
