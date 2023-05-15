from datetime import datetime
from src.database import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    code       = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name       = db.Column(db.String(80), unique=True, nullable=False)
    price      = db.Column(db.Float, nullable=False)
    expiration = db.Column(db.Date, nullable=True)
    create_at  = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    user_id = db.Column(db.String(10), 
                        db.ForeignKey('user.id',
                                        onupdate="CASCADE",
                                        ondelete="RESTRICT"), 
                        nullable=False)