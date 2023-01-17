from flask import Blueprint, render_template,url_for,session, redirect, request, flash, jsonify
from . import db
from .db_models import User, Stock
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json

mod = Blueprint('general', __name__)

@mod.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not current_user.is_authenticated:
            return render_template('login.html')
        else:
            return redirect(url_for("general.home_page"))
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("general.home_page"))
                flash('Logged In', category = "success") 
            else:
                flash('Incorrect Password', category = "error")
        else:
            flash('email does not exist', category = "error")
        return render_template('login.html')

@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("general.login"))


@mod.route('/home', methods = ["GET", "POST"])
@login_required
def home_page():
    user_stock_prices = {}
    for stock in current_user.stocks:
        price = find_price(stock.ticker)
        user_stock_prices[stock.ticker] = price
    if request.method == "GET":
        return render_template('home.html',user = current_user,stock_ticker=None, prices=user_stock_prices)
    elif request.method == "POST":
        ticker = str(request.form.get("stock_search")).upper()
        price = find_price(ticker)
        if price == -1:
            flash("Stock ticker symbol does not exist", category = "error")
            return redirect(url_for("general.home_page"))
        else:
            return render_template('home.html',user=current_user,stock_ticker=ticker,prices=user_stock_prices, price=price)


@mod.route("/signup", methods=["GET","POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form.get("sign_up_email")
        password = request.form.get("sign_up_password")
        verified = request.form.get("verified_password")

        user = False
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password != verified:
            flash("passwords do not match", category= "error")
        elif len(password) < 5:
            flash("password not long enough", category= "error")
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect(url_for("general.login"))

        return render_template("signup.html")

@mod.route("/addStock", methods=["POST"])
def add_stock():
    stock = json.loads(request.data)
    new_stock = Stock(ticker=stock, user_id=current_user.id)
    db.session.add(new_stock)
    db.session.commit()
    flash("Added " + stock + "to: " + current_user.id, category='success')
    return render_template("homt.html", user = current_user)

@mod.route("/deleteStock", methods=["POST"])
def delete_stock():
    stock = json.loads(request.data)
    stockid = stock['stock_id']
    stock = Stock.query.get(stockid)
    if stock:
        if stock.user_id == current_user.id:
            db.session.delete(stock)
            db.session.commit()
    return jsonify({})


def find_price(stock):
    API_KEY="004481d51de14c829427e8d3730526d0"
    ticker = stock
    api=f'&apikey={API_KEY}'

    prefix = 'https://api.twelvedata.com/time_series?'
    add_on = f'symbol={ticker}'
    interval = '&interval=1min'
    link = prefix + add_on + interval + api

    response = requests.get(link)
    data = response.json()

    if 'code' in data:
        return -1
    else:
        price = data['values'][0]['close']
        # rounded = round(int(price),2)
        # return str(rounded)
        return str(float(price))