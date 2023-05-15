from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.models.account import Account, account_schema, accounts_schema
from src.models.income import Income, income_schema, incomes_schema
from src.models.expense import Expense, expense_schema, expenses_schema
from src.database import db
import werkzeug
import sqlalchemy.exc


movement = Blueprint("movement",
                 __name__,
                 url_prefix="/api/v1/movement")

@movement.get("/income")
def read_all():
    incomes=Income.query.order_by(Income.code).all()
    
    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK

@movement.post("/income")
def income():
    
    post_data = None
    
    try:
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    income=Income(code = request.get_json().get("code", None),
              balance = request.get_json().get("balance", None),
              account_code = request.get_json().get("account_code", None),)
    
    account = Account.query.filter_by(code=income.account_code).one_or_none()
    
    if not account:
        return {"error": "Wrong account"}, HTTPStatus.UNAUTHORIZED

    try:
        account.balance= (request.get_json().get("balance", account.balance)) + income.balance
        db.session.add(income)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":income_schema.dump(income)}, HTTPStatus.CREATED

@movement.delete("/income/<int:code>")
def delete(code):
    income=Income.query.filter_by(code=code).first()
    
    if(not income):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Resource could not be deleted",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":""}, HTTPStatus.NO_CONTENT

@movement.get("/income/date")
def read_by_date_range():
    initial_date = request.args.get("initial_date")
    final_date = request.args.get("final_date")

    if not initial_date or not final_date:
        return {"error": "initial and final date query parameters are required"}, HTTPStatus.BAD_REQUEST

    try:
        incomes = Income.query.filter(Income.fecha.between(initial_date, final_date)).all()
    except ValueError:
        return {"error": "Invalid date format"}, HTTPStatus.BAD_REQUEST

    if not incomes:
        return {"error": "No resources found"}, HTTPStatus.NOT_FOUND

    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK




