from datetime import datetime
from src.database import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

class Account(db.Model):
    code             = db.Column(db.String(5), primary_key=True)
    observations     = db.Column(db.String(80), nullable=False)
    balance          = db.Column(db.Double, nullable=False)
    registered_phone = db.Column(db.String(10), nullable=True)
    create_at        = db.Column(db.DateTime, default=datetime.now())
    updated_at       = db.Column(db.DateTime, onupdate=datetime.now())
    
    user_id = db.Column(db.String(10), 
                        db.ForeignKey('user.id',
                                        onupdate="CASCADE",
                                        ondelete="RESTRICT"), 
                        nullable=False)
    
    
class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Account
        include_fk = True
account_schema=AccountSchema()
accounts_schema=AccountSchema(many=True)