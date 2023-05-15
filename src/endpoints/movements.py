from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.models.account import Account, account_schema, accounts_schema
from src.models.income import Income, income_schema, incomes_schema
from src.models.expense import Expense, expense_schema, expenses_schema
from src.database import db
import werkzeug
import sqlalchemy.exc
from datetime import datetime



movement = Blueprint("movement",
                 __name__,
                 url_prefix="/api/v1/movement")

@movement.get("/income")
def read_all_incomes():
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
        account.balance = (request.get_json().get("balance", account.balance )) + income.balance
        db.session.add(income)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":income_schema.dump(income)}, HTTPStatus.CREATED

@movement.delete("/income/<int:code>")
def deleteIncome(code):
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
def read_by_date_range_income():
    data = request.json
    initial_date = data.get("initial_date")
    final_date = data.get("final_date")

    if not initial_date or not final_date:
        return {"error": "initial and final date query parameters are required"}, HTTPStatus.BAD_REQUEST

    try:
        initial_date = datetime.strptime(initial_date, "%Y-%m-%d")
        final_date = datetime.strptime(final_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Bad date format 'YYYY-MM-DD'."}, HTTPStatus.BAD_REQUEST

    if initial_date > final_date:
        return {"error": "Initial date cannot be latter than final"}, HTTPStatus.BAD_REQUEST

    incomes = Income.query.filter(Income.create_at.between(initial_date, final_date)).all()

    if not incomes:
        return {"error": "incomes not found"}, HTTPStatus.NOT_FOUND

    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK

@movement.get("/expense")
def read_all_expenses():
    expenses=Expense.query.order_by(Expense.code).all()
    
    return {"data": expenses_schema.dump(expenses)}, HTTPStatus.OK

@movement.post("/expense")
def expense():
    
    post_data = None
    
    try:
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    expense=Expense(code = request.get_json().get("code", None),
              balance = request.get_json().get("balance", None),
              account_code = request.get_json().get("account_code", None),)
    
    account = Account.query.filter_by(code=expense.account_code).one_or_none()
    
    if not account:
        return {"error": "Wrong account"}, HTTPStatus.UNAUTHORIZED

    try:
        account.balance = (request.get_json().get("balance", account.balance + (-expense.balance))) 
        db.session.add(expense)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":expense_schema.dump(expense)}, HTTPStatus.CREATED

@movement.delete("/expense/<int:code>")
def delete(code):
    expense=Expense.query.filter_by(code=code).first()
    
    if(not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(expense)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Resource could not be deleted",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":""}, HTTPStatus.NO_CONTENT

@movement.get("/expense/date")
def read_by_date_range():
    data = request.json
    initial_date = data.get("initial_date")
    final_date = data.get("final_date")

    if not initial_date or not final_date:
        return {"error": "initial and final date query parameters are required"}, HTTPStatus.BAD_REQUEST

    try:
        initial_date = datetime.strptime(initial_date, "%Y-%m-%d")
        final_date = datetime.strptime(final_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Bad date format 'YYYY-MM-DD'."}, HTTPStatus.BAD_REQUEST

    if initial_date > final_date:
        return {"error": "Initial date cannot be later than final"}, HTTPStatus.BAD_REQUEST

    expenses = Expense.query.filter(Expense.create_at.between(initial_date, final_date)).all()

    if not expenses:
        return {"error": "expenses not found"}, HTTPStatus.NOT_FOUND

    return {"data": expenses_schema.dump(expenses)}, HTTPStatus.OK





