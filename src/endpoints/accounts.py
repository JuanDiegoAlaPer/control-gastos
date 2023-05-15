from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.account import Account, account_schema, accounts_schema


accounts = Blueprint("accounts", 
                  __name__,
                  url_prefix="/api/v1/accounts")

@accounts.get("/")
def read_all():
    accounts=Account.query.order_by(Account.code).all()
    
    return {"data": accounts_schema.dump(accounts)}, HTTPStatus.OK


@accounts.get("/<int:code>")
def read_one(code):
    account=Account.query.filter_by(code=code).first()
    
    if(not account):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data":account_schema.dump(account)}, HTTPStatus.OK

@accounts.post("/")
def create():
    post_data=None
    
    try:
        post_data=request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    account=Account(code = request.get_json().get("code", None),
              observations = request.get_json().get("observations", None),
              balance = request.get_json().get("balance", None),
              registered_phone = request.get_json().get("registered_phone", None),
              user_id = request.get_json().get("user_id", None),)
    
    try:
        db.session.add(account)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":account_schema.dump(account)}, HTTPStatus.CREATED


@accounts.put('/<int:code>')
def update(code):
    post_data=None
    
    try:
        post_data=request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
    
    account=Account.query.filter_by(code=code).first()
    
    if(not account):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    account.observations=request.get_json().get("observations", account.observations)
    account.balance=request.get_json().get("balance", account.balance)
    account.registered_phone=request.get_json().get("registered_phone", account.registered_phone)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":account_schema.dump(account)}, HTTPStatus.OK
        
@accounts.delete("/<int:code>")
def delete(code):
    account=Account.query.filter_by(code=code).first()
    
    if(not account):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(account)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Resource could not be deleted",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":""}, HTTPStatus.NO_CONTENT