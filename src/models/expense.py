from datetime import datetime
from src.database import db, ma

class Expense(db.Model):
    code             = db.Column(db.String(10), primary_key=True)
    balance          = db.Column(db.Double, nullable=False)
    create_at        = db.Column(db.DateTime, default=datetime.now())
    
    account_code = db.Column(db.String(5), 
                        db.ForeignKey('account.code',
                                        onupdate="CASCADE",
                                        ondelete="RESTRICT"), 
                        nullable=False)
    
    
class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Expense
        include_fk = True
expense_schema=ExpenseSchema()
expenses_schema=ExpenseSchema(many=True)