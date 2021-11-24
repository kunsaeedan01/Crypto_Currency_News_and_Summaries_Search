import random
import psycopg2
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from scrapper import Scrapper
from summarizer import Summary
from pprint import pprint
from functools import wraps
import jwt
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0512rahat@localhost/APP-W05-practice'
app.config['SECRET_KEY'] = 'JustDemonstration'
db = SQLAlchemy(app)
my_value = ""


class User(db.Model) :
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String())
    password = db.Column(db.String())
    token = db.Column(db.String())


class Paragraphs(db.Model):
    __tablename__ = 'paragraphs'
    id = db.Column('id', db.Integer, primary_key=True)
    text = db.Column('text', db.String)

    def __init__(self, id, text):
        self.id = id
        self.text = text


class Summaries(db.Model):
    __tablename__ = 'summaries'
    id = db.Column('id', db.Integer, primary_key=True)
    summary = db.Column('summary', db.String)

    def __init__(self, id, summary):
        self.id = id
        self.summary = summary


db.create_all()
# currency = Scrapper("bitcoin")
# paragraphs = currency.scrap_articles()
# text_AI = Summary(paragraphs)
# final_summary = text_AI.do_summary()
#
# for item in paragraphs:
#     id_num = random.randint(1, 1000)
#     insert = Paragraphs(id_num, item)
# for item in final_summary:
#     id_num = random.randint(1, 1000)
#     insert = Summaries(id_num, item)


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped





@app.route("/log")
def index():
    # if not session.get('logged_in'):
        return render_template("login.html")
    # else:
        # return "Currently logged in"


@app.route("/public")
def public():
    return "Anyone can see this"


@app.route("/auth")
@check_for_token
def authorised():
    return "This is only viewable with a token"


@app.route("/login", methods=["POST"])
def login():
    if request.form["username"] and request.form["password"] == "password":
        session["logged_in"] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)

        },
        app.config['SECRET_KEY'], algorithm="HS256")
        return token
    else:
        return make_response("Could not verify", 403, {'WWW-Authenticate': 'Basic realm: "login realm"'})



@app.route("/news", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        crypto = request.form["nm"]


        return redirect(url_for("show_news", coin=crypto))
    else:
        return render_template("index.html")


@app.route("/news/<coin>", methods=["GET", "POST"])
def show_news(coin):
    currency = Scrapper(coin)
    paragraphs = currency.scrap_articles()
    text_AI = Summary(paragraphs)
    final_summary = text_AI.do_summary()
    for item in paragraphs:
        id_num = random.randint(1, 1000)
        insert = Paragraphs(id_num, item)
        db.session.add(insert)
        db.session.commit()
    for item in final_summary:
        id_num = random.randint(1, 1000)
        insert = Summaries(id_num, item)
        db.session.add(insert)
        db.session.commit()
    return render_template("results.html", news_list=paragraphs, sum_list=final_summary, coin=coin)

    # return render_template("results.html", news_list=paragraphs, sum_list=final_summary)







if __name__ == "__main__":
    app.run(debug=True)





